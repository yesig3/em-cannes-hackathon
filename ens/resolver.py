"""
ENS Name Resolution

Resolve ENS names to addresses and reverse-resolve addresses to names.
Uses web3.py built-in ENS support (no external libraries needed).
"""

import logging
from typing import Optional

from web3 import Web3

from config import RPC_URL, ENS_APP_URL, NETWORK_LABEL

logger = logging.getLogger(__name__)

# ── Web3 Provider ───────────────────────────────────────────────────────────

_w3: Optional[Web3] = None


def get_web3() -> Web3:
    """Get or create web3 instance with ENS support."""
    global _w3
    if _w3 is None:
        _w3 = Web3(Web3.HTTPProvider(RPC_URL))
    return _w3


# ── Resolution ──────────────────────────────────────────────────────────────


def resolve_name(name: str) -> dict:
    """
    Resolve an ENS name to an Ethereum address.

    Args:
        name: ENS name (e.g., "vitalik.eth", "execution-market.eth")

    Returns:
        dict with address, name, network, and ENS app link
    """
    w3 = get_web3()

    try:
        address = w3.ens.address(name)
    except Exception as exc:
        logger.error("Failed to resolve %s: %s", name, exc)
        return {
            "name": name,
            "address": None,
            "resolved": False,
            "error": str(exc),
            "network": NETWORK_LABEL,
        }

    if address is None:
        return {
            "name": name,
            "address": None,
            "resolved": False,
            "error": "Name not registered or expired",
            "network": NETWORK_LABEL,
        }

    return {
        "name": name,
        "address": address,
        "resolved": True,
        "network": NETWORK_LABEL,
        "ens_link": f"{ENS_APP_URL}/{name}",
    }


def reverse_resolve(address: str) -> dict:
    """
    Reverse-resolve an Ethereum address to an ENS name.

    Args:
        address: Ethereum address (0x...)

    Returns:
        dict with name (if set), address, and resolution status
    """
    w3 = get_web3()

    try:
        name = w3.ens.name(address)
    except Exception as exc:
        logger.error("Failed to reverse-resolve %s: %s", address, exc)
        return {
            "address": address,
            "name": None,
            "resolved": False,
            "error": str(exc),
        }

    if name is None:
        return {
            "address": address,
            "name": None,
            "resolved": False,
            "error": "No reverse record set",
        }

    return {
        "address": address,
        "name": name,
        "resolved": True,
        "network": NETWORK_LABEL,
        "ens_link": f"{ENS_APP_URL}/{name}",
    }


def resolve_multiple(names: list[str]) -> list[dict]:
    """Batch-resolve multiple ENS names."""
    return [resolve_name(name) for name in names]
