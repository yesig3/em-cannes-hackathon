"""
ERC-8004 Identity on Hedera via Ultravioleta Facilitator

Register agents, validate identity, and query metadata — all gasless.
The Facilitator pays gas on Hedera (testnet or mainnet based on config).
"""

import logging
from typing import Optional

import httpx

from config import FACILITATOR_URL, FACILITATOR_NETWORK

logger = logging.getLogger(__name__)


async def register_agent(
    recipient: str,
    agent_uri: str = "https://execution.market/agent-card.json",
    metadata: Optional[list] = None,
) -> dict:
    """
    Register an ERC-8004 agent on Hedera (gasless via Facilitator).

    Args:
        recipient: Wallet address to receive the agent NFT
        agent_uri: IPFS or HTTPS URI for agent metadata
        metadata: Optional list of {"key": "...", "value": "..."} pairs
    """
    payload = {
        "x402Version": 1,
        "network": FACILITATOR_NETWORK,
        "agentUri": agent_uri,
        "recipient": recipient,
        "metadata": metadata or [],
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(f"{FACILITATOR_URL}/register", json=payload)

    data = resp.json()
    if resp.status_code == 200:
        logger.info(
            "Agent registered on %s: agentId=%s, tx=%s",
            FACILITATOR_NETWORK,
            data.get("agentId"),
            data.get("txHash", "")[:20],
        )
    else:
        logger.error(
            "Registration failed on %s: %s",
            FACILITATOR_NETWORK,
            data,
        )

    return {"status_code": resp.status_code, **data}


async def get_identity(agent_id: int) -> dict:
    """
    Get agent identity from ERC-8004 on Hedera.

    Returns agent owner, URI, metadata, and registration status.
    """
    url = f"{FACILITATOR_URL}/identity/{FACILITATOR_NETWORK}/{agent_id}"

    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(url)

    if resp.status_code == 200:
        return {"found": True, **resp.json()}
    elif resp.status_code == 404:
        return {"found": False, "agent_id": agent_id}
    else:
        return {"found": False, "error": resp.text, "status_code": resp.status_code}


async def get_identity_by_owner(wallet: str) -> dict:
    """Look up agent by wallet address on Hedera."""
    url = f"{FACILITATOR_URL}/identity/{FACILITATOR_NETWORK}/owner/{wallet}"

    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(url)

    if resp.status_code == 200:
        return {"found": True, **resp.json()}
    return {"found": False, "wallet": wallet}


async def get_total_supply() -> int:
    """Get total number of registered agents on Hedera."""
    url = f"{FACILITATOR_URL}/identity/{FACILITATOR_NETWORK}/total-supply"

    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(url)

    if resp.status_code == 200:
        data = resp.json()
        return data.get("totalSupply", 0)
    return 0
