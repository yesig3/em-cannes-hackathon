"""
ENS Text Records — Agent Metadata On-Chain

Read and format ENS text records for Execution Market agents.
Uses web3.py ENS resolver to query on-chain text records.

Text records follow ENSIP-5 (EIP-634) and use the key prefix
"com.execution.market." for Execution Market-specific metadata.
"""

import logging
from typing import Optional

from web3 import Web3
from eth_utils import to_bytes
from eth_abi import encode

from config import (
    RPC_URL,
    EM_TEXT_RECORDS,
    EM_TEXT_RECORD_PREFIX,
    NETWORK_LABEL,
    ERC8004_IDENTITY_REGISTRY,
    FACILITATOR_URL,
)
from resolver import get_web3

logger = logging.getLogger(__name__)


# ── Namehash (EIP-137) ─────────────────────────────────────────────────────

def namehash(name: str) -> bytes:
    """
    Compute ENS namehash per EIP-137.

    namehash('') = 0x00...00
    namehash('eth') = keccak256(namehash('') + keccak256('eth'))
    namehash('vitalik.eth') = keccak256(namehash('eth') + keccak256('vitalik'))
    """
    if not name:
        return b"\x00" * 32

    labels = name.split(".")
    node = b"\x00" * 32
    for label in reversed(labels):
        label_hash = Web3.keccak(text=label)
        node = Web3.keccak(node + label_hash)
    return node


# ── Text Record Reading ────────────────────────────────────────────────────

# Minimal resolver ABI for text() function
RESOLVER_TEXT_ABI = [
    {
        "inputs": [
            {"name": "node", "type": "bytes32"},
            {"name": "key", "type": "string"},
        ],
        "name": "text",
        "outputs": [{"name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    }
]


def get_text_record(name: str, key: str) -> Optional[str]:
    """
    Read a single text record from an ENS name.

    Args:
        name: ENS name (e.g., "vitalik.eth")
        key: Text record key (e.g., "url", "com.execution.market.agentId")

    Returns:
        Text record value, or None if not set
    """
    w3 = get_web3()

    try:
        # Get the resolver for this name
        resolver_addr = w3.ens.resolver(name)
        if resolver_addr is None:
            logger.debug("No resolver for %s", name)
            return None

        resolver = w3.eth.contract(
            address=resolver_addr.address,
            abi=RESOLVER_TEXT_ABI,
        )

        node = namehash(name)
        value = resolver.functions.text(node, key).call()
        return value if value else None

    except Exception as exc:
        logger.debug("Failed to read text record %s for %s: %s", key, name, exc)
        return None


def get_standard_records(name: str) -> dict:
    """
    Read standard ENS text records (ENSIP-5).

    Returns common records like url, description, avatar, email, etc.
    """
    standard_keys = [
        "url",
        "description",
        "avatar",
        "email",
        "com.twitter",
        "com.github",
        "org.telegram",
        "com.discord",
    ]

    records = {}
    for key in standard_keys:
        value = get_text_record(name, key)
        if value is not None:
            records[key] = value

    return {
        "name": name,
        "records": records,
        "count": len(records),
        "network": NETWORK_LABEL,
    }


def get_em_metadata(name: str) -> dict:
    """
    Read Execution Market-specific text records from an ENS name.

    Reads all keys under "com.execution.market.*" prefix.
    """
    metadata = {}
    for friendly_key, full_key in EM_TEXT_RECORDS.items():
        value = get_text_record(name, full_key)
        if value is not None:
            metadata[friendly_key] = value

    return {
        "name": name,
        "em_metadata": metadata,
        "count": len(metadata),
        "prefix": EM_TEXT_RECORD_PREFIX,
        "network": NETWORK_LABEL,
    }


def get_all_records(name: str) -> dict:
    """
    Read both standard and EM-specific text records.

    Returns a complete view of all discoverable metadata for an ENS name.
    """
    standard = get_standard_records(name)
    em = get_em_metadata(name)

    return {
        "name": name,
        "standard_records": standard["records"],
        "em_metadata": em["em_metadata"],
        "total_records": standard["count"] + em["count"],
        "network": NETWORK_LABEL,
    }


# ── Proposed Text Records for Execution Market ─────────────────────────────

def proposed_agent_records(
    agent_id: int = 2106,
    world_id_verified: bool = True,
    world_id_level: str = "orb",
    reputation: float = 4.8,
    tasks_completed: int = 127,
    chains: str = "base,ethereum,polygon,arbitrum,hedera",
) -> dict:
    """
    Generate the proposed ENS text records for an Execution Market agent.

    These records would be written to execution-market.eth (or subnames)
    to make agent metadata discoverable on-chain.
    """
    return {
        "com.execution.market.agentId": str(agent_id),
        "com.execution.market.role": "agent",
        "com.execution.market.worldIdVerified": str(world_id_verified).lower(),
        "com.execution.market.worldIdLevel": world_id_level,
        "com.execution.market.reputation": str(reputation),
        "com.execution.market.tasksCompleted": str(tasks_completed),
        "com.execution.market.chains": chains,
        "url": "https://execution.market",
        "description": "Universal Execution Layer — AI agents publish bounties, verified humans execute them",
        "avatar": f"eip155:8453/erc721:{ERC8004_IDENTITY_REGISTRY}/{agent_id}",
        "com.twitter": "@ExecutionMarket",
        "com.github": "UltravioletaDAO",
    }
