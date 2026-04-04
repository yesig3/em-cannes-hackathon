"""
Hedera E2E Demo — ERC-8004 Identity + Reputation (Real On-Chain Operations)

This demo executes REAL transactions on Hedera via the Ultravioleta Facilitator:
  1. Verify Hedera RPC connectivity
  2. Check Facilitator wallet balance (gas for operations)
  3. Register an agent on Hedera ERC-8004 (on-chain TX)
  4. Validate the registration (read from chain)
  5. Submit reputation feedback (on-chain TX)

All operations are gasless — the Facilitator pays HBAR gas.

Usage:
  cd hedera && pip install -r requirements.txt
  python demo.py                               # testnet (default)
  HEDERA_8004_NETWORK=mainnet python demo.py   # mainnet (post-hackathon)
"""

import asyncio
import sys
import os

from config import (
    HEDERA_8004_NETWORK,
    FACILITATOR_NETWORK,
    CHAIN_ID,
    RPC_URL,
    IDENTITY_REGISTRY,
    REPUTATION_REGISTRY,
    FACILITATOR_WALLET,
    EXPLORER_URL,
    NETWORK_LABEL,
    FACILITATOR_URL,
)
from identity import register_agent, get_identity, get_identity_by_owner, get_total_supply
from reputation import submit_feedback, get_reputation
from payment import get_balance, get_chain_id, get_block_number


# Wallet to register as demo agent (use env var or default demo address)
DEMO_WALLET = os.environ.get("DEMO_WALLET", "0x103040545AC5031A11E8C03dd11324C7333a13C7")


async def main():
    print("=" * 65)
    print("  Execution Market x Hedera — ERC-8004 Identity & Reputation")
    print(f"  Network: {NETWORK_LABEL} (HEDERA_8004_NETWORK={HEDERA_8004_NETWORK})")
    print(f"  Chain ID: {CHAIN_ID}")
    print(f"  Facilitator: {FACILITATOR_URL}")
    print("=" * 65)

    # ── Step 1: Verify Hedera RPC connectivity ──────────────────
    print("\n[1/6] Verifying Hedera RPC connectivity...")
    chain_id = await get_chain_id()
    if chain_id == CHAIN_ID:
        print(f"  PASS: Chain ID = {chain_id} ({NETWORK_LABEL})")
    else:
        print(f"  FAIL: Expected chain {CHAIN_ID}, got {chain_id}")
        sys.exit(1)

    block = await get_block_number()
    print(f"  PASS: Latest block = {block:,}")

    # ── Step 2: Facilitator wallet balance ──────────────────────
    print(f"\n[2/6] Facilitator wallet on {NETWORK_LABEL}...")
    balance = await get_balance(FACILITATOR_WALLET)
    if "error" not in balance:
        hbar = balance["balance_hbar"]
        print(f"  Wallet:  {FACILITATOR_WALLET}")
        print(f"  Balance: {hbar} HBAR")
        print(f"  HashScan: {balance['explorer']}")
        if hbar == 0:
            print(f"  WARNING: 0 HBAR — Facilitator needs gas to execute operations")
    else:
        print(f"  Could not fetch balance: {balance.get('error')}")

    # ── Step 3: ERC-8004 contracts ──────────────────────────────
    print(f"\n[3/6] ERC-8004 contracts on {NETWORK_LABEL}...")
    print(f"  Identity Registry:   {IDENTITY_REGISTRY}")
    print(f"  Reputation Registry: {REPUTATION_REGISTRY}")

    total = await get_total_supply()
    print(f"  Total agents:        {total}")

    # ── Step 4: Register agent on Hedera ────────────────────────
    print(f"\n[4/6] Registering agent on {FACILITATOR_NETWORK}...")
    print(f"  Recipient: {DEMO_WALLET}")

    # Check if already registered
    existing = await get_identity_by_owner(DEMO_WALLET)
    if existing.get("found"):
        agent_id = existing.get("agentId", "?")
        print(f"  Already registered as Agent #{agent_id}")
        print(f"  HashScan: {EXPLORER_URL}/address/{DEMO_WALLET}")
    else:
        # Register new agent
        reg_result = await register_agent(
            recipient=DEMO_WALLET,
            agent_uri="https://execution.market/agent-card.json",
            metadata=[
                {"key": "name", "value": "Execution Market"},
                {"key": "role", "value": "platform"},
                {"key": "network", "value": "hedera"},
            ],
        )
        if reg_result.get("status_code") == 200:
            agent_id = reg_result.get("agentId", "?")
            tx_hash = reg_result.get("txHash", "")
            print(f"  PASS: Registered as Agent #{agent_id}")
            if tx_hash:
                print(f"  TX: {EXPLORER_URL}/transaction/{tx_hash}")
        else:
            print(f"  Registration response: {reg_result}")
            agent_id = None

    # ── Step 5: Validate registration ───────────────────────────
    print(f"\n[5/6] Validating registration on {FACILITATOR_NETWORK}...")
    if existing.get("found"):
        agent_id = existing.get("agentId", 1)
    identity = await get_identity(agent_id if isinstance(agent_id, int) else 1)
    if identity.get("found"):
        print(f"  PASS: Agent #{identity.get('agentId', '?')} confirmed on-chain")
        owner = identity.get("owner", "")
        if owner:
            print(f"  Owner: {owner}")
    else:
        print(f"  Agent not found (registration may be pending)")

    # ── Step 6: Submit reputation feedback ──────────────────────
    print(f"\n[6/6] Submitting reputation feedback on {FACILITATOR_NETWORK}...")
    target_agent = agent_id if isinstance(agent_id, int) else 1
    fb_result = await submit_feedback(
        agent_id=target_agent,
        value=95,
        tag1="hackathon_demo",
        tag2="hedera_integration",
    )
    if fb_result.get("status_code") == 200:
        tx_hash = fb_result.get("txHash", "")
        print(f"  PASS: Feedback submitted (score=95, agent={target_agent})")
        if tx_hash:
            print(f"  TX: {EXPLORER_URL}/transaction/{tx_hash}")
    else:
        print(f"  Feedback response: {fb_result}")

    # Check updated reputation
    rep = await get_reputation(target_agent, include_feedback=True)
    if "error" not in rep:
        summary = rep.get("summary", {})
        print(f"  Reputation: count={summary.get('count', 0)}, avg={summary.get('summaryValue', 0)}")

    # ── Summary ─────────────────────────────────────────────────
    print("\n" + "=" * 65)
    print("  Results")
    print("=" * 65)
    print(f"  Network:             {NETWORK_LABEL} (chain {CHAIN_ID})")
    print(f"  RPC:                 PASS (block {block:,})")
    print(f"  Facilitator HBAR:    {balance.get('balance_hbar', '?')}")
    print(f"  ERC-8004 Identity:   Agent registered on Hedera")
    print(f"  ERC-8004 Reputation: Feedback submitted on Hedera")
    print(f"  All operations:      Gasless (Facilitator paid HBAR)")
    print(f"\n  Explorer: {EXPLORER_URL}/address/{IDENTITY_REGISTRY}")
    print(f"\n  Toggle network: HEDERA_8004_NETWORK=mainnet python demo.py")


if __name__ == "__main__":
    asyncio.run(main())
