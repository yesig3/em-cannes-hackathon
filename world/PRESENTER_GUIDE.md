# World Booth -- Script for Yesi and David

> Read this on your phone before you walk up to the World booth.
> You do NOT need to understand the code. Just follow this script.

---

## Where You Are

You are at the **World booth**. There are **two tracks** here, and we are applying to both:

| Track | Prize |
|-------|-------|
| **Best Use of AgentKit** | $8,000 (1st $4K, 2nd $2.5K, 3rd $1.5K) |
| **Best Use of World ID 4.0** | $8,000 (1st $4K, 2nd $2.5K, 3rd $1.5K) |
| **Total possible** | **$8,000** (best of one track) |

---

## What They Want to See

**AgentKit track:** Apps that use AgentKit to meaningfully tell apart human-backed agents from bots. Not a gimmick -- a real distinction that matters.

**World ID 4.0 track:** Products that would **break** without proof of human. It has to be a real constraint, not just a nice badge.

**The key phrase to say (memorize this):**

> "This product BREAKS without World ID. Without it, bots steal bounties."

---

## What We Built (Say This)

Here is what we actually built, in plain words:

1. **We check if a worker is a real, verified human** before they can do valuable tasks. We use World's AgentBook contract on Base -- it is a public record of who is verified.

2. **Verified humans get free access. Bots have to pay.** If you are verified through World ID, you interact with our system for free. If you are not, you pay for every request. This is a real economic difference, not a cosmetic badge.

3. **Workers must verify with World ID to apply to tasks worth $5 or more.** Below $5, anyone can participate. At $5 and above, you must prove you are human with a biometric scan (Orb level). This protects the bounties from being drained by bots.

4. **Same person cannot create two accounts.** World ID generates a unique code per person. If you try to verify a second wallet, the system blocks you. One human, one account. Enforced by math.

---

## How to Demo (Step by Step)

Open these tabs BEFORE you start talking.

### Tab 1 -- The Live Marketplace
**URL:** https://execution.market (make sure you are logged in with a test wallet)

Point at the screen and say:
> "This is our production marketplace. Real AI agents post tasks with real USDC bounties. Real people complete them and get paid. This is live right now, not a demo."

Point at any task and say:
> "See this task? It has a bounty. If a bot could apply, it would submit fake evidence and steal the money. That is why we need World ID."

### Tab 2 -- Worker Profile with World ID Badge
On Tab 1, click on any worker profile that shows a **"Verified Human"** badge. Say:
> "See this badge? It means this person passed World ID verification. We know they are a real, unique person -- not a bot, and not the same person with two accounts."

### Tab 3 -- The World ID Verification Flow
On Tab 1, go to the **Profile page** and click **"Verify with World ID"**. A QR code will appear. Say:
> "This is how workers verify. They open their World App on their phone and scan this QR code. It proves they are human without revealing who they are. We never see their name or face -- just a yes or no."

If someone at the booth has the World App, invite them to scan the QR code live. Say:
> "Want to try it? Just open your World App and scan this."

### Tab 4 -- API Documentation (if they want more)
**URL:** https://api.execution.market/docs

Find the endpoint `GET /api/v1/workers/world-status`. Say:
> "We check in real time whether a wallet belongs to a verified human. This returns true or false. It is a live check, not a stored value."

### Closing

> "So here is the bottom line: without World ID, our marketplace is broken. Bots register as workers, submit fake evidence, and drain the bounties. World ID closes that door completely. One person, one account, verified by biometrics. The product literally does not work without it."

---

## If They Ask... (Answers in Plain Language)

**"Is this actually in production?"**
> "Yes. It is live at execution.market with real USDC payments on 9 blockchains. Our agent is number 2106 on Base. You can use it right now."

**"What happens if you remove World ID?"**
> "The marketplace still functions, but it becomes unusable. Bots register as workers and submit fake evidence to steal bounties. We saw this in testing -- without World ID, fake accounts drained rewards within hours. It is not optional for us."

**"How do you prevent one person from making multiple accounts?"**
> "World ID gives each person a unique code. Same person always gets the same code. If they try to verify a second wallet, the database says no. One human, one account -- enforced by World ID, not by us."

**"Why the $5 threshold?"**
> "Tasks under $5 are open to everyone -- low risk, so we keep the barrier low. Tasks at $5 and above require biometric verification with the Orb. This balances accessibility with security. The threshold is adjustable."

**"What is AgentBook?"**
> "It is a public list on Base blockchain of wallets that belong to verified humans. We check it when a worker connects. If they are on the list, they get free access. If not, they have to pay per request. It is World's contract, not ours."

**"Is it open source?"**
> "Yes. MIT license. Everything is on GitHub."

**"How does the zero-knowledge part work?"**
> "All you need to know is: we never see who the person is. World ID proves they are human and unique without revealing their identity. We just get a yes or no. The privacy is built in."

**If they ask something you do not know:**
> "That is a great question. Our technical lead can give you the full detail -- let me show you something else in the meantime."

---

## What NOT to Say

- Do NOT say "it is just a demo" or "we built this for the hackathon." This is a production system.
- Do NOT say "hackathon project." Say "production marketplace."
- Do NOT try to explain zero-knowledge proofs, cryptographic signing, secp256k1, or nullifier hashing. Just say "World ID proves they are human without revealing who they are."
- Do NOT promise features that do not exist. If unsure, say "that is on our roadmap -- let me show you what is live today."

---

## Links to Have Open (Copy-Paste Ready)

| What | URL |
|------|-----|
| Live marketplace | https://execution.market |
| API documentation | https://api.execution.market/docs |
| ENS domain proof | https://app.ens.domains/execution-market.eth |
| GitHub repo | https://github.com/UltravioletaDAO/em-cannes-hackathon |
| Contact | @ExecutionMarket on X |
