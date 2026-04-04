# Hedera Integration — AI & Agentic Payments

> **Partner**: Hedera ($15K) | **Track**: AI & Agentic Payments
> **Production**: [execution.market](https://execution.market) | **Agent**: #2106 on Base ERC-8004

---

## What We're Building (30-second pitch)

Execution Market already runs **AI-to-human payments on 9 EVM chains** via x402 protocol. We're extending to **Hedera** by:

1. **ERC-8004 Identity on Hedera** — Agent #2106 identity registered on Hedera (EVM-compatible, gasless via Facilitator)
2. **Agentic Payments on Hedera Testnet** — Execute real token transfers using Hedera SDK
3. **Cross-Chain Architecture** — Show how x402 escrow extends to Hedera's HTS token standard

```
TODAY (9 EVM chains + Solana):

  AI Agent ──→ x402 Escrow ──→ Worker gets paid (USDC, gasless)
       │
       └── ERC-8004 Identity on 16 networks

ADDING HEDERA:

  AI Agent ──→ Hedera SDK ──→ Worker gets paid (HBAR/USDC)
       │
       └── ERC-8004 Identity on Hedera (testnet live)
```

---

## Why Hedera + Execution Market

Hedera's prize explicitly asks for:

| Requirement | How We Meet It |
|-------------|----------------|
| "Execute at least one payment on Hedera Testnet" | Hedera SDK payment demo (HBAR transfer) |
| "Use Hedera Agent Kit, x402, or Hedera SDKs" | Hedera SDK directly + x402 architecture explanation |
| "Bonus: x402 implementation" | x402 runs on 9 chains today; architecture doc shows Hedera extension |
| "Bonus: ERC-8004 agent identity" | Agent #2106 on 16 networks; Hedera testnet contracts deployed |

### What Makes This Unique

Execution Market is the **only live marketplace** where AI agents pay humans for real-world tasks. Adding Hedera means:

- **Agents can pay workers in HBAR** (fast finality, low fees)
- **Agent identity portable to Hedera** (ERC-8004 registry already deployed)
- **Cross-chain reputation** — worker verified on Base, paid on Hedera, reputation shared

---

## Architecture

### Current Payment Flow (9 EVM Chains)

```
┌─────────────┐     ┌───────────────┐     ┌──────────────┐
│  AI Agent    │     │ x402 Escrow   │     │   Worker     │
│  (publisher) │     │ (on-chain)    │     │  (executor)  │
└──────┬──────┘     └───────┬───────┘     └──────┬───────┘
       │                    │                     │
       │ 1. Sign EIP-3009  │                     │
       │───────────────────>│                     │
       │    (pre-auth)      │                     │
       │                    │                     │
       │ 2. Lock escrow     │                     │
       │   (on assignment)  │                     │
       │                    │                     │
       │                    │  3. Release to      │
       │                    │     worker (87%)    │
       │                    │────────────────────>│
       │                    │                     │
       │                    │  4. Fee to treasury  │
       │                    │     (13%)           │
       │                    │                     │
       │ GASLESS — Facilitator pays all gas       │
```

### Hedera Extension (New)

```
┌─────────────┐     ┌───────────────┐     ┌──────────────┐
│  AI Agent    │     │ Hedera SDK    │     │   Worker     │
│  (publisher) │     │ (HTS native)  │     │  (executor)  │
└──────┬──────┘     └───────┬───────┘     └──────┬───────┘
       │                    │                     │
       │ 1. Create transfer │                     │
       │───────────────────>│                     │
       │  (HBAR or USDC)    │                     │
       │                    │                     │
       │ 2. Execute TX      │                     │
       │   (Hedera testnet) │                     │
       │                    │  3. Worker receives  │
       │                    │────────────────────>│
       │                    │                     │
       │ TX on HashScan.io  │                     │
```

### ERC-8004 Identity on Hedera

```
┌──────────────────────────────────────────────────┐
│         ERC-8004 Identity Registry               │
│         (deployed on 16+ networks)               │
│                                                  │
│  Base ────── Agent #2106 (production)            │
│  Ethereum ── Agent #2106                         │
│  Polygon ─── Agent #2106                         │
│  Hedera ──── Agent #2106 (NEW, testnet)          │
│  ...                                             │
│                                                  │
│  Testnet contracts:                              │
│  Identity: 0x8004A818BFB912233c491871b3d84c89A4  │
│  Reputation: 0x8004B663056A597Dffe9eCcC1965A193B │
└──────────────────────────────────────────────────┘
```

---

## Technical Details

### Why Not Direct x402 on Hedera?

USDC on Hedera is a **native HTS (Hedera Token Service) token**, not an ERC-20. Key difference:

| Feature | EVM Chains (ERC-20) | Hedera (HTS) |
|---------|---------------------|--------------|
| `transferWithAuthorization()` (EIP-3009) | YES | NO |
| `permit()` (EIP-2612) | YES | NO |
| `DOMAIN_SEPARATOR` | YES | NO |
| Gasless pre-auth | YES (x402 uses this) | NO |

**x402 relies on EIP-3009** for gasless pre-authorized transfers. HTS doesn't support this. So for Hedera, we use the **native Hedera SDK** for payments and show the architecture for how a future x402-HTS adapter would work.

### Hedera Testnet Configuration

```python
HEDERA_TESTNET = {
    "chain_id": 296,
    "network_type": "evm",
    "rpc_url": "https://testnet.hashio.io/api",
    "explorer": "https://hashscan.io/testnet",
    "tokens": {
        "HBAR": {
            "address": "native",
            "decimals": 8,
        },
        "USDC": {
            "address": "0x0000000000000000000000000000000000068cda",
            "decimals": 6,
            "standard": "HTS",  # Not ERC-20
        },
    },
    "erc8004": {
        "identity": "0x8004A818BFB912233c491871b3d84c89A494BD9e",
        "reputation": "0x8004B663056A597Dffe9eCcC1965A193B7388713",
    },
}
```

### Files to Build

```
hedera/
├── README.md              # Hedera-specific guide for judges
├── payment.py             # Hedera SDK: create account, transfer HBAR/USDC
├── identity.py            # ERC-8004 identity lookup on Hedera
├── demo.py                # End-to-end: account → fund → transfer → verify
├── requirements.txt       # hedera-sdk, python-dotenv, web3
└── tests/
    └── test_payment.py    # Mock Hedera RPC, test transfer flow
```

### Demo Flow (what judges run)

```bash
cd hedera
pip install -r requirements.txt

# End-to-end demo
python demo.py
# Output:
#   1. Created testnet account: 0.0.12345
#   2. Funded from faucet: 100 HBAR
#   3. Transferred 1 HBAR to worker: TX 0x...
#   4. Verified on HashScan: https://hashscan.io/testnet/transaction/0x...
#   5. ERC-8004 identity check: Agent #2106 found on Hedera testnet
```

---

## What The Team In Cannes Should Present

### Talking Points for Hedera Booth

1. **"We're a live marketplace — 9 chains today, extending to Hedera"**
   - Show execution.market in production
   - Point to Swagger docs at api.execution.market/docs
   - "Real USDC payments, real tasks, real workers"

2. **"ERC-8004 agent identity is already on Hedera testnet"**
   - Contracts deployed: `0x8004A818...` (identity), `0x8004B663...` (reputation)
   - Agent #2106 identity portable across chains
   - "Same agent, registered on Base, Ethereum, Polygon... and now Hedera"

3. **"Hedera's fast finality is perfect for task payments"**
   - 3-5 second finality vs 12+ seconds on Ethereum
   - Low fees ($0.0001 per transfer)
   - "Workers get paid faster on Hedera"

4. **"x402 architecture extends to Hedera with an HTS adapter"**
   - Show the architecture diagram
   - "Today: EIP-3009 on EVM. Tomorrow: HTS-native pre-auth on Hedera"
   - "The Facilitator already supports 19 blockchains — Hedera is being added now"

5. **"World ID + ERC-8004 + Hedera = verified humans paid instantly"**
   - Cross-pollinate with World track
   - "Worker verified by World ID on Base, paid in HBAR on Hedera, reputation shared on-chain"

### Expected Questions

**Q: Why not use x402 directly on Hedera?**
A: HTS tokens don't support EIP-3009 (gasless pre-auth). We use native Hedera SDK for now and are designing an HTS-native adapter for x402. The architecture is chain-agnostic — the marketplace doesn't care which chain settles.

**Q: Is ERC-8004 actually deployed on Hedera?**
A: Yes, on testnet. The registry uses CREATE2 for deterministic addresses across chains. Identity: `0x8004A818...`, Reputation: `0x8004B663...`. We're adding it to the Facilitator now.

**Q: What's the Facilitator?**
A: Our gasless transaction relay. Agents sign authorizations, the Facilitator executes on-chain. It already supports 19 blockchains — adding Hedera is an extension, not a rebuild. URL: `facilitator.ultravioletadao.xyz`

**Q: How does cross-chain identity work?**
A: ERC-8004 is deployed on 16+ networks with the same contract address (CREATE2). Agent #2106 is the same entity on Base, Ethereum, Polygon, and now Hedera. Reputation scores are chain-specific but queryable cross-chain via the Facilitator.

**Q: What's the timeline for production Hedera support?**
A: ERC-8004 identity: days (Facilitator update). Payments: depends on HTS adapter design. We're targeting Q2 2026 for production Hedera payments.

---

## Implementation Status

| Component | Status | ETA |
|-----------|--------|-----|
| ERC-8004 contracts on Hedera testnet | DEPLOYED | Done |
| Facilitator Hedera support | IN PROGRESS | Hours |
| Hedera SDK payment demo | TODO | 2-3 hours |
| ERC-8004 identity lookup | TODO | 1 hour |
| End-to-end demo script | TODO | 1 hour |
| Tests | TODO | 1 hour |
| Documentation | THIS FILE | Done |

---

## On-Chain References

| Contract | Network | Address |
|----------|---------|---------|
| ERC-8004 Identity Registry | Hedera Testnet | `0x8004A818BFB912233c491871b3d84c89A494BD9e` |
| ERC-8004 Reputation Registry | Hedera Testnet | `0x8004B663056A597Dffe9eCcC1965A193B7388713` |
| ERC-8004 Identity Registry | All Mainnets | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` |
| Execution Market Agent | Base Mainnet | Agent #2106 |
| Hedera Testnet RPC | JSON-RPC Relay | `https://testnet.hashio.io/api` |
| Hedera Explorer | HashScan | `https://hashscan.io/testnet` |

---

## Related Documentation

- [World Integration Guide](./WORLD_JUDGES_GUIDE.md) — World ID + AgentKit details
- [ENS Integration Plan](./ENS_INTEGRATION.md) — ENS naming for AI agents
- [Production API Docs](https://api.execution.market/docs) — Full Swagger UI
- [Execution Market Source](https://github.com/UltravioletaDAO/execution-market) — Open source
