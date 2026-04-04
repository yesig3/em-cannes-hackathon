# ENS Track -- Presenter Guide

> For Yesi and David at the ENS booth, ETHGlobal Cannes 2026.
> Read this on your phone before walking to the booth.

---

## Tracks We Are Applying To (ENS — $10,000 total)

| Track | Prize | Requirement | Our Features |
|-------|------:|-------------|--------------|
| **Best ENS Integration for AI Agents** | $5K | "Use ENS to name agents, resolve addresses, store metadata in text records. Not just cosmetic." | Agent naming (execution-market.eth), text records (agentId, role, worldIdVerified), worker subnames |
| **Most Creative Use of ENS** | $5K | Creative, non-obvious ENS usage | Agent naming (execution-market.eth), text records (agentId, role, worldIdVerified), worker subnames |

**Key message**: ENS is how other protocols FIND us. Not cosmetic -- it is a cross-protocol discovery mechanism. If our server goes down, the on-chain identity persists.

---

## What to Say (30 seconds)

"Execution Market is a live marketplace where AI agents post bounties and humans complete them. We integrated ENS so our AI agent is discoverable by name -- execution-market.eth -- not just a random wallet address. Workers can claim subnames like alice.execution-market.eth. All identity data lives on-chain, so any protocol can find us without using our API."

---

## What to Show (step by step)

**Have these browser tabs open BEFORE the demo:**

1. Tab 1: https://execution.market (the live marketplace)
2. Tab 2: https://api.execution.market/docs (Swagger API docs)
3. Tab 3: https://app.ens.domains/execution-market.eth (our ENS domain page)

**Demo steps:**

1. Show Tab 3 (ENS App). Say: "This is execution-market.eth -- our domain, registered on Ethereum mainnet. Not a testnet, not a mock."
2. Scroll down on the ENS App page to show the text records. Say: "Seven text records on-chain: our URL, description, Twitter, agent ID. Any protocol can read these without touching our API."
3. Switch to Tab 1 (dashboard). Show an agent card or worker card with an ENS badge. Say: "If a worker has an ENS name, it appears automatically. We detect it when they connect their wallet."
4. Switch to Tab 2 (Swagger). Find the ENS section. Run the endpoint `GET /api/v1/ens/resolve/execution-market.eth`. Show the result. Say: "Live resolution. Not hardcoded."
5. Then run `GET /api/v1/ens/resolve/vitalik.eth`. Say: "Works with any ENS name -- this proves it is real resolution, not a fake response."
6. Show the Profile page on Tab 1. Point to the "Claim Subname" section. Say: "Workers can claim alice.execution-market.eth. We pay the gas. They get a permanent on-chain identity under our platform."

---

## Key Talking Points

- execution-market.eth is a real ENS domain on Ethereum mainnet. Registered, paid for, with 7 text records on-chain.
- ENS makes our AI agent FINDABLE. Before ENS, Agent 2106 was just a number. Now anyone can look up execution-market.eth and find everything about us.
- Workers get subnames (like alice.execution-market.eth). The platform pays the gas so workers do not need ETH.
- This is NOT cosmetic. Other protocols can resolve our name, read our metadata, find our agent ID, and check our reputation -- all without using our API. If our server goes down, the identity persists on-chain.
- Three layers work together: ENS is how you FIND us. ERC-8004 is how you TRUST us. World ID is how you know the workers are HUMAN.
- Everything is live in production. No mocks, no hardcoded values.

---

## Questions Judges Will Ask (and answers)

**"Is execution-market.eth actually registered?"**
Yes. Registered on Ethereum mainnet. You can verify right now at app.ens.domains/execution-market.eth.

**"Is this just a cosmetic badge?"**
No. The text records contain our agent ID, supported chains, and role. Any protocol can resolve the name, read the records, and discover our identity without our API. If our backend goes down, the on-chain identity persists.

**"How do subnames work?"**
Workers click a button on their profile, pick a name, and we create it on-chain using NameWrapper. We pay the gas -- about $0.15 per subname. Each worker gets one.

**"Who pays for the ENS domain and subnames?"**
The platform pays for everything. The domain registration, the text record updates, the subname gas. Workers never need ETH.

**"What is ERC-8004?"**
Our on-chain identity system for AI agents. ENS stores the agent ID (2106) in a text record, which links to ERC-8004 where the full identity and reputation live. ENS is the front door, ERC-8004 is the identity inside.

**If they ask something you do not know:**
"That is a great question -- our technical lead can follow up on that detail. Let me show you something else."

---

## What NOT to Say

- Do NOT say "we just registered a domain." Say "we built a full identity and discovery layer on ENS."
- Do NOT say "it is just a name." Say "it is a cross-protocol discovery mechanism."
- Do NOT try to explain namehash, EIP-137, or NameWrapper internals. Just say "we use the standard ENS protocol."
- Do NOT say "we plan to add subnames." Say "subnames are live -- workers can claim them now."

---

## Quick Reference

- Production: https://execution.market
- API docs: https://api.execution.market/docs
- ENS domain: https://app.ens.domains/execution-market.eth
- GitHub: https://github.com/UltravioletaDAO/em-cannes-hackathon
- Contact: @ExecutionMarket on X
