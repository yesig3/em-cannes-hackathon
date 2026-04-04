"""
Hedera Network Configuration

Toggle between testnet and mainnet via HEDERA_8004_NETWORK env var.
Default: testnet (for hackathon demo). Switch to mainnet post-hackathon.
"""

import os

# ── Network toggle ──────────────────────────────────────────────────────────
# "testnet" (default, hackathon) or "mainnet" (production)
HEDERA_8004_NETWORK = os.environ.get("HEDERA_8004_NETWORK", "testnet")

# ── Derived configuration ───────────────────────────────────────────────────

_CONFIGS = {
    "testnet": {
        "facilitator_network": "hedera-testnet",
        "chain_id": 296,
        "rpc_url": os.environ.get(
            "HEDERA_RPC_URL", "https://testnet.hashio.io/api"
        ),
        "identity_registry": "0x8004A818BFB912233c491871b3d84c89A494BD9e",
        "reputation_registry": "0x8004B663056A597Dffe9eCcC1965A193B7388713",
        "facilitator_wallet": "0x34033041a5944B8F10f8E4D8496Bfb84f1A293A8",
        "explorer": "https://hashscan.io/testnet",
        "label": "Hedera Testnet",
    },
    "mainnet": {
        "facilitator_network": "hedera",
        "chain_id": 295,
        "rpc_url": os.environ.get(
            "HEDERA_RPC_URL", "https://mainnet.hashio.io/api"
        ),
        "identity_registry": "0x8004A169FB4a3325136EB29fA0ceB6D2e539a432",
        "reputation_registry": "0x8004BAa17C55a88189AE136b182e5fdA19dE9b63",
        "facilitator_wallet": "0x103040545AC5031A11E8C03dd11324C7333a13C7",
        "explorer": "https://hashscan.io/mainnet",
        "label": "Hedera Mainnet",
    },
}


def get_config() -> dict:
    """Return active Hedera config based on HEDERA_8004_NETWORK."""
    network = HEDERA_8004_NETWORK.lower().strip()
    if network not in _CONFIGS:
        raise ValueError(
            f"Invalid HEDERA_8004_NETWORK='{network}'. Use 'testnet' or 'mainnet'."
        )
    return _CONFIGS[network]


# Convenience accessors
FACILITATOR_URL = os.environ.get(
    "X402_FACILITATOR_URL", "https://facilitator.ultravioletadao.xyz"
)
FACILITATOR_NETWORK = get_config()["facilitator_network"]
CHAIN_ID = get_config()["chain_id"]
RPC_URL = get_config()["rpc_url"]
IDENTITY_REGISTRY = get_config()["identity_registry"]
REPUTATION_REGISTRY = get_config()["reputation_registry"]
FACILITATOR_WALLET = get_config()["facilitator_wallet"]
EXPLORER_URL = get_config()["explorer"]
NETWORK_LABEL = get_config()["label"]
