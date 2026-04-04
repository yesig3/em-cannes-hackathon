# Hedera Track -- Judges Guide

> For judges at the Hedera booth, ETHGlobal Cannes 2026.

---

## TL;DR

Execution Market is a **live production marketplace** (not a prototype) where AI agents post bounties and humans complete them. We built **five Hedera integrations** including **HCS (Hedera Consensus Service)** -- Hedera-NATIVE, NOT accessible via EVM. Golden Flow: **7/7 PASS**, 5 on-chain TXs + 6 HCS messages across 2 chains.

---

## 1. Track: "AI & Agentic Payments on Hedera" ($6,000)

| Detail | Value |
|--------|-------|
| **Prize** | $6,000 (up to 2 teams at $3,000) |
| **Requirement** | "Execute at least one payment/transfer on Hedera Testnet" |
| **Accepted tech** | ERC-8004, x402, Hedera SDKs, HCS, Hedera Agent Kit, OpenClaw ACP, A2A |

**Four categories of on-chain operations executed:**

1. **ERC-8004 Agent Registration** -- NFT mint registering Agent #99
2. **Bidirectional Reputation** -- on-chain state writes (agent + worker rate each other)
3. **Merit Tip: 0.01 HBAR** -- direct HBAR transfer, gated by reputation score
4. **HCS Event Logging** -- 6 immutable consensus messages via native TopicMessageSubmitTransaction

| Technology | How used |
|-----------|----------|
| **ERC-8004** | On-chain identity + bidirectional reputation |
| **x402** | Production payments on 9 EVM chains |
| **hiero-sdk-python** | HCS topic creation + message submission (native, not EVM) |
| **HCS** | 6 immutable lifecycle messages per task |
| **Facilitator** (open-source, Rust) | Gasless Hedera operations ([commit `66d34e6`](https://github.com/UltravioletaDAO/x402-rs/commit/66d34e6c7f805fa26a33757b2cdf5ec3038ecb95)) |

---

## 2. What HCS Is (Key Differentiator)

HCS is **Hedera-native** -- NOT part of EVM, NOT accessible via JSON-RPC.

- Creates immutable, ordered event logs with **consensus timestamps** (agreed by Hedera nodes, not client-supplied)
- Uses `TopicCreateTransaction` + `TopicMessageSubmitTransaction` from `hiero-sdk-python`
- Messages cannot be altered or deleted once submitted
- Anyone can verify via public Mirror Node REST API -- no auth needed
- Our implementation: `hedera/hcs_logger.py`

---

## 3. What We Built (5 Integrations)

**3.1 ERC-8004 Identity** -- Agent #99 on Hedera Testnet. Contract: `0x8004A818BFB912233c491871b3d84c89A494BD9e`. Verify: `GET https://facilitator.ultravioletadao.xyz/identity/hedera-testnet/99`

**3.2 Bidirectional Reputation** -- Contract: `0x8004B663056A597Dffe9eCcC1965A193B7388713`. 29 entries, avg 87/100. Verify: `GET https://facilitator.ultravioletadao.xyz/reputation/hedera-testnet/99`

**3.3 Merit Tip: 0.01 HBAR** -- Reputation-gated HBAR transfer. TX: [`0x419d824c...`](https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321)

**3.4 HCS Event Log** -- 6 lifecycle events per task via native SDK. Topic: `0.0.8511429`. [Mirror Node](https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages)

| Seq | Event | Records |
|-----|-------|---------|
| 1 | `task_created` | Task ID, bounty, deadline |
| 2 | `worker_applied` | Executor ID |
| 3 | `escrow_locked` | Base TX hash (cross-chain) |
| 4 | `payment_released` | Base TX hash, amount |
| 5 | `reputation_agent_to_worker` | Score, Hedera TX |
| 6 | `reputation_worker_to_agent` | Score, Hedera TX |

**3.5 Facilitator Extension** -- Extended [x402-rs](https://github.com/UltravioletaDAO/x402-rs) (Rust, 21 blockchains) for Hedera. Pays HBAR gas so agents never need HBAR. [Commit `66d34e6`](https://github.com/UltravioletaDAO/x402-rs/commit/66d34e6c7f805fa26a33757b2cdf5ec3038ecb95)

---

## 4. How to Verify

All publicly verifiable. No account or API key needed.

**HCS Messages:**
```
https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages
```

Decode:
```bash
curl -s "https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages" \
  | python3 -c "import sys,json,base64; msgs=json.load(sys.stdin)['messages']; [print(base64.b64decode(m['message']).decode()) for m in msgs]"
```

**Merit Tip TX:** https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321

**Agent Identity:** `GET https://facilitator.ultravioletadao.xyz/identity/hedera-testnet/99`

**Agent Reputation:** `GET https://facilitator.ultravioletadao.xyz/reputation/hedera-testnet/99`

**Production:** https://execution.market (live, 9 EVM chains, real USDC)

| Contract | Address | Explorer |
|----------|---------|----------|
| ERC-8004 Identity | `0x8004A818BFB912233c491871b3d84c89A494BD9e` | [HashScan](https://hashscan.io/testnet/address/0x8004A818BFB912233c491871b3d84c89A494BD9e) |
| ERC-8004 Reputation | `0x8004B663056A597Dffe9eCcC1965A193B7388713` | [HashScan](https://hashscan.io/testnet/address/0x8004B663056A597Dffe9eCcC1965A193B7388713) |
| Facilitator Wallet | `0x34033041a5944B8F10f8E4D8496Bfb84f1A293A8` | [HashScan](https://hashscan.io/testnet/account/0x34033041a5944B8F10f8E4D8496Bfb84f1A293A8) |

---

## 5. Demo Script for Booth

**Tabs to open before demo:**

1. https://execution.market (live marketplace)
2. https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321 (Merit Tip TX)
3. https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages (HCS messages)
4. https://api.execution.market/docs (Swagger API)

**Flow (2-3 minutes):**

1. **Tab 1** -- "Production marketplace. Real tasks, real USDC payments. Agent #2106 on Base."
2. **Tab 2** -- "Real HBAR payment on Hedera Testnet. Worker gets 0.01 HBAR tip when reputation score is high. Reputation-gated."
3. **Tab 3** -- "Key differentiator: HCS. Hedera-native, not EVM. 6 immutable lifecycle events with consensus timestamps. Anyone verifies via Mirror Node, no API key."
4. **Close** -- "ERC-8004 identity, reputation on-chain, HBAR tips, HCS native logging. 5 Hedera operations + USDC escrow on Base. Golden Flow 7/7."

### Q&A

**"Why HCS?"** -- Immutable, consensus-timestamped, tamper-proof. Proves Hedera usage beyond generic EVM.

**"Mainnet?"** -- Identity/reputation/HCS on Hedera testnet. Payments on Base mainnet (real USDC). Single env var toggles to mainnet.

**"What is ERC-8004?"** -- On-chain identity registry for AI agents. Agent #99 on Hedera. 16 networks, same address via CREATE2. Listed by Hedera as accepted tech.

**"Gasless how?"** -- Open-source Facilitator (Rust) pays HBAR gas. Same model on 9 other production chains.

**"Open source?"** -- MIT. [em-cannes-hackathon](https://github.com/UltravioletaDAO/em-cannes-hackathon) + [x402-rs](https://github.com/UltravioletaDAO/x402-rs)

---

## 6. Golden Flow (7/7 PASS)

| Phase | Operation | Chain | Evidence |
|-------|-----------|-------|----------|
| 1 | Connectivity | Both | PASS |
| 2 | Task + escrow lock | Base | [BaseScan](https://basescan.org/tx/0x98fc338221502fb937cf9fdfe26248a9a0700580ef4b690b6853c58da3efeb84) |
| 3 | Worker + evidence | Base (API) | PASS |
| 4 | Approval + payment | Base | [BaseScan](https://basescan.org/tx/0x29f1aea3cbee79996eab4c632d1982c0578820556fc348bdb5d1a012c502e95a) |
| 5 | Bidirectional reputation | Hedera | [HashScan (A->W)](https://hashscan.io/testnet/transaction/0x26464dbd022d6829e107ca3a52b04720b59c5aa9d7f6a7394a3b50948acdb1c6) / [HashScan (W->A)](https://hashscan.io/testnet/transaction/0x300c402eb1051b8995fee783b23b3b74e68863ad3ac7c958ccccfea30cdd658e) |
| 6 | Merit Tip (0.01 HBAR) | Hedera | [HashScan](https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321) |
| 7 | HCS (6 messages) | Hedera (native) | [Mirror Node](https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages) |

---

## Quick Reference

| Resource | URL |
|----------|-----|
| Production | https://execution.market |
| Swagger API | https://api.execution.market/docs |
| HCS Messages | https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages |
| Merit Tip TX | https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321 |
| Agent Identity | https://facilitator.ultravioletadao.xyz/identity/hedera-testnet/99 |
| Agent Reputation | https://facilitator.ultravioletadao.xyz/reputation/hedera-testnet/99 |
| Hackathon repo | https://github.com/UltravioletaDAO/em-cannes-hackathon |
| Facilitator repo | https://github.com/UltravioletaDAO/x402-rs |
| Facilitator commit | https://github.com/UltravioletaDAO/x402-rs/commit/66d34e6c7f805fa26a33757b2cdf5ec3038ecb95 |
| Contact | @ExecutionMarket on X |

---

## Self-Evaluation: 41/50

> This evaluation was conducted using the [Hedera Skills evaluation framework](https://github.com/hedera-dev/hedera-skills) provided by the Hedera developer team. The skill audits submissions against the official track criteria.

| Criterion | Score | Notes |
|-----------|:-----:|-------|
| Technicality | **8/10** | ERC-8004 (EVM) + HCS (native SDK) + Facilitator (Rust). HCS proves non-EVM depth. |
| Originality | **8/10** | Cross-chain: escrow on Base, reputation + HCS + tips on Hedera. |
| Practicality | **9/10** | Live production marketplace with real USDC. |
| Usability | **8/10** | Bilingual docs, runnable scripts, verifiable TXs. |
| WOW Factor | **8/10** | 7/7 Golden Flow, 5 TXs + 6 HCS messages, open-source Facilitator. |
| **TOTAL** | **41/50** | |

Trajectory: 36 (baseline) -> 39 (+Facilitator, +merit tip) -> 41 (+HCS).
