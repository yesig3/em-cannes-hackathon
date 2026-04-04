# Booth de Hedera -- Guion para Yesi y David

> Lean esto en el celular antes de acercarse al booth de Hedera.
> NO necesitan entender el codigo. Solo sigan este guion.

---

## Donde Estan

Estan en el **booth de Hedera**. El track se llama **"AI & Agentic Payments on Hedera"** y el premio es **$6,000** (dividido entre hasta 2 equipos, o sea $3,000 cada uno).

---

## Que Quieren Ver los Jueces

Los jueces quieren ver que **realmente hicimos algo en Hedera** -- no solo hablar de ello. Especificamente, quieren al menos un pago, transferencia de token u operacion financiera en la red de prueba de Hedera.

Nosotros hicimos **cinco** cosas en Hedera, no solo una:

1. Registramos la identidad de un agente de IA en Hedera (como un pasaporte digital)
2. Le dimos a ese agente una puntuacion de reputacion en Hedera
3. Hicimos un pago real en HBAR (una propina a un buen trabajador)
4. Registramos cada paso de una tarea en el registro de mensajes unico de Hedera (llamado HCS)
5. Extendimos nuestro servidor open-source (el Facilitator) para soportar Hedera

---

## Que Decir (Su Apertura -- 30 Segundos)

Digan esto naturalmente, con sus propias palabras:

> "Construimos Execution Market -- es un marketplace en vivo donde agentes de IA publican tareas con recompensas en efectivo, y personas reales las completan por pago instantaneo. Ya funciona en 9 blockchains con dinero real. Para este hackathon, agregamos Hedera. Registramos la identidad de nuestro agente en Hedera, le damos propinas en HBAR a buenos trabajadores, y -- esto es lo importante -- registramos cada paso de una tarea en el Consensus Service de Hedera. HCS es algo que solo Hedera tiene. Ninguna otra blockchain puede hacer esto. Cada evento es permanente y cualquiera puede verificarlo."

---

## Como Hacer la Demo (Paso a Paso)

Abran estas 3 pestanas del navegador ANTES de empezar a hablar. Tenganlas listas.

### Pestana 1 -- El Marketplace en Vivo
**URL:** https://execution.market

Senalen la pantalla y digan:
> "Este es nuestro marketplace en produccion. Agentes de IA reales crean tareas, personas reales las completan y les pagan automaticamente en USDC. Esto no es un prototipo -- esta funcionando ahora mismo."

### Pestana 2 -- La Transaccion de Propina en HBAR
**URL:** https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321

Senalen los detalles de la transaccion y digan:
> "Este es un pago real en Hedera. Cuando un trabajador hace buen trabajo -- su puntuacion de reputacion esta arriba del 55% -- el sistema automaticamente le envia una propina de 0.01 HBAR. Esta es esa transaccion. Pueden verla aqui mismo en HashScan, el explorador de bloques de Hedera."

### Pestana 3 -- El Registro de Mensajes HCS
**URL:** https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages

Senalen la lista de mensajes y digan:
> "Esta es nuestra arma secreta. Hedera tiene algo llamado Consensus Service -- es como un libro de registros permanente que no se puede alterar. Cada vez que algo pasa en una tarea -- creada, trabajador aplico, pago bloqueado, pago liberado, ambas partes se calificaron -- lo escribimos aqui. Son 6 mensajes por una tarea. Cualquiera en el mundo puede ver esto. No se necesita contrasena, no se necesita clave de API. Solo abran esta URL."

### Cierre
> "Entonces tenemos cinco integraciones con Hedera: identidad del agente, reputacion, propinas en HBAR, registro de eventos en HCS, y nuestro servidor Facilitator open-source que hace todo esto sin costo de gas. Ademas, nuestros pagos principales de garantia corren en Base. Nuestra prueba de punta a punta paso 7 de 7 pasos en ambas cadenas."

---

## Si Preguntan... (Respuestas en Lenguaje Simple)

**"Por que no pagan la recompensa completa en Hedera?"**
> "Buena pregunta. USDC funciona diferente en cada cadena. Ahora mismo la mayor liquidez de USDC esta en Base, asi que ahi hacemos los pagos principales. Usamos Hedera para lo que hace mejor -- identidad, reputacion, propinas, y ese increible registro de mensajes. A medida que USDC crece en Hedera, podemos mover los pagos completos ahi tambien."

**"Que es HCS?"**
> "Piensen en el como un libro de registros que no se puede alterar y que solo Hedera tiene. Cada vez que algo pasa en una tarea, escribimos un mensaje ahi. Recibe una marca de tiempo de la propia red de Hedera, asi que saben que es real. Cualquiera puede verificarlo. Es como un recibo que nunca se puede cambiar."

**"Esto es solo en testnet?"**
> "La identidad, reputacion, propinas y mensajes HCS estan en el testnet de Hedera. Nuestro marketplace real y los pagos en USDC estan en Base mainnet con dinero real. Pasar a mainnet de Hedera es solo un cambio de configuracion de nuestro lado."

**"Que es ERC-8004?"**
> "Es un estandar de identidad para agentes de IA. Piensen en el como un pasaporte. Nuestro agente es el numero 99 en Hedera. Funciona en 16 redes con la misma direccion. Hedera lo lista como tecnologia aceptada para este track."

**"Como es gasless?"**
> "Tenemos un servidor llamado el Facilitator que paga las comisiones de red en nombre de los agentes y trabajadores. Entonces nadie necesita tener HBAR para usar nuestra plataforma en Hedera. Hacemos lo mismo en 9 cadenas en produccion."

**"Cuantas blockchains soportan?"**
> "Nueve en produccion con dinero real, mas Solana. Hedera es la mas reciente."

**Si preguntan algo que no saben:**
> "Excelente pregunta. Nuestro lider tecnico puede darles todos los detalles de eso -- dejenme mostrarles otra cosa mientras tanto."

---

## Que NO Decir

- NO digan "solo esta en testnet." Digan: "Identidad, reputacion y HCS estan en testnet de Hedera. Los pagos estan en Base mainnet con dinero real."
- NO digan "no soportamos Hedera realmente." Tenemos 5 integraciones en vivo.
- NO intenten explicar detalles tecnicos como EIP-3009, diferencias de tokens HTS, o como funciona gasless por debajo. Si preguntan, digan "nuestro sistema de pagos es agnostico a la cadena" y sigan adelante.
- NO prometan una fecha de mainnet. Digan "esta en nuestro roadmap."

---

## Links para Tener Abiertos (Listos para Copiar y Pegar)

| Que | URL |
|-----|-----|
| Marketplace en vivo | https://execution.market |
| Transaccion de propina HBAR | https://hashscan.io/testnet/transaction/0x419d824ca972ddae63b6da1597bad2c4c52172fa1339897d1e2a95c36e9a3321 |
| Mensajes HCS (6 eventos) | https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.8511429/messages |
| Documentacion del API | https://api.execution.market/docs |
| Identidad del agente en Hedera | https://facilitator.ultravioletadao.xyz/identity/hedera-testnet/99 |
| Reputacion del agente en Hedera | https://facilitator.ultravioletadao.xyz/reputation/hedera-testnet/99 |
| Repositorio en GitHub | https://github.com/UltravioletaDAO/em-cannes-hackathon |
| Guia para jueces (tecnica) | [JUDGES_GUIDE.es.md](JUDGES_GUIDE.es.md) |
| Contacto | @ExecutionMarket en X |
