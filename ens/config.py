"""
ENS Network Configuration

Toggle between Sepolia testnet and Ethereum mainnet via ENS_NETWORK env var.
Default: mainnet (read-only operations are free — no gas needed for resolution).
"""

import os

# ── Network toggle ──────────────────────────────────────────────────────────
# "mainnet" (default, free reads) or "sepolia" (testnet, for write demos)
ENS_NETWORK = os.environ.get("ENS_NETWORK", "mainnet")

# ── Derived configuration ───────────────────────────────────────────────────

_CONFIGS = {
    "mainnet": {
        "chain_id": 1,
        "rpc_url": os.environ.get(
            "ETHEREUM_RPC_URL",
            "https://ethereum-rpc.publicnode.com",
        ),
        "ens_registry": "0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e",
        "ens_universal_resolver": "0xce01f8eee7E479C928F8919abD53E553a36CeF67",
        "explorer": "https://etherscan.io",
        "ens_app": "https://app.ens.domains",
        "label": "Ethereum Mainnet",
    },
    "sepolia": {
        "chain_id": 11155111,
        "rpc_url": os.environ.get(
            "SEPOLIA_RPC_URL",
            "https://ethereum-sepolia-rpc.publicnode.com",
        ),
        "ens_registry": "0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e",
        "ens_universal_resolver": "0xc8Af999e38273D658BE1b921b88A9Ddf005769cC",
        "explorer": "https://sepolia.etherscan.io",
        "ens_app": "https://app.ens.domains",
        "label": "Sepolia Testnet",
    },
}


def get_config() -> dict:
    """Return active ENS config based on ENS_NETWORK."""
    network = ENS_NETWORK.lower().strip()
    if network not in _CONFIGS:
        raise ValueError(
            f"Invalid ENS_NETWORK='{network}'. Use 'mainnet' or 'sepolia'."
        )
    return _CONFIGS[network]


# Convenience accessors
CHAIN_ID = get_config()["chain_id"]
RPC_URL = get_config()["rpc_url"]
ENS_REGISTRY = get_config()["ens_registry"]
UNIVERSAL_RESOLVER = get_config()["ens_universal_resolver"]
EXPLORER_URL = get_config()["explorer"]
ENS_APP_URL = get_config()["ens_app"]
NETWORK_LABEL = get_config()["label"]

# ERC-8004 cross-reference (same contracts as hedera/ and world/)
ERC8004_IDENTITY_REGISTRY = "0x8004A169FB4a3325136EB29fA0ceB6D2e539a432"
FACILITATOR_URL = os.environ.get(
    "X402_FACILITATOR_URL", "https://facilitator.ultravioletadao.xyz"
)

# ── Execution Market ENS Configuration ──────────────────────────────────────
# Text record keys for agent metadata
EM_TEXT_RECORD_PREFIX = "com.execution.market"
EM_TEXT_RECORDS = {
    "agentId": f"{EM_TEXT_RECORD_PREFIX}.agentId",
    "role": f"{EM_TEXT_RECORD_PREFIX}.role",
    "worldIdVerified": f"{EM_TEXT_RECORD_PREFIX}.worldIdVerified",
    "worldIdLevel": f"{EM_TEXT_RECORD_PREFIX}.worldIdLevel",
    "reputation": f"{EM_TEXT_RECORD_PREFIX}.reputation",
    "tasksCompleted": f"{EM_TEXT_RECORD_PREFIX}.tasksCompleted",
    "chains": f"{EM_TEXT_RECORD_PREFIX}.chains",
}
