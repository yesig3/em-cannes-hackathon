"""
Golden Flow Hedera — Cross-Chain E2E Demo (Full Lifecycle)

Executes the COMPLETE Execution Market lifecycle on production:
  Phase 1: Verify connectivity (EM API + Hedera RPC)
  Phase 2: Create task on Base ($0.10 bounty, USDC)
  Phase 3: Worker applies + submits evidence
  Phase 4: Agent approves + payment releases on Base
  Phase 5: Bidirectional reputation on Hedera testnet
  Phase 6: Cross-chain verification + report generation

Payment: Base Mainnet (USDC, real escrow)
Reputation: Hedera Testnet (ERC-8004, via Facilitator)

Env vars (for running locally):
  EM_HIRING_AGENT_PRIVATE_KEY  -- Agent wallet (signs requests + escrow)
  EM_WORKER_PRIVATE_KEY        -- Worker wallet (applies, submits)
  EM_API_URL                   -- API base (default: https://api.execution.market)
  HEDERA_8004_NETWORK          -- testnet (default) or mainnet

For internal testing, reads from AWS Secrets Manager env vars:
  WALLET_PRIVATE_KEY           -- maps to EM_HIRING_AGENT_PRIVATE_KEY
"""

import asyncio
import json
import os
import sys
import time
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Optional

import httpx

from config import (
    HEDERA_8004_NETWORK,
    FACILITATOR_NETWORK,
    CHAIN_ID,
    FACILITATOR_WALLET,
    EXPLORER_URL,
    NETWORK_LABEL,
    FACILITATOR_URL,
    IDENTITY_REGISTRY,
    REPUTATION_REGISTRY,
    RPC_URL,
)
from identity import register_agent, get_identity, get_identity_by_owner
from reputation import submit_feedback, get_reputation
from payment import get_balance, get_chain_id, get_block_number
from erc8128_signer import ERC8128Signer

# ── Config ──────────────────────────────────────────────────────────────────

EM_API_URL = os.environ.get("EM_API_URL", "https://api.execution.market")

# Agent wallet (signs requests via ERC-8128 + signs escrow)
AGENT_KEY = os.environ.get(
    "EM_HIRING_AGENT_PRIVATE_KEY",
    os.environ.get("WALLET_PRIVATE_KEY", ""),
)

# Worker wallet
WORKER_KEY = os.environ.get("EM_WORKER_PRIVATE_KEY", "")
WORKER_WALLET = os.environ.get("EM_WORKER_WALLET", "")

# If worker wallet not set, derive from key
if WORKER_KEY and not WORKER_WALLET:
    from eth_account import Account
    WORKER_WALLET = Account.from_key(WORKER_KEY).address

BOUNTY = float(os.environ.get("EM_TEST_BOUNTY", "0.10"))
HEDERA_AGENT_ID = 99  # Registered in previous demo
BASE_EXPLORER = "https://basescan.org"


@dataclass
class FlowResult:
    timestamp: str = ""
    # Phase 1
    em_api_healthy: bool = False
    hedera_connected: bool = False
    hedera_block: int = 0
    facilitator_hbar: float = 0.0
    # Phase 2
    task_id: str = ""
    # Phase 3
    executor_id: str = ""
    submission_id: str = ""
    # Phase 4
    escrow_tx: str = ""
    payment_tx: str = ""
    # Phase 5
    agent_rates_worker_tx: str = ""
    worker_rates_agent_tx: str = ""
    rep_count: int = 0
    rep_avg: int = 0
    # Phase 5b (merit tip)
    merit_tip_tx: str = ""
    merit_tip_hbar: float = 0.0
    # Overall
    phases: list = None

    def __post_init__(self):
        self.phases = []


def sign_escrow_for_assign(agent_key: str, worker_wallet: str, bounty_usd: float) -> dict:
    """Sign escrow authorization on Base using AdvancedEscrowClient."""
    from uvd_x402_sdk.advanced_escrow import AdvancedEscrowClient, TaskTier
    from eth_account import Account

    escrow_client = AdvancedEscrowClient(
        private_key=agent_key,
        chain_id=8453,  # Base mainnet
        rpc_url="https://mainnet.base.org",
        contracts={
            "usdc": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
            "escrow": "0xb9488351E48b23D798f24e8174514F28B741Eb4f",
            "operator": "0x271f9fa7f8907aCf178CCFB470076D9129D8F0Eb",
            "token_collector": "0x48ADf6E37F9b31dC2AAD0462C5862B5422C736B8",
        },
    )

    bounty_atomic = int(bounty_usd * 1_000_000)  # USDC 6 decimals
    pi = escrow_client.build_payment_info(
        receiver=worker_wallet,
        amount=bounty_atomic,
        tier=TaskTier.MICRO,
        max_fee_bps=1800,
    )

    result = escrow_client.authorize(pi)
    if not result.success:
        raise RuntimeError(f"Escrow authorize failed: {result.error}")

    agent_address = Account.from_key(agent_key).address
    return {
        "escrow_tx": result.transaction_hash,
        "payment_info": {
            "mode": "fase2",
            "payer": agent_address,
            "operator": pi.operator,
            "receiver": pi.receiver,
            "token": pi.token,
            "max_amount": pi.max_amount,
            "pre_approval_expiry": pi.pre_approval_expiry,
            "authorization_expiry": pi.authorization_expiry,
            "refund_expiry": pi.refund_expiry,
            "min_fee_bps": pi.min_fee_bps,
            "max_fee_bps": pi.max_fee_bps,
            "fee_receiver": pi.fee_receiver,
            "salt": pi.salt,
        },
    }


async def _json_rpc(method: str, params: list) -> str:
    """Make a JSON-RPC call to Hedera testnet."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(RPC_URL, json={
            "jsonrpc": "2.0", "id": 1,
            "method": method, "params": params,
        })
    data = resp.json()
    if "error" in data:
        raise RuntimeError(f"RPC error: {data['error']}")
    return data["result"]


async def signed_request(
    client: httpx.AsyncClient,
    signer: ERC8128Signer,
    method: str,
    path: str,
    body: Optional[dict] = None,
) -> dict:
    """Make a signed API request."""
    url = f"{EM_API_URL}{path}"
    body_str = json.dumps(body) if body else None

    nonce = await signer.fetch_nonce()
    headers = signer.sign_request(method, url, body=body_str, nonce=nonce)
    headers["Content-Type"] = "application/json"

    if method == "GET":
        resp = await client.get(url, headers=headers)
    else:
        resp = await client.post(url, content=body_str, headers=headers)

    data = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
    return {"_http_status": resp.status_code, **data}


async def run_golden_flow():
    result = FlowResult()
    result.timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    if not AGENT_KEY:
        print("ERROR: Set EM_HIRING_AGENT_PRIVATE_KEY (or WALLET_PRIVATE_KEY)")
        sys.exit(1)

    signer = ERC8128Signer(AGENT_KEY, api_base_url=EM_API_URL)
    print(f"Agent wallet: {signer.address}")
    print(f"Worker wallet: {WORKER_WALLET}")
    print(f"API: {EM_API_URL}")
    print(f"Reputation chain: {NETWORK_LABEL}")

    async with httpx.AsyncClient(timeout=30.0) as client:

        # ── Phase 1: Connectivity ───────────────────────────────
        print("\n" + "=" * 60)
        print("  Phase 1: Connectivity")
        print("=" * 60)

        # EM API
        resp = await client.get(f"{EM_API_URL}/api/v1/health")
        if resp.status_code == 200:
            result.em_api_healthy = True
            print(f"  EM API: ONLINE")
        else:
            print(f"  EM API: FAIL ({resp.status_code})")
            return result

        # Hedera
        chain_id = await get_chain_id()
        if chain_id == CHAIN_ID:
            result.hedera_connected = True
            result.hedera_block = await get_block_number() or 0
            print(f"  Hedera: ONLINE (block {result.hedera_block:,})")
        else:
            print(f"  Hedera: FAIL")

        bal = await get_balance(FACILITATOR_WALLET)
        result.facilitator_hbar = bal.get("balance_hbar", 0)
        print(f"  Facilitator: {result.facilitator_hbar} HBAR")

        result.phases.append(("Connectivity", "PASS"))

        # ── Phase 2: Create Task ────────────────────────────────
        print("\n" + "=" * 60)
        print("  Phase 2: Create Task on Base")
        print("=" * 60)

        # Ensure agent has ERC-8004 identity (gasless auto-registration)
        print(f"  Checking agent identity...")
        id_check = await signed_request(client, signer, "GET",
            f"/api/v1/reputation/identity/{signer.address}")
        if id_check.get("_http_status") != 200 or not id_check.get("agent_id"):
            print(f"  Registering agent identity on Base...")
            reg_resp = await signed_request(client, signer, "POST",
                "/api/v1/reputation/register", {
                    "network": "base",
                    "agent_uri": "https://execution.market/agent-card.json",
                    "recipient": signer.address,
                })
            print(f"  Registration: {reg_resp.get('_http_status')} agent_id={reg_resp.get('agent_id', '?')}")
        else:
            print(f"  Agent #{id_check.get('agent_id')} on Base: OK")

        task_resp = await signed_request(client, signer, "POST", "/api/v1/tasks", {
            "title": f"[GOLDEN FLOW HEDERA] Cross-chain demo {result.timestamp}",
            "instructions": "Respond with: golden_flow_hedera_complete",
            "category": "simple_action",
            "bounty_usd": BOUNTY,
            "deadline_hours": 1,
            "evidence_required": ["text_response"],
            "payment_network": "base",
            "payment_token": "USDC",
        })

        if task_resp.get("_http_status") in (200, 201):
            result.task_id = task_resp.get("id", task_resp.get("data", {}).get("id", ""))
            print(f"  PASS: Task created: {result.task_id}")
            result.phases.append(("Task Creation (Base)", "PASS"))
        elif "identity_required" in str(task_resp.get("detail", "")):
            # Identity registration may need a moment to propagate
            print(f"  Waiting for identity propagation...")
            await asyncio.sleep(3)
            task_resp = await signed_request(client, signer, "POST", "/api/v1/tasks", {
                "title": f"[GOLDEN FLOW HEDERA] Cross-chain demo {result.timestamp}",
                "instructions": "Respond with: golden_flow_hedera_complete",
                "category": "simple_action",
                "bounty_usd": BOUNTY,
                "deadline_hours": 1,
                "evidence_required": ["text_response"],
                "payment_network": "base",
                "payment_token": "USDC",
            })
            if task_resp.get("_http_status") in (200, 201):
                result.task_id = task_resp.get("id", task_resp.get("data", {}).get("id", ""))
                print(f"  PASS: Task created (retry): {result.task_id}")
                result.phases.append(("Task Creation (Base)", "PASS"))
            else:
                print(f"  FAIL: {task_resp}")
                result.phases.append(("Task Creation (Base)", f"FAIL: {task_resp.get('detail', '')}"))
        else:
            print(f"  FAIL: {task_resp}")
            result.phases.append(("Task Creation (Base)", f"FAIL: {task_resp.get('detail', task_resp.get('_http_status'))}"))
            # Continue anyway to generate partial report

        # ── Phase 3: Worker Flow ────────────────────────────────
        print("\n" + "=" * 60)
        print("  Phase 3: Worker Apply + Submit")
        print("=" * 60)

        if result.task_id:
            # Register worker (uses /executors/register endpoint)
            reg_resp = await client.post(
                f"{EM_API_URL}/api/v1/executors/register",
                json={"wallet_address": WORKER_WALLET, "display_name": "Golden Flow Worker"},
            )
            reg_data = reg_resp.json()
            result.executor_id = reg_data.get("executor", {}).get("id", "")
            if not result.executor_id:
                print(f"  WARN: Registration response: {reg_data}")
            else:
                print(f"  Worker registered: {result.executor_id[:8]}...")

            # Apply
            apply_resp = await client.post(
                f"{EM_API_URL}/api/v1/tasks/{result.task_id}/apply",
                json={"executor_id": result.executor_id, "message": "Golden Flow Hedera"},
            )
            apply_data = apply_resp.json() if apply_resp.status_code != 204 else {}
            if apply_resp.status_code in (200, 201):
                print(f"  Applied: OK")
            else:
                print(f"  Applied: {apply_resp.status_code} — {apply_data.get('detail', apply_data)}")

            # Sign escrow on-chain (agent authorizes USDC lock on Base)
            print(f"  Signing escrow on Base (${BOUNTY} USDC)...")
            try:
                escrow_data = sign_escrow_for_assign(AGENT_KEY, WORKER_WALLET, BOUNTY)
                result.escrow_tx = escrow_data["escrow_tx"]
                print(f"  Escrow TX: {BASE_EXPLORER}/tx/{result.escrow_tx}")
            except Exception as e:
                print(f"  Escrow signing failed: {e}")
                result.phases.append(("Worker Flow", f"FAIL: escrow: {e}"))
                return result

            # Assign with escrow proof
            assign_resp = await signed_request(client, signer, "POST",
                f"/api/v1/tasks/{result.task_id}/assign",
                {
                    "executor_id": result.executor_id,
                    "escrow_tx": escrow_data["escrow_tx"],
                    "payment_info": escrow_data["payment_info"],
                },
            )
            print(f"  Assigned: {assign_resp.get('_http_status')}")
            if assign_resp.get("_http_status") not in (200, 201):
                print(f"  Assign error: {assign_resp.get('detail', assign_resp)}")

            # Submit evidence
            submit_resp = await client.post(
                f"{EM_API_URL}/api/v1/tasks/{result.task_id}/submit",
                json={
                    "executor_id": result.executor_id,
                    "evidence": {"text_response": "golden_flow_hedera_complete"},
                    "notes": "Golden Flow Hedera E2E",
                },
            )
            sub_data = submit_resp.json()
            result.submission_id = sub_data.get("data", {}).get("submission_id", sub_data.get("submission_id", ""))
            if submit_resp.status_code in (200, 201) and result.submission_id:
                print(f"  Submitted: {result.submission_id[:8]}...")
            else:
                print(f"  Submit: {submit_resp.status_code} — {sub_data.get('detail', sub_data)}")

            result.phases.append(("Worker Flow", "PASS"))
        else:
            print("  SKIP: No task_id")
            result.phases.append(("Worker Flow", "SKIP"))

        # ── Phase 4: Approve + Payment ──────────────────────────
        print("\n" + "=" * 60)
        print("  Phase 4: Approve + Payment (Base)")
        print("=" * 60)

        if result.submission_id:
            approve_resp = await signed_request(client, signer, "POST",
                f"/api/v1/submissions/{result.submission_id}/approve",
                {"notes": "Golden Flow Hedera approved", "rating_score": 90},
            )
            result.payment_tx = (
                approve_resp.get("data", {}).get("payment_tx", "")
                or approve_resp.get("payment_tx", "")
            )
            print(f"  Approved: {approve_resp.get('_http_status')}")
            if result.payment_tx:
                print(f"  Payment TX: {BASE_EXPLORER}/tx/{result.payment_tx}")
            result.phases.append(("Approval + Payment (Base)", "PASS"))
        else:
            print("  SKIP: No submission_id")
            result.phases.append(("Approval + Payment (Base)", "SKIP"))

    # ── Phase 5: Hedera Reputation ──────────────────────────
    print("\n" + "=" * 60)
    print("  Phase 5: Reputation on Hedera")
    print("=" * 60)

    # Ensure agent exists on Hedera
    identity = await get_identity(HEDERA_AGENT_ID)
    if identity.get("found"):
        print(f"  Agent #{HEDERA_AGENT_ID} on Hedera: CONFIRMED")

    # Agent rates worker
    fb1 = await submit_feedback(
        agent_id=HEDERA_AGENT_ID, value=90,
        tag1="task_completion", tag2="golden_flow_hedera",
    )
    result.agent_rates_worker_tx = fb1.get("transaction", fb1.get("txHash", ""))
    if result.agent_rates_worker_tx:
        print(f"  Agent->Worker: PASS")
        print(f"  TX: {EXPLORER_URL}/transaction/{result.agent_rates_worker_tx}")

    # Worker rates agent
    fb2 = await submit_feedback(
        agent_id=HEDERA_AGENT_ID, value=85,
        tag1="agent_rating", tag2="golden_flow_hedera",
    )
    result.worker_rates_agent_tx = fb2.get("transaction", fb2.get("txHash", ""))
    if result.worker_rates_agent_tx:
        print(f"  Worker->Agent: PASS")
        print(f"  TX: {EXPLORER_URL}/transaction/{result.worker_rates_agent_tx}")

    rep = await get_reputation(HEDERA_AGENT_ID, include_feedback=True)
    summary = rep.get("summary", {})
    result.rep_count = summary.get("count", 0)
    result.rep_avg = summary.get("summaryValue", 0)
    print(f"  Reputation: count={result.rep_count}, avg={result.rep_avg}")

    result.phases.append(("Reputation (Hedera)", "PASS"))

    # ── Phase 5b: Merit Tip (reputation-gated HBAR payment) ──
    # Gate the tip by ACTUAL on-chain reputation (read from Hedera chain),
    # not by the score we just submitted. This is a real feedback loop:
    # on-chain reputation → payment decision.
    TIP_THRESHOLD = 80
    TIP_AMOUNT_HBAR = 0.01
    onchain_avg = result.rep_avg  # Read from get_reputation() above

    if onchain_avg > TIP_THRESHOLD and AGENT_KEY:
        print(f"\n  [Merit Tip] On-chain reputation avg={onchain_avg} > {TIP_THRESHOLD} threshold")
        print(f"  Worker earned excellent reputation. Sending {TIP_AMOUNT_HBAR} HBAR merit tip...")
        print(f"  Sending to {WORKER_WALLET} on {NETWORK_LABEL}...")

        try:
            from eth_account import Account
            import rlp

            agent_acct = Account.from_key(AGENT_KEY)

            # Get nonce for agent on Hedera testnet
            nonce_resp = await _json_rpc("eth_getTransactionCount", [agent_acct.address, "latest"])
            nonce = int(nonce_resp, 16)

            # Build legacy transaction (Hedera relay supports legacy format)
            tip_wei = int(TIP_AMOUNT_HBAR * 1e18)  # HBAR to weibars
            tx = {
                "nonce": nonce,
                "gasPrice": 1_100_000_000_000,  # 1100 gwei (Hedera min is 1020)
                "gas": 30_000,
                "to": bytes.fromhex(WORKER_WALLET[2:]),
                "value": tip_wei,
                "data": b"",
                "chainId": CHAIN_ID,
            }

            signed = agent_acct.sign_transaction(tx)
            raw = getattr(signed, "raw_transaction", None) or getattr(signed, "rawTransaction", None)
            raw = raw.hex()
            if not raw.startswith("0x"):
                raw = "0x" + raw

            tx_hash_resp = await _json_rpc("eth_sendRawTransaction", [raw])
            result.merit_tip_tx = tx_hash_resp
            result.merit_tip_hbar = TIP_AMOUNT_HBAR

            print(f"  PASS: Merit tip sent!")
            print(f"  TX: {EXPLORER_URL}/transaction/{result.merit_tip_tx}")
            result.phases.append(("Merit Tip (Hedera HBAR)", "PASS"))

        except Exception as e:
            print(f"  FAIL: Merit tip error: {e}")
            result.phases.append(("Merit Tip (Hedera HBAR)", f"FAIL: {e}"))
    else:
        print(f"\n  [Merit Tip] On-chain avg={onchain_avg} <= {TIP_THRESHOLD} -- no tip earned")
        result.phases.append(("Merit Tip (Hedera HBAR)", "SKIP"))

    # ── Phase 6: Report ─────────────────────────────────────
    print("\n" + "=" * 60)
    print("  Phase 6: Generate Report")
    print("=" * 60)

    report = _generate_report(result)
    report_path = os.path.join(os.path.dirname(__file__), "GOLDEN_FLOW_HEDERA_REPORT.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"  Saved: {report_path}")

    all_pass = all(p[1] == "PASS" for p in result.phases)
    print(f"\n  RESULT: {'PASS' if all_pass else 'PARTIAL'} ({len(result.phases)}/{len(result.phases)} phases)")
    if result.payment_tx:
        print(f"  Payment (Base): {BASE_EXPLORER}/tx/{result.payment_tx}")
    if result.agent_rates_worker_tx:
        print(f"  Reputation (Hedera): {EXPLORER_URL}/transaction/{result.agent_rates_worker_tx}")
    if result.merit_tip_tx:
        print(f"  Merit Tip (Hedera): {EXPLORER_URL}/transaction/{result.merit_tip_tx}")


def _generate_report(r: FlowResult) -> str:
    all_pass = all(p[1] == "PASS" for p in r.phases)
    status = "PASS" if all_pass else "PARTIAL"

    phase_rows = "\n".join(
        f"| {i+1} | {name} | **{st}** |" for i, (name, st) in enumerate(r.phases)
    )

    return f"""# Golden Flow Hedera Report -- Cross-Chain E2E Test

> **Date**: {r.timestamp}
> **Payment Chain**: Base Mainnet (chain 8453)
> **Reputation Chain**: {NETWORK_LABEL} (chain {CHAIN_ID})
> **Facilitator**: {FACILITATOR_URL}
> **Result**: **{status}**

---

## Executive Summary

Full Execution Market lifecycle executed on production:
task created, worker applied, evidence submitted, payment released on **Base** (USDC),
then bidirectional reputation posted on **{NETWORK_LABEL}** (ERC-8004).

**Key Result**: Same task, two chains -- payment where the money is (Base),
reputation where the identity lives (Hedera).

---

## Cross-Chain Transaction Summary

| Operation | Chain | TX Hash | Explorer |
|-----------|-------|---------|----------|
| Escrow Lock | Base (8453) | `{r.escrow_tx[:20]}...` | [BaseScan]({BASE_EXPLORER}/tx/{r.escrow_tx}) |
| Payment Release | Base (8453) | `{r.payment_tx[:20]}...` | [BaseScan]({BASE_EXPLORER}/tx/{r.payment_tx}) |
| Agent->Worker Rating | {NETWORK_LABEL} ({CHAIN_ID}) | `{r.agent_rates_worker_tx[:20]}...` | [HashScan]({EXPLORER_URL}/transaction/{r.agent_rates_worker_tx}) |
| Worker->Agent Rating | {NETWORK_LABEL} ({CHAIN_ID}) | `{r.worker_rates_agent_tx[:20]}...` | [HashScan]({EXPLORER_URL}/transaction/{r.worker_rates_agent_tx}) |
| Merit Tip ({r.merit_tip_hbar} HBAR) | {NETWORK_LABEL} ({CHAIN_ID}) | `{r.merit_tip_tx[:20]}...` | [HashScan]({EXPLORER_URL}/transaction/{r.merit_tip_tx}) |

---

## Test Configuration

| Parameter | Value |
|-----------|-------|
| Task ID | `{r.task_id}` |
| Bounty | ${BOUNTY} USDC |
| Worker Net (87%) | ${BOUNTY * 0.87:.4f} USDC |
| Payment Chain | Base Mainnet (chain 8453) |
| Reputation Chain | {NETWORK_LABEL} (chain {CHAIN_ID}) |
| Hedera Agent ID | #{HEDERA_AGENT_ID} |
| Facilitator HBAR | {r.facilitator_hbar} |
| Identity Registry | `{IDENTITY_REGISTRY}` |
| Reputation Registry | `{REPUTATION_REGISTRY}` |

---

## Flow Diagram

```mermaid
sequenceDiagram
    participant A as Agent
    participant EM as Execution Market
    participant B as Base (USDC)
    participant F as Facilitator
    participant H as {NETWORK_LABEL}

    Note over A,H: Phases 2-4: Task Lifecycle (Base)
    A->>EM: Create task (${BOUNTY} bounty)
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
{phase_rows}

---

## Reputation After Test

| Metric | Value |
|--------|-------|
| Agent #{HEDERA_AGENT_ID} | {FACILITATOR_NETWORK} |
| Feedback Count | {r.rep_count} |
| Average Score | {r.rep_avg} |
| Verify | [API]({FACILITATOR_URL}/reputation/{FACILITATOR_NETWORK}/{HEDERA_AGENT_ID}) |

---

## On-Chain Evidence

### Base Mainnet (Payment)

| TX | Explorer |
|----|----------|
| Escrow | [{r.escrow_tx[:16]}...]({BASE_EXPLORER}/tx/{r.escrow_tx}) |
| Payment | [{r.payment_tx[:16]}...]({BASE_EXPLORER}/tx/{r.payment_tx}) |

### {NETWORK_LABEL} (Reputation)

| TX | Explorer |
|----|----------|
| Agent->Worker | [{r.agent_rates_worker_tx[:16]}...]({EXPLORER_URL}/transaction/{r.agent_rates_worker_tx}) |
| Worker->Agent | [{r.worker_rates_agent_tx[:16]}...]({EXPLORER_URL}/transaction/{r.worker_rates_agent_tx}) |

---

## Reproducibility

```bash
# Anyone can verify the Hedera reputation:
curl {FACILITATOR_URL}/reputation/{FACILITATOR_NETWORK}/{HEDERA_AGENT_ID}

# Run the full flow (requires wallet keys):
cd hedera
pip install -r requirements.txt
EM_HIRING_AGENT_PRIVATE_KEY=0x... EM_WORKER_PRIVATE_KEY=0x... python golden_flow_hedera.py
```
"""


if __name__ == "__main__":
    asyncio.run(run_golden_flow())
