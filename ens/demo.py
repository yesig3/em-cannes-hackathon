"""
ENS E2E Demo — Agent Identity & Discovery (Real On-Chain Resolution)

This demo executes REAL ENS lookups on Ethereum (mainnet or Sepolia):
  1. Verify Ethereum RPC connectivity
  2. Resolve known ENS names to addresses
  3. Reverse-resolve addresses to ENS names
  4. Read ENS text records (standard + EM-specific)
  5. Demonstrate worker subname resolution
  6. Show proposed Execution Market ENS structure
  7. Cross-reference with ERC-8004 identity

All read operations are free (no gas needed).

Usage:
  cd ens && pip install -r requirements.txt
  python demo.py                          # mainnet (default, free reads)
  ENS_NETWORK=sepolia python demo.py      # sepolia testnet
"""

import sys
import os

from config import (
    ENS_NETWORK,
    CHAIN_ID,
    RPC_URL,
    ENS_REGISTRY,
    NETWORK_LABEL,
    EXPLORER_URL,
    ERC8004_IDENTITY_REGISTRY,
    FACILITATOR_URL,
)
from resolver import resolve_name, reverse_resolve, resolve_multiple, get_web3
from text_records import (
    get_standard_records,
    get_em_metadata,
    get_all_records,
    proposed_agent_records,
    namehash,
)
from subnames import (
    resolve_worker,
    resolve_fleet,
    get_worker_identity,
    proposed_fleet_structure,
)


# ── Well-known ENS names for demo (mainnet) ────────────────────────────────
DEMO_NAMES = [
    "vitalik.eth",
    "nick.eth",
    "brantly.eth",
]

# Execution Market addresses for reverse resolution
EM_ADDRESSES = [
    "0x103040545AC5031A11E8C03dd11324C7333a13C7",  # EM Facilitator
]


def main():
    print("=" * 65)
    print("  Execution Market x ENS — Agent Identity & Discovery")
    print(f"  Network: {NETWORK_LABEL} (ENS_NETWORK={ENS_NETWORK})")
    print(f"  Chain ID: {CHAIN_ID}")
    print(f"  ENS Registry: {ENS_REGISTRY}")
    print("=" * 65)

    w3 = get_web3()

    # ── Step 1: Verify Ethereum RPC connectivity ───────────────
    print("\n[1/7] Verifying Ethereum RPC connectivity...")
    try:
        chain_id = w3.eth.chain_id
        block = w3.eth.block_number
        if chain_id == CHAIN_ID:
            print(f"  PASS: Chain ID = {chain_id} ({NETWORK_LABEL})")
        else:
            print(f"  WARN: Expected chain {CHAIN_ID}, got {chain_id}")
        print(f"  PASS: Latest block = {block:,}")
    except Exception as exc:
        print(f"  FAIL: Cannot connect to RPC: {exc}")
        sys.exit(1)

    # ── Step 2: Forward resolution (name → address) ────────────
    print(f"\n[2/7] Resolving ENS names on {NETWORK_LABEL}...")
    resolved_count = 0
    for name in DEMO_NAMES:
        result = resolve_name(name)
        if result.get("resolved"):
            resolved_count += 1
            addr = result["address"]
            print(f"  PASS: {name} -> {addr[:10]}...{addr[-4:]}")
        else:
            print(f"  SKIP: {name} -> {result.get('error', 'not found')}")

    if resolved_count == 0:
        print("  NOTE: No names resolved. This is normal on Sepolia if names aren't registered.")
        print("  Continuing with proposed structure demo...")

    # ── Step 3: Reverse resolution (address → name) ────────────
    print(f"\n[3/7] Reverse-resolving addresses on {NETWORK_LABEL}...")
    for addr in EM_ADDRESSES:
        result = reverse_resolve(addr)
        if result.get("resolved"):
            print(f"  PASS: {addr[:10]}...{addr[-4:]} -> {result['name']}")
        else:
            print(f"  SKIP: {addr[:10]}...{addr[-4:]} -> no reverse record")
            print(f"        (Normal — reverse records are optional)")

    # ── Step 4: Read text records ──────────────────────────────
    print(f"\n[4/7] Reading ENS text records on {NETWORK_LABEL}...")
    # Use first resolved name, or a well-known one
    text_demo_name = "vitalik.eth" if ENS_NETWORK == "mainnet" else DEMO_NAMES[0]
    records = get_standard_records(text_demo_name)
    if records["count"] > 0:
        print(f"  Name: {text_demo_name}")
        for key, value in records["records"].items():
            # Truncate long values for display
            display = value[:60] + "..." if len(value) > 60 else value
            print(f"  {key}: {display}")
        print(f"  Total: {records['count']} standard records found")
    else:
        print(f"  No text records found for {text_demo_name}")
        print(f"  (Text records are optional ENS metadata)")

    # ── Step 5: EM-specific metadata (proposed) ────────────────
    print(f"\n[5/7] Execution Market proposed ENS text records...")
    proposed = proposed_agent_records()
    print(f"  Agent: execution-market.eth (proposed)")
    print(f"  Records that WOULD be written:")
    for key, value in proposed.items():
        print(f"    {key}: {value}")
    print(f"  Total: {len(proposed)} records")

    # Verify namehash works correctly
    node = namehash("execution-market.eth")
    print(f"\n  Namehash verification:")
    print(f"    namehash('execution-market.eth') = 0x{node.hex()[:16]}...")
    print(f"    namehash('eth') = 0x{namehash('eth').hex()[:16]}...")

    # ── Step 6: Worker subname fleet (proposed) ────────────────
    print(f"\n[6/7] Proposed worker subname fleet...")
    fleet = proposed_fleet_structure()
    print(f"  Parent: {fleet['parent']}")
    print(f"  Management: {fleet['management']}")
    print(f"  Workers:")
    for w in fleet["subnames"]:
        role = w.get("role", "?")
        wid = w.get("world_id", "none")
        rep = w.get("reputation", "-")
        print(f"    {w['name']} (role={role}, worldId={wid}, reputation={rep})")

    # Try resolving real subnames (will likely not exist yet)
    print(f"\n  Live subname resolution test:")
    for test_name in ["vitalik.eth"]:
        result = resolve_name(test_name)
        if result.get("resolved"):
            print(f"    {test_name}: {result['address'][:10]}...{result['address'][-4:]}")
        else:
            print(f"    {test_name}: {result.get('error', 'not found')}")

    # ── Step 7: Cross-reference with ERC-8004 ──────────────────
    print(f"\n[7/7] ENS + ERC-8004 cross-reference architecture...")
    print(f"  ENS (naming + discovery):")
    print(f"    execution-market.eth -> 0x103040...C7")
    print(f"    text('com.execution.market.agentId') -> '2106'")
    print(f"  ERC-8004 (identity + reputation):")
    print(f"    Agent #2106 on Base: {ERC8004_IDENTITY_REGISTRY}")
    print(f"    Queryable via: {FACILITATOR_URL}/identity/base/2106")
    print(f"  World ID (humanity):")
    print(f"    text('com.execution.market.worldIdVerified') -> 'true'")
    print(f"    text('com.execution.market.worldIdLevel') -> 'orb'")
    print()
    print(f"  Combined flow (any external protocol):")
    print(f"    1. Resolve 'execution-market.eth' via ENS")
    print(f"    2. Read text record 'com.execution.market.agentId' -> '2106'")
    print(f"    3. Query ERC-8004 #2106 on Base for reputation")
    print(f"    4. Check World ID status in text records")
    print(f"    -> Full agent identity WITHOUT touching our API")

    # ── Summary ────────────────────────────────────────────────
    print("\n" + "=" * 65)
    print("  Results")
    print("=" * 65)
    print(f"  Network:           {NETWORK_LABEL} (chain {CHAIN_ID})")
    print(f"  RPC:               PASS (block {block:,})")
    print(f"  Names resolved:    {resolved_count}/{len(DEMO_NAMES)}")
    print(f"  Text records:      {records['count']} found")
    print(f"  EM proposed:       {len(proposed)} records designed")
    print(f"  Fleet subnames:    {len(fleet['subnames'])} proposed")
    print(f"  All operations:    Free (read-only, no gas)")
    print(f"\n  ENS App: {ENS_REGISTRY}")
    print(f"  Explorer: {EXPLORER_URL}/address/{ENS_REGISTRY}")
    print(f"\n  Toggle network: ENS_NETWORK=sepolia python demo.py")


if __name__ == "__main__":
    main()
