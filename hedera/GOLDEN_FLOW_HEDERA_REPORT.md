# Golden Flow Hedera Report -- Cross-Chain E2E Test

> **Date**: 2026-04-04 19:05 UTC
> **Payment Chain**: Base Mainnet (chain 8453)
> **Reputation Chain**: Hedera Testnet (chain 296)
> **Facilitator**: https://facilitator.ultravioletadao.xyz
> **Result**: **PASS**

---

## Executive Summary

Full Execution Market lifecycle executed on production:
task created, worker applied, evidence submitted, payment released on **Base** (USDC),
then bidirectional reputation posted on **Hedera Testnet** (ERC-8004).

**Key Result**: Same task, two chains -- payment where the money is (Base),
reputation where the identity lives (Hedera).

---

## Cross-Chain Transaction Summary

| Operation | Chain | TX Hash | Explorer |
|-----------|-------|---------|----------|
| Escrow Lock | Base (8453) | `0xe2e802fd9d68700269...` | [BaseScan](https://basescan.org/tx/0xe2e802fd9d68700269ecd5d6dbf3b393ae791c9f03fa567484bce818ab765e9e) |
| Payment Release | Base (8453) | `0x0a2390e8ee38be7d05...` | [BaseScan](https://basescan.org/tx/0x0a2390e8ee38be7d057d1a01f4b09213ed0fcd692e4d721910d41a8842d8e194) |
| Agent->Worker Rating | Hedera Testnet (296) | `0xe2a6e701e072b9b4e0...` | [HashScan](https://hashscan.io/testnet/transaction/0xe2a6e701e072b9b4e0f22c009de92af3043c9b361a6568b97a1913cfe2bacf55) |
| Worker->Agent Rating | Hedera Testnet (296) | `0xc8876dad47bed24284...` | [HashScan](https://hashscan.io/testnet/transaction/0xc8876dad47bed24284595d96aa3bfa4b196554674b836276f8ed448f07ab37e1) |

---

## Test Configuration

| Parameter | Value |
|-----------|-------|
| Task ID | `d6c6a1b5-fb21-4427-9c8f-e767cc6c82d2` |
| Bounty | $0.05 USDC |
| Worker Net (87%) | $0.0435 USDC |
| Payment Chain | Base Mainnet (chain 8453) |
| Reputation Chain | Hedera Testnet (chain 296) |
| Hedera Agent ID | #99 |
| Facilitator HBAR | 2097.265209 |
| Identity Registry | `0x8004A818BFB912233c491871b3d84c89A494BD9e` |
| Reputation Registry | `0x8004B663056A597Dffe9eCcC1965A193B7388713` |

---

## Flow Diagram

```mermaid
sequenceDiagram
    participant A as Agent
    participant EM as Execution Market
    participant B as Base (USDC)
    participant F as Facilitator
    participant H as Hedera Testnet

    Note over A,H: Phases 2-4: Task Lifecycle (Base)
    A->>EM: Create task ($0.05 bounty)
    EM->>B: Escrow lock
    A->>EM: Approve submission
    EM->>B: Payment release

    Note over A,H: Phase 5: Cross-Chain Reputation (Hedera)
    A->>F: Agent rates Worker (score=90)
    F->>H: giveFeedback on-chain
    A->>F: Worker rates Agent (score=85)
    F->>H: giveFeedback on-chain
```

---

## Phase Results

| # | Phase | Status |
|---|-------|--------|
| 1 | Connectivity | **PASS** |
| 2 | Task Creation (Base) | **PASS** |
| 3 | Worker Flow | **PASS** |
| 4 | Approval + Payment (Base) | **PASS** |
| 5 | Reputation (Hedera) | **PASS** |

---

## Reputation After Test

| Metric | Value |
|--------|-------|
| Agent #99 | hedera-testnet |
| Feedback Count | 19 |
| Average Score | 88 |
| Verify | [API](https://facilitator.ultravioletadao.xyz/reputation/hedera-testnet/99) |

---

## On-Chain Evidence

### Base Mainnet (Payment)

| TX | Explorer |
|----|----------|
| Escrow | [0xe2e802fd9d6870...](https://basescan.org/tx/0xe2e802fd9d68700269ecd5d6dbf3b393ae791c9f03fa567484bce818ab765e9e) |
| Payment | [0x0a2390e8ee38be...](https://basescan.org/tx/0x0a2390e8ee38be7d057d1a01f4b09213ed0fcd692e4d721910d41a8842d8e194) |

### Hedera Testnet (Reputation)

| TX | Explorer |
|----|----------|
| Agent->Worker | [0xe2a6e701e072b9...](https://hashscan.io/testnet/transaction/0xe2a6e701e072b9b4e0f22c009de92af3043c9b361a6568b97a1913cfe2bacf55) |
| Worker->Agent | [0xc8876dad47bed2...](https://hashscan.io/testnet/transaction/0xc8876dad47bed24284595d96aa3bfa4b196554674b836276f8ed448f07ab37e1) |

---

## Reproducibility

```bash
# Anyone can verify the Hedera reputation:
curl https://facilitator.ultravioletadao.xyz/reputation/hedera-testnet/99

# Run the full flow (requires wallet keys):
cd hedera
pip install -r requirements.txt
EM_HIRING_AGENT_PRIVATE_KEY=0x... EM_WORKER_PRIVATE_KEY=0x... python golden_flow_hedera.py
```
