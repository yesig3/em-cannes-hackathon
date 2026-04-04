# Hedera Track -- Guia para Jueces

> Para jueces en el booth de Hedera, ETHGlobal Cannes 2026.

---

## TL;DR

Execution Market es un **marketplace en produccion** (no un prototipo) donde agentes IA publican bounties y humanos las completan. Construimos **cinco integraciones con Hedera** incluyendo **HCS (Hedera Consensus Service)** -- NATIVO de Hedera, NO accesible via EVM. Golden Flow: **7/7 PASS**, 5 TXs on-chain + 6 mensajes HCS en 2 chains.

---

## 1. Track: "AI & Agentic Payments on Hedera" ($6,000)

| Detalle | Valor |
|---------|-------|
| **Premio** | $6,000 (hasta 2 equipos a $3,000) |
| **Requisito** | "Ejecutar al menos un pago/transferencia en Hedera Testnet" |
| **Tech aceptadas** | ERC-8004, x402, Hedera SDKs, HCS, Hedera Agent Kit, OpenClaw ACP, A2A |

**Cuatro categorias de operaciones on-chain ejecutadas:**

1. **Registro ERC-8004** -- mint de NFT registrando Agente #99
2. **Reputacion Bidireccional** -- escrituras on-chain (agente + worker se califican mutuamente)
3. **Merit Tip: 0.01 HBAR** -- transferencia directa de HBAR, gatekeada por reputacion
4. **Registro HCS** -- 6 mensajes de consenso inmutables via TopicMessageSubmitTransaction nativo

| Tecnologia | Uso |
|-----------|-----|
| **ERC-8004** | Identidad on-chain + reputacion bidireccional |
| **x402** | Pagos en produccion en 9 chains EVM |
| **hiero-sdk-python** | Creacion de topics HCS + envio de mensajes (nativo, no EVM) |
| **HCS** | 6 mensajes inmutables por tarea |
| **Facilitator** (open-source, Rust) | Operaciones gasless en Hedera ([commit `66d34e6`](https://github.com/UltravioletaDAO/x402-rs/commit/66d34e6c7f805fa26a33757b2cdf5ec3038ecb95)) |

---

## 2. Que es HCS (Diferenciador Clave)

HCS es **nativo de Hedera** -- NO es parte del EVM, NO accesible via JSON-RPC.

- Crea logs de eventos inmutables y ordenados con **timestamps de consenso** (acordados por nodos de Hedera, no del cliente)
- Usa `TopicCreateTransaction` + `TopicMessageSubmitTransaction` de `hiero-sdk-python`
- Mensajes no se pueden alterar ni eliminar
- Cualquiera verifica via API REST publica del Mirror Node -- sin auth
- Implementacion: `hedera/hcs_logger.py`

---

## 3. Que Construimos (5 Integraciones)

**3.1 Identidad ERC-8004** -- Agente #99 en Hedera Testnet. Contrato: `0x8004A818BFB912233c491871b3d84c89A494BD9e`. Verificar: `GET https://facilitator.ultravioletadao.xyz/identity/hedera-testnet/99`

**3.2 Reputacion Bidireccional** -- Contrato: `0x8004B663056A597Dffe9eCcC1965A193B7388713`. 29 entradas, promedio 87/100. Verificar: `GET https://facilitator.ultravioletadao.xyz/reputation/hedera-testnet/99`

**3.3 Merit Tip: 0.01 HBAR** -- Transferencia HBAR gatekeada por reputacion. TX: [`0x419d824c...`](https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321)

**3.4 Log HCS** -- 6 eventos por tarea via SDK nativo. Topic: `0.0.8511429`. [Mirror Node](https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages)

| Seq | Evento | Registra |
|-----|--------|----------|
| 1 | `task_created` | ID tarea, bounty, deadline |
| 2 | `worker_applied` | ID ejecutor |
| 3 | `escrow_locked` | TX hash Base (cross-chain) |
| 4 | `payment_released` | TX hash Base, monto |
| 5 | `reputation_agent_to_worker` | Puntaje, TX Hedera |
| 6 | `reputation_worker_to_agent` | Puntaje, TX Hedera |

**3.5 Extension del Facilitator** -- Extendimos [x402-rs](https://github.com/UltravioletaDAO/x402-rs) (Rust, 21 blockchains) para Hedera. Paga gas HBAR. [Commit `66d34e6`](https://github.com/UltravioletaDAO/x402-rs/commit/66d34e6c7f805fa26a33757b2cdf5ec3038ecb95)

---

## 4. Como Verificar

Todo verificable publicamente. Sin cuenta ni API key.

**Mensajes HCS:**
```
https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages
```

Decodificar:
```bash
curl -s "https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages" \
  | python3 -c "import sys,json,base64; msgs=json.load(sys.stdin)['messages']; [print(base64.b64decode(m['message']).decode()) for m in msgs]"
```

**TX Merit Tip:** https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321

**Identidad Agente:** `GET https://facilitator.ultravioletadao.xyz/identity/hedera-testnet/99`

**Reputacion Agente:** `GET https://facilitator.ultravioletadao.xyz/reputation/hedera-testnet/99`

**Produccion:** https://execution.market (en vivo, 9 chains EVM, USDC real)

| Contrato | Direccion | Explorer |
|----------|-----------|----------|
| ERC-8004 Identity | `0x8004A818BFB912233c491871b3d84c89A494BD9e` | [HashScan](https://hashscan.io/testnet/address/0x8004A818BFB912233c491871b3d84c89A494BD9e) |
| ERC-8004 Reputation | `0x8004B663056A597Dffe9eCcC1965A193B7388713` | [HashScan](https://hashscan.io/testnet/address/0x8004B663056A597Dffe9eCcC1965A193B7388713) |
| Wallet Facilitator | `0x34033041a5944B8F10f8E4D8496Bfb84f1A293A8` | [HashScan](https://hashscan.io/testnet/account/0x34033041a5944B8F10f8E4D8496Bfb84f1A293A8) |

---

## 5. Script de Demo para Booth

**Pestanas a abrir antes de la demo:**

1. https://execution.market (marketplace en vivo)
2. https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321 (TX Merit Tip)
3. https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages (mensajes HCS)
4. https://api.execution.market/docs (Swagger API)

**Flujo (2-3 minutos):**

1. **Pestana 1** -- "Marketplace en produccion. Tareas reales, pagos USDC reales. Agente #2106 en Base."
2. **Pestana 2** -- "Pago real de HBAR en Hedera Testnet. Worker recibe 0.01 HBAR cuando tiene buen puntaje. Gatekeado por reputacion."
3. **Pestana 3** -- "Diferenciador clave: HCS. Nativo de Hedera, no EVM. 6 eventos inmutables con timestamps de consenso. Cualquiera verifica via Mirror Node, sin API key."
4. **Cierre** -- "Identidad ERC-8004, reputacion on-chain, tips HBAR, registro HCS nativo. 5 operaciones Hedera + escrow USDC en Base. Golden Flow 7/7."

### Preguntas

**"Por que HCS?"** -- Inmutable, timestamps de consenso, a prueba de manipulacion. Demuestra uso de Hedera mas alla de EVM generico.

**"Mainnet?"** -- Identidad/reputacion/HCS en Hedera testnet. Pagos en Base mainnet (USDC real). Una variable de entorno cambia a mainnet.

**"Que es ERC-8004?"** -- Registro de identidad on-chain para agentes IA. Agente #99 en Hedera. 16 redes, misma direccion via CREATE2. Listado por Hedera como tech aceptada.

**"Gasless como?"** -- Facilitator open-source (Rust) paga gas HBAR. Mismo modelo en 9 chains de produccion.

**"Open source?"** -- MIT. [em-cannes-hackathon](https://github.com/UltravioletaDAO/em-cannes-hackathon) + [x402-rs](https://github.com/UltravioletaDAO/x402-rs)

---

## 6. Golden Flow (7/7 PASS)

| Fase | Operacion | Chain | Evidencia |
|------|-----------|-------|-----------|
| 1 | Conectividad | Ambas | PASS |
| 2 | Tarea + lock escrow | Base | [BaseScan](https://basescan.org/tx/0x98fc338221502fb937cf9fdfe26248a9a0700580ef4b690b6853c58da3efeb84) |
| 3 | Worker + evidencia | Base (API) | PASS |
| 4 | Aprobacion + pago | Base | [BaseScan](https://basescan.org/tx/0x29f1aea3cbee79996eab4c632d1982c0578820556fc348bdb5d1a012c502e95a) |
| 5 | Reputacion bidireccional | Hedera | [HashScan (A->W)](https://hashscan.io/testnet/transaction/0x26464dbd022d6829e107ca3a52b04720b59c5aa9d7f6a7394a3b50948acdb1c6) / [HashScan (W->A)](https://hashscan.io/testnet/transaction/0x300c402eb1051b8995fee783b23b3b74e68863ad3ac7c958ccccfea30cdd658e) |
| 6 | Merit Tip (0.01 HBAR) | Hedera | [HashScan](https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321) |
| 7 | HCS (6 mensajes) | Hedera (nativo) | [Mirror Node](https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages) |

---

## Referencia Rapida

| Recurso | URL |
|---------|-----|
| Produccion | https://execution.market |
| Swagger API | https://api.execution.market/docs |
| Mensajes HCS | https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages |
| TX Merit Tip | https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321 |
| Identidad Agente | https://facilitator.ultravioletadao.xyz/identity/hedera-testnet/99 |
| Reputacion Agente | https://facilitator.ultravioletadao.xyz/reputation/hedera-testnet/99 |
| Repo hackathon | https://github.com/UltravioletaDAO/em-cannes-hackathon |
| Repo Facilitator | https://github.com/UltravioletaDAO/x402-rs |
| Commit Facilitator | https://github.com/UltravioletaDAO/x402-rs/commit/66d34e6c7f805fa26a33757b2cdf5ec3038ecb95 |
| Contacto | @ExecutionMarket en X |

---

## Auto-Evaluacion: 41/50

> Esta evaluacion fue realizada utilizando el [framework de evaluacion Hedera Skills](https://github.com/hedera-dev/hedera-skills) proporcionado por el equipo de desarrollo de Hedera. El skill audita submissions contra los criterios oficiales del track.

| Criterio | Puntaje | Notas |
|----------|:-------:|-------|
| Technicality | **8/10** | ERC-8004 (EVM) + HCS (SDK nativo) + Facilitator (Rust). HCS demuestra profundidad no-EVM. |
| Originality | **8/10** | Cross-chain: escrow en Base, reputacion + HCS + tips en Hedera. |
| Practicality | **9/10** | Marketplace en produccion con USDC real. |
| Usability | **8/10** | Docs bilingues, scripts ejecutables, TXs verificables. |
| WOW Factor | **8/10** | Golden Flow 7/7, 5 TXs + 6 mensajes HCS, Facilitator open-source. |
| **TOTAL** | **41/50** | |

Trayectoria: 36 (base) -> 39 (+Facilitator, +merit tip) -> 41 (+HCS).
