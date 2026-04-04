# Integracion Hedera — Pagos Agentivos con IA

> **Socio**: Hedera ($15K) | **Track**: AI & Agentic Payments
> **Produccion**: [execution.market](https://execution.market) | **Agente**: #2106 en Base ERC-8004

---

## Que Construimos

Execution Market ejecuta **pagos de IA a humanos en 9 cadenas EVM** via x402. Extendimos a **Hedera** con cinco integraciones:

1. **Identidad ERC-8004 en Hedera** — Agente #99 registrado en testnet (gasless via Facilitator)
2. **Reputacion Bidireccional** — Feedback on-chain agente-a-worker y worker-a-agente
3. **Merit Tip: 0.01 HBAR** — Transferencia directa de HBAR gatekeada por reputacion
4. **Registro de Eventos HCS** — Hedera Consensus Service nativo (NO EVM) para audit trail inmutable
5. **Extension Open-Source del Facilitator** — [x402-rs](https://github.com/UltravioletaDAO/x402-rs) extendido para Hedera ([commit `66d34e6`](https://github.com/UltravioletaDAO/x402-rs/commit/66d34e6c7f805fa26a33757b2cdf5ec3038ecb95))

---

## Arquitectura

### Flujo de Pago Actual (9 Cadenas EVM)

```
┌─────────────┐     ┌───────────────┐     ┌──────────────┐
│  Agente IA   │     │ x402 Escrow   │     │  Trabajador  │
└──────┬──────┘     └───────┬───────┘     └──────┬───────┘
       │ 1. Firma EIP-3009 │                     │
       │───────────────────>│                     │
       │ 2. Bloquea escrow  │                     │
       │                    │  3. Libera (87%)    │
       │                    │────────────────────>│
       │                    │  4. Comision (13%)  │
       │ GASLESS — Facilitator paga todo el gas   │
```

### Extension a Hedera

```
┌─────────────┐     ┌───────────────┐     ┌──────────────┐
│  Agente IA   │     │ Hedera SDK    │     │  Trabajador  │
└──────┬──────┘     └───────┬───────┘     └──────┬───────┘
       │ 1. Crea transferencia                    │
       │───────────────────>│                     │
       │  (HBAR o USDC)     │                     │
       │ 2. Ejecuta TX      │  3. Trabajador recibe│
       │   (Hedera testnet) │────────────────────>│
       │ TX en HashScan.io  │                     │
```

### Identidad ERC-8004 en Hedera

```
┌──────────────────────────────────────────────────┐
│         ERC-8004 Identity Registry               │
│         (desplegado en 16+ redes)                │
│                                                  │
│  Base ────── Agente #2106 (produccion)           │
│  Ethereum ── Agente #2106                        │
│  Polygon ─── Agente #2106                        │
│  Hedera ──── Agente #2106 (NUEVO, testnet)       │
│                                                  │
│  Contratos en testnet:                           │
│  Identidad: 0x8004A818BFB912233c491871b3d84c89A4│
│  Reputacion: 0x8004B663056A597Dffe9eCcC1965A193B│
└──────────────────────────────────────────────────┘
```

---

## Por Que No x402 Directamente en Hedera?

USDC en Hedera es **HTS nativo (Hedera Token Service)**, no ERC-20:

| Caracteristica | Cadenas EVM (ERC-20) | Hedera (HTS) |
|----------------|----------------------|--------------|
| `transferWithAuthorization()` (EIP-3009) | SI | NO |
| `permit()` (EIP-2612) | SI | NO |
| Pre-auth gasless | SI (x402 usa esto) | NO |

x402 depende de EIP-3009 para escrow gasless. HTS no lo soporta. Para Hedera, usamos **SDK nativo de Hedera** para pagos (transferencias HBAR) y ERC-8004 para identidad/reputacion (llamadas EVM estandar funcionan).

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
#   5. ERC-8004 identity check: Agente #2106 encontrado
```

---

## Referencias On-Chain

| Contrato | Red | Direccion |
|----------|-----|-----------|
| ERC-8004 Identity Registry | Hedera Testnet | `0x8004A818BFB912233c491871b3d84c89A494BD9e` |
| ERC-8004 Reputation Registry | Hedera Testnet | `0x8004B663056A597Dffe9eCcC1965A193B7388713` |
| ERC-8004 Identity Registry | Todos los Mainnets | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` |
| Agente Execution Market | Base Mainnet | Agente #2106 |
| Hedera Testnet RPC | JSON-RPC Relay | `https://testnet.hashio.io/api` |
| Hedera Explorer | HashScan | `https://hashscan.io/testnet` |

---

## Relacionado

- [Prueba de Integracion](PROOF_OF_INTEGRATION.es.md) — TX hashes, Golden Flow 7/7, arquitectura
- [Guia para Jueces](JUDGES_GUIDE.es.md) — Links de verificacion, script de demo
- [Guia para Presentadores](PRESENTER_GUIDE.es.md) — Talking points para booth de Hedera
- [API en Produccion](https://api.execution.market/docs) — Swagger UI
- [Codigo Fuente](https://github.com/UltravioletaDAO/execution-market) — Open source
