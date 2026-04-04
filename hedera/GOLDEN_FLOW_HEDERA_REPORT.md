# Golden Flow Hedera Report -- Cross-Chain E2E Test

> **Date**: 2026-04-04 19:54 UTC
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
| Escrow Lock | Base (8453) | `0x7c0fc1a4b69e8d1e89...` | [BaseScan](https://basescan.org/tx/0x7c0fc1a4b69e8d1e89641bc5e735f7b892f8e4f863fe8d37c435c4f33695c6b2) |
| Payment Release | Base (8453) | `0x2d6ca373c4748a3c37...` | [BaseScan](https://basescan.org/tx/0x2d6ca373c4748a3c37c180f8c6637a0b51f22facddcfb7fd46d1e464d01df08b) |
| Agent->Worker Rating | Hedera Testnet (296) | `0x9e6474208b70c14fb6...` | [HashScan](https://hashscan.io/testnet/transaction/0x9e6474208b70c14fb608de0e1a5ddeb8219d9a0ec2687ba6596e905db45893e5) |
| Worker->Agent Rating | Hedera Testnet (296) | `0x78e2b71b4bc719de45...` | [HashScan](https://hashscan.io/testnet/transaction/0x78e2b71b4bc719de457f44f3e018ce799888454a54523294a43690f318f0d572) |
| Merit Tip (0.01 HBAR) | Hedera Testnet (296) | `0x820ab464bef9e8f1c7...` | [HashScan](https://hashscan.io/testnet/transaction/0x820ab464bef9e8f1c75f9249abf909748c43cb6a5b60846f00fce908a0edb28c) |

---

## Test Configuration

| Parameter | Value |
|-----------|-------|
| Task ID | `c767b255-00bc-4de7-8638-f5d777440248` |
| Bounty | $0.05 USDC |
| Worker Net (87%) | $0.0435 USDC |
| Payment Chain | Base Mainnet (chain 8453) |
| Reputation Chain | Hedera Testnet (chain 296) |
| Hedera Agent ID | #99 |
| Facilitator HBAR | 2096.513655 |
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

---

## Reputation After Test

| Metric | Value |
|--------|-------|
| Agent #99 | hedera-testnet |
| Feedback Count | 25 |
| Average Score | 87 |
| Verify | [API](https://facilitator.ultravioletadao.xyz/reputation/hedera-testnet/99) |

---

## On-Chain Evidence

### Base Mainnet (Payment)

| TX | Explorer |
|----|----------|
| Escrow | [0x7c0fc1a4b69e8d...](https://basescan.org/tx/0x7c0fc1a4b69e8d1e89641bc5e735f7b892f8e4f863fe8d37c435c4f33695c6b2) |
| Payment | [0x2d6ca373c4748a...](https://basescan.org/tx/0x2d6ca373c4748a3c37c180f8c6637a0b51f22facddcfb7fd46d1e464d01df08b) |

### Hedera Testnet (Reputation)

| TX | Explorer |
|----|----------|
| Agent->Worker | [0x9e6474208b70c1...](https://hashscan.io/testnet/transaction/0x9e6474208b70c14fb608de0e1a5ddeb8219d9a0ec2687ba6596e905db45893e5) |
| Worker->Agent | [0x78e2b71b4bc719...](https://hashscan.io/testnet/transaction/0x78e2b71b4bc719de457f44f3e018ce799888454a54523294a43690f318f0d572) |

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
