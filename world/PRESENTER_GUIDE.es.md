# Booth de World -- Guion para Yesi y David

> Lean esto en el celular antes de acercarse al booth de World.
> NO necesitan entender el codigo. Solo sigan este guion.

---

## Donde Estan

Estan en el **booth de World**. Hay **dos tracks** aqui, y estamos aplicando a ambos:

| Track | Premio |
|-------|--------|
| **Best Use of AgentKit** | $8,000 (1ro $4K, 2do $2.5K, 3ro $1.5K) |
| **Best Use of World ID 4.0** | $8,000 (1ro $4K, 2do $2.5K, 3ro $1.5K) |
| **Total posible** | **$8,000** (lo mejor de un track) |

---

## Que Quieren Ver los Jueces

**Track AgentKit:** Apps que usan AgentKit para distinguir de verdad a agentes respaldados por humanos de bots. No un adorno -- una distincion real que importa.

**Track World ID 4.0:** Productos que se **rompen** sin prueba de humanidad. Tiene que ser una restriccion real, no solo una insignia bonita.

**La frase clave que deben decir (memoricenla):**

> "Este producto SE ROMPE sin World ID. Sin el, los bots roban las recompensas."

---

## Que Construimos (Digan Esto)

Esto es lo que construimos, en palabras simples:

1. **Verificamos si un trabajador es un humano real y verificado** antes de que pueda hacer tareas valiosas. Usamos el contrato AgentBook de World en Base -- es un registro publico de quien esta verificado.

2. **Los humanos verificados tienen acceso gratis. Los bots tienen que pagar.** Si estas verificado con World ID, interactuas con nuestro sistema gratis. Si no, pagas por cada solicitud. Esto es una diferencia economica real, no una insignia cosmetica.

3. **Los trabajadores deben verificarse con World ID para aplicar a tareas de $5 o mas.** Debajo de $5, cualquiera puede participar. A partir de $5, debes probar que eres humano con un escaneo biometrico (nivel Orb). Esto protege las recompensas de ser drenadas por bots.

4. **La misma persona no puede crear dos cuentas.** World ID genera un codigo unico por persona. Si intentas verificar una segunda wallet, el sistema te bloquea. Un humano, una cuenta. Forzado por matematicas.

---

## Como Hacer la Demo (Paso a Paso)

Abran estas pestanas ANTES de empezar a hablar.

### Pestana 1 -- El Marketplace en Vivo
**URL:** https://execution.market (asegurense de estar logueados con una wallet de prueba)

Senalen la pantalla y digan:
> "Este es nuestro marketplace en produccion. Agentes de IA reales publican tareas con recompensas reales en USDC. Personas reales las completan y les pagan. Esto esta en vivo ahora mismo, no es un demo."

Senalen cualquier tarea y digan:
> "Ven esta tarea? Tiene una recompensa. Si un bot pudiera aplicar, enviaria evidencia falsa y se robaria el dinero. Por eso necesitamos World ID."

### Pestana 2 -- Perfil de Trabajador con Insignia World ID
En la Pestana 1, hagan clic en el perfil de cualquier trabajador que muestre la insignia **"Verified Human"**. Digan:
> "Ven esta insignia? Significa que esta persona paso la verificacion de World ID. Sabemos que es una persona real y unica -- no un bot, y no la misma persona con dos cuentas."

### Pestana 3 -- El Flujo de Verificacion de World ID
En la Pestana 1, vayan a la **pagina de Perfil** y hagan clic en **"Verify with World ID"**. Aparecera un codigo QR. Digan:
> "Asi se verifican los trabajadores. Abren su World App en el celular y escanean este codigo QR. Prueba que son humanos sin revelar quienes son. Nosotros nunca vemos su nombre ni su cara -- solo un si o un no."

Si alguien en el booth tiene la World App, invitenlos a escanear el QR en vivo. Digan:
> "Quieren probarlo? Solo abran su World App y escaneen esto."

### Pestana 4 -- Documentacion del API (si quieren mas)
**URL:** https://api.execution.market/docs

Busquen el endpoint `GET /api/v1/workers/world-status`. Digan:
> "Verificamos en tiempo real si una wallet pertenece a un humano verificado. Esto devuelve verdadero o falso. Es una verificacion en vivo, no un valor guardado."

### Cierre

> "Entonces la conclusion es esta: sin World ID, nuestro marketplace esta roto. Los bots se registran como trabajadores, envian evidencia falsa y se drenan las recompensas. World ID cierra esa puerta completamente. Una persona, una cuenta, verificada por biometria. El producto literalmente no funciona sin esto."

---

## Si Preguntan... (Respuestas en Lenguaje Simple)

**"Esto esta en produccion de verdad?"**
> "Si. Esta en vivo en execution.market con pagos reales en USDC en 9 blockchains. Nuestro agente es el numero 2106 en Base. Pueden usarlo ahora mismo."

**"Que pasa si quitan World ID?"**
> "El marketplace sigue funcionando, pero se vuelve inutilizable. Los bots se registran como trabajadores y envian evidencia falsa para robar recompensas. Vimos esto en pruebas -- sin World ID, las cuentas falsas drenaron recompensas en horas. No es opcional para nosotros."

**"Como evitan que una persona haga multiples cuentas?"**
> "World ID le da a cada persona un codigo unico. La misma persona siempre obtiene el mismo codigo. Si intentan verificar una segunda wallet, la base de datos dice que no. Un humano, una cuenta -- forzado por World ID, no por nosotros."

**"Por que el umbral de $5?"**
> "Las tareas bajo $5 estan abiertas para todos -- bajo riesgo, asi que mantenemos la barrera baja. Las tareas de $5 o mas requieren verificacion biometrica con el Orb. Esto balancea accesibilidad con seguridad. El umbral es ajustable."

**"Que es AgentBook?"**
> "Es una lista publica en la blockchain de Base de wallets que pertenecen a humanos verificados. Lo verificamos cuando un trabajador se conecta. Si estan en la lista, tienen acceso gratis. Si no, tienen que pagar por solicitud. Es un contrato de World, no nuestro."

**"Es open source?"**
> "Si. Licencia MIT. Todo esta en GitHub."

**"Como funciona la parte de zero-knowledge?"**
> "Lo que necesitan saber es: nosotros nunca vemos quien es la persona. World ID prueba que son humanos y unicos sin revelar su identidad. Solo recibimos un si o un no. La privacidad viene incorporada."

**Si preguntan algo que no saben:**
> "Excelente pregunta. Nuestro lider tecnico puede darles todos los detalles -- dejenme mostrarles otra cosa mientras tanto."

---

## Que NO Decir

- NO digan "es solo un demo" ni "lo construimos para el hackathon." Es un sistema en produccion.
- NO digan "proyecto de hackathon." Digan "marketplace en produccion."
- NO intenten explicar pruebas de zero-knowledge, firma criptografica, secp256k1, o hashing de nullifiers. Solo digan "World ID prueba que son humanos sin revelar quienes son."
- NO prometan funcionalidades que no existen. Si no estan seguros, digan "eso esta en nuestro roadmap -- dejenme mostrarles lo que tenemos en vivo hoy."

---

## Links para Tener Abiertos (Listos para Copiar y Pegar)

| Que | URL |
|-----|-----|
| Marketplace en vivo | https://execution.market |
| Documentacion del API | https://api.execution.market/docs |
| Dominio ENS (prueba de identidad) | https://app.ens.domains/execution-market.eth |
| Repositorio en GitHub | https://github.com/UltravioletaDAO/em-cannes-hackathon |
| Contacto | @ExecutionMarket en X |
