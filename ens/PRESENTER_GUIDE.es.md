# ENS Track -- Guia para Presentadores

> Para Yesi y David en el booth de ENS, ETHGlobal Cannes 2026.
> Lean esto en el celular antes de acercarse al booth.

---

## Que Decir (30 segundos)

"Execution Market es un marketplace en produccion donde agentes de IA publican tareas con recompensas y humanos las completan. Integramos ENS para que nuestro agente de IA sea encontrable por nombre -- execution-market.eth -- no solo una direccion de wallet aleatoria. Los workers pueden reclamar subnombres como alice.execution-market.eth. Toda la identidad vive on-chain, asi que cualquier protocolo puede encontrarnos sin usar nuestro API."

---

## Que Mostrar (paso a paso)

**Tengan estas pestanas abiertas ANTES de la demo:**

1. Pestana 1: https://execution.market (el marketplace en vivo)
2. Pestana 2: https://api.execution.market/docs (documentacion del API)
3. Pestana 3: https://app.ens.domains/execution-market.eth (nuestra pagina en ENS)

**Pasos de la demo:**

1. Mostrar Pestana 3 (ENS App). Decir: "Este es execution-market.eth -- nuestro dominio, registrado en Ethereum mainnet. No es testnet, no es un mock."
2. Bajar en la pagina de ENS App para mostrar los text records. Decir: "Siete registros de texto on-chain: nuestra URL, descripcion, Twitter, ID de agente. Cualquier protocolo puede leer esto sin tocar nuestro API."
3. Cambiar a Pestana 1 (dashboard). Mostrar una tarjeta de agente o worker con insignia ENS. Decir: "Si un worker tiene un nombre ENS, aparece automaticamente. Lo detectamos cuando conectan su wallet."
4. Cambiar a Pestana 2 (Swagger). Buscar la seccion ENS. Ejecutar el endpoint `GET /api/v1/ens/resolve/execution-market.eth`. Mostrar el resultado. Decir: "Resolucion en vivo. No esta hardcodeado."
5. Luego ejecutar `GET /api/v1/ens/resolve/vitalik.eth`. Decir: "Funciona con cualquier nombre ENS -- esto prueba que es resolucion real, no una respuesta falsa."
6. Mostrar la pagina de Perfil en Pestana 1. Senalar la seccion "Claim Subname". Decir: "Los workers pueden reclamar alice.execution-market.eth. Nosotros pagamos el gas. Obtienen una identidad permanente on-chain bajo nuestra plataforma."

---

## Puntos Clave

- execution-market.eth es un dominio ENS real en Ethereum mainnet. Registrado, pagado, con 7 registros de texto on-chain.
- ENS hace que nuestro agente de IA sea ENCONTRABLE. Antes de ENS, Agente 2106 era solo un numero. Ahora cualquiera puede buscar execution-market.eth y encontrar todo sobre nosotros.
- Los workers obtienen subnombres (como alice.execution-market.eth). La plataforma paga el gas para que los workers no necesiten ETH.
- Esto NO es cosmetico. Otros protocolos pueden resolver nuestro nombre, leer nuestros metadatos, encontrar nuestro ID de agente y verificar nuestra reputacion -- todo sin usar nuestro API. Si nuestro servidor se cae, la identidad persiste on-chain.
- Tres capas funcionan juntas: ENS es como nos ENCUENTRAN. ERC-8004 es como CONFIAN en nosotros. World ID es como saben que los workers son HUMANOS.
- Todo esta en produccion. Sin mocks, sin valores hardcodeados.

---

## Preguntas que los Jueces Van a Hacer (y respuestas)

**"execution-market.eth esta registrado de verdad?"**
Si. Registrado en Ethereum mainnet. Pueden verificarlo ahora mismo en app.ens.domains/execution-market.eth.

**"Es solo una insignia cosmetica?"**
No. Los text records contienen nuestro ID de agente, chains soportadas y rol. Cualquier protocolo puede resolver el nombre, leer los registros y descubrir nuestra identidad sin nuestro API. Si nuestro backend se cae, la identidad on-chain persiste.

**"Como funcionan los subnombres?"**
Los workers hacen clic en un boton en su perfil, escogen un nombre, y nosotros lo creamos on-chain usando NameWrapper. Nosotros pagamos el gas -- como $0.15 por subnombre. Cada worker obtiene uno.

**"Quien paga por el dominio ENS y los subnombres?"**
La plataforma paga todo. El registro del dominio, las actualizaciones de text records, el gas de los subnombres. Los workers nunca necesitan ETH.

**"Que es ERC-8004?"**
Nuestro sistema de identidad on-chain para agentes de IA. ENS guarda el ID del agente (2106) en un text record, que se conecta con ERC-8004 donde viven la identidad completa y la reputacion. ENS es la puerta de entrada, ERC-8004 es la identidad adentro.

**Si preguntan algo que no saben:**
"Excelente pregunta -- nuestro lider tecnico puede darles mas detalle sobre eso. Dejenme mostrarles otra cosa."

---

## Que NO Decir

- NO digan "solo registramos un dominio." Digan "construimos una capa completa de identidad y descubrimiento sobre ENS."
- NO digan "es solo un nombre." Digan "es un mecanismo de descubrimiento entre protocolos."
- NO intenten explicar namehash, EIP-137 o internos de NameWrapper. Solo digan "usamos el protocolo estandar de ENS."
- NO digan "planeamos agregar subnombres." Digan "los subnombres estan en vivo -- los workers pueden reclamarlos ahora."

---

## Referencia Rapida

- Produccion: https://execution.market
- Documentacion del API: https://api.execution.market/docs
- Dominio ENS: https://app.ens.domains/execution-market.eth
- GitHub: https://github.com/UltravioletaDAO/em-cannes-hackathon
- Contacto: @ExecutionMarket en X
