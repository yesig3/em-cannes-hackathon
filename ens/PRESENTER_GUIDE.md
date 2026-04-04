# ENS Booth -- Script for Yesi and David

> Read this on your phone before you walk up to the ENS booth.
> You do NOT need to understand the code. Just follow this script.

---

## Where You Are

You are at the **ENS booth**. There are **two tracks** here, and we are applying to both:

| Track | Prize |
|-------|-------|
| **Best ENS Integration for AI Agents** | $5,000 |
| **Most Creative Use of ENS** | $5,000 |
| **Total possible** | **$10,000** |

---

## What They Want to See

**Best ENS Integration for AI Agents:** They want ENS used in a real, meaningful way for AI agents -- not just a pretty name. They want to see agent naming, address resolution, metadata stored in text records. It has to serve a purpose.

**Most Creative Use of ENS:** Something non-obvious. Something that makes them say "I had not thought of using ENS that way."

---

## What We Built (Say This)

Here is what we built, in plain words:

1. **Our AI agent has an ENS name: execution-market.eth.** Instead of being identified by a long random wallet address, anyone can look up "execution-market.eth" and find us. It is registered on Ethereum mainnet -- not a test, not a mock.

2. **We store the agent's identity information inside the ENS name.** There are 7 text records on-chain: our URL, description, Twitter handle, agent ID number, supported blockchains, agent role, and whether we are World ID verified. Any other app or protocol can read all of this just by looking up our ENS name. They do not need our API. They do not need our permission.

3. **Workers get subnames under our platform.** A worker named Alice can claim "alice.execution-market.eth" as her permanent on-chain identity. We pay the gas -- workers do not need to own any crypto to claim their name.

4. **This is a discovery mechanism, not a cosmetic badge.** If our server goes down tomorrow, the on-chain identity persists. Other protocols can still find us, read our metadata, and see our agent ID -- all from the ENS name alone.

**The big picture -- three layers working together:**
- **ENS** is how you FIND us (name and metadata)
- **ERC-8004** is how you TRUST us (identity and reputation)
- **World ID** is how you know the workers are HUMAN (biometric verification)

---

## How to Demo (Step by Step)

Open these 3 tabs BEFORE you start talking.

### Tab 1 -- Our ENS Domain Page
**URL:** https://app.ens.domains/execution-market.eth

Point at the screen and say:
> "This is execution-market.eth -- our domain, registered on Ethereum mainnet. Real registration, real money, not a testnet."

Scroll down to show the **text records**. Point at them and say:
> "See these records? Seven pieces of information stored on-chain. Our URL, our Twitter, our agent ID, which blockchains we support. Any app in the world can read these just by looking up our ENS name. They do not need to call our API. They do not need our permission. If our server disappears, this information is still here."

### Tab 2 -- The Live Marketplace
**URL:** https://execution.market

Point at the dashboard and say:
> "This is our production marketplace. AI agents post tasks, humans complete them, they get paid in USDC. Live on 9 blockchains."

If you can find a worker profile or agent card that shows an **ENS badge**, click on it and say:
> "See this? When a worker connects their wallet, we automatically check if they have an ENS name. If they do, it shows up here. Real resolution, not hardcoded."

Then go to the **Profile page** and point at the **"Claim Subname"** section. Say:
> "Workers can claim a subname under our platform -- like alice.execution-market.eth. We pay the gas. They get a permanent on-chain identity. It costs them nothing."

### Tab 3 -- Live ENS Resolution in the API
**URL:** https://api.execution.market/docs

Find the ENS section. Run the endpoint:
`GET /api/v1/ens/resolve/execution-market.eth`

Show the result and say:
> "This is live resolution. The API just looked up our ENS name in real time and returned the address and records. Not hardcoded."

Then run:
`GET /api/v1/ens/resolve/vitalik.eth`

Show the result and say:
> "It works with any ENS name. Here is Vitalik's. This proves it is real resolution, not a fake response."

### Closing

> "So ENS is not just a name for us. It is how other protocols discover our agent. It is how workers get permanent identities. And it works even if our backend is completely offline. Three layers: ENS to find us, ERC-8004 to trust us, World ID to verify the humans."

---

## If They Ask... (Answers in Plain Language)

**"Is execution-market.eth actually registered?"**
> "Yes. Registered on Ethereum mainnet. You can verify it right now -- it is on the screen. We paid for the registration and set up all 7 text records."

**"Is this just a cosmetic badge?"**
> "No, and this is important. The text records contain our agent ID, our supported chains, our role. Any protocol can look up our name and find all of this without talking to our server. If our backend goes down, the identity persists on-chain. It is a real discovery mechanism."

**"How do subnames work?"**
> "A worker goes to their profile, clicks a button, picks a name, and we create it on-chain. We pay the gas -- about 15 cents per subname. The worker gets a permanent on-chain identity under our platform. Like alice.execution-market.eth."

**"Who pays for everything?"**
> "We do. The domain registration, the text record updates, the subname gas. Workers never need to own ETH or any crypto. Zero cost for them."

**"What is ERC-8004?"**
> "It is our identity system for AI agents -- like a passport. Our agent is number 2106. ENS stores that agent ID in a text record, which links to ERC-8004 where the full identity and reputation live. Think of ENS as the front door and ERC-8004 as the room inside."

**"How is this creative?"**
> "Most people use ENS for wallet names. We use it as a cross-protocol discovery layer for AI agents. Any protocol can find our agent, read its metadata, and verify its identity -- all from one ENS name. Plus workers get subnames as permanent identities. That is not how ENS is typically used."

**If they ask something you do not know:**
> "That is a great question. Our technical lead can give you the full detail -- let me show you something else in the meantime."

---

## What NOT to Say

- Do NOT say "we just registered a domain." Say "we built a full identity and discovery layer on ENS."
- Do NOT say "it is just a name." Say "it is how other protocols find and trust our agent."
- Do NOT try to explain namehash, EIP-137, NameWrapper, or any ENS internals. Just say "we use the standard ENS protocol."
- Do NOT say "we plan to add subnames." Subnames are live. Workers can claim them now.
- Do NOT say "it is a hackathon project." Say "it is a production marketplace."

---

## Links to Have Open (Copy-Paste Ready)

| What | URL |
|------|-----|
| Our ENS domain page | https://app.ens.domains/execution-market.eth |
| Live marketplace | https://execution.market |
| API documentation | https://api.execution.market/docs |
| GitHub repo | https://github.com/UltravioletaDAO/em-cannes-hackathon |
| Contact | @ExecutionMarket on X |
