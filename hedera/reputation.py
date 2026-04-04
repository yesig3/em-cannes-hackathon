"""
ERC-8004 Reputation on Hedera via Ultravioleta Facilitator

Submit feedback, query reputation scores, respond to feedback — all gasless.
"""

import logging
from typing import Optional

import httpx

from config import FACILITATOR_URL, FACILITATOR_NETWORK

logger = logging.getLogger(__name__)


async def submit_feedback(
    agent_id: int,
    value: int = 95,
    tag1: str = "",
    tag2: str = "",
    endpoint: str = "",
    feedback_uri: str = "",
) -> dict:
    """
    Submit reputation feedback for an agent on Hedera (gasless).

    Args:
        agent_id: ERC-8004 agent ID to rate
        value: Score 0-100 (95 = excellent)
        tag1: Category tag (e.g., "task_completion")
        tag2: Sub-category tag
        endpoint: Service endpoint that was rated
        feedback_uri: IPFS/HTTPS URI with detailed feedback
    """
    payload = {
        "x402Version": 1,
        "network": FACILITATOR_NETWORK,
        "feedback": {
            "agentId": agent_id,
            "value": value,
            "valueDecimals": 0,
            "tag1": tag1,
            "tag2": tag2,
            "endpoint": endpoint,
            "feedbackUri": feedback_uri,
            "feedbackHash": None,
            "proof": None,
        },
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(f"{FACILITATOR_URL}/feedback", json=payload)

    data = resp.json()
    if resp.status_code == 200:
        logger.info(
            "Feedback submitted on %s: agent=%d, value=%d, tx=%s",
            FACILITATOR_NETWORK,
            agent_id,
            value,
            data.get("txHash", "")[:20],
        )
    else:
        logger.error(
            "Feedback failed on %s: %s",
            FACILITATOR_NETWORK,
            data,
        )

    return {"status_code": resp.status_code, **data}


async def get_reputation(
    agent_id: int,
    tag1: Optional[str] = None,
    include_feedback: bool = False,
) -> dict:
    """
    Get reputation score for an agent on Hedera.

    Args:
        agent_id: ERC-8004 agent ID
        tag1: Filter by category tag
        include_feedback: Include individual feedback entries
    """
    url = f"{FACILITATOR_URL}/reputation/{FACILITATOR_NETWORK}/{agent_id}"
    params = {}
    if tag1:
        params["tag1"] = tag1
    if include_feedback:
        params["includeFeedback"] = "true"

    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(url, params=params)

    if resp.status_code == 200:
        return resp.json()
    return {"error": resp.text, "status_code": resp.status_code}
