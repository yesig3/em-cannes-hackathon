# Hedera Track -- Judges Guide

> **For judges at the Hedera booth, ETHGlobal Cannes 2026.**
> Everything you need to evaluate our submission in one document.

---

## TL;DR

Execution Market is a **live production marketplace** where AI agents post bounties and humans complete them for instant payment. We built **five Hedera integrations** for this hackathon, including **HCS (Hedera Consensus Service)** -- a Hedera-NATIVE feature that is NOT accessible via EVM or JSON-RPC. Our Golden Flow E2E test passes **7/7 phases** with **5 on-chain transactions + 6 HCS messages** across 2 chains.

---

## 1. What is HCS (Hedera Consensus Service)?

HCS is a **Hedera-native feature** -- it is NOT part of the EVM and cannot be accessed through JSON-RPC relay or any generic EVM tooling.

**What it does:**
- Creates an **immutable, ordered event log** with consensus timestamps agreed by Hedera's network nodes (not client-supplied timestamps)
- Messages are submitted via `TopicCreateTransaction` and `TopicMessageSubmitTransaction` from the **hiero-sdk-python** (official Hedera SDK)
- Once submitted, messages **cannot be altered or deleted**
- Any third party can read and verify messages via the **public Mirror Node REST API** -- no authentication, no API key, completely open

**Why it matters for this submission:**
- Proves we use Hedera **beyond generic EVM compatibility** -- HCS requires the native Hedera SDK
- Creates a **tamper-proof audit trail** of every task lifecycle event
- Messages include cross-chain references (Base TX hashes), linking payment evidence across chains
- Consensus timestamps provide **ordering guarantees** that client-side timestamps cannot

**Our implementation:** `hedera/hcs_logger.py` -- a Python module using `hiero-sdk-python` that creates topics and submits structured JSON messages for each lifecycle event.

---

## 2. Track: "AI & Agentic Payments on Hedera" ($6,000)

| Detail | Value |
|--------|-------|
| **Track** | AI & Agentic Payments on Hedera |
| **Prize** | $6,000 (up to 2 teams at $3,000 each) |
| **Requirement** | "Execute at least one payment, token transfer, or financial operation on Hedera Testnet" |
| **Accepted technologies** | ERC-8004 (Trustless Agents), x402, Hedera SDKs, HCS, Hedera Agent Kit, OpenClaw ACP, A2A |

**How we meet the requirement:**

We executed **four categories of on-chain operations** on Hedera Testnet:

1. **ERC-8004 Agent Registration** -- NFT mint (token transfer) registering Agent #99
2. **Bidirectional Reputation Feedback** -- on-chain state writes (agent rates worker + worker rates agent)
3. **Merit Tip: 0.01 HBAR** -- direct HBAR transfer to worker, gated by reputation score
4. **HCS Event Logging** -- 6 immutable consensus messages via native TopicMessageSubmitTransaction

**Accepted technologies we use:**

| Technology | How we use it |
|-----------|---------------|
| **ERC-8004** (Trustless Agents) | On-chain agent identity + bidirectional reputation |
| **x402** (Payment Standard) | Production payment protocol on 9 EVM chains |
| **hiero-sdk-python** (Hedera SDK) | HCS topic creation + message submission (native, not EVM) |
| **HCS** (Hedera Consensus Service) | Immutable event logging -- 6 lifecycle messages per task |
| **Facilitator** (open-source, Rust) | Gasless operations on Hedera (extended for this hackathon) |

---

## 3. What We Built on Hedera (Complete List)

### 3.1 ERC-8004 Identity (EVM)

Agent #99 registered on Hedera Testnet via the ERC-8004 Identity Registry. Same CREATE2-deployed contract used on 16 networks. The agent has an on-chain identity discoverable by any other agent on Hedera.

- **Contract**: `0x8004A818BFB912233c491871b3d84c89A494BD9e`
- **Agent ID**: 99
- **Verify**: `GET https://facilitator.ultravioletadao.xyz/identity/hedera-testnet/99`

### 3.2 ERC-8004 Bidirectional Reputation (EVM)

Both agent-to-worker and worker-to-agent reputation scores written to the Reputation Registry on Hedera Testnet. These are real on-chain state writes that create verifiable trust signals.

- **Contract**: `0x8004B663056A597Dffe9eCcC1965A193B7388713`
- **Feedback Count**: 29 entries, average score 87/100
- **Verify**: `GET https://facilitator.ultravioletadao.xyz/reputation/hedera-testnet/99`

### 3.3 Merit Tip: 0.01 HBAR (EVM Transfer)

When a worker receives a reputation score above the threshold, the agent automatically sends a **direct HBAR transfer** as a merit reward. This is a real payment on Hedera Testnet, gated by on-chain reputation data.

- **Amount**: 0.01 HBAR per merit tip
- **TX**: [`0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321`](https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321)
- **Mechanism**: Reputation-gated -- only workers who deliver quality work receive the tip

### 3.4 HCS Event Log (NATIVE -- Not EVM)

Every task lifecycle event is logged as an immutable, timestamped, ordered message on an HCS topic. This uses `hiero-sdk-python` with `TopicCreateTransaction` and `TopicMessageSubmitTransaction` -- **Hedera-native APIs that are NOT accessible via EVM or JSON-RPC relay.**

- **Topic**: `0.0.8511429`
- **Messages**: 6 lifecycle events per task
- **Mirror Node**: `https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages`
- **SDK**: `hiero-sdk-python` (official Hedera Python SDK)

**The 6 events logged:**

| Seq | Event | What it records |
|-----|-------|-----------------|
| 1 | `task_created` | Task ID, bounty amount, deadline, payment chain |
| 2 | `worker_applied` | Executor ID, application timestamp |
| 3 | `escrow_locked` | Base TX hash of escrow lock (cross-chain reference) |
| 4 | `payment_released` | Base TX hash of payment release, amount |
| 5 | `reputation_agent_to_worker` | Score, Hedera TX hash |
| 6 | `reputation_worker_to_agent` | Score, Hedera TX hash |

### 3.5 Facilitator Extension (Open-Source, Rust)

Extended the [x402-rs Facilitator](https://github.com/UltravioletaDAO/x402-rs) (production Rust server, 21 blockchains) to support Hedera mainnet (chain 295) + testnet (chain 296). This is not a demo wrapper -- it is a contribution to open-source infrastructure that any project can use.

- **Commit**: [`66d34e6`](https://github.com/UltravioletaDAO/x402-rs/commit/66d34e6c7f805fa26a33757b2cdf5ec3038ecb95)
- **What it does**: Pays HBAR gas for all Hedera operations so agents never need to hold HBAR

---

## 4. How to Verify (For Judges)

All evidence is publicly verifiable. No account or API key needed.

### HCS Messages (Hedera-Native Event Log)

Open in browser or curl:

```
https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages
```

Each message contains:
- `sequence_number` -- ordering guaranteed by Hedera consensus
- `consensus_timestamp` -- timestamp agreed by network nodes
- `message` -- base64-encoded JSON with event type and payload

To decode a message:

```bash
curl -s "https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages" \
  | python3 -c "import sys,json,base64; msgs=json.load(sys.stdin)['messages']; [print(base64.b64decode(m['message']).decode()) for m in msgs]"
```

### Merit Tip Transaction

```
https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321
```

Shows a direct 0.01 HBAR transfer from the Facilitator wallet to the worker address.

### Agent Identity

```
GET https://facilitator.ultravioletadao.xyz/identity/hedera-testnet/99
```

Returns Agent #99's on-chain identity metadata (name, role, URI).

### Agent Reputation

```
GET https://facilitator.ultravioletadao.xyz/reputation/hedera-testnet/99
```

Returns feedback count, average score, and individual feedback entries.

### Production Platform

```
https://execution.market
```

The live marketplace running on 9 EVM chains with real USDC payments. This is not a hackathon prototype.

### On-Chain Contracts (Hedera Testnet)

| Contract | Address | Explorer |
|----------|---------|----------|
| ERC-8004 Identity Registry | `0x8004A818BFB912233c491871b3d84c89A494BD9e` | [HashScan](https://hashscan.io/testnet/address/0x8004A818BFB912233c491871b3d84c89A494BD9e) |
| ERC-8004 Reputation Registry | `0x8004B663056A597Dffe9eCcC1965A193B7388713` | [HashScan](https://hashscan.io/testnet/address/0x8004B663056A597Dffe9eCcC1965A193B7388713) |
| Facilitator Wallet | `0x34033041a5944B8F10f8E4D8496Bfb84f1A293A8` | [HashScan](https://hashscan.io/testnet/account/0x34033041a5944B8F10f8E4D8496Bfb84f1A293A8) |

---

## 5. Demo Script for Booth

### Before the Demo

Have these tabs open:

1. **Tab 1**: https://execution.market (the live marketplace)
2. **Tab 2**: https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321 (Merit Tip TX)
3. **Tab 3**: https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages (HCS messages)
4. **Tab 4**: https://api.execution.market/docs (Swagger API)

### Talking Points (2-3 minutes)

**Opening (30 seconds):**

"Execution Market is a live marketplace where AI agents post bounties and humans complete them for payment. We run on 9 chains in production with real USDC. For this hackathon, we added Hedera -- not just as another EVM chain, but using Hedera-native features."

**Show Tab 1 -- Dashboard (30 seconds):**

"This is our production dashboard. Real tasks, real payments. Agent number 2106 on Base."

**Show Tab 2 -- Merit Tip TX (30 seconds):**

"Here is a real HBAR payment on Hedera Testnet. When a worker gets a high reputation score, the agent automatically tips them 0.01 HBAR. This is reputation-gated -- only good workers get tipped."

**Show Tab 3 -- HCS Messages (60 seconds):**

"This is the key differentiator. We use Hedera Consensus Service -- a Hedera-native feature that does NOT exist on EVM. Every task lifecycle event gets logged as an immutable message with a consensus timestamp agreed by Hedera nodes. You can see 6 events here: task created, worker applied, escrow locked, payment released, and both reputation updates. Anyone can verify this -- no API key needed, just hit the Mirror Node REST API."

**Closing (30 seconds):**

"So we are using ERC-8004 for identity, reputation feedback on-chain, HBAR merit tips as payment, and HCS for Hedera-native immutable event logging. Five operations on Hedera Testnet, plus production USDC escrow on Base. And we extended our open-source Facilitator -- a Rust server that supports 21 blockchains -- to add Hedera support."

### Q&A Prep

**"Why HCS instead of just logging to a database?"**
HCS provides immutable, consensus-timestamped messages that no one can alter -- not even us. It is a tamper-proof audit trail. A database can be edited. HCS cannot. Also, it demonstrates that we use Hedera beyond generic EVM -- this is a Hedera-native feature.

**"Is this running on mainnet?"**
Identity and reputation are on Hedera Testnet. Payments are on Base Mainnet (real USDC). Our production marketplace runs on 9 EVM mainnets. Hedera mainnet is the next step -- the code already supports it via a single environment variable toggle.

**"What is ERC-8004?"**
An on-chain identity registry for AI agents. Think of it as a passport -- Agent #99 is our platform's identity on Hedera. Deployed on 16 networks with the same address via CREATE2. Listed by Hedera as an accepted technology ("Trustless Agents").

**"How are payments gasless?"**
Our open-source Facilitator (Rust server) pays HBAR gas for all Hedera operations. Agents and workers never need to hold HBAR. Same model used on 9 other chains in production.

**"What is the merit tip?"**
A direct 0.01 HBAR transfer that the agent sends automatically when a worker's reputation score exceeds the threshold. It is a real financial operation gated by on-chain reputation data.

**"How does HCS work technically?"**
We create an HCS topic using `TopicCreateTransaction`, then submit messages using `TopicMessageSubmitTransaction` -- both from the `hiero-sdk-python` SDK. Messages are JSON payloads with event type and data. Hedera nodes agree on the timestamp and ordering. Anyone reads them via the Mirror Node REST API.

**"Is this open source?"**
Yes. MIT license. The hackathon repo is at github.com/UltravioletaDAO/em-cannes-hackathon. The Facilitator extension is at github.com/UltravioletaDAO/x402-rs.

**If they ask something you do not know:**
"Great question -- our technical lead can follow up on the details. Let me show you what we have live."

---

## 6. Golden Flow Summary

The Golden Flow is our comprehensive E2E acceptance test. It executes the full Execution Market lifecycle across 2 chains.

**Result: 7/7 PASS**

| Phase | Operation | Chain | Result |
|-------|-----------|-------|--------|
| 1 | Connectivity check | Both | PASS |
| 2 | Task creation + escrow lock | Base Mainnet | PASS |
| 3 | Worker apply + evidence submission | Base (API) | PASS |
| 4 | Approval + payment release | Base Mainnet | PASS |
| 5 | Bidirectional reputation | Hedera Testnet | PASS |
| 6 | Merit Tip (0.01 HBAR) | Hedera Testnet | PASS |
| 7 | HCS Event Logging (6 messages) | Hedera Testnet (native) | PASS |

**On-chain evidence: 5 TXs + 6 HCS messages**

| # | Operation | Chain | Evidence |
|---|-----------|-------|----------|
| 1 | Escrow Lock | Base | [BaseScan](https://basescan.org/tx/0x98fc338221502fb937cf9fdfe26248a9a0700580ef4b690b6853c58da3efeb84) |
| 2 | Payment Release | Base | [BaseScan](https://basescan.org/tx/0x29f1aea3cbee79996eab4c632d1982c0578820556fc348bdb5d1a012c502e95a) |
| 3 | Agent-to-Worker Rating | Hedera | [HashScan](https://hashscan.io/testnet/transaction/0x26464dbd022d6829e107ca3a52b04720b59c5aa9d7f6a7394a3b50948acdb1c6) |
| 4 | Worker-to-Agent Rating | Hedera | [HashScan](https://hashscan.io/testnet/transaction/0x300c402eb1051b8995fee783b23b3b74e68863ad3ac7c958ccccfea30cdd658e) |
| 5 | Merit Tip (0.01 HBAR) | Hedera | [HashScan](https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321) |
| 6 | HCS Event Log (6 msgs) | Hedera (native) | [Mirror Node](https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages) |

---

## Quick Reference

| Resource | URL |
|----------|-----|
| Production marketplace | https://execution.market |
| Swagger API docs | https://api.execution.market/docs |
| HCS Messages (Mirror Node) | https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages |
| Merit Tip TX | https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321 |
| Agent Identity API | https://facilitator.ultravioletadao.xyz/identity/hedera-testnet/99 |
| Agent Reputation API | https://facilitator.ultravioletadao.xyz/reputation/hedera-testnet/99 |
| Hackathon repo | https://github.com/UltravioletaDAO/em-cannes-hackathon |
| Facilitator repo | https://github.com/UltravioletaDAO/x402-rs |
| Facilitator commit (Hedera) | https://github.com/UltravioletaDAO/x402-rs/commit/66d34e6c7f805fa26a33757b2cdf5ec3038ecb95 |
| Contact | @ExecutionMarket on X |

---

## Self-Evaluation Score: 41/50

We iteratively improved this submission using automated evaluation against the track criteria:

| Criterion | Score | Notes |
|-----------|:-----:|-------|
| Technicality | **8/10** | ERC-8004 (EVM) + HCS (native SDK) + Facilitator (Rust infra). HCS proves non-EVM depth. |
| Originality | **8/10** | Cross-chain composability: escrow on Base, reputation + HCS + tips on Hedera. |
| Practicality | **9/10** | Live production marketplace at execution.market with real USDC payments. |
| Usability | **8/10** | Bilingual docs (EN+ES), runnable scripts, verifiable TX hashes on explorers. |
| WOW Factor | **8/10** | 7/7 Golden Flow across 2 chains, 5 TXs + 6 HCS messages, open-source Facilitator. |
| **TOTAL** | **41/50** | Competitive for $3K prize. Strongest in Practicality (production system). |

**Improvement trajectory**: 36/50 (baseline) -> 39/50 (+Facilitator, +merit tip) -> 41/50 (+HCS).
