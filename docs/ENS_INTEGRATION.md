# ENS Integration — Best ENS Integration for AI Agents

> **Partner**: ENS ($10K) | **Track**: Best ENS Integration for AI Agents
> **Production**: [execution.market](https://execution.market) | **Agent**: #2106 on Base ERC-8004

---

## What We're Building (30-second pitch)

AI agents need **discoverable, human-readable identities** — not just wallet addresses. We're integrating ENS into Execution Market so that:

- **Agents are discoverable by name**: `execution-market.eth` resolves to Agent #2106
- **Worker metadata lives on-chain**: ENS text records store `agentId`, `worldIdVerified`, `role`
- **Worker fleets use subnames**: `alice.execution.eth`, `bob.execution.eth`

This isn't cosmetic — it makes AI agents **queryable by anyone, from any protocol, without our API**.

```
TODAY (database-only identity):

  "Who is Agent #2106?"
     → Must query execution.market API
     → Locked inside our database
     → Not discoverable externally

WITH ENS:

  "Who is execution-market.eth?"
     → Anyone can resolve via ENS (no API needed)
     → Metadata in text records (on-chain, permanent)
     → Discoverable in ENS explorers, wallets, other dApps
```

---

## Why ENS + Execution Market

ENS's prize explicitly asks for:

| Requirement | How We Meet It |
|-------------|----------------|
| "Use ENS to name agents, resolve addresses" | `execution-market.eth` → Agent #2106 address |
| "Store agent metadata in text records" | `agentId`, `worldIdVerified`, `role`, `reputation` |
| "Spin up subname registries for agent fleets" | Workers get `alice.execution.eth` subnames |
| "Not just cosmetic — must improve identity or discoverability" | Agents queryable cross-protocol without our API |
| "Functional demos (no hard-coded values)" | Live resolution against Sepolia ENS |

---

## Architecture

### ENS as the Naming Layer for ERC-8004

```
┌─────────────────────────────────────────────────────────────┐
│                    IDENTITY STACK                           │
│                                                             │
│  ┌─────────────┐    ┌──────────────┐    ┌───────────────┐  │
│  │ ENS Names   │    │  ERC-8004    │    │   World ID    │  │
│  │ (discovery) │    │  (identity)  │    │  (humanity)   │  │
│  └──────┬──────┘    └──────┬───────┘    └───────┬───────┘  │
│         │                  │                    │           │
│    Human-readable     On-chain agent       ZK proof of     │
│    names + metadata   ID + reputation      unique human    │
│         │                  │                    │           │
│         └──────────────────┼────────────────────┘           │
│                            │                                │
│                    ┌───────▼────────┐                       │
│                    │ Execution      │                       │
│                    │ Market         │                       │
│                    │ (marketplace)  │                       │
│                    └────────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

### Resolution Flow

```
┌──────────┐    ┌─────────────┐    ┌──────────────┐    ┌──────────┐
│  Anyone  │    │ ENS Resolver│    │  Text Records│    │ ERC-8004 │
│ (query)  │    │  (on-chain) │    │  (on-chain)  │    │ Registry │
└────┬─────┘    └──────┬──────┘    └──────┬───────┘    └────┬─────┘
     │                 │                  │                  │
     │ resolve         │                  │                  │
     │ "execution-     │                  │                  │
     │  market.eth"    │                  │                  │
     │────────────────>│                  │                  │
     │                 │                  │                  │
     │ 0x103040...     │                  │                  │
     │<────────────────│                  │                  │
     │                 │                  │                  │
     │ getText         │                  │                  │
     │ "com.execution  │                  │                  │
     │  .market.       │                  │                  │
     │  agentId"       │                  │                  │
     │────────────────>│─────────────────>│                  │
     │                 │                  │                  │
     │ "2106"          │                  │                  │
     │<────────────────│<─────────────────│                  │
     │                 │                  │                  │
     │ Now query       │                  │                  │
     │ ERC-8004 #2106  │                  │                  │
     │─────────────────│──────────────────│─────────────────>│
     │                 │                  │                  │
     │ Full agent      │                  │                  │
     │ identity +      │                  │                  │
     │ reputation      │                  │                  │
     │<────────────────│──────────────────│──────────────────│
```

### Subname Registry for Workers

```
execution.eth (agent owner)
    │
    ├── alice.execution.eth  → 0xAlice... (worker wallet)
    │     └── text: role=worker, worldIdVerified=true, rating=4.8
    │
    ├── bob.execution.eth    → 0xBob... (worker wallet)
    │     └── text: role=worker, worldIdVerified=false, rating=4.2
    │
    └── oracle.execution.eth → 0xOracle... (AI verifier)
          └── text: role=verifier, agentId=2106
```

---

## ENS Text Records Schema

| Key | Example Value | Purpose |
|-----|---------------|---------|
| `com.execution.market.agentId` | `"2106"` | ERC-8004 agent ID (cross-reference) |
| `com.execution.market.role` | `"agent"` or `"worker"` | Role in the marketplace |
| `com.execution.market.worldIdVerified` | `"true"` | World ID verification status |
| `com.execution.market.worldIdLevel` | `"orb"` | Verification level (orb/device) |
| `com.execution.market.reputation` | `"4.8"` | On-chain reputation score |
| `com.execution.market.tasksCompleted` | `"127"` | Total tasks completed |
| `url` | `"https://execution.market"` | Platform URL |
| `description` | `"Universal Execution Layer"` | Agent description |
| `avatar` | `"eip155:8453/erc721:0x8004.../2106"` | NFT avatar (ERC-8004 identity NFT) |

---

## Implementation Plan

### Files to Build

```
ens/
├── README.md              # ENS-specific guide for judges
├── resolver.py            # ENS name → address resolution
├── text_records.py        # Read/write agent metadata in ENS records
├── subnames.py            # Create/resolve worker subnames
├── demo.py                # End-to-end: resolve + records + subnames
├── requirements.txt       # web3[ens], python-dotenv
└── tests/
    └── test_resolver.py   # Mock ENS, test resolution + records
```

### Phase-by-Phase

**Phase 4.1: resolver.py (~30 min)**
```python
from web3 import Web3

w3 = Web3(Web3.HTTPProvider(ETHEREUM_RPC_URL))

def resolve_agent(name: str) -> str:
    """Resolve ENS name to address."""
    return w3.ens.address(name)
    # "execution-market.eth" → "0x103040..."

def reverse_resolve(address: str) -> str:
    """Address to ENS name."""
    return w3.ens.name(address)
    # "0x103040..." → "execution-market.eth"
```

**Phase 4.2: text_records.py (~1 hour)**
```python
def get_agent_metadata(name: str) -> dict:
    """Read all EM text records from ENS."""
    resolver = w3.ens.resolver(name)
    return {
        "agentId": resolver.caller.text(namehash(name), "com.execution.market.agentId"),
        "role": resolver.caller.text(namehash(name), "com.execution.market.role"),
        "worldIdVerified": resolver.caller.text(namehash(name), "com.execution.market.worldIdVerified"),
        # ...
    }
```

**Phase 4.3: subnames.py (~1.5 hours)**
```python
def resolve_worker(worker_name: str) -> dict:
    """Resolve worker subname to address + metadata."""
    # "alice.execution.eth" → {address, role, worldIdVerified, ...}
    address = w3.ens.address(worker_name)
    metadata = get_agent_metadata(worker_name)
    return {"address": address, **metadata}
```

**Phase 4.4: demo.py (~30 min)**
```bash
python demo.py
# Output:
#   1. Resolving execution-market.eth → 0x103040...
#   2. Reading text records:
#      agentId: 2106
#      role: agent
#      worldIdVerified: true
#   3. Resolving alice.execution.eth → 0xAlice...
#      role: worker, rating: 4.8
#   4. Cross-referencing ERC-8004 #2106 on Base...
#      Agent verified, reputation: 4.8/5.0
```

---

## Demo for Judges

### What Judges Run

```bash
cd ens
pip install -r requirements.txt

# Resolve agent name
python -c "from resolver import resolve_agent; print(resolve_agent('execution-market.eth'))"
# → 0x103040545AC5031A11E8C03dd11324C7333a13C7

# Read metadata
python -c "from text_records import get_agent_metadata; print(get_agent_metadata('execution-market.eth'))"
# → {agentId: "2106", role: "agent", worldIdVerified: "true"}

# Full demo
python demo.py
```

### What Judges See on execution.market

- Worker profiles show ENS name (if registered)
- Agent profiles show ENS name alongside ERC-8004 ID
- Text records queryable without our API (decentralized)

---

## Why This Isn't Cosmetic

### Problem 1: Agent Discoverability
Without ENS: To find Agent #2106, you must know our API URL and the numeric ID. No Google, no wallet lookup, no cross-protocol discovery.
With ENS: `execution-market.eth` is resolvable from any ENS client, wallet, or dApp. Google indexes `.eth` names.

### Problem 2: Metadata Lock-In
Without ENS: Worker metadata (reputation, World ID status) lives in our Supabase database. If our API goes down, the data is inaccessible.
With ENS: Critical metadata in text records is on-chain, permanent, queryable by anyone without trusting our API.

### Problem 3: Fleet Management
Without ENS: 10 workers = 10 wallet addresses. No hierarchy, no discovery.
With ENS: `alice.execution.eth`, `bob.execution.eth` — a fleet under one domain. Discoverable, hierarchical, on-chain.

### Problem 4: Cross-Protocol Identity
Without ENS: Other AI agent protocols can't look up our agents without integrating our API.
With ENS: Any protocol can resolve `execution-market.eth` → get address → read text records → find ERC-8004 agent ID → query on-chain reputation. Zero integration needed.

---

## FAQ

**Q: Do you own execution-market.eth?**
A: For the hackathon demo, we use Sepolia testnet (free registration). Production ENS registration is planned post-hackathon.

**Q: Why not just use ERC-8004 for everything?**
A: ERC-8004 provides on-chain identity and reputation. ENS provides **naming and discovery**. They're complementary layers: ENS is how you FIND an agent, ERC-8004 is how you TRUST it.

**Q: How do subnames work for worker fleets?**
A: The agent owner registers `execution.eth`, then creates subnames via NameWrapper. Workers get `alice.execution.eth` automatically when they register on the platform. The subname resolves to their wallet and carries their metadata.

**Q: What about ENS on L2s?**
A: ENS supports L2 resolution via CCIP-Read (EIP-3668). Worker subnames could be managed on Base (low cost) while resolving on mainnet. This aligns with our existing Base-first architecture.

**Q: How does this integrate with World ID?**
A: When a worker verifies with World ID, their ENS text record `com.execution.market.worldIdVerified` is updated to `"true"`. Anyone resolving their ENS name can see they're a verified human — without touching our API or database.

---

## Implementation Status

| Component | Status | ETA |
|-----------|--------|-----|
| Architecture design | DONE | This document |
| resolver.py | TODO | 30 min |
| text_records.py | TODO | 1 hour |
| subnames.py | TODO | 1.5 hours |
| demo.py | TODO | 30 min |
| Tests | TODO | 1 hour |
| README | TODO | 30 min |
| Sepolia registration | TODO | 15 min |

**Total estimated**: ~5 hours

---

## Related Documentation

- [World Integration Guide](./WORLD_JUDGES_GUIDE.md) — World ID + AgentKit details
- [Hedera Integration Plan](./HEDERA_INTEGRATION.md) — Hedera payments + ERC-8004
- [Production API Docs](https://api.execution.market/docs) — Full Swagger UI
- [ERC-8004 Registry](https://basescan.org/address/0x8004A169FB4a3325136EB29fA0ceB6D2e539a432) — On-chain identity
