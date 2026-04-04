"""
ENS Subnames — Worker Fleet Discovery

Resolve worker subnames under a parent ENS domain.
Example: alice.execution.eth, bob.execution.eth

Subnames are resolved the same way as regular ENS names (namehash).
The parent domain owner can create subnames via NameWrapper.
"""

import logging
from typing import Optional

from resolver import resolve_name, reverse_resolve, get_web3
from text_records import get_text_record, namehash, get_em_metadata

logger = logging.getLogger(__name__)


def resolve_worker(worker_subname: str) -> dict:
    """
    Resolve a worker subname to address + metadata.

    Args:
        worker_subname: Full subname (e.g., "alice.execution.eth")

    Returns:
        dict with address, ENS metadata, and EM-specific records
    """
    # Step 1: Resolve subname to address
    resolution = resolve_name(worker_subname)

    if not resolution.get("resolved"):
        return {
            "subname": worker_subname,
            "resolved": False,
            "error": resolution.get("error", "Subname not registered"),
        }

    # Step 2: Read EM metadata from text records
    em_data = get_em_metadata(worker_subname)

    return {
        "subname": worker_subname,
        "address": resolution["address"],
        "resolved": True,
        "em_metadata": em_data.get("em_metadata", {}),
        "ens_link": resolution.get("ens_link"),
    }


def resolve_fleet(parent_domain: str, worker_names: list[str]) -> dict:
    """
    Resolve multiple workers under a parent domain.

    Args:
        parent_domain: Parent ENS domain (e.g., "execution.eth")
        worker_names: List of worker labels (e.g., ["alice", "bob", "oracle"])

    Returns:
        dict with resolved workers, parent info, and fleet summary
    """
    workers = []
    resolved_count = 0

    for name in worker_names:
        subname = f"{name}.{parent_domain}"
        result = resolve_worker(subname)
        workers.append(result)
        if result.get("resolved"):
            resolved_count += 1

    # Also resolve the parent domain
    parent = resolve_name(parent_domain)

    return {
        "parent_domain": parent_domain,
        "parent_resolved": parent.get("resolved", False),
        "parent_address": parent.get("address"),
        "workers": workers,
        "total_workers": len(worker_names),
        "resolved_workers": resolved_count,
    }


def get_worker_identity(worker_subname: str) -> dict:
    """
    Get complete worker identity from ENS + ERC-8004.

    Combines ENS resolution with ERC-8004 cross-reference:
    1. Resolve subname to address
    2. Read EM text records (agentId, worldIdVerified, etc.)
    3. If agentId found, cross-reference with ERC-8004 registry

    This demonstrates ENS as the DISCOVERY layer and ERC-8004 as the TRUST layer.
    """
    resolution = resolve_worker(worker_subname)

    if not resolution.get("resolved"):
        return resolution

    # Check for ERC-8004 cross-reference
    em_metadata = resolution.get("em_metadata", {})
    agent_id = em_metadata.get("agentId")

    identity = {
        **resolution,
        "identity_layers": {
            "ens": {
                "name": worker_subname,
                "address": resolution["address"],
                "status": "resolved",
            },
            "erc8004": {
                "agentId": agent_id,
                "status": "linked" if agent_id else "not_linked",
                "registry": "0x8004A169FB4a3325136EB29fA0ceB6D2e539a432",
            },
            "worldId": {
                "verified": em_metadata.get("worldIdVerified", "unknown"),
                "level": em_metadata.get("worldIdLevel", "unknown"),
            },
        },
    }

    return identity


# ── Proposed Subname Structure ──────────────────────────────────────────────

def proposed_fleet_structure() -> dict:
    """
    Generate the proposed ENS subname structure for Execution Market.

    This shows how worker subnames would be organized under execution.eth.
    """
    return {
        "parent": "execution.eth",
        "description": "Execution Market agent fleet",
        "subnames": [
            {
                "name": "alice.execution.eth",
                "role": "worker",
                "world_id": "orb",
                "reputation": 4.8,
                "tasks": 42,
            },
            {
                "name": "bob.execution.eth",
                "role": "worker",
                "world_id": "device",
                "reputation": 4.2,
                "tasks": 15,
            },
            {
                "name": "oracle.execution.eth",
                "role": "verifier",
                "world_id": "orb",
                "reputation": 5.0,
                "tasks": 200,
            },
            {
                "name": "platform.execution.eth",
                "role": "agent",
                "agent_id": 2106,
                "description": "Main platform agent",
            },
        ],
        "management": "NameWrapper (ERC-1155) — parent owner controls subnames",
        "cost": "Free on Sepolia, $5-10/year on mainnet",
    }
