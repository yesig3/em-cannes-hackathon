# Hedera Track -- Guia para Presentadores

> Para Yesi y David en el booth de Hedera, ETHGlobal Cannes 2026.
> Lean esto en el celular antes de acercarse al booth.

---

## Que Decir (30 segundos)

"Execution Market es un marketplace en produccion donde agentes de IA publican tareas con recompensas y humanos las completan a cambio de un pago instantaneo. Ya funcionamos en 9 blockchains. Estamos agregando Hedera porque su rapidez y costos bajos lo hacen ideal para pagar a los workers de forma casi inmediata. Tambien desplegamos nuestro sistema de identidad en Hedera testnet."

---

## Que Mostrar (paso a paso)

**Tengan estas pestanas abiertas ANTES de la demo:**

1. Pestana 1: https://execution.market (el marketplace en vivo)
2. Pestana 2: https://api.execution.market/docs (documentacion del API)
3. Pestana 3: https://hashscan.io/testnet (explorador de bloques de Hedera)

**Pasos de la demo:**

1. Mostrar Pestana 1 (dashboard). Decir: "Este es nuestro marketplace en produccion. Los agentes de IA crean tareas, los humanos las completan, y los pagos se hacen automaticamente en USDC."
2. Cambiar a Pestana 2 (Swagger). Ir al endpoint de Health. Decir: "Esto esta en vivo -- 9 chains EVM mas Solana hoy."
3. Cambiar a Pestana 3 (HashScan). Mostrar el contrato de identidad ERC-8004 en Hedera testnet: `0x8004A818BFB912233c491871b3d84c89A494BD9e`. Decir: "Desplegamos nuestro registro de identidad en Hedera testnet. Agente 2106 -- el mismo agente, ahora visible en Hedera."
4. Decir: "Hedera finaliza en 3-5 segundos y cuesta fracciones de centavo. Eso significa que los workers reciben su pago mas rapido y mas barato que en Ethereum."
5. Si tienen el demo script corriendo, mostrar la salida en terminal: creacion de cuenta, transferencia de HBAR, transaccion confirmada en HashScan. Decir: "Este es un pago en vivo en Hedera testnet."

---

## Puntos Clave

- Somos un marketplace EN PRODUCCION, no un prototipo de hackathon. Pagos reales en USDC en 9 chains hoy.
- La finalidad de 3-5 segundos de Hedera significa que los workers reciben su pago casi instantaneamente. Las comisiones son casi cero.
- Nuestra identidad de agente (ERC-8004) ya esta desplegada en Hedera testnet. Mismos contratos, mismo agente, mas chains.
- Usamos el protocolo x402 para pagos sin gas. El agente firma, nuestra infraestructura paga todo el gas. Los workers nunca necesitan tener HBAR para gas.
- Hedera es la chain numero 10 para nosotros. Nuestra arquitectura es agnostica a la chain -- agregar una nueva es directo.
- Los workers pueden ser verificados en una chain (como Base) y recibir pago en otra (como Hedera). La reputacion viaja entre chains.

---

## Preguntas que los Jueces Van a Hacer (y respuestas)

**"Por que Hedera especificamente?"**
Finalidad rapida (3-5 segundos vs 12+ en Ethereum), comisiones muy bajas (fracciones de centavo), y compatibilidad EVM para que nuestros contratos existentes se desplieguen directamente.

**"Esto corre en Hedera mainnet?"**
Los contratos de identidad estan en Hedera testnet. El demo de pagos es en testnet. Nuestro marketplace en produccion corre en 9 mainnets EVM hoy -- Hedera mainnet es el siguiente paso.

**"Como funciona x402 en Hedera?"**
Hoy x402 usa EIP-3009 (un estandar de pago sin gas) que no existe nativamente en Hedera todavia. Por ahora usamos el SDK de Hedera directamente para pagos. La arquitectura esta disenada para agregar un adaptador para el servicio nativo de tokens de Hedera.

**"Que es ERC-8004?"**
Es un registro de identidad on-chain para agentes de IA. Piensen en ello como un pasaporte -- Agente 2106 es la identidad de nuestra plataforma. Esta desplegado en 16 redes con la misma direccion, incluyendo Hedera testnet ahora.

**"Cuantas chains soportan?"**
9 chains EVM en produccion (Base, Ethereum, Polygon, Arbitrum, Avalanche, Optimism, Celo, Monad, SKALE) mas Solana. Hedera se esta agregando ahora.

**Si preguntan algo que no saben:**
"Excelente pregunta -- nuestro lider tecnico puede darles mas detalle sobre eso. Dejenme mostrarles otra cosa."

---

## Que NO Decir

- NO digan "solo tenemos testnet." Digan "la identidad esta desplegada en Hedera testnet, la integracion a produccion esta en progreso."
- NO digan "no soportamos Hedera todavia." Digan "ya soportamos 9 chains y Hedera se esta agregando ahora."
- NO intenten explicar EIP-3009 o diferencias de tokens HTS. Solo digan "nuestro sistema de pagos es agnostico a la chain."
- NO prometan fecha de lanzamiento en mainnet. Digan "esta en nuestro roadmap para Q2 2026."

---

## Referencia Rapida

- Produccion: https://execution.market
- Documentacion del API: https://api.execution.market/docs
- Explorador Hedera: https://hashscan.io/testnet
- GitHub: https://github.com/UltravioletaDAO/em-cannes-hackathon
- Contacto: @ExecutionMarket en X
