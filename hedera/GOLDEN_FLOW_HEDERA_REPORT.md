# Golden Flow Hedera Report -- Cross-Chain E2E Test

> **Date**: 2026-04-04 20:36 UTC
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
| Escrow Lock | Base (8453) | `0x8308ddd152a50a6e08...` | [BaseScan](https://basescan.org/tx/0x8308ddd152a50a6e08b8a199c67952800a9fffa16761d2811e08fcbd38404e6e) |
| Payment Release | Base (8453) | `0xaffdb027d41389679c...` | [BaseScan](https://basescan.org/tx/0xaffdb027d41389679ccb1201179349c00e682fc6f26e0b153e5b6aa246121872) |
| Agent->Worker Rating | Hedera Testnet (296) | `0xc5ca1696439f658aa6...` | [HashScan](https://hashscan.io/testnet/transaction/0xc5ca1696439f658aa6ec5d16d31e611eda0406b37ae69a40e91ab3a69aa8e2f0) |
| Worker->Agent Rating | Hedera Testnet (296) | `0x3744d028d1fcad0ac7...` | [HashScan](https://hashscan.io/testnet/transaction/0x3744d028d1fcad0ac75eeec622e742b0429b5c1be9f866474a34bd01624b230b) |
| Merit Tip (0.01 HBAR) | Hedera Testnet (296) | `0x1c4ce9dc6fa8e4dab7...` | [HashScan](https://hashscan.io/testnet/transaction/0x1c4ce9dc6fa8e4dab790eb41ea94035aba30aa76c7a67e674dab88832d4f7e83) |

---

## Test Configuration

| Parameter | Value |
|-----------|-------|
| Task ID | `1e076d51-979a-4977-b194-644e6da6e090` |
| Bounty | $0.05 USDC |
| Worker Net (87%) | $0.0435 USDC |
| Payment Chain | Base Mainnet (chain 8453) |
| Reputation Chain | Hedera Testnet (chain 296) |
| Hedera Agent ID | #99 |
| Facilitator HBAR | 2096.263137 |
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
| 6 | Merit Tip (Hedera HBAR) | **PASS** |
| 7 | HCS Event Log (Hedera Native) | **PASS** |

---

## Reputation After Test

| Metric | Value |
|--------|-------|
| Agent #99 | hedera-testnet |
| Feedback Count | 27 |
| Average Score | 87 |
| Verify | [API](https://facilitator.ultravioletadao.xyz/reputation/hedera-testnet/99) |

---

## On-Chain Evidence

### Base Mainnet (Payment)

| TX | Explorer |
|----|----------|
| Escrow | [0x8308ddd152a50a...](https://basescan.org/tx/0x8308ddd152a50a6e08b8a199c67952800a9fffa16761d2811e08fcbd38404e6e) |
| Payment | [0xaffdb027d41389...](https://basescan.org/tx/0xaffdb027d41389679ccb1201179349c00e682fc6f26e0b153e5b6aa246121872) |

### Hedera Testnet (Reputation)

| TX | Explorer |
|----|----------|
| Agent->Worker | [0xc5ca1696439f65...](https://hashscan.io/testnet/transaction/0xc5ca1696439f658aa6ec5d16d31e611eda0406b37ae69a40e91ab3a69aa8e2f0) |
| Worker->Agent | [0x3744d028d1fcad...](https://hashscan.io/testnet/transaction/0x3744d028d1fcad0ac75eeec622e742b0429b5c1be9f866474a34bd01624b230b) |

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
