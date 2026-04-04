"""
HCS Logger — Hedera Consensus Service Event Logging

Logs task lifecycle events to an HCS topic on Hedera testnet/mainnet.
This is a Hedera-NATIVE feature (not EVM) — requires the Hedera SDK.
Messages are immutable and verifiable via Mirror Node REST API.

Usage:
    logger = HCSLogger()
    topic_id = logger.create_topic("Execution Market Events")
    logger.log_event(topic_id, "task_created", {"task_id": "abc", "bounty": 0.10})
    messages = await logger.get_messages(topic_id)
"""

import base64
import json
import logging
import os
import time
from datetime import datetime, timezone
from typing import Optional

import httpx

from hiero_sdk_python import (
    Client,
    Network,
    AccountId,
    PrivateKey,
    TopicCreateTransaction,
    TopicMessageSubmitTransaction,
    TopicId,
)

from config import HEDERA_8004_NETWORK

logger = logging.getLogger(__name__)

# Mirror Node URLs
MIRROR_URLS = {
    "testnet": "https://testnet.mirrornode.hedera.com",
    "mainnet": "https://mainnet.mirrornode.hedera.com",
}


class HCSLogger:
    """Log events to Hedera Consensus Service (HCS)."""

    def __init__(
        self,
        operator_id: Optional[str] = None,
        operator_key: Optional[str] = None,
        network: Optional[str] = None,
    ):
        self.network = network or HEDERA_8004_NETWORK
        self.mirror_url = MIRROR_URLS.get(self.network, MIRROR_URLS["testnet"])

        op_id = operator_id or os.environ.get("HEDERA_OPERATOR_ID", "")
        op_key = operator_key or os.environ.get("HEDERA_OPERATOR_KEY", "")

        if not op_id or not op_key:
            raise ValueError(
                "HEDERA_OPERATOR_ID and HEDERA_OPERATOR_KEY required for HCS"
            )

        self.client = Client(Network(self.network))
        self.operator_id = AccountId.from_string(op_id)
        self.operator_key = PrivateKey.from_string(op_key)
        self.client.set_operator(self.operator_id, self.operator_key)

    def create_topic(self, memo: str = "Execution Market Task Events") -> str:
        """
        Create an HCS topic. Returns topic_id string (e.g. "0.0.NNNNN").
        """
        receipt = (
            TopicCreateTransaction(
                memo=memo,
                admin_key=self.operator_key.public_key(),
            )
            .freeze_with(self.client)
            .sign(self.operator_key)
            .execute(self.client)
        )

        topic_id = str(receipt.topic_id)
        logger.info("HCS topic created: %s (memo: %s)", topic_id, memo)
        return topic_id

    def log_event(self, topic_id: str, event_type: str, payload: dict) -> int:
        """
        Submit an event message to an HCS topic.
        Returns the sequence number of the message.

        Fire-and-forget safe — exceptions are caught and logged.
        """
        message = json.dumps({
            "type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **payload,
        })

        try:
            tid = TopicId.from_string(topic_id)
            receipt = (
                TopicMessageSubmitTransaction(topic_id=tid, message=message)
                .freeze_with(self.client)
                .sign(self.operator_key)
                .execute(self.client)
            )
            seq = getattr(receipt, "topic_sequence_number", 0) or 0
            logger.info(
                "HCS event logged: type=%s, topic=%s, seq=%d",
                event_type, topic_id, seq,
            )
            return seq
        except Exception as e:
            logger.warning("HCS log_event failed (non-blocking): %s", e)
            return -1

    async def get_messages(
        self,
        topic_id: str,
        expected_count: int = 0,
        max_retries: int = 5,
        retry_delay: float = 2.0,
    ) -> list:
        """
        Read messages from an HCS topic via Mirror Node REST API.
        Polls with retries to handle propagation delay (3-10 seconds).
        """
        url = f"{self.mirror_url}/api/v1/topics/{topic_id}/messages?limit=50&order=asc"

        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.get(url)

                if resp.status_code != 200:
                    logger.warning("Mirror Node returned %d", resp.status_code)
                    continue

                data = resp.json()
                raw_messages = data.get("messages", [])

                messages = []
                for msg in raw_messages:
                    try:
                        decoded = base64.b64decode(msg["message"]).decode("utf-8")
                        parsed = json.loads(decoded)
                        parsed["_sequence"] = msg.get("sequence_number")
                        parsed["_consensus"] = msg.get("consensus_timestamp")
                        messages.append(parsed)
                    except Exception:
                        messages.append({"_raw": msg["message"], "_error": "decode_failed"})

                if expected_count <= 0 or len(messages) >= expected_count:
                    return messages

                # Not enough messages yet — wait for propagation
                if attempt < max_retries - 1:
                    await _async_sleep(retry_delay)

            except Exception as e:
                logger.warning("Mirror Node read failed (attempt %d): %s", attempt + 1, e)
                if attempt < max_retries - 1:
                    await _async_sleep(retry_delay)

        return messages if 'messages' in dir() else []


async def _async_sleep(seconds: float):
    """Async-compatible sleep."""
    import asyncio
    await asyncio.sleep(seconds)
