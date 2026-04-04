# Hedera Booth -- Script for Yesi and David

> Read this on your phone before you walk up to the Hedera booth.
> You do NOT need to understand the code. Just follow this script.

---

## Where You Are

You are at the **Hedera booth**. The track is called **"AI & Agentic Payments on Hedera"** and the prize is **$6,000** (split between up to 2 teams, so $3,000 each).

---

## What They Want to See

The judges want to see that you **actually did something on Hedera** -- not just talked about it. Specifically, they want at least one payment, token transfer, or financial operation on Hedera's test network.

We did **five** things on Hedera, not just one:

1. We registered an AI agent identity on Hedera (like a digital passport)
2. We gave that agent a reputation score on Hedera
3. We made a real HBAR payment (a small tip to a good worker)
4. We logged every step of a task on Hedera's unique message log (called HCS)
5. We extended our open-source server (the Facilitator) to support Hedera

---

## What to Say (Your Opening -- 30 Seconds)

Say this naturally, in your own words:

> "We built Execution Market -- it is a live marketplace where AI agents post tasks with cash rewards, and real people complete them for instant payment. It already runs on 9 blockchains with real money. For this hackathon, we added Hedera. We registered our agent's identity on Hedera, we tip good workers in HBAR, and -- this is the big one -- we log every single step of a task on Hedera's Consensus Service. HCS is something only Hedera has. No other blockchain can do this. Every event is permanent and anyone can verify it."

---

## How to Demo (Step by Step)

Open these 3 browser tabs BEFORE you start talking. Have them ready.

### Tab 1 -- The Live Marketplace
**URL:** https://execution.market

Point at the screen and say:
> "This is our production marketplace. Real AI agents create tasks, real people complete them, and they get paid automatically in USDC. This is not a prototype -- it is live right now."

### Tab 2 -- The HBAR Tip Transaction
**URL:** https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321

Point at the transaction details and say:
> "This is a real payment on Hedera. When a worker does a good job -- their reputation score is above 55% -- the system automatically sends them a tip of 0.01 HBAR. This is that transaction. You can see it right here on HashScan, Hedera's block explorer."

### Tab 3 -- The HCS Message Log
**URL:** https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages

Point at the list of messages and say:
> "This is our secret weapon. Hedera has something called the Consensus Service -- it is like a permanent, tamper-proof log book. Every time something happens in a task -- created, worker applied, payment locked, payment released, both parties rated each other -- we write it here. That is 6 messages for one task. Anyone in the world can see this. No password needed, no API key needed. Just open this URL."

### Closing
> "So we have five Hedera integrations: agent identity, reputation, HBAR tips, HCS event logging, and our open-source Facilitator server that makes all of this gasless. Plus our main escrow payments run on Base. Our end-to-end test passed 7 out of 7 steps across both chains."

---

## If They Ask... (Answers in Plain Language)

**"Why not pay the full bounty on Hedera?"**
> "Great question. USDC works differently on each chain. Right now the deepest liquidity for USDC is on Base, so that is where we do the main payments. We use Hedera for what it does best -- identity, reputation, tips, and that amazing message log. As USDC grows on Hedera, we can move full payments there too."

**"What is HCS?"**
> "Think of it as an immutable log book that only Hedera has. Every time something happens in a task, we write a message there. It gets a timestamp from the Hedera network itself, so you know it is real. Anyone can check it. It is like a receipt that can never be changed."

**"Is this only on testnet?"**
> "The identity, reputation, tips, and HCS messages are on Hedera testnet. Our actual marketplace and USDC payments are on Base mainnet with real money. Moving to Hedera mainnet is just a configuration change on our side."

**"What is ERC-8004?"**
> "It is an identity standard for AI agents. Think of it like a passport. Our agent is number 99 on Hedera. It works across 16 networks with the same address. Hedera lists it as accepted technology for this track."

**"How is this gasless?"**
> "We have a server called the Facilitator that pays the network fees on behalf of agents and workers. So nobody needs to hold HBAR to use our platform on Hedera. We do the same thing across 9 chains in production."

**"How many blockchains do you support?"**
> "Nine in production with real money, plus Solana. Hedera is the newest addition."

**If they ask something you do not know:**
> "That is a great question. Our technical lead can give you the full detail on that -- let me show you something else in the meantime."

---

## What NOT to Say

- Do NOT say "it is only on testnet." Say: "Identity, reputation, and HCS are on Hedera testnet. Payments are on Base mainnet with real money."
- Do NOT say "we do not really support Hedera." We have 5 live integrations.
- Do NOT try to explain technical details like EIP-3009, HTS token differences, or how gasless works under the hood. If they ask, say "our payment system is chain-agnostic" and move on.
- Do NOT promise a mainnet date. Say "it is on our roadmap."

---

## Links to Have Open (Copy-Paste Ready)

| What | URL |
|------|-----|
| Live marketplace | https://execution.market |
| HBAR tip transaction | https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321 |
| HCS messages (6 events) | https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages |
| API documentation | https://api.execution.market/docs |
| Agent identity on Hedera | https://facilitator.ultravioletadao.xyz/identity/hedera-testnet/99 |
| Agent reputation on Hedera | https://facilitator.ultravioletadao.xyz/reputation/hedera-testnet/99 |
| GitHub repo | https://github.com/UltravioletaDAO/em-cannes-hackathon |
| Judges guide (technical) | [JUDGES_GUIDE.md](JUDGES_GUIDE.md) |
| Contact | @ExecutionMarket on X |
