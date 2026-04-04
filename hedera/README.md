# Hedera Integration — AI & Agentic Payments

> **Partner**: Hedera ($15K) | **Track**: AI & Agentic Payments
> **Production**: [execution.market](https://execution.market) | **Agent**: #2106 on Base ERC-8004

---

## What We Built

Execution Market runs **AI-to-human payments on 9 EVM chains** via x402. We extended to **Hedera** with five integrations:

1. **ERC-8004 Identity on Hedera** — Agent #99 registered on testnet (gasless via Facilitator)
2. **Bidirectional Reputation** — On-chain agent-to-worker and worker-to-agent feedback
3. **Merit Tip: 0.01 HBAR** — Reputation-gated direct HBAR transfer to high-performing workers
4. **HCS Event Logging** — Hedera-native Consensus Service (NOT EVM) for immutable task lifecycle audit trail
5. **Open-Source Facilitator Extension** — [x402-rs](https://github.com/UltravioletaDAO/x402-rs) extended for Hedera ([commit `66d34e6`](https://github.com/UltravioletaDAO/x402-rs/commit/66d34e6c7f805fa26a33757b2cdf5ec3038ecb95))

---

## Architecture

### Current Payment Flow (9 EVM Chains)

```
┌─────────────┐     ┌───────────────┐     ┌──────────────┐
│  AI Agent    │     │ x402 Escrow   │     │   Worker     │
└──────┬──────┘     └───────┬───────┘     └──────┬───────┘
       │ 1. Sign EIP-3009  │                     │
       │───────────────────>│                     │
       │ 2. Lock escrow     │                     │
       │                    │  3. Release (87%)   │
       │                    │────────────────────>│
       │                    │  4. Fee (13%)       │
       │ GASLESS — Facilitator pays all gas       │
```

### Hedera Extension

```
┌─────────────┐     ┌───────────────┐     ┌──────────────┐
│  AI Agent    │     │ Hedera SDK    │     │   Worker     │
└──────┬──────┘     └───────┬───────┘     └──────┬───────┘
       │ 1. Create transfer │                     │
       │───────────────────>│                     │
       │  (HBAR or USDC)    │                     │
       │ 2. Execute TX      │  3. Worker receives │
       │   (Hedera testnet) │────────────────────>│
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
│                                                  │
│  Testnet contracts:                              │
│  Identity: 0x8004A818BFB912233c491871b3d84c89A4  │
│  Reputation: 0x8004B663056A597Dffe9eCcC1965A193B │
└──────────────────────────────────────────────────┘
```

---

## Why Not Direct x402 on Hedera?

USDC on Hedera is **native HTS (Hedera Token Service)**, not ERC-20:

| Feature | EVM Chains (ERC-20) | Hedera (HTS) |
|---------|---------------------|--------------|
| `transferWithAuthorization()` (EIP-3009) | YES | NO |
| `permit()` (EIP-2612) | YES | NO |
| Gasless pre-auth | YES (x402 uses this) | NO |

x402 relies on EIP-3009 for gasless escrow. HTS doesn't support it. For Hedera, we use **native Hedera SDK** for payments (HBAR transfers) and ERC-8004 for identity/reputation (standard EVM calls work).

---

## Demo

```bash
cd hedera
pip install -r requirements.txt
python demo.py
# Output:
#   1. Created testnet account: 0.0.12345
#   2. Funded from faucet: 100 HBAR
#   3. Transferred 1 HBAR to worker: TX 0x...
#   4. Verified on HashScan
#   5. ERC-8004 identity check: Agent #2106 found
```

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

## Related

- [Proof of Integration](PROOF_OF_INTEGRATION.md) — TX hashes, Golden Flow 7/7, architecture
- [Judges Guide](JUDGES_GUIDE.md) — Verification links, demo script for booth
- [Presenter Guide](PRESENTER_GUIDE.md) — Talking points for Hedera booth
- [Production API](https://api.execution.market/docs) — Swagger UI
- [Source](https://github.com/UltravioletaDAO/execution-market) — Open source
