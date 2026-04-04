# Hedera Track -- Presenter Guide

> For Yesi and David at the Hedera booth, ETHGlobal Cannes 2026.
> Read this on your phone before walking to the booth.
> **See also**: [Judges Guide](../docs/HEDERA_JUDGES_GUIDE.md) for the full technical breakdown with all verification links.

---

## What to Say (30 seconds)

"Execution Market is a live marketplace where AI agents post bounties and humans complete them for instant payment. We run on 9 blockchains in production with real USDC. For this hackathon, we added Hedera with five integrations -- including HCS, Hedera Consensus Service, which is a Hedera-native feature that does not exist on EVM. Every task lifecycle event is logged as an immutable message that anyone can verify."

---

## What to Show (step by step)

**Have these browser tabs open BEFORE the demo:**

1. Tab 1: https://execution.market (the live marketplace)
2. Tab 2: https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321 (Merit Tip TX)
3. Tab 3: https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages (HCS messages)
4. Tab 4: https://api.execution.market/docs (Swagger API docs)

**Demo steps:**

1. Show Tab 1 (dashboard). Say: "This is our production marketplace. AI agents create tasks, humans complete them, and payments happen automatically in USDC."
2. Switch to Tab 2 (Merit Tip TX on HashScan). Say: "This is a real HBAR payment on Hedera testnet. When a worker gets a high reputation score, the agent tips them 0.01 HBAR automatically. Reputation-gated payment."
3. Switch to Tab 3 (HCS Mirror Node). Say: "This is our key differentiator -- Hedera Consensus Service. Every lifecycle event is logged as an immutable message with a consensus timestamp from Hedera nodes. You can see 6 events: task created, worker applied, escrow locked, payment released, and both reputation ratings. Anyone can verify -- no API key needed."
4. Say: "So we use ERC-8004 for identity, reputation on-chain, HBAR merit tips, and HCS for native event logging. Five operations on Hedera, plus USDC escrow on Base. Golden Flow: 7 out of 7 phases pass."
5. If asked for more depth, switch to Tab 4 (Swagger) and show the health endpoint. Say: "This is live -- 9 EVM chains in production today."

---

## Key Talking Points

- We are a LIVE production marketplace, not a hackathon prototype. Real USDC payments on 9 chains today.
- **HCS (Hedera Consensus Service)** is our key differentiator -- it is Hedera-NATIVE, not EVM. We use `hiero-sdk-python` to log every task event as an immutable message. Consensus timestamps are agreed by Hedera nodes, not our server.
- **Merit Tip**: 0.01 HBAR direct transfer when workers score above the reputation threshold. Real financial operation, gated by on-chain reputation.
- ERC-8004 identity and bidirectional reputation are on Hedera testnet. Agent #99 is our platform identity.
- We extended our open-source Facilitator (Rust, 21 blockchains) to support Hedera. Agents never need HBAR for gas.
- Workers can be verified on one chain (like Base) and build reputation on another (like Hedera). Cross-chain composability.
- Golden Flow E2E: **7/7 PASS** -- 5 on-chain TXs + 6 HCS messages across 2 chains.

---

## Questions Judges Will Ask (and answers)

**"Why Hedera specifically?"**
Fast finality (3-5 seconds), very low fees (fractions of a cent), EVM compatibility for our identity contracts, AND HCS -- a Hedera-native feature for immutable event logging that does not exist on any other chain.

**"What is HCS and why do you use it?"**
Hedera Consensus Service creates an immutable, ordered event log with timestamps agreed by Hedera nodes. We log every task lifecycle event -- creation, application, escrow, payment, reputation. It is a tamper-proof audit trail that anyone can verify via the public Mirror Node API. It proves we use Hedera beyond generic EVM.

**"Is this running on Hedera mainnet?"**
Identity, reputation, and HCS are on Hedera testnet. USDC payments run on Base mainnet (real money). Our code supports mainnet via a single environment variable toggle.

**"What is ERC-8004?"**
An on-chain identity registry for AI agents. Agent #99 is our platform's identity on Hedera. Deployed on 16 networks with the same address. Listed by Hedera as accepted technology ("Trustless Agents").

**"How are payments gasless?"**
Our open-source Facilitator (Rust server) pays HBAR gas for everything. Agents and workers never need HBAR.

**"How many chains do you support?"**
9 EVM chains in production (Base, Ethereum, Polygon, Arbitrum, Avalanche, Optimism, Celo, Monad, SKALE) plus Solana. Hedera is the newest addition.

**If they ask something you do not know:**
"Great question -- our technical lead can follow up on that detail. Let me show you something else."

---

## What NOT to Say

- Do NOT say "we only have testnet." Say "identity, reputation, and HCS are on Hedera testnet; payments are on Base mainnet."
- Do NOT say "we do not support Hedera yet." Say "Hedera is live with 5 integrations -- identity, reputation, HBAR tips, HCS, and Facilitator extension."
- Do NOT try to explain EIP-3009 or HTS token differences. Just say "our payment system is chain-agnostic."
- Do NOT promise a mainnet launch date. Say "it is on our roadmap for Q2 2026."

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
| Judges Guide | [docs/HEDERA_JUDGES_GUIDE.md](../docs/HEDERA_JUDGES_GUIDE.md) |
| Contact | @ExecutionMarket on X |
