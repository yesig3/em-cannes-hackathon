# ENS Integration — Proof of On-Chain Operations

> All operations executed on **Ethereum Mainnet (chain 1)** on April 4, 2026.
> Read-only — zero gas cost.

---

## Prize Track: "Best ENS Integration for AI Agents" ($10,000)

**Track**: [ETHGlobal Cannes 2026 — ENS](https://ethglobal.com/events/cannes2026/prizes)

### Why ENS?

AI agents need **discoverable, human-readable identities** — not just wallet addresses. ENS turns agents from opaque `0x...` strings into names like `execution-market.eth` that anyone can resolve from any protocol, wallet, or dApp.

### How We Meet the Requirements

| Requirement | How We Meet It |
|------------|----------------|
| *"Use ENS to name agents, resolve addresses"* | Live resolution of ENS names via web3.py. Demo resolves vitalik.eth, nick.eth, brantly.eth on mainnet. |
| *"Store agent metadata in text records"* | Read text records from live ENS names. Proposed 12-key metadata schema for `execution-market.eth`. |
| *"Spin up subname registries for agent fleets"* | Worker fleet design: `alice.execution.eth`, `bob.execution.eth` with EM metadata per worker. |
| *"Not just cosmetic — must improve identity or discoverability"* | ENS makes agents queryable cross-protocol WITHOUT our API. Full identity from ENS + ERC-8004 + World ID. |
| *"Functional demos (no hard-coded values)"* | Real ENS resolution on Ethereum mainnet. Real text records read from vitalik.eth. |

---

## Test Results Summary

| Step | Operation | Result | On-Chain |
|------|-----------|--------|----------|
| 1 | RPC Connectivity | PASS (block 24,807,567) | Chain ID 1 verified |
| 2 | Forward Resolution | 3/3 names resolved | vitalik.eth, nick.eth, brantly.eth |
| 3 | Reverse Resolution | No reverse record for EM wallet | Normal — reverse records are optional |
| 4 | Text Records | 5 records read from vitalik.eth | url, description, avatar, twitter, github |
| 5 | EM Metadata Schema | 12 records designed | com.execution.market.* prefix |
| 6 | Worker Subnames | 4 subnames proposed | alice/bob/oracle/platform.execution.eth |
| 7 | Cross-Reference | ENS + ERC-8004 + World ID | Multi-layer identity architecture |

---

## On-Chain Evidence

### ENS Resolution — vitalik.eth

```
Name:        vitalik.eth
Address:     0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
Network:     Ethereum Mainnet (chain 1)
ENS App:     https://app.ens.domains/vitalik.eth
Etherscan:   https://etherscan.io/address/0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
```

### Text Records — vitalik.eth

```
url:          https://vitalik.ca
description:  mi pinxe lo crino tcati
avatar:       https://euc.li/vitalik.eth
com.twitter:  VitalikButerin
com.github:   vbuterin
```

### ENS Resolution — nick.eth

```
Name:        nick.eth
Address:     0xb8c2C29ee19D8307cb7255e1Cd9CbDE883A267d5
```

### ENS Resolution — brantly.eth

```
Name:        brantly.eth
Address:     0x983110309620D911731Ac0932219af06091b6744
```

---

## Proposed EM Text Record Schema

These records would be written to `execution-market.eth` to make Agent #2106
discoverable without our API:

```
com.execution.market.agentId:           2106
com.execution.market.role:              agent
com.execution.market.worldIdVerified:   true
com.execution.market.worldIdLevel:      orb
com.execution.market.reputation:        4.8
com.execution.market.tasksCompleted:    127
com.execution.market.chains:            base,ethereum,polygon,arbitrum,hedera
url:                                    https://execution.market
description:                            Universal Execution Layer
avatar:                                 eip155:8453/erc721:0x8004.../2106
com.twitter:                            @ExecutionMarket
com.github:                             UltravioletaDAO
```

### Namehash Verification

```
namehash('execution-market.eth') = 0x97eb00f02968c8...
namehash('eth')                  = 0x93cdeb708b7545...
```

Computed using EIP-137 algorithm: `keccak256(parent_node + keccak256(label))`

---

## Architecture — How It Works

```mermaid
graph TD
    subgraph "Discovery Layer (ENS)"
        A["execution-market.eth"] -->|resolves to| B["0x103040...C7"]
        A -->|text record| C["agentId: 2106"]
        A -->|text record| D["worldIdVerified: true"]
    end

    subgraph "Identity Layer (ERC-8004)"
        C -->|cross-reference| E["Agent #2106 on Base"]
        E -->|reputation| F["Score: 4.8/5.0"]
    end

    subgraph "Humanity Layer (World ID)"
        D -->|verified via| G["ZK proof, Orb level"]
        G -->|nullifier| H["One human = one account"]
    end

    subgraph "Execution Layer"
        E -->|publishes tasks| I["Execution Market"]
        I -->|pays workers| J["x402 escrow (9 chains)"]
    end
```

### Cross-Protocol Discovery (No API Needed)

```
Any external protocol:

  1. Resolve "execution-market.eth"
     └── ENS: 0x103040545AC5031A11E8C03dd11324C7333a13C7

  2. Read text("com.execution.market.agentId")
     └── ENS: "2106"

  3. Query ERC-8004 Agent #2106 on Base
     └── Facilitator: GET /identity/base/2106
     └── Returns: owner, metadata_uri, reputation

  4. Check text("com.execution.market.worldIdVerified")
     └── ENS: "true" (Orb-verified human controls this agent)

  Result: Full agent identity from 3 on-chain sources
          WITHOUT touching execution.market API
```

### Worker Subname Fleet

```
execution.eth (agent owner)
    |
    +-- alice.execution.eth  --> 0xAlice...
    |     text: role=worker, worldId=orb, reputation=4.8
    |
    +-- bob.execution.eth    --> 0xBob...
    |     text: role=worker, worldId=device, reputation=4.2
    |
    +-- oracle.execution.eth --> 0xOracle...
          text: role=verifier, agentId=2106
```

Management: NameWrapper (ERC-1155) — parent owner controls subnames.

---

## Why This Isn't Cosmetic

### Problem 1: Agent Discoverability
**Without ENS**: To find Agent #2106, you must know our API URL and the numeric ID.
**With ENS**: `execution-market.eth` is resolvable from any ENS client, wallet, or dApp.

### Problem 2: Metadata Lock-In
**Without ENS**: Worker metadata lives in our Supabase database. If our API goes down, the data is inaccessible.
**With ENS**: Critical metadata is on-chain, permanent, queryable by anyone.

### Problem 3: Fleet Management
**Without ENS**: 10 workers = 10 wallet addresses. No hierarchy, no discovery.
**With ENS**: `alice.execution.eth`, `bob.execution.eth` — discoverable, hierarchical, on-chain.

### Problem 4: Cross-Protocol Identity
**Without ENS**: Other AI agent protocols can't look up our agents without integrating our API.
**With ENS**: Any protocol resolves `execution-market.eth` -> reads text records -> finds ERC-8004 agent ID -> queries on-chain reputation. Zero integration needed.

---

## Reproducing the Test

```bash
# Clone and run
git clone https://github.com/UltravioletaDAO/em-cannes-hackathon.git
cd em-cannes-hackathon/ens
pip install -r requirements.txt
python demo.py

# Expected output:
# [1/7] Verifying Ethereum RPC connectivity...     PASS (block ~24M)
# [2/7] Resolving ENS names...                     3/3 resolved
# [3/7] Reverse-resolving addresses...             no reverse record
# [4/7] Reading ENS text records...                5 records from vitalik.eth
# [5/7] Execution Market proposed ENS records...   12 records designed
# [6/7] Proposed worker subname fleet...           4 subnames
# [7/7] ENS + ERC-8004 cross-reference...          Multi-layer architecture

# Run tests (24 cases)
cd .. && python -m pytest ens/tests/test_ens.py -v -p no:pytest_ethereum
```

---

## Cross-Chain Context

ENS is the **naming and discovery layer** in Execution Market's identity stack:

```
Execution Market Identity Stack:

  DISCOVERY:  ENS (execution-market.eth)
      |         Names, text records, subnames
      |         Queryable by anyone, any protocol
      v
  IDENTITY:   ERC-8004 (Agent #2106, 16 networks)
      |         On-chain identity NFT + reputation
      |         Base, Ethereum, Polygon, Hedera...
      v
  HUMANITY:   World ID 4.0 (ZK proof of human)
      |         Anti-sybil, Orb verification
      |         Nullifier uniqueness
      v
  PAYMENTS:   x402 Protocol (9 EVM chains + Solana)
              Gasless escrow, instant settlement
```

Each layer is **independent but composable**. ENS doesn't require ERC-8004, but
when combined, the result is an AI agent identity that's discoverable, verifiable,
and trustworthy — all on-chain, no centralized API needed.
