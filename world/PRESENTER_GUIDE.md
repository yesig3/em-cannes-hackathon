# World Track -- Presenter Guide

> For Yesi and David at the World / Worldcoin booth, ETHGlobal Cannes 2026.
> Read this on your phone before walking to the booth.

---

## Tracks We Are Applying To (World — $20,000 total)

| Track | Prize | Requirement | Our Features |
|-------|------:|-------------|--------------|
| **Best Use of AgentKit** | $8K (1st $4K, 2nd $2.5K, 3rd $1.5K) | "Apps that use AgentKit to meaningfully distinguish human-backed agents from bots" | AgentBook on-chain human verification, x402 gateway (humans free, bots pay) |
| **Best Use of World ID 4.0** | $8K (1st $4K, 2nd $2.5K, 3rd $1.5K) | "Products that break without proof of human. Real constraint, not cosmetic." | RP signing (secp256k1), Cloud API v4, anti-sybil (nullifier UNIQUE), $5+ Orb enforcement |

**Key message**: This product BREAKS without World ID. Without it, bots steal bounties. Not cosmetic -- structural.

---

## What to Say (30 seconds)

"Execution Market is a live marketplace where AI agents post bounties for real-world tasks and real humans complete them for payment. We integrated World ID so that only verified humans -- not bots -- can claim bounties. If you are not verified, you literally cannot access tasks worth $5 or more. It is live in production right now at execution.market."

---

## What to Show (step by step)

**Have these browser tabs open BEFORE the demo:**

1. Tab 1: https://execution.market (logged in with test wallet)
2. Tab 2: https://api.execution.market/docs (Swagger API docs)
3. Tab 3: https://app.ens.domains/execution-market.eth (shows we are real)
4. Phone: World App ready to scan a QR code

**Demo steps:**

1. Show Tab 1 (dashboard). Point to a task with a bounty amount. Say: "These are real tasks posted by AI agents, with real USDC payments."
2. Click on a worker profile. Show the "Verified Human" badge. Say: "This badge means they passed World ID verification -- we know they are a real, unique person."
3. Switch to Tab 2 (Swagger). Find the endpoint `GET /api/v1/workers/world-status`. Show it returns `is_human: true` or `false`. Say: "We check on-chain in real time."
4. Go back to Tab 1. Open the Profile page. Click "Verify with World ID." Show the QR code that appears. Say: "Workers scan this with their World App. Zero-knowledge proof -- we never see their identity, just a yes/no."
5. Say: "If the same person tries to verify a second account, they get blocked. One human, one account. Enforced by math, not by us."

---

## Key Talking Points

- We are LIVE in production with real payments, not a hackathon prototype.
- World ID stops bots from stealing bounties meant for humans.
- One person = one account. If you try to cheat, the system blocks you automatically.
- Tasks worth $5 or more REQUIRE biometric (Orb) verification. Lower-value tasks are open to everyone.
- We also use World's AgentBook contract to check if a wallet belongs to a verified human -- free, instant, on-chain.
- Without World ID, our marketplace breaks. Bots would drain every bounty.

---

## Questions Judges Will Ask (and answers)

**"Is this actually in production?"**
Yes. Live at execution.market with real USDC payments on 9 blockchains. Agent number 2106 on Base.

**"What happens without World ID?"**
The marketplace still works, but bots can register as workers and steal bounties by submitting fake evidence. World ID closes that hole completely.

**"How do you prevent one person from making multiple accounts?"**
World ID generates a unique code (called a nullifier) per person. Same person, same code -- always. If they try to verify a second wallet, the database rejects it.

**"What is the $5 threshold?"**
Tasks under $5 are open to anyone. Tasks at $5 and above require Orb-level verification (biometric iris scan). This balances security with accessibility. The threshold is adjustable.

**"Is it open source?"**
Yes. MIT license. github.com/UltravioletaDAO/execution-market

**If they ask something you do not know:**
"That is a great question -- our technical lead can follow up on that detail. Let me show you something else."

---

## What NOT to Say

- Do NOT say "it is just a demo" or "we built this yesterday." It is a production system.
- Do NOT say "hackathon project." Say "production marketplace."
- Do NOT try to explain zero-knowledge proofs or cryptography. Just say "World ID proves they are human without revealing who they are."
- Do NOT promise features that do not exist yet. If unsure, redirect: "That is on our roadmap -- let me show you what we have live today."

---

## Quick Reference

- Production: https://execution.market
- API docs: https://api.execution.market/docs
- GitHub: https://github.com/UltravioletaDAO/em-cannes-hackathon
- ENS domain: execution-market.eth
- Contact: @ExecutionMarket on X
