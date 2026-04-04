# Hedera Track -- Guia para Presentadores

> Para Yesi y David en el booth de Hedera, ETHGlobal Cannes 2026.
> Lean esto en el celular antes de acercarse al booth.
> **Detalles tecnicos completos**: [Guia para Jueces](JUDGES_GUIDE.es.md)

---

## Que Decir (30 segundos)

"Execution Market es un marketplace en vivo donde agentes de IA publican bounties y humanos las completan por pago instantaneo. 9 blockchains en produccion con USDC real. Para este hackathon, agregamos Hedera con cinco integraciones -- incluyendo HCS, un feature nativo de Hedera que no existe en EVM. Cada evento se registra como mensaje inmutable que cualquiera puede verificar."

---

## Que Mostrar

**Abrir estas pestanas ANTES de la demo:**

1. https://execution.market (marketplace en vivo)
2. https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321 (TX Merit Tip)
3. https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages (mensajes HCS)
4. https://api.execution.market/docs (Swagger API)

**Pasos:**

1. **Pestana 1** (dashboard): "Marketplace en produccion. Agentes IA crean tareas, humanos las completan, pagos automaticos en USDC."
2. **Pestana 2** (TX Merit Tip): "Pago real de HBAR en Hedera testnet. Worker recibe 0.01 HBAR automaticamente cuando tiene buen puntaje de reputacion."
3. **Pestana 3** (HCS Mirror Node): "Diferenciador clave -- Hedera Consensus Service. Cada evento registrado como mensaje inmutable con timestamp de consenso. 6 eventos: tarea creada, worker aplico, escrow bloqueado, pago liberado, ambas calificaciones. Cualquiera verifica, sin API key."
4. **Cierre**: "Identidad ERC-8004, reputacion on-chain, merit tips HBAR, registro HCS nativo. 5 operaciones Hedera + escrow USDC en Base. Golden Flow 7/7."
5. Si piden mas: Pestana 4 (Swagger), mostrar health endpoint. "En vivo -- 9 chains EVM en produccion."

---

## Puntos Clave

- Marketplace EN PRODUCCION, no un prototipo. USDC real en 9 chains.
- **HCS** es NATIVO de Hedera, no EVM. `hiero-sdk-python` para registro inmutable. Timestamps de consenso de nodos Hedera.
- **Merit Tip**: 0.01 HBAR cuando workers superan umbral de reputacion.
- Identidad ERC-8004 + reputacion bidireccional en Hedera testnet. Agente #99.
- Facilitator open-source (Rust, 21 blockchains) extendido para Hedera. Agentes nunca necesitan HBAR.
- Composabilidad cross-chain: verificado en Base, pagado en Hedera, reputacion compartida.
- Golden Flow: **7/7 PASS** -- 5 TXs + 6 mensajes HCS en 2 chains.

---

## Preguntas Esperadas

**"Por que Hedera?"** -- Finalidad rapida (3-5s), fees bajos, compatibilidad EVM para identidad, Y HCS para registro inmutable nativo.

**"Que es HCS?"** -- Log de eventos inmutable y ordenado con timestamps de consenso. Audit trail a prueba de manipulacion. Verificable via API publica del Mirror Node. Demuestra uso de Hedera mas alla de EVM.

**"Mainnet?"** -- Identidad/reputacion/HCS en Hedera testnet. USDC en Base mainnet. Una variable de entorno cambia a mainnet.

**"Que es ERC-8004?"** -- Identidad on-chain para agentes IA. Agente #99 en Hedera. 16 redes, misma direccion. Listado por Hedera como tech aceptada.

**"Gasless?"** -- Facilitator (Rust) paga gas HBAR. Mismo modelo en 9 chains de produccion.

**"Cuantas chains?"** -- 9 EVM + Solana en produccion. Hedera es la mas reciente.

**Si no saben:** "Excelente pregunta -- nuestro lider tecnico puede dar seguimiento. Dejenme mostrarles otra cosa."

---

## Que NO Decir

- NO "solo testnet" --> "identidad/reputacion/HCS en Hedera testnet; pagos en Base mainnet"
- NO "no soportamos Hedera" --> "Hedera en vivo con 5 integraciones"
- NO explicar EIP-3009 ni diferencias HTS. Decir "sistema de pagos agnostico a la chain"
- NO prometer fecha de mainnet. Decir "en nuestro roadmap para Q2 2026"

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
| Guia para Jueces | [JUDGES_GUIDE.es.md](JUDGES_GUIDE.es.md) |
| Contacto | @ExecutionMarket en X |
