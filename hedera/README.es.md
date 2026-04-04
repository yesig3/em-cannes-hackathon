# Integracion Hedera — Pagos Agentivos con IA

> **Socio**: Hedera ($15K) | **Track**: AI & Agentic Payments
> **Produccion**: [execution.market](https://execution.market) | **Agente**: #2106 en Base ERC-8004

---

## Que Estamos Construyendo (pitch de 30 segundos)

Execution Market ya ejecuta **pagos de IA a humanos en 9 cadenas EVM** via protocolo x402. Estamos extendiendolo a **Hedera** con:

1. **Identidad ERC-8004 en Hedera** — Agente #2106 registrado en Hedera (compatible con EVM, gasless via Facilitator)
2. **Pagos Agentivos en Hedera Testnet** — Transferencias reales de tokens usando Hedera SDK
3. **Arquitectura Cross-Chain** — Mostramos como el escrow x402 se extiende al estandar de tokens HTS de Hedera

```
HOY (9 cadenas EVM + Solana):

  Agente IA ──→ x402 Escrow ──→ Trabajador recibe pago (USDC, gasless)
       │
       └── Identidad ERC-8004 en 16 redes

AGREGANDO HEDERA:

  Agente IA ──→ Hedera SDK ──→ Trabajador recibe pago (HBAR/USDC)
       │
       └── Identidad ERC-8004 en Hedera (testnet activo)
```

---

## Por Que Hedera + Execution Market

El premio de Hedera pide explicitamente:

| Requisito | Como Lo Cumplimos |
|-----------|-------------------|
| "Ejecutar al menos un pago en Hedera Testnet" | Demo de pago con Hedera SDK (transferencia HBAR) |
| "Usar Hedera Agent Kit, x402, o Hedera SDKs" | Hedera SDK directamente + explicacion de arquitectura x402 |
| "Bonus: implementacion x402" | x402 corre en 9 cadenas hoy; documento de arquitectura muestra extension a Hedera |
| "Bonus: identidad de agente ERC-8004" | Agente #2106 en 16 redes; contratos en Hedera testnet desplegados |

### Que Lo Hace Unico

Execution Market es el **unico marketplace en produccion** donde agentes de IA pagan a humanos por tareas del mundo real. Agregar Hedera significa:

- **Los agentes pueden pagar trabajadores en HBAR** (finalidad rapida, comisiones bajas)
- **Identidad del agente portable a Hedera** (registro ERC-8004 ya desplegado)
- **Reputacion cross-chain** — trabajador verificado en Base, pagado en Hedera, reputacion compartida

---

## Arquitectura

### Flujo de Pago Actual (9 Cadenas EVM)

```
┌─────────────┐     ┌───────────────┐     ┌──────────────┐
│  Agente IA   │     │ x402 Escrow   │     │  Trabajador  │
│ (publicador) │     │ (on-chain)    │     │  (ejecutor)  │
└──────┬──────┘     └───────┬───────┘     └──────┬───────┘
       │                    │                     │
       │ 1. Firma EIP-3009 │                     │
       │───────────────────>│                     │
       │    (pre-auth)      │                     │
       │                    │                     │
       │ 2. Bloquea escrow  │                     │
       │   (al asignar)     │                     │
       │                    │                     │
       │                    │  3. Libera al        │
       │                    │     trabajador (87%) │
       │                    │────────────────────>│
       │                    │                     │
       │                    │  4. Comision a       │
       │                    │     tesoreria (13%)  │
       │                    │                     │
       │ GASLESS — Facilitator paga todo el gas   │
```

### Extension a Hedera (Nuevo)

```
┌─────────────┐     ┌───────────────┐     ┌──────────────┐
│  Agente IA   │     │ Hedera SDK    │     │  Trabajador  │
│ (publicador) │     │ (HTS nativo)  │     │  (ejecutor)  │
└──────┬──────┘     └───────┬───────┘     └──────┬───────┘
       │                    │                     │
       │ 1. Crea transferencia                    │
       │───────────────────>│                     │
       │  (HBAR o USDC)     │                     │
       │                    │                     │
       │ 2. Ejecuta TX      │                     │
       │   (Hedera testnet) │                     │
       │                    │  3. Trabajador recibe│
       │                    │────────────────────>│
       │                    │                     │
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
│  ...                                             │
│                                                  │
│  Contratos en testnet:                           │
│  Identidad: 0x8004A818BFB912233c491871b3d84c89A4│
│  Reputacion: 0x8004B663056A597Dffe9eCcC1965A193B│
└──────────────────────────────────────────────────┘
```

---

## Detalles Tecnicos

### Por Que No x402 Directamente en Hedera?

USDC en Hedera es un **token nativo HTS (Hedera Token Service)**, no un ERC-20. Diferencia clave:

| Caracteristica | Cadenas EVM (ERC-20) | Hedera (HTS) |
|----------------|----------------------|--------------|
| `transferWithAuthorization()` (EIP-3009) | SI | NO |
| `permit()` (EIP-2612) | SI | NO |
| `DOMAIN_SEPARATOR` | SI | NO |
| Pre-auth gasless | SI (x402 usa esto) | NO |

**x402 depende de EIP-3009** para transferencias pre-autorizadas sin gas. HTS no soporta esto. Entonces para Hedera, usamos el **SDK nativo de Hedera** para pagos y mostramos la arquitectura de como funcionaria un futuro adaptador x402-HTS.

### Configuracion de Hedera Testnet

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

### Archivos a Construir

```
hedera/
├── README.md              # Guia especifica de Hedera para jueces
├── payment.py             # Hedera SDK: crear cuenta, transferir HBAR/USDC
├── identity.py            # Consulta de identidad ERC-8004 en Hedera
├── demo.py                # End-to-end: cuenta → fondear → transferir → verificar
├── requirements.txt       # hedera-sdk, python-dotenv, web3
└── tests/
    └── test_payment.py    # Mock de Hedera RPC, test del flujo de transferencia
```

### Flujo del Demo (lo que ejecutan los jueces)

```bash
cd hedera
pip install -r requirements.txt

# Demo end-to-end
python demo.py
# Output:
#   1. Created testnet account: 0.0.12345
#   2. Funded from faucet: 100 HBAR
#   3. Transferred 1 HBAR to worker: TX 0x...
#   4. Verified on HashScan: https://hashscan.io/testnet/transaction/0x...
#   5. ERC-8004 identity check: Agent #2106 found on Hedera testnet
```

---

## Que Debe Presentar el Equipo en Cannes

### Puntos Clave para el Stand de Hedera

1. **"Somos un marketplace en produccion — 9 cadenas hoy, extendiendose a Hedera"**
   - Mostrar execution.market en produccion
   - Apuntar a los docs de Swagger en api.execution.market/docs
   - "Pagos reales en USDC, tareas reales, trabajadores reales"

2. **"La identidad de agente ERC-8004 ya esta en Hedera testnet"**
   - Contratos desplegados: `0x8004A818...` (identidad), `0x8004B663...` (reputacion)
   - Identidad del Agente #2106 portable entre cadenas
   - "Mismo agente, registrado en Base, Ethereum, Polygon... y ahora Hedera"

3. **"La finalidad rapida de Hedera es perfecta para pagos de tareas"**
   - 3-5 segundos de finalidad vs 12+ segundos en Ethereum
   - Comisiones bajas ($0.0001 por transferencia)
   - "Los trabajadores reciben su pago mas rapido en Hedera"

4. **"La arquitectura x402 se extiende a Hedera con un adaptador HTS"**
   - Mostrar el diagrama de arquitectura
   - "Hoy: EIP-3009 en EVM. Manana: pre-auth nativo de HTS en Hedera"
   - "El Facilitator ya soporta 19 blockchains — Hedera se esta agregando ahora"

5. **"World ID + ERC-8004 + Hedera = humanos verificados pagados al instante"**
   - Cruzar con el track de World
   - "Trabajador verificado por World ID en Base, pagado en HBAR en Hedera, reputacion compartida on-chain"

### Preguntas Esperadas

**P: Por que no usar x402 directamente en Hedera?**
R: Los tokens HTS no soportan EIP-3009 (pre-auth gasless). Usamos el SDK nativo de Hedera por ahora y estamos disenando un adaptador nativo de HTS para x402. La arquitectura es agnostica a la cadena — al marketplace no le importa cual cadena liquida.

**P: ERC-8004 esta realmente desplegado en Hedera?**
R: Si, en testnet. El registro usa CREATE2 para direcciones deterministicas entre cadenas. Identidad: `0x8004A818...`, Reputacion: `0x8004B663...`. Lo estamos agregando al Facilitator ahora.

**P: Que es el Facilitator?**
R: Nuestro relay de transacciones gasless. Los agentes firman autorizaciones, el Facilitator ejecuta on-chain. Ya soporta 19 blockchains — agregar Hedera es una extension, no una reconstruccion. URL: `facilitator.ultravioletadao.xyz`

**P: Como funciona la identidad cross-chain?**
R: ERC-8004 esta desplegado en 16+ redes con la misma direccion de contrato (CREATE2). El Agente #2106 es la misma entidad en Base, Ethereum, Polygon, y ahora Hedera. Los puntajes de reputacion son especificos por cadena pero consultables cross-chain via el Facilitator.

**P: Cual es la linea de tiempo para soporte de Hedera en produccion?**
R: Identidad ERC-8004: dias (actualizacion del Facilitator). Pagos: depende del diseno del adaptador HTS. Estamos apuntando a Q2 2026 para pagos en produccion en Hedera.

---

## Estado de Implementacion

| Componente | Estado | ETA |
|------------|--------|-----|
| Contratos ERC-8004 en Hedera testnet | DESPLEGADO | Listo |
| Soporte de Hedera en Facilitator | EN PROGRESO | Horas |
| Demo de pago con Hedera SDK | POR HACER | 2-3 horas |
| Consulta de identidad ERC-8004 | POR HACER | 1 hora |
| Script de demo end-to-end | POR HACER | 1 hora |
| Tests | POR HACER | 1 hora |
| Documentacion | ESTE ARCHIVO | Listo |

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

## Documentacion Relacionada

- [Guia de Integracion World](./WORLD_JUDGES_GUIDE.md) — Detalles de World ID + AgentKit
- [Plan de Integracion ENS](./ENS_INTEGRATION.md) — Nombres ENS para agentes de IA
- [Docs de la API en Produccion](https://api.execution.market/docs) — Swagger UI completo
- [Codigo Fuente de Execution Market](https://github.com/UltravioletaDAO/execution-market) — Open source
