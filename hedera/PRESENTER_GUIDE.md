# Hedera Track -- Presenter Guide

> For Yesi and David at the Hedera booth, ETHGlobal Cannes 2026.
> Read this on your phone before walking to the booth.

---

## What to Say (30 seconds)

"Execution Market is a live marketplace where AI agents post bounties and humans complete them for instant payment. We already run on 9 blockchains. We are adding Hedera because its fast finality and low fees make it ideal for paying workers quickly. We also deployed our agent identity system on Hedera testnet so our agent is discoverable across chains."

---

## What to Show (step by step)

**Have these browser tabs open BEFORE the demo:**

1. Tab 1: https://execution.market (the live marketplace)
2. Tab 2: https://api.execution.market/docs (Swagger API docs)
3. Tab 3: https://hashscan.io/testnet (Hedera block explorer)

**Demo steps:**

1. Show Tab 1 (dashboard). Say: "This is our production marketplace. AI agents create tasks, humans complete them, and payments happen automatically in USDC."
2. Switch to Tab 2 (Swagger). Scroll to the Health endpoint. Say: "This is live -- 9 EVM chains plus Solana today."
3. Switch to Tab 3 (HashScan). Show the ERC-8004 identity contract on Hedera testnet: `0x8004A818BFB912233c491871b3d84c89A494BD9e`. Say: "We deployed our agent identity registry on Hedera testnet. Agent 2106 -- same agent, now discoverable on Hedera."
4. Say: "Hedera finalizes in 3-5 seconds and costs fractions of a cent. That means workers get paid faster and cheaper than on Ethereum."
5. If you have the demo script running, show the terminal output: account creation, HBAR transfer, transaction confirmed on HashScan. Say: "This is a live payment on Hedera testnet."

---

## Key Talking Points

- We are a LIVE production marketplace, not a hackathon prototype. Real USDC payments on 9 chains today.
- Hedera's 3-5 second finality means workers get paid almost instantly. Fees are nearly zero.
- Our agent identity (ERC-8004) is already deployed on Hedera testnet. Same contracts, same agent, more chains.
- We use x402 protocol for gasless payments. The agent signs, our infrastructure pays all gas fees. Workers never need to hold HBAR for gas.
- Hedera is chain number 10 for us. Our architecture is chain-agnostic -- adding a new chain is straightforward.
- Workers can be verified on one chain (like Base) and get paid on another (like Hedera). Reputation travels across chains.

---

## Questions Judges Will Ask (and answers)

**"Why Hedera specifically?"**
Fast finality (3-5 seconds vs 12+ on Ethereum), very low fees (fractions of a cent), and EVM compatibility so our existing contracts deploy directly.

**"Is this running on Hedera mainnet?"**
Identity contracts are on Hedera testnet. Payments demo is on testnet. Our production marketplace runs on 9 EVM mainnets today -- Hedera mainnet is next.

**"How does x402 work on Hedera?"**
Today x402 uses EIP-3009 (a gasless payment standard) which does not exist natively on Hedera yet. So for now we use the Hedera SDK directly for payments. The architecture is designed to add an adapter for Hedera's native token service.

**"What is ERC-8004?"**
It is an on-chain identity registry for AI agents. Think of it like a passport -- Agent 2106 is our platform's identity. It is deployed on 16 networks with the same address, including Hedera testnet now.

**"How many chains do you support?"**
9 EVM chains in production (Base, Ethereum, Polygon, Arbitrum, Avalanche, Optimism, Celo, Monad, SKALE) plus Solana. Hedera is being added now.

**If they ask something you do not know:**
"That is a great question -- our technical lead can follow up on that detail. Let me show you something else."

---

## What NOT to Say

- Do NOT say "we only have testnet." Say "identity is deployed on Hedera testnet, production integration is in progress."
- Do NOT say "we do not support Hedera yet." Say "we already support 9 chains and Hedera is being added now."
- Do NOT try to explain EIP-3009 or HTS token differences. Just say "our payment system is chain-agnostic."
- Do NOT promise a mainnet launch date. Say "it is on our roadmap for Q2 2026."

---

## Quick Reference

- Production: https://execution.market
- API docs: https://api.execution.market/docs
- Hedera Explorer: https://hashscan.io/testnet
- GitHub: https://github.com/UltravioletaDAO/em-cannes-hackathon
- Contact: @ExecutionMarket on X
