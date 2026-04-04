"""
Hedera E2E Demo — ERC-8004 Identity + Reputation + Payments

Judges can run this script to see the full integration:
  cd hedera && pip install -r requirements.txt && python demo.py

Configurable via HEDERA_8004_NETWORK env var:
  HEDERA_8004_NETWORK=testnet python demo.py   (default, hackathon)
  HEDERA_8004_NETWORK=mainnet python demo.py   (post-hackathon)
"""

import asyncio
import sys

from config import (
    HEDERA_8004_NETWORK,
    FACILITATOR_NETWORK,
    CHAIN_ID,
    RPC_URL,
    IDENTITY_REGISTRY,
    REPUTATION_REGISTRY,
    EXPLORER_URL,
    NETWORK_LABEL,
    FACILITATOR_URL,
)
from identity import get_identity, get_identity_by_owner, get_total_supply
from reputation import get_reputation
from payment import get_balance, get_chain_id, get_block_number


# Execution Market Agent #2106 (Base) — check if registered on Hedera too
EM_AGENT_ID = 2106
# Facilitator wallet (holds HBAR for gas)
FACILITATOR_WALLET = "0x103040545AC5031A11E8C03dd11324C7333a13C7"


async def main():
    print("=" * 60)
    print(f"  Execution Market x Hedera — E2E Demo")
    print(f"  Network: {NETWORK_LABEL} (HEDERA_8004_NETWORK={HEDERA_8004_NETWORK})")
    print(f"  Chain ID: {CHAIN_ID}")
    print(f"  RPC: {RPC_URL}")
    print(f"  Facilitator: {FACILITATOR_URL}")
    print("=" * 60)

    # ── Step 1: Verify Hedera connectivity ──────────────────────
    print("\n[1/5] Verifying Hedera RPC connectivity...")
    chain_id = await get_chain_id()
    if chain_id == CHAIN_ID:
        print(f"  OK: Chain ID = {chain_id} ({NETWORK_LABEL})")
    else:
        print(f"  ERROR: Expected chain {CHAIN_ID}, got {chain_id}")
        sys.exit(1)

    block = await get_block_number()
    print(f"  OK: Latest block = {block}")

    # ── Step 2: Check ERC-8004 contracts ────────────────────────
    print(f"\n[2/5] ERC-8004 contracts on {NETWORK_LABEL}...")
    print(f"  Identity Registry: {IDENTITY_REGISTRY}")
    print(f"  Reputation Registry: {REPUTATION_REGISTRY}")
    print(f"  Explorer: {EXPLORER_URL}/address/{IDENTITY_REGISTRY}")

    total = await get_total_supply()
    print(f"  Total registered agents: {total}")

    # ── Step 3: Query agent identity ────────────────────────────
    print(f"\n[3/5] Querying Agent #1 on {FACILITATOR_NETWORK}...")
    identity = await get_identity(1)
    if identity.get("found"):
        print(f"  OK: Agent #1 found")
        print(f"  Owner: {identity.get('owner', 'unknown')}")
    else:
        print(f"  Agent #1 not found (no registrations yet on this network)")

    # Check if EM Agent #2106 exists on Hedera
    print(f"\n  Checking EM Agent #{EM_AGENT_ID} on {FACILITATOR_NETWORK}...")
    em_identity = await get_identity(EM_AGENT_ID)
    if em_identity.get("found"):
        print(f"  OK: EM Agent #{EM_AGENT_ID} registered on Hedera!")
    else:
        print(f"  Agent #{EM_AGENT_ID} not registered on Hedera yet")
        print(f"  (Register via POST {FACILITATOR_URL}/register)")

    # ── Step 4: Query reputation ────────────────────────────────
    print(f"\n[4/5] Querying reputation on {FACILITATOR_NETWORK}...")
    rep = await get_reputation(1)
    if "error" not in rep:
        print(f"  OK: Reputation data available")
        print(f"  Data: {rep}")
    else:
        print(f"  No reputation data yet (expected for new network)")

    # ── Step 5: Check Facilitator wallet balance ────────────────
    print(f"\n[5/5] Facilitator wallet balance on {NETWORK_LABEL}...")
    balance = await get_balance(FACILITATOR_WALLET)
    if "error" not in balance:
        print(f"  Wallet: {FACILITATOR_WALLET}")
        print(f"  Balance: {balance['balance_hbar']} HBAR")
        print(f"  Explorer: {balance['explorer']}")
    else:
        print(f"  Could not fetch balance: {balance.get('error')}")

    # ── Summary ─────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  Summary")
    print("=" * 60)
    print(f"  Network:          {NETWORK_LABEL}")
    print(f"  RPC connected:    Yes (block {block})")
    print(f"  ERC-8004:         {IDENTITY_REGISTRY[:10]}...{IDENTITY_REGISTRY[-6:]}")
    print(f"  Agents on chain:  {total}")
    print(f"  Facilitator HBAR: {balance.get('balance_hbar', '?')}")
    print(f"\n  To switch to mainnet: HEDERA_8004_NETWORK=mainnet python demo.py")
    print(f"  To register agent:   POST {FACILITATOR_URL}/register")


if __name__ == "__main__":
    asyncio.run(main())
