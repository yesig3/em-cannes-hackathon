# World Track -- Guia para Presentadores

> Para Yesi y David en el booth de World / Worldcoin, ETHGlobal Cannes 2026.
> Lean esto en el celular antes de acercarse al booth.

---

## Tracks a los que Aplicamos (World — $20,000 total)

| Track | Premio | Requisito | Nuestras Features |
|-------|-------:|-----------|-------------------|
| **Best Use of AgentKit** | $8K (1ro $4K, 2do $2.5K, 3ro $1.5K) | "Apps que usan AgentKit para distinguir agentes respaldados por humanos de bots" | AgentBook verificacion humana on-chain, gateway x402 (humanos gratis, bots pagan) |
| **Best Use of World ID 4.0** | $8K (1ro $4K, 2do $2.5K, 3ro $1.5K) | "Productos que se rompen sin prueba de humanidad. Restriccion real, no cosmetica." | RP signing (secp256k1), Cloud API v4, anti-sybil (nullifier UNIQUE), enforcement Orb $5+ |

**Mensaje clave**: Este producto SE ROMPE sin World ID. Sin el, los bots roban bounties. No es cosmetico -- es estructural.

---

## Que Decir (30 segundos)

"Execution Market es un marketplace en produccion donde agentes de IA publican tareas con recompensas y humanos reales las completan a cambio de un pago. Integramos World ID para que solo humanos verificados -- no bots -- puedan reclamar las recompensas. Si no estas verificado, literalmente no puedes acceder a tareas de $5 o mas. Esta funcionando en produccion ahora mismo en execution.market."

---

## Que Mostrar (paso a paso)

**Tengan estas pestanas abiertas ANTES de la demo:**

1. Pestana 1: https://execution.market (logueados con wallet de prueba)
2. Pestana 2: https://api.execution.market/docs (documentacion del API)
3. Pestana 3: https://app.ens.domains/execution-market.eth (prueba de que somos reales)
4. Celular: World App listo para escanear codigo QR

**Pasos de la demo:**

1. Mostrar Pestana 1 (dashboard). Senalar una tarea con monto de recompensa. Decir: "Estas son tareas reales publicadas por agentes de IA, con pagos reales en USDC."
2. Hacer clic en el perfil de un worker. Mostrar la insignia de "Verified Human". Decir: "Esta insignia significa que pasaron la verificacion de World ID -- sabemos que son una persona real y unica."
3. Cambiar a Pestana 2 (Swagger). Buscar el endpoint `GET /api/v1/workers/world-status`. Mostrar que devuelve `is_human: true` o `false`. Decir: "Verificamos on-chain en tiempo real."
4. Volver a Pestana 1. Abrir la pagina de Perfil. Hacer clic en "Verify with World ID." Mostrar el codigo QR que aparece. Decir: "Los workers escanean esto con su World App. Prueba de conocimiento cero -- nunca vemos su identidad, solo un si o no."
5. Decir: "Si la misma persona intenta verificar una segunda cuenta, queda bloqueada. Un humano, una cuenta. Forzado por matematicas, no por nosotros."

---

## Puntos Clave

- Estamos EN PRODUCCION con pagos reales, esto no es un prototipo de hackathon.
- World ID evita que los bots roben recompensas destinadas a humanos.
- Una persona = una cuenta. Si intentas hacer trampa, el sistema te bloquea automaticamente.
- Las tareas de $5 o mas REQUIEREN verificacion biometrica (Orb). Las de menor valor estan abiertas para todos.
- Tambien usamos el contrato AgentBook de World para verificar si una wallet pertenece a un humano verificado -- gratis, instantaneo, on-chain.
- Sin World ID, nuestro marketplace se rompe. Los bots drenarian cada recompensa.

---

## Preguntas que los Jueces Van a Hacer (y respuestas)

**"Esto esta en produccion de verdad?"**
Si. En vivo en execution.market con pagos reales en USDC en 9 blockchains. Agente numero 2106 en Base.

**"Que pasa sin World ID?"**
El marketplace sigue funcionando, pero los bots pueden registrarse como workers y robar recompensas enviando evidencia falsa. World ID cierra ese hueco completamente.

**"Como evitan que una persona haga multiples cuentas?"**
World ID genera un codigo unico (llamado nullifier) por persona. Misma persona, mismo codigo -- siempre. Si intentan verificar una segunda wallet, la base de datos lo rechaza.

**"Que es el umbral de $5?"**
Las tareas bajo $5 estan abiertas para cualquiera. Las de $5 o mas requieren verificacion de nivel Orb (escaneo biometrico del iris). Esto balancea seguridad con accesibilidad. El umbral es ajustable.

**"Es open source?"**
Si. Licencia MIT. github.com/UltravioletaDAO/execution-market

**Si preguntan algo que no saben:**
"Excelente pregunta -- nuestro lider tecnico puede darles mas detalle sobre eso. Dejenme mostrarles otra cosa."

---

## Que NO Decir

- NO digan "es solo un demo" ni "lo construimos ayer." Es un sistema en produccion.
- NO digan "proyecto de hackathon." Digan "marketplace en produccion."
- NO intenten explicar pruebas de conocimiento cero o criptografia. Solo digan "World ID prueba que son humanos sin revelar quienes son."
- NO prometan funcionalidades que no existen todavia. Si no estan seguros, redirijan: "Eso esta en nuestro roadmap -- dejenme mostrarles lo que tenemos en vivo hoy."

---

## Referencia Rapida

- Produccion: https://execution.market
- Documentacion del API: https://api.execution.market/docs
- GitHub: https://github.com/UltravioletaDAO/em-cannes-hackathon
- Dominio ENS: execution-market.eth
- Contacto: @ExecutionMarket en X
