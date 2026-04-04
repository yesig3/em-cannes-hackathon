# Hedera Track -- Guia para Jueces

> **Para jueces en el booth de Hedera, ETHGlobal Cannes 2026.**
> Todo lo que necesitan para evaluar nuestra submission en un documento.

---

## TL;DR

Execution Market es un **marketplace en produccion** donde agentes de IA publican bounties y humanos las completan por pago instantaneo. Construimos **cinco integraciones con Hedera** para este hackathon, incluyendo **HCS (Hedera Consensus Service)** -- un feature NATIVO de Hedera que NO es accesible via EVM ni JSON-RPC. Nuestro Golden Flow E2E pasa **7/7 fases** con **5 transacciones on-chain + 6 mensajes HCS** en 2 chains.

---

## 1. Que es HCS (Hedera Consensus Service)?

HCS es un **feature nativo de Hedera** -- NO es parte del EVM y no se puede acceder mediante JSON-RPC relay ni herramientas EVM genericas.

**Que hace:**
- Crea un **log de eventos inmutable y ordenado** con timestamps de consenso acordados por los nodos de la red de Hedera (no timestamps del cliente)
- Los mensajes se envian via `TopicCreateTransaction` y `TopicMessageSubmitTransaction` del **hiero-sdk-python** (SDK oficial de Hedera)
- Una vez enviados, los mensajes **no se pueden alterar ni eliminar**
- Cualquier tercero puede leer y verificar los mensajes via la **API REST publica del Mirror Node** -- sin autenticacion, sin API key, completamente abierto

**Por que importa para esta submission:**
- Demuestra que usamos Hedera **mas alla de compatibilidad EVM generica** -- HCS requiere el SDK nativo de Hedera
- Crea una **pista de auditoria a prueba de manipulacion** de cada evento del ciclo de vida de una tarea
- Los mensajes incluyen referencias cross-chain (TX hashes de Base), vinculando evidencia de pago entre chains
- Los timestamps de consenso proveen **garantias de ordenamiento** que timestamps del lado cliente no pueden dar

**Nuestra implementacion:** `hedera/hcs_logger.py` -- un modulo Python usando `hiero-sdk-python` que crea topics y envia mensajes JSON estructurados para cada evento del ciclo de vida.

---

## 2. Track: "AI & Agentic Payments on Hedera" ($6,000)

| Detalle | Valor |
|---------|-------|
| **Track** | AI & Agentic Payments on Hedera |
| **Premio** | $6,000 (hasta 2 equipos a $3,000 cada uno) |
| **Requisito** | "Ejecutar al menos un pago, transferencia de tokens u operacion financiera en Hedera Testnet" |
| **Tecnologias aceptadas** | ERC-8004 (Trustless Agents), x402, Hedera SDKs, HCS, Hedera Agent Kit, OpenClaw ACP, A2A |

**Como cumplimos el requisito:**

Ejecutamos **cuatro categorias de operaciones on-chain** en Hedera Testnet:

1. **Registro de Agente ERC-8004** -- mint de NFT (transferencia de token) registrando al Agente #99
2. **Feedback Bidireccional de Reputacion** -- escrituras de estado on-chain (agente califica worker + worker califica agente)
3. **Merit Tip: 0.01 HBAR** -- transferencia directa de HBAR al worker, gatekeada por puntaje de reputacion
4. **Registro de Eventos HCS** -- 6 mensajes de consenso inmutables via TopicMessageSubmitTransaction nativo

**Tecnologias aceptadas que usamos:**

| Tecnologia | Como la usamos |
|-----------|----------------|
| **ERC-8004** (Trustless Agents) | Identidad on-chain de agente + reputacion bidireccional |
| **x402** (Estandar de Pagos) | Protocolo de pagos en produccion en 9 chains EVM |
| **hiero-sdk-python** (SDK de Hedera) | Creacion de topics HCS + envio de mensajes (nativo, no EVM) |
| **HCS** (Hedera Consensus Service) | Registro inmutable de eventos -- 6 mensajes de ciclo de vida por tarea |
| **Facilitator** (open-source, Rust) | Operaciones gasless en Hedera (extendido para este hackathon) |

---

## 3. Que Construimos en Hedera (Lista Completa)

### 3.1 Identidad ERC-8004 (EVM)

Agente #99 registrado en Hedera Testnet via el Registro de Identidad ERC-8004. Mismo contrato desplegado con CREATE2 usado en 16 redes. El agente tiene una identidad on-chain descubrible por cualquier otro agente en Hedera.

- **Contrato**: `0x8004A818BFB912233c491871b3d84c89A494BD9e`
- **Agent ID**: 99
- **Verificar**: `GET https://facilitator.ultravioletadao.xyz/identity/hedera-testnet/99`

### 3.2 Reputacion Bidireccional ERC-8004 (EVM)

Puntajes de reputacion agente-a-worker y worker-a-agente escritos en el Registro de Reputacion en Hedera Testnet. Son escrituras de estado on-chain reales que crean senales de confianza verificables.

- **Contrato**: `0x8004B663056A597Dffe9eCcC1965A193B7388713`
- **Feedback Count**: 29 entradas, puntaje promedio 87/100
- **Verificar**: `GET https://facilitator.ultravioletadao.xyz/reputation/hedera-testnet/99`

### 3.3 Merit Tip: 0.01 HBAR (Transferencia EVM)

Cuando un worker recibe un puntaje de reputacion por encima del umbral, el agente automaticamente envia una **transferencia directa de HBAR** como recompensa por merito. Es un pago real en Hedera Testnet, gatekeado por datos de reputacion on-chain.

- **Monto**: 0.01 HBAR por merit tip
- **TX**: [`0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321`](https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321)
- **Mecanismo**: Gatekeado por reputacion -- solo workers que entregan trabajo de calidad reciben el tip

### 3.4 Log de Eventos HCS (NATIVO -- No EVM)

Cada evento del ciclo de vida de una tarea se registra como un mensaje inmutable, con timestamp y ordenado, en un topic HCS. Esto usa `hiero-sdk-python` con `TopicCreateTransaction` y `TopicMessageSubmitTransaction` -- **APIs nativas de Hedera que NO son accesibles via EVM ni JSON-RPC relay.**

- **Topic**: `0.0.8511429`
- **Mensajes**: 6 eventos de ciclo de vida por tarea
- **Mirror Node**: `https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages`
- **SDK**: `hiero-sdk-python` (SDK oficial de Python para Hedera)

**Los 6 eventos registrados:**

| Seq | Evento | Que registra |
|-----|--------|--------------|
| 1 | `task_created` | ID de tarea, monto del bounty, deadline, chain de pago |
| 2 | `worker_applied` | ID del ejecutor, timestamp de aplicacion |
| 3 | `escrow_locked` | TX hash de Base del lock de escrow (referencia cross-chain) |
| 4 | `payment_released` | TX hash de Base de la liberacion de pago, monto |
| 5 | `reputation_agent_to_worker` | Puntaje, TX hash de Hedera |
| 6 | `reputation_worker_to_agent` | Puntaje, TX hash de Hedera |

### 3.5 Extension del Facilitator (Open-Source, Rust)

Extendimos el [Facilitator x402-rs](https://github.com/UltravioletaDAO/x402-rs) (servidor Rust en produccion, 21 blockchains) para soportar Hedera mainnet (chain 295) + testnet (chain 296). No es un wrapper de demo -- es una contribucion a infraestructura open-source que cualquier proyecto puede usar.

- **Commit**: [`66d34e6`](https://github.com/UltravioletaDAO/x402-rs/commit/66d34e6c7f805fa26a33757b2cdf5ec3038ecb95)
- **Que hace**: Paga gas HBAR para todas las operaciones en Hedera para que agentes nunca necesiten tener HBAR

---

## 4. Como Verificar (Para Jueces)

Toda la evidencia es verificable publicamente. No se necesita cuenta ni API key.

### Mensajes HCS (Log Nativo de Eventos Hedera)

Abrir en navegador o con curl:

```
https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages
```

Cada mensaje contiene:
- `sequence_number` -- ordenamiento garantizado por consenso de Hedera
- `consensus_timestamp` -- timestamp acordado por nodos de la red
- `message` -- JSON codificado en base64 con tipo de evento y datos

Para decodificar un mensaje:

```bash
curl -s "https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages" \
  | python3 -c "import sys,json,base64; msgs=json.load(sys.stdin)['messages']; [print(base64.b64decode(m['message']).decode()) for m in msgs]"
```

### Transaccion Merit Tip

```
https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321
```

Muestra una transferencia directa de 0.01 HBAR de la wallet del Facilitator a la direccion del worker.

### Identidad del Agente

```
GET https://facilitator.ultravioletadao.xyz/identity/hedera-testnet/99
```

Retorna los metadatos de identidad on-chain del Agente #99 (nombre, rol, URI).

### Reputacion del Agente

```
GET https://facilitator.ultravioletadao.xyz/reputation/hedera-testnet/99
```

Retorna conteo de feedback, puntaje promedio, y entradas individuales de feedback.

### Plataforma en Produccion

```
https://execution.market
```

El marketplace en vivo corriendo en 9 chains EVM con pagos reales en USDC. No es un prototipo de hackathon.

### Contratos On-Chain (Hedera Testnet)

| Contrato | Direccion | Explorer |
|----------|-----------|----------|
| Registro de Identidad ERC-8004 | `0x8004A818BFB912233c491871b3d84c89A494BD9e` | [HashScan](https://hashscan.io/testnet/address/0x8004A818BFB912233c491871b3d84c89A494BD9e) |
| Registro de Reputacion ERC-8004 | `0x8004B663056A597Dffe9eCcC1965A193B7388713` | [HashScan](https://hashscan.io/testnet/address/0x8004B663056A597Dffe9eCcC1965A193B7388713) |
| Wallet del Facilitator | `0x34033041a5944B8F10f8E4D8496Bfb84f1A293A8` | [HashScan](https://hashscan.io/testnet/account/0x34033041a5944B8F10f8E4D8496Bfb84f1A293A8) |

---

## 5. Script de Demo para el Booth

### Antes de la Demo

Tener estas pestanas abiertas:

1. **Pestana 1**: https://execution.market (el marketplace en vivo)
2. **Pestana 2**: https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321 (TX Merit Tip)
3. **Pestana 3**: https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages (mensajes HCS)
4. **Pestana 4**: https://api.execution.market/docs (Swagger API)

### Puntos de Conversacion (2-3 minutos)

**Apertura (30 segundos):**

"Execution Market es un marketplace en vivo donde agentes de IA publican bounties y humanos las completan por pago. Corremos en 9 chains en produccion con USDC real. Para este hackathon, agregamos Hedera -- no solo como otro chain EVM, sino usando features nativos de Hedera."

**Mostrar Pestana 1 -- Dashboard (30 segundos):**

"Este es nuestro dashboard de produccion. Tareas reales, pagos reales. Agente numero 2106 en Base."

**Mostrar Pestana 2 -- TX Merit Tip (30 segundos):**

"Aqui hay un pago real de HBAR en Hedera Testnet. Cuando un worker recibe un puntaje de reputacion alto, el agente automaticamente le envia 0.01 HBAR como propina. Esto esta gatekeado por reputacion -- solo workers buenos reciben la propina."

**Mostrar Pestana 3 -- Mensajes HCS (60 segundos):**

"Este es el diferenciador clave. Usamos Hedera Consensus Service -- un feature nativo de Hedera que NO existe en EVM. Cada evento del ciclo de vida de una tarea se registra como un mensaje inmutable con un timestamp de consenso acordado por los nodos de Hedera. Pueden ver 6 eventos aqui: tarea creada, worker aplico, escrow bloqueado, pago liberado, y ambas calificaciones de reputacion. Cualquiera puede verificar esto -- no se necesita API key, solo consultar la API REST del Mirror Node."

**Cierre (30 segundos):**

"Entonces estamos usando ERC-8004 para identidad, feedback de reputacion on-chain, merit tips en HBAR como pago, y HCS para registro inmutable de eventos nativo de Hedera. Cinco operaciones en Hedera Testnet, mas escrow de USDC en produccion en Base. Y extendimos nuestro Facilitator open-source -- un servidor Rust que soporta 21 blockchains -- para agregar soporte de Hedera."

### Preparacion para Preguntas

**"Por que HCS en vez de simplemente guardar en una base de datos?"**
HCS provee mensajes inmutables, con timestamps de consenso, que nadie puede alterar -- ni siquiera nosotros. Es una pista de auditoria a prueba de manipulacion. Una base de datos se puede editar. HCS no. Ademas, demuestra que usamos Hedera mas alla de EVM generico -- esto es un feature nativo de Hedera.

**"Esto corre en mainnet?"**
Identidad y reputacion estan en Hedera Testnet. Pagos estan en Base Mainnet (USDC real). Nuestro marketplace en produccion corre en 9 mainnets EVM. Hedera mainnet es el proximo paso -- el codigo ya lo soporta via una sola variable de entorno.

**"Que es ERC-8004?"**
Un registro de identidad on-chain para agentes de IA. Piensen en ello como un pasaporte -- Agente #99 es la identidad de nuestra plataforma en Hedera. Desplegado en 16 redes con la misma direccion via CREATE2. Listado por Hedera como tecnologia aceptada ("Trustless Agents").

**"Como son los pagos gasless?"**
Nuestro Facilitator open-source (servidor Rust) paga gas HBAR para todas las operaciones en Hedera. Agentes y workers nunca necesitan tener HBAR. Mismo modelo usado en 9 otras chains en produccion.

**"Que es el merit tip?"**
Una transferencia directa de 0.01 HBAR que el agente envia automaticamente cuando el puntaje de reputacion de un worker supera el umbral. Es una operacion financiera real gatekeada por datos de reputacion on-chain.

**"Como funciona HCS tecnicamente?"**
Creamos un topic HCS usando `TopicCreateTransaction`, luego enviamos mensajes usando `TopicMessageSubmitTransaction` -- ambos del SDK `hiero-sdk-python`. Los mensajes son payloads JSON con tipo de evento y datos. Los nodos de Hedera acuerdan el timestamp y el orden. Cualquiera los lee via la API REST del Mirror Node.

**"Es open source?"**
Si. Licencia MIT. El repo del hackathon esta en github.com/UltravioletaDAO/em-cannes-hackathon. La extension del Facilitator esta en github.com/UltravioletaDAO/x402-rs.

**Si preguntan algo que no saben:**
"Excelente pregunta -- nuestro lider tecnico puede dar seguimiento con los detalles. Dejenme mostrarles lo que tenemos en vivo."

---

## 6. Resumen del Golden Flow

El Golden Flow es nuestro test de aceptacion E2E completo. Ejecuta el ciclo de vida completo de Execution Market en 2 chains.

**Resultado: 7/7 PASS**

| Fase | Operacion | Chain | Resultado |
|------|-----------|-------|-----------|
| 1 | Verificacion de conectividad | Ambas | PASS |
| 2 | Creacion de tarea + lock de escrow | Base Mainnet | PASS |
| 3 | Worker aplica + envia evidencia | Base (API) | PASS |
| 4 | Aprobacion + liberacion de pago | Base Mainnet | PASS |
| 5 | Reputacion bidireccional | Hedera Testnet | PASS |
| 6 | Merit Tip (0.01 HBAR) | Hedera Testnet | PASS |
| 7 | Registro de Eventos HCS (6 mensajes) | Hedera Testnet (nativo) | PASS |

**Evidencia on-chain: 5 TXs + 6 mensajes HCS**

| # | Operacion | Chain | Evidencia |
|---|-----------|-------|-----------|
| 1 | Lock de Escrow | Base | [BaseScan](https://basescan.org/tx/0x98fc338221502fb937cf9fdfe26248a9a0700580ef4b690b6853c58da3efeb84) |
| 2 | Liberacion de Pago | Base | [BaseScan](https://basescan.org/tx/0x29f1aea3cbee79996eab4c632d1982c0578820556fc348bdb5d1a012c502e95a) |
| 3 | Calificacion Agente-a-Worker | Hedera | [HashScan](https://hashscan.io/testnet/transaction/0x26464dbd022d6829e107ca3a52b04720b59c5aa9d7f6a7394a3b50948acdb1c6) |
| 4 | Calificacion Worker-a-Agente | Hedera | [HashScan](https://hashscan.io/testnet/transaction/0x300c402eb1051b8995fee783b23b3b74e68863ad3ac7c958ccccfea30cdd658e) |
| 5 | Merit Tip (0.01 HBAR) | Hedera | [HashScan](https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321) |
| 6 | Log de Eventos HCS (6 msgs) | Hedera (nativo) | [Mirror Node](https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages) |

---

## Referencia Rapida

| Recurso | URL |
|---------|-----|
| Marketplace en produccion | https://execution.market |
| Documentacion Swagger API | https://api.execution.market/docs |
| Mensajes HCS (Mirror Node) | https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages |
| TX Merit Tip | https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321 |
| API Identidad del Agente | https://facilitator.ultravioletadao.xyz/identity/hedera-testnet/99 |
| API Reputacion del Agente | https://facilitator.ultravioletadao.xyz/reputation/hedera-testnet/99 |
| Repo del hackathon | https://github.com/UltravioletaDAO/em-cannes-hackathon |
| Repo del Facilitator | https://github.com/UltravioletaDAO/x402-rs |
| Commit Facilitator (Hedera) | https://github.com/UltravioletaDAO/x402-rs/commit/66d34e6c7f805fa26a33757b2cdf5ec3038ecb95 |
| Contacto | @ExecutionMarket en X |

---

## Puntaje de Auto-Evaluacion: 41/50

Mejoramos iterativamente esta submission usando evaluacion automatizada contra los criterios del track:

| Criterio | Puntaje | Notas |
|----------|:-------:|-------|
| Technicality | **8/10** | ERC-8004 (EVM) + HCS (SDK nativo) + Facilitator (infra Rust). HCS demuestra profundidad no-EVM. |
| Originality | **8/10** | Composabilidad cross-chain: escrow en Base, reputacion + HCS + tips en Hedera. |
| Practicality | **9/10** | Marketplace en produccion en execution.market con pagos USDC reales. |
| Usability | **8/10** | Docs bilingues (EN+ES), scripts ejecutables, TX hashes verificables en explorers. |
| WOW Factor | **8/10** | Golden Flow 7/7 en 2 chains, 5 TXs + 6 mensajes HCS, Facilitator open-source. |
| **TOTAL** | **41/50** | Competitivo para premio de $3K. Mas fuerte en Practicality (sistema en produccion). |

**Trayectoria de mejora**: 36/50 (base) -> 39/50 (+Facilitator, +merit tip) -> 41/50 (+HCS).
