# Booth de ENS -- Guion para Yesi y David

> Lean esto en el celular antes de acercarse al booth de ENS.
> NO necesitan entender el codigo. Solo sigan este guion.

---

## Donde Estan

Estan en el **booth de ENS**. Hay **dos tracks** aqui, y estamos aplicando a ambos:

| Track | Premio |
|-------|--------|
| **Best ENS Integration for AI Agents** | $5,000 |
| **Most Creative Use of ENS** | $5,000 |
| **Total posible** | **$10,000** |

---

## Que Quieren Ver los Jueces

**Best ENS Integration for AI Agents:** Quieren que ENS se use de forma real y significativa para agentes de IA -- no solo un nombre bonito. Quieren ver nombrado de agentes, resolucion de direcciones, metadata guardada en registros de texto. Tiene que servir un proposito.

**Most Creative Use of ENS:** Algo no obvio. Algo que los haga decir "no habia pensado en usar ENS asi."

---

## Que Construimos (Digan Esto)

Esto es lo que construimos, en palabras simples:

1. **Nuestro agente de IA tiene un nombre ENS: execution-market.eth.** En vez de ser identificado por una direccion de wallet larga y aleatoria, cualquiera puede buscar "execution-market.eth" y encontrarnos. Esta registrado en Ethereum mainnet -- no es una prueba, no es falso.

2. **Guardamos la informacion de identidad del agente dentro del nombre ENS.** Hay 7 registros de texto on-chain: nuestra URL, descripcion, Twitter, numero de agente, blockchains soportadas, rol del agente, y si estamos verificados con World ID. Cualquier otra app o protocolo puede leer todo esto solo buscando nuestro nombre ENS. No necesitan nuestro API. No necesitan nuestro permiso.

3. **Los trabajadores obtienen subnombres bajo nuestra plataforma.** Una trabajadora llamada Alice puede reclamar "alice.execution-market.eth" como su identidad permanente on-chain. Nosotros pagamos el gas -- los trabajadores no necesitan tener crypto para reclamar su nombre.

4. **Esto es un mecanismo de descubrimiento, no una insignia cosmetica.** Si nuestro servidor se cae manana, la identidad on-chain persiste. Otros protocolos pueden seguir encontrandonos, leer nuestros metadatos y ver nuestro ID de agente -- todo desde el nombre ENS solamente.

**La vision completa -- tres capas trabajando juntas:**
- **ENS** es como nos ENCUENTRAN (nombre y metadatos)
- **ERC-8004** es como CONFIAN en nosotros (identidad y reputacion)
- **World ID** es como saben que los trabajadores son HUMANOS (verificacion biometrica)

---

## Como Hacer la Demo (Paso a Paso)

Abran estas 3 pestanas ANTES de empezar a hablar.

### Pestana 1 -- Nuestra Pagina de Dominio ENS
**URL:** https://app.ens.domains/execution-market.eth

Senalen la pantalla y digan:
> "Este es execution-market.eth -- nuestro dominio, registrado en Ethereum mainnet. Registro real, dinero real, no es testnet."

Bajen para mostrar los **registros de texto**. Senalenlos y digan:
> "Ven estos registros? Siete datos guardados on-chain. Nuestra URL, nuestro Twitter, nuestro ID de agente, que blockchains soportamos. Cualquier app en el mundo puede leer esto solo buscando nuestro nombre ENS. No necesitan llamar a nuestro API. No necesitan nuestro permiso. Si nuestro servidor desaparece, esta informacion sigue aqui."

### Pestana 2 -- El Marketplace en Vivo
**URL:** https://execution.market

Senalen el dashboard y digan:
> "Este es nuestro marketplace en produccion. Agentes de IA publican tareas, humanos las completan, les pagan en USDC. En vivo en 9 blockchains."

Si encuentran un perfil de trabajador o tarjeta de agente que muestre una **insignia ENS**, hagan clic y digan:
> "Ven esto? Cuando un trabajador conecta su wallet, automaticamente verificamos si tiene un nombre ENS. Si lo tiene, aparece aqui. Resolucion real, no esta escrita a mano."

Luego vayan a la **pagina de Perfil** y senalen la seccion **"Claim Subname"**. Digan:
> "Los trabajadores pueden reclamar un subnombre bajo nuestra plataforma -- como alice.execution-market.eth. Nosotros pagamos el gas. Obtienen una identidad permanente on-chain. No les cuesta nada."

### Pestana 3 -- Resolucion ENS en Vivo en el API
**URL:** https://api.execution.market/docs

Busquen la seccion ENS. Ejecuten el endpoint:
`GET /api/v1/ens/resolve/execution-market.eth`

Muestren el resultado y digan:
> "Esto es resolucion en vivo. El API acaba de buscar nuestro nombre ENS en tiempo real y devolvio la direccion y los registros. No esta escrito a mano."

Luego ejecuten:
`GET /api/v1/ens/resolve/vitalik.eth`

Muestren el resultado y digan:
> "Funciona con cualquier nombre ENS. Aqui esta el de Vitalik. Esto prueba que es resolucion real, no una respuesta falsa."

### Cierre

> "Entonces ENS no es solo un nombre para nosotros. Es como otros protocolos descubren a nuestro agente. Es como los trabajadores obtienen identidades permanentes. Y funciona aunque nuestro servidor este completamente fuera de linea. Tres capas: ENS para encontrarnos, ERC-8004 para confiar en nosotros, World ID para verificar a los humanos."

---

## Si Preguntan... (Respuestas en Lenguaje Simple)

**"execution-market.eth esta registrado de verdad?"**
> "Si. Registrado en Ethereum mainnet. Pueden verificarlo ahora mismo -- esta en la pantalla. Pagamos por el registro y configuramos los 7 registros de texto."

**"Es solo una insignia cosmetica?"**
> "No, y esto es importante. Los registros de texto contienen nuestro ID de agente, nuestras cadenas soportadas, nuestro rol. Cualquier protocolo puede buscar nuestro nombre y encontrar todo esto sin hablar con nuestro servidor. Si nuestro backend se cae, la identidad persiste on-chain. Es un mecanismo de descubrimiento real."

**"Como funcionan los subnombres?"**
> "Un trabajador va a su perfil, hace clic en un boton, escoge un nombre, y nosotros lo creamos on-chain. Nosotros pagamos el gas -- como 15 centavos por subnombre. El trabajador obtiene una identidad permanente on-chain bajo nuestra plataforma. Como alice.execution-market.eth."

**"Quien paga por todo?"**
> "Nosotros. El registro del dominio, las actualizaciones de registros de texto, el gas de los subnombres. Los trabajadores nunca necesitan tener ETH ni ninguna crypto. Costo cero para ellos."

**"Que es ERC-8004?"**
> "Es nuestro sistema de identidad para agentes de IA -- como un pasaporte. Nuestro agente es el numero 2106. ENS guarda ese ID de agente en un registro de texto, que se conecta con ERC-8004 donde viven la identidad completa y la reputacion. Piensen en ENS como la puerta de entrada y ERC-8004 como la habitacion adentro."

**"Como es esto creativo?"**
> "La mayoria de la gente usa ENS para nombres de wallet. Nosotros lo usamos como una capa de descubrimiento entre protocolos para agentes de IA. Cualquier protocolo puede encontrar a nuestro agente, leer sus metadatos y verificar su identidad -- todo desde un nombre ENS. Ademas los trabajadores obtienen subnombres como identidades permanentes. Asi no se usa ENS tipicamente."

**Si preguntan algo que no saben:**
> "Excelente pregunta. Nuestro lider tecnico puede darles todos los detalles -- dejenme mostrarles otra cosa mientras tanto."

---

## Que NO Decir

- NO digan "solo registramos un dominio." Digan "construimos una capa completa de identidad y descubrimiento sobre ENS."
- NO digan "es solo un nombre." Digan "es como otros protocolos encuentran y confian en nuestro agente."
- NO intenten explicar namehash, EIP-137, NameWrapper, ni ningun detalle interno de ENS. Solo digan "usamos el protocolo estandar de ENS."
- NO digan "planeamos agregar subnombres." Los subnombres estan en vivo. Los trabajadores pueden reclamarlos ahora.
- NO digan "es un proyecto de hackathon." Digan "es un marketplace en produccion."

---

## Links para Tener Abiertos (Listos para Copiar y Pegar)

| Que | URL |
|-----|-----|
| Nuestra pagina de dominio ENS | https://app.ens.domains/execution-market.eth |
| Marketplace en vivo | https://execution.market |
| Documentacion del API | https://api.execution.market/docs |
| Repositorio en GitHub | https://github.com/UltravioletaDAO/em-cannes-hackathon |
| Contacto | @ExecutionMarket en X |
