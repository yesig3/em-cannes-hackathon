# Integracion World — Guia para Jueces

> **Partner**: World ($20K) | **Tracks**: AgentKit ($8K) + World ID 4.0 ($8K)
> **Produccion**: [execution.market](https://execution.market) | **API**: [api.execution.market/docs](https://api.execution.market/docs)

---

## Que Construimos (pitch de 30 segundos)

Execution Market es un **marketplace en produccion** donde agentes de IA publican recompensas por tareas del mundo real y humanos verificados las ejecutan. Integramos **World AgentKit** y **World ID 4.0** para resolver el problema critico: **como evitar que los bots roben recompensas destinadas a humanos reales?**

```
Sin World ID:            Con World ID:

Bot crea cuenta          Bot crea cuenta
Bot aplica a tarea       Bot aplica a tarea
Bot falsifica evidencia  Gate de World ID: "Demuestra que eres humano"
Bot recibe $10           Bot no puede → BLOQUEADO
Agente pierde plata      Solo humanos verificados reciben pago
```

---

## Track 1: AgentKit — Verificacion Humana On-Chain

### Que Hace

Usamos el contrato **AgentBook** (desplegado en Base por World) para verificar si la wallet de un worker pertenece a un humano real y verificado. Es una **consulta on-chain gratuita, de solo lectura** — sin gas, sin transaccion, instantanea.

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
                    │  SI  → Verificado    │
                    │  NO  → No verificado │
                    └─────────────────────┘
```

### Como Se Integra con Execution Market

1. Un worker aplica a una tarea
2. El backend llama a `lookupHuman(worker_wallet)` en Base via JSON-RPC
3. Si `humanId > 0`: el worker recibe una **insignia de "Humano Verificado"** en su perfil
4. La insignia es visible para agentes de IA que revisan solicitudes — genera confianza

### Gateway x402 (Humanos Gratis, Bots Pagan)

Construimos un **servidor Hono** usando el SDK `@worldcoin/agentkit` que controla el acceso a la API:

```
┌─────────────┐     ┌──────────────────┐     ┌───────────────┐
│  API Client  │────>│  x402 Gateway    │────>│  EM API       │
│              │     │  (port 4021)     │     │               │
│  Humano? ───│─SI──│─> Acceso gratis  │     │  /tasks       │
│  Bot? ──────│─NO──│─> Paga $0.001/req│     │  /workers     │
└─────────────┘     └──────────────────┘     └───────────────┘
```

### Archivos Clave

| Archivo | Proposito |
|---------|-----------|
| `world/agentkit/agentbook.py` | Consulta on-chain (Python, standalone, cero imports de EM) |
| `world/agentkit/gateway-server.ts` | Gateway x402+AgentKit (TypeScript, Hono) |
| `world/agentkit/WorldHumanBadge.tsx` | Componente React de insignia |
| `world/migrations/003_world_agentkit.sql` | Esquema DB para almacenamiento de humanId |

### Comandos para Demo en Vivo

```bash
# 1. Verificar una wallet no verificada
curl -s "https://api.execution.market/api/v1/workers/world-status?wallet=0x0000000000000000000000000000000000000000" | python -m json.tool
# → { "is_human": false, "human_id": 0 }

# 2. Verificar on-chain directamente (Foundry)
cast call 0xE1D1D3526A6FAa37eb36bD10B933C1b77f4561a4 \
  "lookupHuman(address)(uint256)" \
  0x0000000000000000000000000000000000000000 \
  --rpc-url https://mainnet.base.org
# → 0

# 3. Ejecutar el gateway
cd world/agentkit && npm install && npx tsx gateway-server.ts
# → Listening on http://localhost:4021
```

---

## Track 2: World ID 4.0 — Prueba de Humanidad ZK

### Que Hace

World ID 4.0 proporciona **prueba de humanidad de conocimiento cero (zero-knowledge)**. Un worker demuestra que es un humano unico sin revelar su identidad. El sistema garantiza:

- **Un humano = una cuenta** (unicidad del nullifier)
- **Tareas >= $5 requieren verificacion Orb** (prueba a nivel biometrico)
- **Sin World ID = sin acceso a tareas de alto valor** (el producto literalmente DEJA DE FUNCIONAR)

### El Flujo

```
┌──────────┐    ┌───────────┐    ┌────────────┐    ┌──────────────┐
│  Worker   │    │ Dashboard │    │  Backend   │    │ Cloud API v4 │
│ (Browser) │    │  (React)  │    │ (FastAPI)  │    │  (World)     │
└────┬─────┘    └─────┬─────┘    └─────┬──────┘    └──────┬───────┘
     │                │                │                   │
     │ Clic Verificar │                │                   │
     │───────────────>│                │                   │
     │                │ GET /rp-sig    │                   │
     │                │───────────────>│                   │
     │                │                │ Genera nonce      │
     │                │                │ Firma (secp256k1) │
     │                │<───────────────│                   │
     │                │ {nonce, sig}   │                   │
     │  Abre IDKit    │                │                   │
     │<───────────────│                │                   │
     │                │                │                   │
     │ Escanea QR con │                │                   │
     │ World App      │                │                   │
     │                │                │                   │
     │ Prueba ZK lista│                │                   │
     │───────────────>│                │                   │
     │                │ POST /verify   │                   │
     │                │ {responses[]}  │                   │
     │                │───────────────>│                   │
     │                │                │ POST /v4/verify   │
     │                │                │──────────────────>│
     │                │                │<──────────────────│
     │                │                │ {success: true}   │
     │                │                │                   │
     │                │                │ Almacena nullifier│
     │                │                │ (constraint UNIQUE)│
     │                │                │ Actualiza executor│
     │                │<───────────────│                   │
     │  Aparece insignia               │                   │
     │<───────────────│                │                   │
```

### Anti-Sybil: Como Funciona el Nullifier

```
Persona "Juan" verifica Cuenta A:
  nullifier = f(Juan, app_id, action) = 0xabc123...
  → INSERT INTO world_id_verifications (nullifier = 0xabc123...)
  → EXITOSO

Persona "Juan" intenta verificar Cuenta B:
  nullifier = f(Juan, app_id, action) = 0xabc123...  (EL MISMO!)
  → INSERT INTO world_id_verifications (nullifier = 0xabc123...)
  → VIOLACION DE CONSTRAINT UNIQUE → HTTP 409 "Ya fue usado"
  → BLOQUEADO
```

El nullifier es **deterministico**: misma persona + misma app = mismo nullifier. Siempre. Esto se garantiza a nivel de base de datos con `UNIQUE (nullifier_hash)`.

### Enforcement: Tareas >= $5 Requieren Orb

```
Worker aplica a tarea de $8:
  │
  ├── world_id_verified? ──── NO ──→ HTTP 403
  │                                   "world_id_orb_required"
  │                                   "Tareas >= $5 requieren verificacion Orb"
  │
  └── SI ──→ world_id_level == "orb"?
                │
                ├── NO (solo device) ──→ HTTP 403
                │
                └── SI ──→ Solicitud aceptada
```

### Archivos Clave

| Archivo | Proposito |
|---------|-----------|
| `world/worldid/client.py` | Firma RP (secp256k1) + verificacion Cloud API v4 (standalone) |
| `world/worldid/router.py` | Endpoints FastAPI: GET /rp-signature, POST /verify |
| `world/worldid/WorldIdVerification.tsx` | Widget IDKit v4 (React, basado en props) |
| `world/migrations/001_world_id_verification.sql` | DB: tabla de verificaciones + constraints anti-sybil |
| `world/migrations/002_world_id_rls.sql` | Politicas de Row-Level Security |

### Comandos para Demo en Vivo

```bash
# 1. Obtener firma RP (demuestra que la criptografia del backend funciona)
curl -s "https://api.execution.market/api/v1/world-id/rp-signature?action=verify-worker" | python -m json.tool
# → { nonce: "00abc...", signature: "def123...", rp_id: "...", app_id: "app_..." }

# 2. Flujo de verificacion completo: abrir https://execution.market/profile
#    → Clic en "Verificar con World ID"
#    → Escanear QR con World App
#    → La insignia aparece en el perfil

# 3. Prueba anti-sybil: desconectar wallet, conectar otra wallet
#    → Intentar verificar con el mismo World ID
#    → HTTP 409: "Este World ID ya fue usado"

# 4. Prueba de enforcement: crear tarea de $5+, aplicar sin Orb
#    → HTTP 403: "world_id_orb_required"
```

---

## Detalles Criptograficos (para jueces tecnicos)

### Firma RP (especificacion v4)

```
message = 0x01                          // byte de version
        || nonce[32]                    // aleatorio, hasheado al campo BN254
        || created_at[8]               // uint64 big-endian (segundos)
        || expires_at[8]               // created_at + 300 (TTL de 5 min)
        || keccak256(action)[32]        // hash de la accion
        = 81 bytes en total

msg_hash = keccak256(EIP-191_prefix || message)

signature = secp256k1_sign_recoverable(msg_hash, signing_key)
          = 65 bytes (r[32] + s[32] + v[1])
```

### Payload Cloud API v4

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

### Esquema de Base de Datos

```sql
-- Nucleo anti-sybil
CREATE TABLE world_id_verifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  executor_id UUID REFERENCES executors(id) ON DELETE CASCADE,
  nullifier_hash TEXT NOT NULL,
  merkle_root TEXT,
  proof TEXT,
  verification_level TEXT CHECK (verification_level IN ('orb', 'device')),
  verified_at TIMESTAMPTZ DEFAULT NOW(),

  CONSTRAINT uq_world_id_nullifier UNIQUE (nullifier_hash),  -- un humano = una cuenta
  CONSTRAINT uq_world_id_executor UNIQUE (executor_id)        -- un executor = una verificacion
);

ALTER TABLE world_id_verifications ENABLE ROW LEVEL SECURITY;
```

---

## Donde Buscar (Referencia Rapida para Jueces)

| Que | Donde |
|-----|-------|
| **Dashboard en vivo** | https://execution.market |
| **Docs de API (Swagger)** | https://api.execution.market/docs |
| **Contrato AgentBook** | [0xE1D1...a4 en Basescan](https://basescan.org/address/0xE1D1D3526A6FAa37eb36bD10B933C1b77f4561a4) |
| **ERC-8004 Agent #2106** | [0x8004...32 en Basescan](https://basescan.org/address/0x8004A169FB4a3325136EB29fA0ceB6D2e539a432) |
| **Endpoints de World ID** | GET `/api/v1/world-id/rp-signature` + POST `/api/v1/world-id/verify` |
| **Endpoint de AgentBook** | GET `/api/v1/workers/world-status?wallet=0x...` |
| **Codigo fuente** | Este repo: carpeta `world/` |
| **Fuente en produccion** | [github.com/UltravioletaDAO/execution-market](https://github.com/UltravioletaDAO/execution-market) |

---

## Preguntas Frecuentes

### General

**P: Esto esta realmente en produccion?**
R: Si. Execution Market esta en vivo en [execution.market](https://execution.market) con pagos reales en USDC en 9 cadenas EVM + Solana. El Agent #2106 esta registrado en el Base ERC-8004 Identity Registry. Los workers estan completando tareas reales hoy.

**P: Que hace Execution Market sin World ID?**
R: Funciona — pero es vulnerable. Cualquier bot puede registrarse como worker, enviar evidencia falsa generada por IA y robar recompensas. World ID cierra este vector de ataque por completo.

**P: En que se diferencia de solo verificar la antiguedad o saldo de la wallet?**
R: La antiguedad y el saldo de una wallet son trivialmente falsificables (crear 100 wallets, fondear desde un mixer). World ID usa verificacion biometrica (escaneo de iris) para vincular un humano fisico a una identidad criptografica. El mecanismo de nullifier hace que las multicuentas sean matematicamente imposibles.

### Track 1 (AgentKit)

**P: La verificacion de AgentBook bloquea a los workers?**
R: No, es no-bloqueante. Los workers pueden aplicar sin verificacion de AgentBook. La insignia es informativa — ayuda a los agentes de IA a priorizar humanos verificados al revisar solicitudes.

**P: Por que usar x402 para el gateway?**
R: x402 es el protocolo de pago que ya usamos para liquidaciones de tareas. El gateway lo extiende: los humanos verificados obtienen acceso gratuito a la API (ya demostraron su humanidad), los bots deben pagar por peticion. Esto alinea incentivos — estar verificado tiene un valor tangible.

**P: Que pasa si el contrato AgentBook esta caido?**
R: La llamada RPC tiene un timeout de 15 segundos. Si falla, la solicitud del worker procede normalmente sin la insignia. La verificacion es best-effort, nunca bloqueante.

### Track 2 (World ID 4.0)

**P: Que pasa si World ID esta caido?**
R: La firma RP es local (nuestro backend, usando coincurve). La unica dependencia externa es Cloud API v4 para verificacion de pruebas. Si esta caido, los workers aun pueden usar la plataforma para tareas menores a $5 (no se requiere Orb). Las tareas de alto valor se bloquean hasta que Cloud API se recupere — esto es por diseno (seguridad > disponibilidad para operaciones financieras).

**P: Los workers pueden evadir el requisito de Orb para $5?**
R: No. El enforcement es del lado del servidor en `apply_to_task()`. El frontend muestra un gate, pero incluso si se evade via llamadas directas a la API, el backend retorna HTTP 403. El umbral es configurable via la API de admin sin redespliegue.

**P: Que pasa si alguien pierde acceso a su World ID?**
R: El nullifier es deterministico. Si se re-verifican con el mismo World ID (incluso desde un dispositivo nuevo), obtienen el mismo nullifier, que se mapea a su cuenta existente. Si necesitan migrar a una nueva wallet, un admin puede eliminar manualmente el registro de verificacion anterior.

**P: Como se conecta esto con ERC-8004?**
R: Cuando un worker se verifica con World ID, disparamos una actualizacion asincrona (fire-and-forget) a sus metadatos de agente ERC-8004 (via Facilitator). Esto significa que su estado de verificacion de World ID es consultable on-chain por otros protocolos — no esta encerrado dentro de nuestra base de datos.

**P: El umbral de $5 es arbitrario?**
R: Es configurable. Elegimos $5 porque: (a) las tareas menores a $5 tienen bajo incentivo sybil (no vale la pena falsificar), (b) la verificacion Orb requiere presencia fisica en un dispositivo Orb, lo cual es un punto de friccion. $5 balancea seguridad con accesibilidad. Los agentes podran solicitar umbrales mas altos por tarea en el futuro.

### Tecnico

**P: Por que secp256k1 para la firma RP en vez de Ed25519?**
R: La especificacion v4 de World ID requiere secp256k1 con hashing de mensajes EIP-191. Esto se alinea con el esquema de firmas nativo de Ethereum, haciendo la verificacion interoperable con contratos on-chain.

**P: Por que almacenar la prueba en la base de datos?**
R: Para trazabilidad. El hash del nullifier es suficiente para anti-sybil, pero almacenar la prueba completa permite re-verificacion futura si World actualiza su logica de verificacion, y proporciona evidencia en la resolucion de disputas.

**P: Cual es la diferencia entre verificacion Orb y Device?**
R: Orb = escaneo biometrico de iris (mayor nivel de seguridad, requiere dispositivo Orb fisico). Device = verificacion basada en telefono (menor nivel de seguridad, mas facil de falsificar). Nuestro enforcement requiere Orb para operaciones financieras ($5+) porque la verificacion a nivel de device se puede evadir con multiples telefonos.

---

## Script del Demo (para Yesi/David en el Booth de World)

### Preparacion (antes del demo)
- Abrir https://execution.market en el navegador (logueado con wallet de prueba)
- Abrir https://api.execution.market/docs en segunda pestana
- Tener World App lista en el telefono
- Terminal abierta con comandos `curl` listos

### Flujo del Demo (4 minutos)

**0:00-0:30 — El Problema**
"Esto es Execution Market — un marketplace en vivo donde agentes de IA publican recompensas por tareas del mundo real. El problema: como evitar que los bots roben recompensas destinadas a humanos reales?"

**0:30-1:30 — Track 1: AgentKit**
- Mostrar consulta a AgentBook en Swagger: GET `/workers/world-status?wallet=0x000...` → `is_human: false`
- "Llamamos al contrato AgentBook en Base — gratis, instantaneo, sin gas"
- Mostrar la insignia en la tarjeta de perfil de un worker verificado: "Humano Verificado #42"

**1:30-3:00 — Track 2: World ID 4.0**
- Clic en "Verificar con World ID" en la pagina de perfil
- Mostrar el widget IDKit abriendose
- Escanear QR con World App (demo en vivo)
- Mostrar la insignia apareciendo despues de la verificacion
- "Esto es anti-sybil — la misma persona intentando verificar una segunda cuenta recibe HTTP 409"
- Mostrar el `enforcement de $5+`: "Sin Orb, literalmente no puedes aplicar a tareas de alto valor"

**3:00-3:30 — Produccion**
- "Esto no es un prototipo de hackathon. Esta corriendo en produccion con pagos reales en USDC."
- Mostrar los docs de Swagger, el endpoint de health, la agent card

**3:30-4:00 — Cierre**
- "World ID + ERC-8004 = verificacion humana trustless para marketplaces de IA-a-humano"
- "El producto deja de funcionar sin World ID. Eso es por diseno."

### Preparacion para Preguntas
- "Cuantos usuarios?" → En produccion con workers activos. Agent #2106 en Base.
- "Que cadenas?" → 9 EVM + Solana. Pagos via protocolo x402.
- "Open source?" → Si, licencia MIT. github.com/UltravioletaDAO/execution-market
