# World Integration — Judges Guide

> **Partner**: World ($20K) | **Tracks**: AgentKit ($8K) + World ID 4.0 ($8K)
> **Production**: [execution.market](https://execution.market) | **API**: [api.execution.market/docs](https://api.execution.market/docs)

---

## What We Built (30-second pitch)

Execution Market is a **live production marketplace** where AI agents publish bounties for real-world tasks and verified humans execute them. We integrated **World AgentKit** and **World ID 4.0** to solve the critical problem: **how do you stop bots from stealing bounties meant for real humans?**

```
Without World ID:        With World ID:
                        
Bot creates account      Bot creates account
Bot applies to task      Bot applies to task
Bot fakes evidence       World ID gate: "Prove you're human"
Bot gets paid $10        Bot can't → BLOCKED
Agent loses money        Only verified humans get paid
```

---

## Track 1: AgentKit — On-Chain Human Verification

### What It Does

We use the **AgentBook contract** (deployed on Base by World) to check if a worker's wallet belongs to a real, verified human. This is a **free, read-only on-chain lookup** — no gas, no transaction, instant.

```
                    ┌─────────────────────┐
                    │   AgentBook (Base)   │
                    │  0xE1D1...a4         │
                    └──────┬──────────────┘
                           │
                  lookupHuman(wallet)
                           │
                    ┌──────▼──────────────┐
                    │  humanId > 0?        │
                    │  YES → Verified ✓    │
                    │  NO  → Not verified  │
                    └─────────────────────┘
```

### How It Integrates with Execution Market

1. Worker applies to a task
2. Backend calls `lookupHuman(worker_wallet)` on Base via JSON-RPC
3. If `humanId > 0`: worker gets a **"Verified Human" badge** on their profile
4. Badge is visible to AI agents reviewing applications — builds trust

### x402 Gateway (Humans Free, Bots Pay)

We built a **Hono server** using `@worldcoin/agentkit` SDK that gates API access:

```
┌─────────────┐     ┌──────────────────┐     ┌───────────────┐
│  API Client  │────>│  x402 Gateway    │────>│  EM API       │
│              │     │  (port 4021)     │     │               │
│  Human? ─────│─YES─│─> Free access    │     │  /tasks       │
│  Bot? ───────│─NO──│─> Pay $0.001/req │     │  /workers     │
└─────────────┘     └──────────────────┘     └───────────────┘
```

### Key Files

| File | Purpose |
|------|---------|
| `world/agentkit/agentbook.py` | On-chain lookup (Python, standalone, zero EM imports) |
| `world/agentkit/gateway-server.ts` | x402+AgentKit gateway (TypeScript, Hono) |
| `world/agentkit/WorldHumanBadge.tsx` | React badge component |
| `world/migrations/003_world_agentkit.sql` | DB schema for humanId storage |

### Live Demo Commands

```bash
# 1. Check an unverified wallet
curl -s "https://api.execution.market/api/v1/workers/world-status?wallet=0x0000000000000000000000000000000000000000" | python -m json.tool
# → { "is_human": false, "human_id": 0 }

# 2. Check on-chain directly (Foundry)
cast call 0xE1D1D3526A6FAa37eb36bD10B933C1b77f4561a4 \
  "lookupHuman(address)(uint256)" \
  0x0000000000000000000000000000000000000000 \
  --rpc-url https://mainnet.base.org
# → 0

# 3. Run the gateway
cd world/agentkit && npm install && npx tsx gateway-server.ts
# → Listening on http://localhost:4021
```

---

## Track 2: World ID 4.0 — ZK Proof of Humanity

### What It Does

World ID 4.0 provides **zero-knowledge proof of humanity**. A worker proves they are a unique human without revealing their identity. The system enforces:

- **One human = one account** (nullifier uniqueness)
- **Tasks >= $5 require Orb verification** (biometric-level proof)
- **No World ID = no access to high-value tasks** (the product literally BREAKS)

### The Flow

```
┌──────────┐    ┌───────────┐    ┌────────────┐    ┌──────────────┐
│  Worker   │    │ Dashboard │    │  Backend   │    │ Cloud API v4 │
│ (Browser) │    │  (React)  │    │ (FastAPI)  │    │  (World)     │
└────┬─────┘    └─────┬─────┘    └─────┬──────┘    └──────┬───────┘
     │                │                │                   │
     │ Click Verify   │                │                   │
     │───────────────>│                │                   │
     │                │ GET /rp-sig    │                   │
     │                │───────────────>│                   │
     │                │                │ Generate nonce    │
     │                │                │ Sign (secp256k1)  │
     │                │<───────────────│                   │
     │                │ {nonce, sig}   │                   │
     │  Open IDKit    │                │                   │
     │<───────────────│                │                   │
     │                │                │                   │
     │ Scan QR with   │                │                   │
     │ World App      │                │                   │
     │                │                │                   │
     │ ZK Proof ready │                │                   │
     │───────────────>│                │                   │
     │                │ POST /verify   │                   │
     │                │ {responses[]}  │                   │
     │                │───────────────>│                   │
     │                │                │ POST /v4/verify   │
     │                │                │──────────────────>│
     │                │                │<──────────────────│
     │                │                │ {success: true}   │
     │                │                │                   │
     │                │                │ Store nullifier   │
     │                │                │ (UNIQUE constraint)│
     │                │                │ Update executor   │
     │                │<───────────────│                   │
     │  Badge appears │                │                   │
     │<───────────────│                │                   │
```

### Anti-Sybil: How the Nullifier Works

```
Person "Juan" verifies Account A:
  nullifier = f(Juan, app_id, action) = 0xabc123...
  → INSERT INTO world_id_verifications (nullifier = 0xabc123...)
  → SUCCESS ✓

Person "Juan" tries to verify Account B:
  nullifier = f(Juan, app_id, action) = 0xabc123...  (SAME!)
  → INSERT INTO world_id_verifications (nullifier = 0xabc123...)
  → UNIQUE CONSTRAINT VIOLATION → HTTP 409 "Already used"
  → BLOCKED ✗
```

The nullifier is **deterministic**: same person + same app = same nullifier. Always. This is enforced at the database level with `UNIQUE (nullifier_hash)`.

### Enforcement: Tasks >= $5 Require Orb

```
Worker applies to $8 task:
  │
  ├── world_id_verified? ──── NO ──→ HTTP 403
  │                                   "world_id_orb_required"
  │                                   "Tasks >= $5 require Orb verification"
  │
  └── YES ──→ world_id_level == "orb"?
                │
                ├── NO (device only) ──→ HTTP 403
                │
                └── YES ──→ Application accepted ✓
```

### Key Files

| File | Purpose |
|------|---------|
| `world/worldid/client.py` | RP signing (secp256k1) + Cloud API v4 verify (standalone) |
| `world/worldid/router.py` | FastAPI endpoints: GET /rp-signature, POST /verify |
| `world/worldid/WorldIdVerification.tsx` | IDKit v4 widget (React, props-based) |
| `world/migrations/001_world_id_verification.sql` | DB: verifications table + anti-sybil constraints |
| `world/migrations/002_world_id_rls.sql` | Row-level security policies |

### Live Demo Commands

```bash
# 1. Get RP signature (proves backend crypto works)
curl -s "https://api.execution.market/api/v1/world-id/rp-signature?action=verify-worker" | python -m json.tool
# → { nonce: "00abc...", signature: "def123...", rp_id: "...", app_id: "app_..." }

# 2. Full verification flow: open https://execution.market/profile
#    → Click "Verify with World ID"
#    → Scan QR with World App
#    → Badge appears on profile

# 3. Anti-sybil test: disconnect wallet, connect different wallet
#    → Try to verify with same World ID
#    → HTTP 409: "This World ID has already been used"

# 4. Enforcement test: create $5+ task, apply without Orb
#    → HTTP 403: "world_id_orb_required"
```

---

## Cryptographic Details (for technical judges)

### RP Signing (v4 spec)

```
message = 0x01                          // version byte
        || nonce[32]                    // random, hashed to BN254 field
        || created_at[8]               // uint64 big-endian (seconds)
        || expires_at[8]               // created_at + 300 (5 min TTL)
        || keccak256(action)[32]        // action hash
        = 81 bytes total

msg_hash = keccak256(EIP-191_prefix || message)

signature = secp256k1_sign_recoverable(msg_hash, signing_key)
          = 65 bytes (r[32] + s[32] + v[1])
```

### Cloud API v4 Payload

```json
{
  "protocol_version": "4.0",
  "nonce": "00abcdef...",
  "action": "verify-worker",
  "responses": [
    {
      "nullifier": "0x...",
      "identifier": "0x...",
      "proof": "0x...",
      "merkle_root": "0x..."
    }
  ]
}
```

### Database Schema

```sql
-- Anti-sybil core
CREATE TABLE world_id_verifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  executor_id UUID REFERENCES executors(id) ON DELETE CASCADE,
  nullifier_hash TEXT NOT NULL,
  merkle_root TEXT,
  proof TEXT,
  verification_level TEXT CHECK (verification_level IN ('orb', 'device')),
  verified_at TIMESTAMPTZ DEFAULT NOW(),

  CONSTRAINT uq_world_id_nullifier UNIQUE (nullifier_hash),  -- one human = one account
  CONSTRAINT uq_world_id_executor UNIQUE (executor_id)        -- one executor = one verification
);

ALTER TABLE world_id_verifications ENABLE ROW LEVEL SECURITY;
```

---

## Where to Look (Quick Reference for Judges)

| What | Where |
|------|-------|
| **Live dashboard** | https://execution.market |
| **API docs (Swagger)** | https://api.execution.market/docs |
| **AgentBook contract** | [0xE1D1...a4 on Basescan](https://basescan.org/address/0xE1D1D3526A6FAa37eb36bD10B933C1b77f4561a4) |
| **ERC-8004 Agent #2106** | [0x8004...32 on Basescan](https://basescan.org/address/0x8004A169FB4a3325136EB29fA0ceB6D2e539a432) |
| **World ID endpoints** | GET `/api/v1/world-id/rp-signature` + POST `/api/v1/world-id/verify` |
| **AgentBook endpoint** | GET `/api/v1/workers/world-status?wallet=0x...` |
| **Source code** | This repo: `world/` folder |
| **Production source** | [github.com/UltravioletaDAO/execution-market](https://github.com/UltravioletaDAO/execution-market) |

---

## FAQ

### General

**Q: Is this actually in production?**
A: Yes. Execution Market is live at [execution.market](https://execution.market) with real USDC payments on 9 EVM chains + Solana. Agent #2106 is registered on Base ERC-8004 Identity Registry. Workers are completing real tasks today.

**Q: What does Execution Market do without World ID?**
A: It works — but it's vulnerable. Any bot can register as a worker, submit AI-generated fake evidence, and steal bounties. World ID closes this attack vector entirely.

**Q: How is this different from just checking wallet age or balance?**
A: Wallet age and balance are trivially fakeable (create 100 wallets, fund from mixer). World ID uses biometric verification (iris scan) to link one physical human to one cryptographic identity. The nullifier mechanism makes multi-accounting mathematically impossible.

### Track 1 (AgentKit)

**Q: Does AgentBook verification block workers?**
A: No, it's non-blocking. Workers can apply without AgentBook verification. The badge is informational — it helps AI agents prioritize verified humans when reviewing applications.

**Q: Why use x402 for the gateway?**
A: x402 is the payment protocol we already use for task settlements. The gateway extends it: verified humans get free API access (they've already proven humanity), bots must pay per request. This aligns incentives — being verified has tangible value.

**Q: What if the AgentBook contract is down?**
A: The RPC call has a 15-second timeout. On failure, the worker's application proceeds normally without the badge. Verification is best-effort, never blocking.

### Track 2 (World ID 4.0)

**Q: What happens if World ID goes down?**
A: The RP signing is local (our backend, using coincurve). The only external dependency is Cloud API v4 for proof verification. If it's down, workers can still use the platform for tasks under $5 (no Orb required). High-value tasks are blocked until Cloud API recovers — this is by design (security > availability for financial operations).

**Q: Can workers bypass the $5 Orb requirement?**
A: No. The enforcement is server-side in `apply_to_task()`. The frontend shows a gate, but even if bypassed via direct API calls, the backend returns HTTP 403. The threshold is configurable via admin API without redeployment.

**Q: What if someone loses access to their World ID?**
A: The nullifier is deterministic. If they re-verify with the same World ID (even from a new device), they get the same nullifier, which maps to their existing account. If they need to move to a new wallet, an admin can manually delete the old verification record.

**Q: How does this link to ERC-8004?**
A: When a worker verifies with World ID, we fire-and-forget an async update to their ERC-8004 agent metadata (via Facilitator). This means their World ID verification status is queryable on-chain by other protocols — it's not locked inside our database.

**Q: Is the $5 threshold arbitrary?**
A: It's configurable. We chose $5 because: (a) tasks under $5 have low sybil incentive (not worth faking), (b) Orb verification requires physical presence at an Orb device, which is a friction point. $5 balances security with accessibility. Agents can request higher thresholds per-task in the future.

### Technical

**Q: Why secp256k1 for RP signing instead of Ed25519?**
A: World ID v4 spec requires secp256k1 with EIP-191 message hashing. This aligns with Ethereum's native signature scheme, making verification interoperable with on-chain contracts.

**Q: Why store the proof in the database?**
A: For audit trail. The nullifier hash is sufficient for anti-sybil, but storing the full proof allows future re-verification if World updates their verification logic, and provides evidence in dispute resolution.

**Q: What's the difference between Orb and Device verification?**
A: Orb = biometric iris scan (highest assurance, requires physical Orb device). Device = phone-based verification (lower assurance, easier to fake). Our enforcement requires Orb for financial operations ($5+) because device-level verification can be bypassed with multiple phones.

---

## Demo Script (for Yesi/David at World Booth)

### Setup (before demo)
- Open https://execution.market in browser (logged in with test wallet)
- Open https://api.execution.market/docs in second tab
- Have World App ready on phone
- Terminal open with `curl` commands ready

### Demo Flow (4 minutes)

**0:00-0:30 — The Problem**
"This is Execution Market — a live marketplace where AI agents post bounties for real-world tasks. The problem: how do you stop bots from stealing bounties meant for real humans?"

**0:30-1:30 — Track 1: AgentKit**
- Show AgentBook lookup in Swagger: GET `/workers/world-status?wallet=0x000...` → `is_human: false`
- "We call the AgentBook contract on Base — free, instant, no gas"
- Show the badge on a verified worker's profile card: "Verified Human #42"

**1:30-3:00 — Track 2: World ID 4.0**
- Click "Verify with World ID" on profile page
- Show IDKit widget opening
- Scan QR with World App (live demo)
- Show the badge appearing after verification
- "This is anti-sybil — same person trying to verify a second account gets HTTP 409"
- Show the `$5+ enforcement`: "Without Orb, you literally cannot apply to high-value tasks"

**3:00-3:30 — Production**
- "This isn't a hackathon prototype. It's running in production with real USDC payments."
- Show the Swagger docs, the health endpoint, the agent card

**3:30-4:00 — Wrap Up**
- "World ID + ERC-8004 = trustless human verification for AI-to-human marketplaces"
- "The product breaks without World ID. That's by design."

### Q&A Prep
- "How many users?" → Production with active workers. Agent #2106 on Base.
- "What chains?" → 9 EVM + Solana. Payments via x402 protocol.
- "Open source?" → Yes, MIT license. github.com/UltravioletaDAO/execution-market
