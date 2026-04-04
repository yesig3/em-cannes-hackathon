"""
Hedera Chain Utilities

Balance checks and RPC connectivity verification via Hedera's JSON-RPC relay.
Used by the demo to verify the Facilitator has HBAR for gas.
"""

import logging
from typing import Optional

import httpx

from config import RPC_URL, CHAIN_ID, EXPLORER_URL, NETWORK_LABEL

logger = logging.getLogger(__name__)


async def get_balance(address: str) -> dict:
    """Get HBAR balance for an address via JSON-RPC."""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_getBalance",
        "params": [address, "latest"],
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(RPC_URL, json=payload)

    data = resp.json()
    if "result" in data:
        wei = int(data["result"], 16)
        # Hedera EVM uses 18 decimals (weibars to HBAR)
        hbar = wei / 1e18
        return {
            "address": address,
            "balance_wei": wei,
            "balance_hbar": round(hbar, 6),
            "network": NETWORK_LABEL,
            "explorer": f"{EXPLORER_URL}/account/{address}",
        }
    return {"error": data.get("error", "Unknown error"), "address": address}


async def get_chain_id() -> Optional[int]:
    """Verify connectivity by fetching chain ID from Hedera RPC."""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_chainId",
        "params": [],
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(RPC_URL, json=payload)
        data = resp.json()
        if "result" in data:
            return int(data["result"], 16)
    except Exception as e:
        logger.error("Failed to get chain ID from %s: %s", RPC_URL, e)
    return None


async def get_block_number() -> Optional[int]:
    """Get latest block number from Hedera RPC."""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_blockNumber",
        "params": [],
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(RPC_URL, json=payload)
        data = resp.json()
        if "result" in data:
            return int(data["result"], 16)
    except Exception as e:
        logger.error("Failed to get block number: %s", e)
    return None
