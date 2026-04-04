# Hedera Track -- Presenter Guide

> For Yesi and David at the Hedera booth, ETHGlobal Cannes 2026.
> Read on your phone before walking to the booth.
> **Full technical details**: [Judges Guide](JUDGES_GUIDE.md)

---

## Track: "AI & Agentic Payments on Hedera" ($6,000)

| Detail | Value |
|--------|-------|
| **Prize** | $6,000 (up to 2 teams at $3,000 each) |
| **Requirement** | "Execute at least one payment, token transfer, or financial operation on Hedera Testnet" |
| **Accepted tech** | ERC-8004, x402, Hedera SDKs, HCS |

**Highlight these in the demo:**
- ERC-8004 identity + bidirectional reputation on Hedera (on-chain state writes)
- Merit Tip: 0.01 HBAR transfer, reputation-gated
- HCS: 6 immutable lifecycle events via native `hiero-sdk-python` (NOT EVM)
- Open-source Facilitator extension (Rust, gasless Hedera operations)
- Golden Flow 7/7 PASS across 2 chains (Base + Hedera)

---

## What to Say (30 seconds)

"Execution Market is a live marketplace where AI agents post bounties and humans complete them for instant payment. 9 blockchains in production with real USDC. For this hackathon, we added Hedera with five integrations -- including HCS, a Hedera-native feature that does not exist on EVM. Every task event is logged as an immutable message anyone can verify."

---

## What to Show

**Open these tabs BEFORE the demo:**

1. https://execution.market (live marketplace)
2. https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321 (Merit Tip TX)
3. https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages (HCS messages)
4. https://api.execution.market/docs (Swagger API)

**Steps:**

1. **Tab 1** (dashboard): "Production marketplace. AI agents create tasks, humans complete them, automatic USDC payments."
2. **Tab 2** (Merit Tip TX): "Real HBAR payment on Hedera testnet. Worker gets 0.01 HBAR tip automatically when reputation score is high."
3. **Tab 3** (HCS Mirror Node): "Key differentiator -- Hedera Consensus Service. Every lifecycle event logged as immutable message with consensus timestamp. 6 events: task created, worker applied, escrow locked, payment released, both reputation ratings. Anyone verifies, no API key."
4. **Close**: "ERC-8004 identity, reputation on-chain, HBAR merit tips, HCS native logging. 5 Hedera operations + USDC escrow on Base. Golden Flow 7/7."
5. If asked for more: Tab 4 (Swagger), show health endpoint. "Live -- 9 EVM chains in production."

---

## Key Points

- LIVE production marketplace, not a prototype. Real USDC on 9 chains.
- **HCS** is Hedera-NATIVE, not EVM. `hiero-sdk-python` for immutable event logging. Consensus timestamps from Hedera nodes.
- **Merit Tip**: 0.01 HBAR direct transfer when workers exceed reputation threshold.
- ERC-8004 identity + bidirectional reputation on Hedera testnet. Agent #99.
- Open-source Facilitator (Rust, 21 blockchains) extended for Hedera. Agents never need HBAR.
- Cross-chain composability: verified on Base, paid on Hedera, reputation shared.
- Golden Flow: **7/7 PASS** -- 5 TXs + 6 HCS messages across 2 chains.

---

## Expected Questions

**"Why Hedera?"** -- Fast finality (3-5s), low fees, EVM compatibility for identity, AND HCS for native immutable logging.

**"What is HCS?"** -- Immutable, ordered event log with consensus timestamps. Tamper-proof audit trail. Verifiable via public Mirror Node API. Proves Hedera usage beyond EVM.

**"Mainnet?"** -- Identity/reputation/HCS on Hedera testnet. USDC payments on Base mainnet. Single env var toggles to mainnet.

**"What is ERC-8004?"** -- On-chain identity for AI agents. Agent #99 on Hedera. 16 networks, same address. Listed by Hedera as accepted tech.

**"Gasless?"** -- Facilitator (Rust) pays HBAR gas. Same model on 9 production chains.

**"How many chains?"** -- 9 EVM + Solana in production. Hedera is the newest.

**If unsure:** "Great question -- our technical lead can follow up. Let me show you something else."

---

## What NOT to Say

- NOT "only testnet" --> "identity/reputation/HCS on Hedera testnet; payments on Base mainnet"
- NOT "don't support Hedera" --> "Hedera live with 5 integrations"
- Do NOT explain EIP-3009 or HTS differences. Say "payment system is chain-agnostic"
- Do NOT promise mainnet date. Say "on our roadmap for Q2 2026"

---

## Quick Reference

| Resource | URL |
|----------|-----|
| Production | https://execution.market |
| API docs | https://api.execution.market/docs |
| HCS Messages | https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages |
| Merit Tip TX | https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321 |
| Agent Identity | https://facilitator.ultravioletadao.xyz/identity/hedera-testnet/99 |
| Agent Reputation | https://facilitator.ultravioletadao.xyz/reputation/hedera-testnet/99 |
| GitHub | https://github.com/UltravioletaDAO/em-cannes-hackathon |
| Judges Guide | [JUDGES_GUIDE.md](JUDGES_GUIDE.md) |
| Contact | @ExecutionMarket on X |
