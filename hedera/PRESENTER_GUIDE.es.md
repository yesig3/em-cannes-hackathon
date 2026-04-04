# Hedera Track -- Guia para Presentadores

> Para Yesi y David en el booth de Hedera, ETHGlobal Cannes 2026.
> Lean esto en el celular antes de acercarse al booth.
> **Ver tambien**: [Guia para Jueces](../docs/HEDERA_JUDGES_GUIDE.es.md) para el desglose tecnico completo con todos los links de verificacion.

---

## Que Decir (30 segundos)

"Execution Market es un marketplace en vivo donde agentes de IA publican bounties y humanos las completan por pago instantaneo. Corremos en 9 blockchains en produccion con USDC real. Para este hackathon, agregamos Hedera con cinco integraciones -- incluyendo HCS, Hedera Consensus Service, que es un feature nativo de Hedera que no existe en EVM. Cada evento del ciclo de vida de una tarea se registra como un mensaje inmutable que cualquiera puede verificar."

---

## Que Mostrar (paso a paso)

**Tengan estas pestanas abiertas ANTES de la demo:**

1. Pestana 1: https://execution.market (el marketplace en vivo)
2. Pestana 2: https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321 (TX Merit Tip)
3. Pestana 3: https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages (mensajes HCS)
4. Pestana 4: https://api.execution.market/docs (Swagger API)

**Pasos de la demo:**

1. Mostrar Pestana 1 (dashboard). Decir: "Este es nuestro marketplace en produccion. Los agentes de IA crean tareas, los humanos las completan, y los pagos se hacen automaticamente en USDC."
2. Cambiar a Pestana 2 (TX Merit Tip en HashScan). Decir: "Este es un pago real de HBAR en Hedera testnet. Cuando un worker recibe un puntaje de reputacion alto, el agente le envia 0.01 HBAR como propina automaticamente. Pago gatekeado por reputacion."
3. Cambiar a Pestana 3 (HCS Mirror Node). Decir: "Este es nuestro diferenciador clave -- Hedera Consensus Service. Cada evento del ciclo de vida se registra como un mensaje inmutable con un timestamp de consenso de los nodos de Hedera. Pueden ver 6 eventos: tarea creada, worker aplico, escrow bloqueado, pago liberado, y ambas calificaciones. Cualquiera puede verificar -- no se necesita API key."
4. Decir: "Entonces usamos ERC-8004 para identidad, reputacion on-chain, merit tips en HBAR, y HCS para registro nativo de eventos. Cinco operaciones en Hedera, mas escrow de USDC en Base. Golden Flow: 7 de 7 fases pasan."
5. Si piden mas detalle, cambiar a Pestana 4 (Swagger) y mostrar el endpoint de health. Decir: "Esto esta en vivo -- 9 chains EVM en produccion hoy."

---

## Puntos Clave

- Somos un marketplace EN PRODUCCION, no un prototipo de hackathon. Pagos reales en USDC en 9 chains hoy.
- **HCS (Hedera Consensus Service)** es nuestro diferenciador clave -- es NATIVO de Hedera, no EVM. Usamos `hiero-sdk-python` para registrar cada evento como mensaje inmutable. Timestamps de consenso acordados por nodos de Hedera, no nuestro servidor.
- **Merit Tip**: 0.01 HBAR de transferencia directa cuando workers superan el umbral de reputacion. Operacion financiera real, gatekeada por reputacion on-chain.
- Identidad ERC-8004 y reputacion bidireccional en Hedera testnet. Agente #99 es nuestra identidad de plataforma.
- Extendimos nuestro Facilitator open-source (Rust, 21 blockchains) para soportar Hedera. Agentes nunca necesitan HBAR para gas.
- Workers pueden ser verificados en una chain (como Base) y construir reputacion en otra (como Hedera). Composabilidad cross-chain.
- Golden Flow E2E: **7/7 PASS** -- 5 TXs on-chain + 6 mensajes HCS en 2 chains.

---

## Preguntas que los Jueces Van a Hacer (y respuestas)

**"Por que Hedera especificamente?"**
Finalidad rapida (3-5 segundos), comisiones muy bajas (fracciones de centavo), compatibilidad EVM para nuestros contratos de identidad, Y HCS -- un feature nativo de Hedera para registro inmutable de eventos que no existe en ninguna otra chain.

**"Que es HCS y por que lo usan?"**
Hedera Consensus Service crea un log de eventos inmutable y ordenado con timestamps acordados por los nodos de Hedera. Registramos cada evento del ciclo de vida de una tarea -- creacion, aplicacion, escrow, pago, reputacion. Es una pista de auditoria a prueba de manipulacion que cualquiera puede verificar via la API publica del Mirror Node. Demuestra que usamos Hedera mas alla de EVM generico.

**"Esto corre en Hedera mainnet?"**
Identidad, reputacion y HCS estan en Hedera testnet. Pagos USDC corren en Base mainnet (dinero real). Nuestro codigo soporta mainnet via una sola variable de entorno.

**"Que es ERC-8004?"**
Un registro de identidad on-chain para agentes de IA. Agente #99 es la identidad de nuestra plataforma en Hedera. Desplegado en 16 redes con la misma direccion. Listado por Hedera como tecnologia aceptada ("Trustless Agents").

**"Como son los pagos gasless?"**
Nuestro Facilitator open-source (servidor Rust) paga gas HBAR para todo. Agentes y workers nunca necesitan HBAR.

**"Cuantas chains soportan?"**
9 chains EVM en produccion (Base, Ethereum, Polygon, Arbitrum, Avalanche, Optimism, Celo, Monad, SKALE) mas Solana. Hedera es la mas reciente.

**Si preguntan algo que no saben:**
"Excelente pregunta -- nuestro lider tecnico puede dar seguimiento. Dejenme mostrarles otra cosa."

---

## Que NO Decir

- NO digan "solo tenemos testnet." Digan "identidad, reputacion y HCS estan en Hedera testnet; pagos estan en Base mainnet."
- NO digan "no soportamos Hedera todavia." Digan "Hedera esta en vivo con 5 integraciones -- identidad, reputacion, HBAR tips, HCS, y extension del Facilitator."
- NO intenten explicar EIP-3009 o diferencias de tokens HTS. Solo digan "nuestro sistema de pagos es agnostico a la chain."
- NO prometan fecha de lanzamiento en mainnet. Digan "esta en nuestro roadmap para Q2 2026."

---

## Referencia Rapida

| Recurso | URL |
|---------|-----|
| Produccion | https://execution.market |
| Documentacion API | https://api.execution.market/docs |
| Mensajes HCS | https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages |
| TX Merit Tip | https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321 |
| Identidad Agente | https://facilitator.ultravioletadao.xyz/identity/hedera-testnet/99 |
| Reputacion Agente | https://facilitator.ultravioletadao.xyz/reputation/hedera-testnet/99 |
| GitHub | https://github.com/UltravioletaDAO/em-cannes-hackathon |
| Guia para Jueces | [docs/HEDERA_JUDGES_GUIDE.es.md](../docs/HEDERA_JUDGES_GUIDE.es.md) |
| Contacto | @ExecutionMarket en X |
