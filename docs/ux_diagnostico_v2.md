# NYC 2026 — rediseño de la app (v2)

Contexto que gobierna todo: **parado en una esquina, una mano, diez segundos**, con sol.
El caso "sentado planificando" existe, pero es el segundo. Todo lo que sigue se decide
con esa jerarquía.

Medición de arranque (Playwright, viewport 375×667, día 1, `file://`):

| | antes (v1) | después (v2) |
|---|---|---|
| alto del día 1 | **5.694 px** (8,5 pantallas) | **2.272 px** (3,4) |
| los 9 días sumados | **52.801 px** | **21.477 px** — 59 % menos scroll |
| alto medio por bloque | ~360 px | ~85 px |
| primer bloque visible al abrir | no: recién a los ~1.100 px | la respuesta a "¿qué toca?" está arriba de todo |
| responde "¿qué toca ahora?" | no | sí: tarjeta fija + marca en la lista + botón en la barra |
| botones por bloque plegado | 7 (✓ ▲ ▼ ✕ Maps Apple Google) | 2 (✓ y →) |

---

## Los 5 problemas, ordenados por lo que cuestan en la calle

### 1. La app sabe la hora y sabe el itinerario, y nunca los cruza
Es el problema más caro y el más barato de arreglar. A las 15:40 en Belmont, la pregunta
es "¿qué toca?" y la respuesta exige scrollear doce bloques leyendo horas. La app tiene
los dos datos: `TODAY` y `b.t`. Nunca los junta.

Peor: `TODAY` se calculaba con `new Date().toISOString()`, que es **UTC**. En Nueva York
(UTC−4), a partir de las 20:00 hora local la app cree que ya es el día siguiente. Toda
la noche de cada día del viaje —justo las horas de Birdland, el Vanguard y Café Wha—
el "hoy" estaba corrido un día. Es un bug real, no cosmético.

### 2. Un bloque cuesta media pantalla o más
Cada bloque muestra, siempre y todo junto: párrafo completo (184 caracteres promedio, 694
el peor), chip del lugar, tres botones de mapa, "acá cerca", "de paso", "+ nota", y una
columna fija de cuatro controles. Nada está plegado. 143 bloques × todo = un día de casi
6.000 px. Encontrar dónde estás es scroll a ciegas.

### 3. Todo pesa lo mismo
"Subte A o D express desde 42 St hasta 125 St" y "★★ TOP OF THE ROCK — entrada 18:15"
se ven idénticos. Los 46 bloques de logística —un tercio del viaje— tienen el mismo
tamaño, el mismo color y los mismos botones que las anclas compradas. Y lo que más grita
en la pantalla son tres botones de mapa verdes y azules repetidos 143 veces, que es
exactamente lo que menos define un bloque.

### 4. La primera pantalla no muestra nada del día
Header alto + tabs + tira de días + tarjeta de día con el `note` completo (hasta 700
caracteres de razonamiento de planificación) ocupan más de una pantalla y media antes
del primer bloque. Ese `note` es material de sillón, no de vereda: explica *por qué* el
día está armado así. Además, al scrollear, el header tapa las pestañas (los dos son
`position:sticky; top:0`), así que para cambiar de pestaña hay que volver arriba de todo.

### 5. Los controles de edición viven encima del contenido
Cada bloque lleva ▲ ▼ ✕ permanentes, y ✕ (borrar) queda justo debajo de ▼ — un pulgar
apurado borra un bloque sin querer. La hora es un `<input>` siempre editable: tocarla
para leerla abre el teclado. De los cuatro controles, el único que se usa caminando es
el ✓. Los otros tres son herramientas de planificación ocupando el mejor espacio de la
pantalla y el peor momento del viaje.

---

## Qué se hizo con cada uno

### 1 → Tarjeta "Ahora" + marcas de tiempo en la lista
- **Tarjeta fija arriba del día** que cruza reloj e itinerario. Tres estados honestos:
  antes del viaje (**"faltan N días"** + con qué arranca), durante (**bloque actual**,
  qué sigue y **en cuántos minutos**), después (el viaje terminó).
- La tarjeta trae las dos acciones de calle en botones grandes: **→ Llegar** (Apple Maps
  desde donde estés) y **✓ marcar hecho**. No hay que entrar a ningún lado.
- En la lista, el bloque actual queda marcado con barra ámbar y los ya pasados se
  atenúan. Es la orientación más barata que existe: se ve sin leer.
- Botón **Ahora** en la barra inferior: salta al bloque actual desde donde estés, y si
  estabas mirando otro día, primero te lleva a hoy.
- Se refresca solo cada 30 s (sin re-renderizar si estás escribiendo una nota).
- **`TODAY` pasa a hora local.** El corrimiento nocturno se terminó.

### 2 → Bloques plegados por defecto, con el dato completo a un toque
El texto **no se borró**: se le dio jerarquía. Un `leadOf()` parte cada texto en título y
resto usando los separadores que ya usa el catálogo (` — `, `. `, `: `) y las ★ del
principio. Plegado se ve: hora · punto de categoría · **título** · teaser de una línea ·
una línea de datos duros (barrio · precio · 🕐 horario · ⚠ · N cerca). Un toque en
cualquier parte despliega **todo lo que había antes, sin recortar**: texto completo,
chips, los tres mapas, "de camino hasta acá", "acá cerca", el barrio, la nota.

El ⚠ de la línea de datos no es decorativo: se enciende cuando el texto plegado esconde
mayúsculas de aviso (`CIERRA LOS SÁBADOS`, `RESERVA NO MODIFICABLE`, `LLEGAR 23:10`).
Avisa que hay algo importante adentro sin obligar a leerlo todo.

### 3 → Tres pesos visuales distintos
- **Logística** (46 bloques): una línea, tipografía chica, gris, sin punto de color, sin
  teaser. Es pegamento, no plan.
- **Normal**: título + teaser + datos.
- **Destacado / con ★**: título más grande, estrella al frente, fondo apenas verde.
- Los **tres botones de mapa se plegaron a uno**: una flecha **→** al lado del ✓, que abre
  Apple Maps caminando desde donde estés. Maps y Google siguen enteros al desplegar.

### 4 → Menos cromo, el "por qué" adonde corresponde
- Header a una línea (44 px en vez de 62) y **header + pestañas en un solo contenedor
  sticky**: ahora las pestañas se alcanzan con el pulgar sin volver arriba.
- Tira de días más baja y con el día de hoy marcado.
- El `note` y el `alt` del día pasan a un desplegable **"por qué este día"**. Están
  completos, pero no entre vos y el itinerario.
- **Swipe horizontal** para cambiar de día: la acción más frecuente deja de exigir subir
  hasta la tira de días. Ignora los contenedores que scrollean solos y exige gesto
  claramente horizontal para no comerse el scroll vertical.

### 5 → Los controles de planificación se van a donde se planifica
▲ ▼ ✕ y la hora editable **solo aparecen con el bloque desplegado**. El ✕ queda separado
y en rojo. Plegado, la columna de acción tiene exactamente dos cosas: **✓** y **→**, las
dos que se usan caminando. La hora plegada es texto, no input: leerla ya no abre el
teclado.

---

## Decisiones de diseño que vale la pena defender

- **Cero claves nuevas en el estado.** Qué bloque está desplegado es UI transitoria y vive
  en un `Set` de módulo, igual que `OPEN_NOTES`. `fresh()`, `migrate()` y `hydrate()`
  quedaron sin tocar: el riesgo que ya rompió la app una vez no se volvió a correr.
- **Nada de modo "calle" vs modo "plan".** Un toggle global es un modo que se queda en el
  lugar equivocado justo cuando lo necesitás. El plegado por bloque resuelve los dos casos
  con un solo gesto y sin memoria.
- **Apple Maps primero.** Son iPhone con Watch: el link de Apple lo levanta el reloj solo.
  Google queda como plan B, un toque más adentro.
- **Contraste subido** (`--ink` y `--mut` más oscuros, títulos a 650) pensando en sol
  directo. La paleta no cambió: ya la conocen.
- **Emojis**: solo los que ya estaban y son Emoji 1.0 (🕐 📍 🚇 ⚠). Lo nuevo usa símbolos
  Unicode viejos: ★ ✕ → ▲ ▼ ✓ ● ‹ › ▸.


---

## Verificación

`/tmp/ux/test_v2.py` — **67 chequeos, 67 en verde**, Playwright a 375×667 y 390×844 sobre
`file://v2.html`:

- las 6 pestañas renderizan, **cero errores JS y cero errores de consola**;
- **cero scroll horizontal**: medido como manda el `CLAUDE.md` —rueda horizontal y
  `window.scrollX`, no `scrollWidth`— en las 6 pestañas, y `scrollWidth` limpio en los 9 días;
- lo que ya andaba sigue andando: tildar, notas, editar la hora, ▲ ▼ ✕, filtro por persona,
  cambiar de día, el mapa, la hoja de ruta, agregar lugar y nota libre, y los links a Apple,
  Google y ↗ Maps con las URLs correctas;
- **resistencia del estado**: se borra cada una de las 11 claves, una por una, y se recorren
  las 6 pestañas. Todo verde. (`fresh`, `migrate` y `hydrate` quedaron sin tocar y la v2 no
  agrega ninguna clave.)
- los tres estados del reloj: antes del viaje, durante y después;
- el bug de UTC: a las 22:30 del 31/8 la app dice día 3, no día 4.

Bug propio del catálogo encontrado de paso: el chip `base:` del día 5 ("JGStay SoHo → New
Jersey (la ÚNICA noche…") medía 359 px dentro de una caja de 317 con `white-space:nowrap`.
El texto quedaba cortado sin aviso, porque `overflow-x:clip` lo tapa. **Pasa igual en la v1.**
En la v2 el chip envuelve.

## Lo que NO se resolvió

1. **Las otras cinco pestañas quedaron como estaban.** Lugares, Mapa, Costos, Transporte y
   Reservas se usan sentado; se les subió el contraste y se les arregló el cromo de arriba,
   nada más. Costos y Transporte siguen siendo tablas con scroll lateral: en un celular eso
   se lee mal, pero es material de sillón y arreglarlo bien es rediseñar tablas, otro trabajo.
2. **El swipe entre días es táctil puro** — no hay equivalente con teclado ni con mouse (en la
   Mac se cambia de día con la tira, como siempre). Y no tiene animación: el día cambia de
   golpe, sin transición que confirme la dirección.
3. **La app sigue sin saber dónde estás.** El "ahora" es solo temporal. Con geolocalización se
   podría decir "estás a 300 m del bloque de las 16:30" o reordenar "acá cerca" por distancia
   real. No se hizo: pide permiso, gasta batería y a dos días del viaje no es el momento de
   estrenar un permiso nuevo.
4. **`leadOf` es una heurística sobre texto en prosa.** Anda bien en los 143 bloques de hoy
   (se revisaron los 143 títulos uno por uno), pero si Juan escribe un bloque a mano sin
   separador temprano, el título va a ser un recorte de 92 caracteres con "…". No rompe nada,
   pero se ve peor que los demás.
5. **El ⚠ depende de un vocabulario en castellano.** Marca 28 de 143 bloques y los 28 son
   advertencias reales, pero es una lista de palabras: si aparece una advertencia escrita con
   otras palabras, no la va a marcar. Es un ayudante, no una garantía — el texto completo
   sigue estando a un toque, que es lo que de verdad importa.
6. **No se probó en un iPhone de verdad.** Todo es Chromium en modo móvil. Safari en iOS
   maneja distinto `-webkit-line-clamp` con `display:-webkit-box`, `100vw` con la barra de
   direcciones, y `position:sticky` dentro de contenedores. **Antes de usarla en la calle hay
   que abrirla una vez en el iPhone de Juan**, que es exactamente donde el 🧭 se rompió la
   otra vez.
