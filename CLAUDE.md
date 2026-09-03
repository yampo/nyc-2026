# NYC 2026 — contexto para trabajar este proyecto

Planificador del viaje de **Juan Pablo (yampo) y Thais a Nueva York, 29 ago – 6 sep 2026**.
No es una app genérica: es *este* viaje, con *estas* reservas y *estos* dos criterios de interés.
Cuando dudes entre "hacerlo general" y "hacerlo correcto para este viaje", elegí lo segundo.

---

## Qué produce

Un solo catálogo de datos alimenta **tres salidas** que tienen que quedar siempre en la misma versión:

| salida | qué es | quién la usa |
|---|---|---|
| `index.html` (raíz) | el sitio publicado en **https://yampo.github.io/nyc-2026/** | Juan y Thais, desde el celular. **Es la que importa.** |
| `NYC_2026_Itinerario.html` | mismo app, pero con Leaflet desde CDN | doble clic en la Mac |
| `NYC_2026_Planificador.xlsx` | 8 hojas: Lugares, Costos, Itinerario, Reservas… | pensar sentado, editar en bloque |

`index.html` de la raíz y `pages/index.html` son **el mismo archivo**: `build_pages.py` escribe los dos.
GitHub Pages sirve el de la raíz.

> **Publicar = commitear.** `git add -A && git commit && git push` dispara el workflow
> `pages-build-deployment` y el sitio queda actualizado en ~1-2 min. No hay otro paso.

---

## Cómo se construye

```bash
.venv/bin/python src/build_all.py            # cadena completa
.venv/bin/python src/build_all.py --test     # cadena + las dos suites de Playwright
```

El orden **no es negociable** — cada paso lee el JSON que escribió el anterior:

```
build_places.py     → data/places.json      210 lugares
build_itinerary.py  → data/itinerary.json   9 días, 142 bloques
build_extras.py     → data/extras.json      transporte, pases, 32 reservas, decisiones
build_app.py        → NYC_2026_Itinerario.html  +  NYC_2026_web.html
build_pages.py      → pages/index.html  +  index.html (raíz)
build_xlsx.py       → NYC_2026_Planificador.xlsx
```

Si un paso falla, `build_all.py` corta la cadena en ese punto a propósito: seguir haría que los
pasos siguientes publiquen datos viejos sin avisar.

**Dependencias:** viven en `.venv/` (ignorado por git). El `python3` del sistema **no** las tiene:
si ves `ModuleNotFoundError: openpyxl`, estás corriendo el intérprete equivocado. Para rearmarlo:
`python3 -m venv .venv && .venv/bin/pip install openpyxl playwright && .venv/bin/playwright install chromium`.
Sin red no se puede: `build_places.py` geocodifica contra Nominatim, pero cachea en
`data/geocode_cache.json`, así que con el caché presente el build corre offline.

---

## Mapa de archivos

```
CLAUDE.md                  este archivo
README.md                  la portada del repo
index.html                 ← GENERADO. lo que publica GitHub Pages. no editar a mano
NYC_2026_Itinerario.html   ← GENERADO. la app para doble clic en la Mac
NYC_2026_Planificador.xlsx ← GENERADO. el Excel
LEEME.md                   changelog para Juan y Thais, en castellano, sin jerga
src/
  build_all.py             corre todo en orden
  build_places.py          EL CATÁLOGO: 210 lugares, uno por llamada a a(...)
  places_gmaps.py          los 71 que salieron de la lista "NY 2026" de Google Maps
  matches_gmaps.py         los 63 que estaban en las dos listas (id del catálogo → nombre en Google)
  build_itinerary.py       los 9 días, bloque por bloque
  build_extras.py          transporte, análisis de pases, checklist de reservas, decisiones abiertas
  build_app.py             mete los JSON dentro de app_template.html
  app_template.html        TODA la app: HTML + CSS + JS en un archivo. acá se toca la interfaz
  build_pages.py           inyecta Leaflet 1.9.4 embebido y escribe el index.html publicable
  build_xlsx.py            las 8 hojas del Excel
  merge_export.py          baja al catálogo las marcas que Juan hizo en el navegador
  merge_interests.py       versión vieja del anterior, solo intereses
  recalc_report.py         diagnóstico: qué quieren y no está agendado, conflictos, huecos
  check_hours.py           chequeo de horarios de apertura
  test_app.py              42 chequeos de la app con Playwright
  test_marca.py            16 chequeos de la marca ★ / ✕ / ☆
  data/*.json              GENERADOS salvo overrides.json y los dos caches de coordenadas
  vendor/leaflet/          Leaflet 1.9.4 vendorizado. se embebe en el sitio, no hace falta npm
```

Todos los scripts resuelven sus rutas **relativas a su propio archivo**, así que corren desde
cualquier directorio. Los entregables salen dentro de `src/` y `build_all.py` los sube a la raíz.

---

## Modelo de datos

### Lugar (`build_places.py`, función `a(...)`)

```python
a(id="vanguard", n="Village Vanguard", cat="musica", hood="West Village", boro="Manhattan",
  sub="14 St (1,2,3)", lat=40.7369, lng=-74.0016, addr="178 7th Ave South",
  cost=45, costN="detalle del costo, va como comentario en el Excel", dur=2,
  why="por qué vale la pena — es lo que Juan y Thais leen para decidir",
  book="estado de la reserva", jp=2, th=2, tags=["jazz"])
```

- `jp` / `th` — **interés de cada uno: 0 no · 1 quizás · 2 sí.** Es el eje de casi todo el filtrado.
- `must` — **marca de tres estados: `1` ★ imprescindible · `-1` ✕ no imprescindible · `0` sin marcar.**
- `src` — `"ambas"` / `"lista"` / `"propuesta"`. Se calcula solo desde `matches_gmaps.py`.
- `aprox=True` — la dirección no se pudo verificar; el pin es del barrio. Se muestra con 📍.
- `free`, `hrs`, `closed`, `main`, `gname` — opcionales.

`data/overrides.json` pisa `jp`, `th` y `must` sin tocar el catálogo. Es lo que escribe
`merge_export.py` cuando Juan exporta su plan desde el navegador.

### Bloque de itinerario (`build_itinerary.py`, función `b(...)`)

`b("22:00", "texto que se lee en la app", "vanguard", "both", "destacado")`
→ hora, texto, `pid` (id de lugar o `""`), `who` (`both`/`jp`/`th`), `kind`
(`destacado`/`comida`/`logistica`/`paseo`/`musica`…).

La hora de fin de cada bloque es la hora de inicio del siguiente: la app la recalcula sola.
Cada día tiene además `note` (el porqué del día) y `alt` (las alternativas y lo que se descartó).

### Estado del navegador

`localStorage['nyc2026.v1']`:
`{ itin, interest, must, mv, res, day, tab, whoF, pv, v, baseHash }`

Tres funciones gobiernan la carga y **hay que entenderlas antes de tocar el estado**:

- `fresh()` — el estado nuevo. **Si agregás una clave, va acá.**
- `migrate(old)` — corre solo cuando `baseHash !== DATA.itinHash`, o sea cuando cambió el
  itinerario. Adopta el itinerario nuevo conservando tildes, notas, bloques agregados a mano,
  intereses y reservas.
- `hydrate(s)` — corre **siempre**. Rellena las claves que falten.

> ⚠️ **El error que ya rompió la app una vez:** agregar una clave nueva al estado y confiar en
> `migrate`. Si el itinerario no cambió, `migrate` **no corre**, y el navegador de alguien con un
> plan guardado llega a `S.claveNueva[id]` sobre `undefined`. Por eso existe `hydrate`, y por eso
> `test_app.py` borra cada clave del estado, una por una, y recorre las 6 pestañas.

---

## Lugares de paso

Entre dos paradas consecutivas, la app lista lo que del catálogo queda **en el camino**. Son
**referencia, no plan**: no tocan el itinerario, no tienen número de visita y hay un test que
falla si la cuenta de bloques cambia al recorrer los días.

- **La medida es el DESVÍO**, no la distancia al lugar: `d(A,P) + d(P,B) - d(A,B)`, o sea cuánto
  se alarga el trayecto si paso por ahí. Son preguntas distintas — el Puente de Brooklyn está a
  800 m de DUMBO y cuesta **cero** metros pasar por él, porque queda sobre la línea al Oculus.
- **Dos regímenes.** Hasta `PASO_CORREDOR` (2,5 km) el tramo se camina y vale todo el corredor,
  con `PASO_DESVIO` (500 m) de tolerancia. Más largo que eso se va en subte y **no se pasa por el
  medio**: solo cuentan los `PASO_PUNTA` (400 m) alrededor de cada extremo.
- **Cada lugar aparece una sola vez por día**, en el tramo donde menos desvío cuesta. Sin esto,
  el domingo el Tenement Museum salía en cuatro tramos seguidos.
- **Se excluyen**: lo ya agendado en cualquier día, `transporte`/`hotel`/`evento`/`teatro`,
  lo cerrado ese día del calendario, y lo que **los dos** bajaron a 0 — eso lo descartaron.
- **Nada que necesite entrada.** Broadway y los clubes de jazz no son desvíos de cinco minutos:
  cuestan $25-112, tienen hora fija y hay que reservar. De `musica` solo pasa lo que se paga en
  la puerta (`!book && cost <= PASO_MUSICA_COVER`) **y de noche** (`PASO_MUSICA_DESDE`): un bar
  con música a las once de la mañana no es una referencia útil. En los 9 días sobreviven dos.
- **Un piso de cercanía además del desvío.** En un tramo corto el desvío miente: si A y B están
  a 100 m, pasar por algo a la vuelta "cuesta" 500 m. Por eso también entra lo que está a menos
  de `PASO_CERCA` de cualquiera de las puntas.
- **El reparto va en dos vueltas, y el orden importa.** Con solo "cada lugar a su tramo más
  barato", los tramos cortos del mismo barrio quedaban mudos. Primero cada tramo se queda con su
  mejor candidato libre (cobertura), después se reparte el resto (desvío). Un lugar sigue
  apareciendo una sola vez por día — hay un test que lo verifica en los 9.
- **Se calcula en el cliente, no en el build** (`dePasoDelDia`), para que siga siendo correcto
  después de que Juan mueva, agregue o saque un bloque. Son ~210 lugares × ~10 tramos por día:
  irrelevante para el navegador.
- En el mapa van como **anillo hueco** (`.mkpaso`) y **no entran en la polilínea** del recorrido:
  la línea une paradas, no referencias.

### La tanda de exploración

47 lugares del catálogo llevan `tags=["exploracion"]`: **no salieron de ninguna de las dos
listas**, los propuse yo para que las filas de paso y los paneles de barrio tengan qué ofrecer
cuando el propio itinerario ya se comió la zona. Llevaron las referencias de paso de 71 a 105.

Reglas que se pusieron para no ensuciar los 210 verificados, y que un test hace cumplir:

- **Interés 1/1 fijo.** Son sugerencias, no plan: con 2 se colarían en "lo que quieren ver" y
  contaminarían el reporte. Juan les sube o baja el interés en la app como a cualquier otro.
- **Coordenadas de Nominatim, validadas contra el centroide del barrio.** No es un trámite:
  a `488 Broadway` (el Haughwout) Nominatim lo mandó a **Staten Island**, y `Pier 84` no
  resolvió hasta reformular la búsqueda. Los dos se corrigieron a mano.
- **Sin `hrs`, a propósito.** Los horarios no están verificados contra la fuente y es mejor no
  tenerlos que tenerlos mal — el test falla si alguien le agrega horarios a uno de estos.
- **Los costos son estimados y lo dicen** en `costN`. 26 de los 47 son gratis, que sí es dato
  firme (calles, plazas, iglesias, parques).

Para agregar más: mismo procedimiento. Geocodificar contra Nominatim, **mirar dónde cayó cada
uno**, y no inventar horarios.

---

### «Acá cerca» ≠ «de paso»

Son dos preguntas distintas y confundirlas engaña:

- **de paso** = qué queda en el camino ENTRE dos paradas. Se mide en **desvío** y cuelga del
  traslado.
- **acá cerca** = qué hay pegado a la parada donde vas a estar. Se mide en **distancia al lugar**
  y va DENTRO del bloque (`ACA_RADIO`, 350 m).

Lo pidió Juan con un caso que lo muestra entero: **OddFellows está adentro de Domino Park**, a
296 m del punto, y salía en la fila de paso del tramo anterior con «+591 m de desvío». El número
era el del tramo que venía de Downtown Brooklyn, no la distancia a la heladería, y el lugar donde
mostrarlo también estaba mal: lo útil es verlo mientras estás en el parque, no antes de llegar.

El reparto es en cascada y el orden importa: **primero** cada lugar se asigna a la parada más
cercana si está dentro de `ACA_RADIO`, **después** lo que queda entra al reparto de tramos. Un
lugar nunca aparece en los dos lados — hay un test que lo verifica en los 9 días.

---

### Caminar un barrio es otra cosa

Un bloque cuyo lugar tiene `cat === 'barrio'` —Harlem, Arthur Avenue, Lower East Side,
Chinatown, DUMBO, West Village: son seis en el viaje— **no tiene "camino"**. Son horas sueltas
dentro de un polígono, así que la pregunta no es "qué queda entre A y B" sino "qué tengo
alrededor mientras camino". Por eso esos bloques llevan su propio panel plegable (`enElBarrio`)
en vez de chips de paso.

- Se toma **por radio Y por barrio**: `BARRIO_RADIO` (700 m) del punto **o** mismo `hood`. El
  `hood` del catálogo es la definición administrativa y no siempre coincide con lo que uno
  camina — Pier 35 está a 940 m del punto del LES y sin embargo es del barrio.
- Cada ficha lleva **descripción y los tres mapas**, no un chip: acá la decisión se toma
  leyendo, no mirando un nombre. Hay un test que falla si a alguna le falta el `why` o
  cualquiera de los tres links.
- Excluye lo mismo que los de paso, y eso importa: en el Lower East Side, **6 de los 10
  lugares del catálogo en 800 m ya están en el itinerario de ese día**. Que un barrio muestre
  poco suele significar que el plan ya lo cubrió, no que falten datos.
- Va plegado por defecto (`OPEN_HOODS`, transitorio como `OPEN_NOTES`): desplegado siempre
  inflaría el itinerario.

---

## El mapa con los 9 días juntos

Opción **«★ Los 9 días juntos»** en el selector del mapa: los nueve recorridos a la vez, cada
uno con su color y su polilínea.

**El color NO es la identidad — el número del día en el pin sí.** Se probaron siete paletas
contra `validate_palette.js` con `--pairs all` (que es el caso real: en un mapa todos los colores
se ven juntos) y **ninguna llega al piso de ΔE 15 en visión normal**; la mejor da 12,4 y hasta la
paleta de referencia de 8 slots falla ahí, con el rojo y el naranja a 7,1. Nueve series
distinguibles solo por color no existen. Por eso:

- cada pin lleva el **orden de la parada dentro de su día** (1, 2, 3…), que es lo que Juan pidió
  para poder seguir la secuencia. Costo dicho: con los nueve días juntos la identidad del día
  queda solo en el color — el popup la nombra («Parada 3 del día 7») y la leyenda aísla;
- la **leyenda aísla**: tocar un día lo deja solo y atenúa el resto — es la salida real cuando
  dos colores se parecen, y con nueve siempre hay dos que se parecen;
- la paleta elegida son los 8 slots categóricos de referencia más un violeta, que al menos
  garantiza que **ninguno lea gris** (el otro modo de fallar).

**Se excluyen los puntos fuera de la ciudad** (`boro` New Jersey o Fuera de NYC). El hotel de
Branchburg está a 60 km y deformaba el encuadre: Manhattan quedaba apretado en una esquina y el
recorrido, ilegible.

`SOLO_DIA` es UI transitoria y vive en una variable de módulo — **no toca el estado guardado**.

---

## Ruta del día a Apple Maps

`app_template.html` genera links `https://maps.apple.com/directions` — el **formato unificado
de iOS 18.4 / watchOS 11.4**, no el viejo `?daddr=`. Parámetros: `source` (si se omite, Maps
arranca desde donde esté el que abre el link), `waypoint` repetido una vez por parada
intermedia, `destination` y `mode` (`walking`/`transit`/`driving`/`cycling`).

- **`?daddr=lat,lng` dejó de funcionar en iOS 18.4.** Por eso `amPunto()` manda
  `nombre, dirección, ciudad` y nunca coordenadas crudas — además así Maps muestra el lugar
  por su nombre en vez de un pin mudo. Hay un test que falla si vuelven a colarse coordenadas.
- El nombre se limpia antes de mandarlo: `"Hotel Ink48 (29-31 ago)"` busca peor que
  `"Hotel Ink48"`. Eso hace `amNombre()`.
- Los lugares `aprox` van por **nombre + barrio**, no por su dirección: justamente es la que
  no se pudo verificar.
- **Un link lleva un solo `mode`**, y los días mezclan caminata con subte: por eso la hoja
  tiene dos botones en vez de adivinar.
- **El Watch no recibe nada.** Se inicia la navegación en el iPhone y el reloj la toma solo,
  con taps en la muñeca. No hay forma de mandarle una ruta directamente desde una web.
- Tope de 15 paradas por ruta (`AM_MAX`). El día más cargado tiene 11.
- **Google Maps es el plan B, y no es equivalente.** Maps URLs (`api=1`) acepta hasta
  **3 waypoints en navegador móvil** (nueve en el resto), y los días tienen entre 6 y 11
  paradas: por eso la ruta de Google va **partida en tramos de 4 paradas** (`GM_PARADAS`),
  no en un link. Cada tramo arranca desde la ubicación actual, así que no hace falta repetir
  la última parada del tramo anterior. Hay un test que recorre los tramos y falla si alguno
  se pasa de 3 waypoints o si entre todos no cubren exactamente las paradas elegidas.
- **Nada de emojis posteriores a Emoji 1.0 (2015).** El icono 🧭 (U+1F9ED, Emoji 11 / 2018)
  salía como un glyph roto en el aparato de Juan: el botón estaba ahí y él no lo veía, dos
  veces seguidas. Todo lo demás que usa la app es Unicode de los 90 (★ ✕ → ↗ ▸) o Emoji 1.0
  (📍 🚇 🕐 ✅). Hay un test con lista blanca en `test_app.py` que escanea el template y falla
  ante cualquier símbolo nuevo: para sumar uno, probalo primero en el aparato de Juan.
- **El plan B va donde se lo necesita.** Primero quedó solo en la hoja del día, y el chip del
  bloque tenía nada más que Apple: Juan lo reportó igual que lo anterior — el respaldo existía
  pero no estaba a mano parado en la calle. Cada bloque con lugar tiene ahora `→ Apple` y
  `→ Google` (`data-nav="apple"` / `"google"`, que es por donde los agarran los tests: buscarlos
  por texto sería frágil), los dos al mismo destino. El `↗ Maps` azul que ya existía es otra
  cosa y se queda: abre la **ficha** del lugar en Google, no la navegación.
- **Un plan B enterrado no es un plan B.** La primera versión puso Google al fondo de la hoja:
  en un iPhone quedaba a 1025px de un viewport de 844, sin ninguna señal de que hubiera más
  abajo, y Juan reportó que "no veía el botón". Ahora lo accionable va arriba —los dos mapas
  antes de la lista de paradas— y hay un test que achica a iPhone SE (375×667), recorre los
  9 días y falla si la sección de Google cae fuera de la pantalla. El día 3, con 11 paradas,
  es el que la empuja más abajo: es el caso que hay que mirar al tocar esta hoja.
- **Sin probar en un iPhone real.** Los ejemplos de la doc de Apple vienen con el escapado
  roto, así que el orden `waypoint` → `destination` sale de la tabla de parámetros, que es la
  parte normativa. Si alguna parada cae mal, es lo primero que hay que mirar.

---

## Cosas que ya costaron tiempo — no repetirlas

- **`overflow-x: hidden` en `body` mata el scroll vertical con rueda y con dedo.** Va `clip`.
  Y medir el desborde con `scrollWidth - clientWidth` da falsos positivos: marca la tira de
  pestañas, que se scrollea a propósito. El test real simula rueda y mira `window.scrollX`.
- **Leaflet se inyecta por índice de string, no con `re.sub`.** Su JS tiene escapes que rompen
  las plantillas de regex.
- **Los tiles son de OpenStreetMap.** CARTO retiró sus basemaps gratuitos y aparecía una marca de
  agua "API KEY REQUIRED" encima del mapa.
- **Nominatim se equivoca.** Trinity Church y el puente de Brooklyn cayeron en el East River.
  Hay 11 coordenadas corregidas a mano y 15 lugares marcados `aprox`.
- **`localStorage` es por origen.** Lo que Juan marca en el `.html` de su Mac (`file://`) **no**
  cruza al sitio (`https://yampo.github.io`). Para que algo se replique a Thais tiene que bajar
  al catálogo vía `merge_export.py`. Esa es la respuesta a "no veo mis marcas en el otro lado".
- **El `verId` cubría solo los datos, no la app.** Un cambio de interfaz sin cambio de
  contenido dejaba el mismo sello: `hayVersionNueva()` comparaba `verId`, veía el mismo y no
  avisaba a nadie, y ⋯ → *Versión del plan* seguía mostrando lo de antes. Ahora el hash de
  `build_app.py` incluye también `app_template.html`. El `itinHash` **no** cambió: sigue
  siendo solo del itinerario, que es lo que debe disparar `migrate`.
- **`git` sobre las carpetas montadas del bridge deja `.git/*.lock` que no se pueden borrar.**
  Desde VS Code, con git nativo, esto no pasa — pero si volvés a laburar por el bridge, ojo.

---

## Cómo está hoy

Versión visible en la app en **⋯ → Versión del plan**.

- **304 lugares** · 63 en las dos listas, 71 solo de Google Maps, el resto nuestros
  (47 de la tanda de exploración + 40 de la selección de Juan + los pedidos sueltos).
- **38 ★ imprescindibles**, 35 de ellos en el itinerario. Los 3 que quedan afuera y por qué:
  **Guggenheim** (fallback deliberado — la rotonda está en montaje hasta el 17/9),
  **Roosevelt Island** (satisfecho de facto: el tranvía y Four Freedoms están el domingo),
  **Museum of the Moving Image** (SE PERDIÓ el 2/9 al mover el encuentro con Thais a las 15:30 —
  su única ventana era el jueves gratis 14-18 y no entra en ningún otro día).
- **9 días, 145 bloques**, 35 ítems en el checklist de reservas.
- Anclas fijas ya compradas o con horario cerrado: festival Charlie Parker (sáb 29/8, Marcus Garvey Park, 14-19 h — VERIFICADO 27/8: cierra Joshua Redman),
  Birdland lun 31/8 20:30, día completo del WTC el jue 3/9,
  MO Lounge + Dizzy's jue 3/9, SUMMIT al atardecer vie 4/9 18:10,
  **Village Vanguard vie 4/9 22:00 — entradas compradas**, Peter Luger sáb 5/9 17:00,
  Café Wha sáb 5/9 23:45.

### Pendiente

1. **MoMA PS1** es el único ★ que no está en el itinerario. Necesita hueco o que Juan lo baje.
2. Cuando Juan termine de marcar ★ / ✕, **rearmar el itinerario garantizando que todos los ★
   entren**, mostrando explícitamente qué hay que sacar o mover. Ese pedido ya está hecho.
3. Verificaciones previas al viaje. **Resueltas el 27/8 contra fuente**:
   - ✅ **Festival Charlie Parker**: sáb 29 en Marcus Garvey Park, 14:00-19:00, cierra Joshua
     Redman con Nat Adderley Jr., Catherine Russell y Nicole Glover. Con salida obligada 18:30
     ven el arranque de Redman, no el final.
   - ✅ **Rotonda del Guggenheim**: CERRADA del 3/8 al 17/9 por el montaje de Taryn Simon. La
     entrada baja de $30 a $16 y sigue el pay-what-you-wish dominical. No se camina la rampa.
   - ✅ **Lincoln Center**: no está "entre temporadas". El Met proyecta ópera gratis en la Josie
     Robertson Plaza del 2 al 7/9 a las 20:00 (jue 3: Tristan und Isolde II y III), y **despejan
     la plaza desde las 18:00** para armar 2.500 sillas. El bloque del jueves 19:55 ya lo dice.
   - ❌ **Neue Galerie**: cerrada por renovación hasta el 12/11. Sacada del catálogo.
   - Pendientes todavía: AirTrain y el ticket con horario del Studio Museum. Las alertas de NJ
     Transit **ya no aplican**: desde el 1/9 Juan no vuelve a New Jersey.
4. **El MoMI se perdió el 2/9** al mover el encuentro con Thais a las 15:30 en Chelsea Market.
   Es ★ 2/2 y su única ventana era el jueves gratis 14-18. Se buscó en viernes (abre 14-20, pero
   ese día es Manhattan: galerías, Morgan gratis 17-20, SUMMIT, Vanguard), sábado (11-18, pero es
   el día de Brooklyn) y domingo (11-18, pero ya tiene el PS1 en Long Island City). Fuera del
   jueves son $20 por cabeza. Si Juan lo quiere igual, la vía es Chelsea Market → Astoria con la
   valija a cuestas: está escrita en las alternativas del jueves con su costo real.
5. **El Top of the Rock quedó fuera del viaje.** Su única chance era la tarde del miércoles, que
   ahora es del MoMA. Compite con el SUMMIT del viernes, que ya tiene el atardecer. (El ancla del
   lunes 31/8 NO se cumplió: Juan no subió.)
6. **Las salsas de HEATONIST se resuelven el jueves 15:45** en la sucursal de dentro del Chelsea
   Market. La parada de Williamsburg del sábado 15:15 dejó de ser necesaria.
7. **Chelsea Market queda dos días seguidos** (jue 15:30 encuentro, vie 14:30 almuerzo grande).
   Señalado a Juan; el viernes es el fácil de mover si prefiere variar.
8. **A decidir con Thais**: High Line, Little Island y Vessel siguen el viernes porque ella no los
   vio (Vessel es 2/2 ★). Si no repiten, libera 9:15-13:00 de ese día.

---

## Los informes de exploración (docs/informe_*.md)

Tres agentes barrieron la web el 27/8 y dejaron **124 propuestas verificadas con URL**, ninguna
repetida de las que ya están en el catálogo:

| archivo | qué trae |
|---|---|
| `informe_1_agenda_29ago_6sep.md` | qué pasa esos nueve días: muestras temporales, ópera gratis, festivales, cierres |
| `informe_2_joyas_por_barrio.md` | 56 lugares poco conocidos en los barrios del recorrido |
| `informe_3_comida.md` | 35 lugares de comida, atados a los huecos reales del itinerario |

`build_informe.py` los convierte en `informe_exploracion.html`: una sola página con las 124
fichas, filtros por informe y por texto, y la **misma mecánica de tres estados que la app**
(★ / ✕ / sin marcar) guardada en `localStorage`, con un botón que copia la selección al
portapapeles. Es una herramienta de decisión, no un documento de lectura — se revisa desde el
celular y lo que sale se pega en el chat.

⚠️ **Dentro de un Artifact la página corre en un iframe con sandbox, y ahí NO existen
`navigator.clipboard`, `alert()`, `confirm()` ni `prompt()`** — fallan sin tirar error, así que
el botón parece roto y no hay nada en consola. La primera versión del exportador usaba los
cuatro y Juan reportó que no podía exportar. Lo que sí funciona: `document.execCommand('copy')`
sobre un `<textarea>` con el texto ya seleccionado, y paneles inline en vez de diálogos. Para
probarlo hay que cargar la página **dentro de un iframe con `sandbox`** — servida por http, no
por `file://` — porque suelta funciona perfecto y el bug no aparece.

**Son material crudo para revisar, no catálogo.** Lo que se apruebe entra por el mismo camino
que la tanda de exploración: `a(...)` en `build_places.py`, interés 1/1, coordenadas
geocodificadas y validadas, sin `hrs` salvo verificación contra fuente oficial.

Cada ítem trae su **nivel de confianza** y la URL. Lo que los agentes no pudieron confirmar está
marcado como tal en vez de omitido — varios sitios (Dizzy's, Birdland, Smalls) cargan la
cartelera por JavaScript y no se dejan leer.

---

## La app nueva y cómo volver atrás

El **27/8 a la noche la interfaz rediseñada pasó a ser la principal**. Quedaron así:

| archivo | qué es | estado en el navegador |
|---|---|---|
| `src/app_template.html` | la app **actual** (la rediseñada) | `nyc2026.v1` — hereda las marcas y notas |
| `src/app_template_anterior.html` | la que estuvo publicada hasta esa noche | — |
| `index.html` | lo que sirve GitHub Pages | `nyc2026.v1` |
| `v1.html` | la anterior, para comparar | `nyc2026.anterior` — no pisa nada |

`build_anterior.py` genera `v1.html`. **No corre dentro de `build_all.py`**: se corre a mano
cuando se quiere regenerar la vieja.

**PARA VOLVER ATRÁS**, si la nueva no convence:

```bash
git mv src/app_template.html src/app_template_v2.html
git mv src/app_template_anterior.html src/app_template.html
python3 src/build_all.py --test && git commit -am "vuelvo a la interfaz anterior" && git push
```

El estado guardado sobrevive: las dos usan `nyc2026.v1` y `fresh`/`migrate`/`hydrate` son
idénticos byte por byte entre las dos.

**Lo que cambió**: tarjeta «Ahora» que cruza la hora con el itinerario, bloques plegados con un
toque para expandir (el día 7 pasó de 5.540 px a 1.652), tres pesos visuales, header y pestañas
en un solo sticky, y swipe para cambiar de día.

⚠️ **Los bloques vienen plegados y el detalle no está en el DOM hasta tocarlos.** Los tests que
miran chips, notas, ▲▼✕ o referencias tienen que llamar a `desplegar()` primero — está en
`test_app.py`. Trece chequeos fallaron por esto y ninguno era una función rota.

---


## Cuando el deploy de Pages se cuelga

El 27/8 a la tarde el sitio quedó dos horas sin actualizarse: `build` pasaba en 20 segundos y
`deploy` moría a los 10 minutos exactos con `Timeout reached, aborting!`, repitiendo
`Current status: updating_pages` y después `Current status:` vacío. Qué se aprendió:

- **`duration: 0ms` en `gh api repos/yampo/nyc-2026/pages/builds/latest` = el build ni arrancó.**
  Si fuera el contenido, construiría algo y fallaría con un error concreto. Ese cero apunta a
  infraestructura, no a nuestro HTML.
- **No reintentes con `gh run rerun`.** Deja un run en `queued` que no se puede cancelar
  (`Cannot cancel a workflow re-run that has not yet queued`, HTTP 409) y encima ensucia el
  estado. La salida buena es **un commit nuevo**: SHA distinto, deployment limpio, sin arrastrar
  los deployments fallidos del SHA anterior.
- El sitio **sigue sirviendo la última versión buena** mientras tanto. No hay urgencia real:
  lo publicado no se rompe, solo no se actualiza.
- Diagnóstico rápido: `gh api repos/yampo/nyc-2026/pages --jq .status` (`built` vs `errored`) y
  `gh api repos/yampo/nyc-2026/pages/builds` para ver el historial con duraciones.

Desde entonces el repo tiene **`.nojekyll`** en la raíz. El sitio es HTML estático con todo
embebido y no usa Jekyll para nada, así que procesarlo era 40 segundos de trabajo inútil y una
etapa más donde fallar.

---

## Versionado — cómo volver a un push anterior

Cada push a `main` es una versión completa y recuperable. Nada se pisa: GitHub Pages sirve
siempre el último, pero los anteriores siguen enteros en la historia.

**El puente entre lo que Juan ve y lo que hay en git** es el sello de versión (⋯ → *Versión del
plan* en la app). `build_all.py` lo imprime al terminar y sugiere taggear el commit con él, así
"volvé a `3d09bc`" es una orden ejecutable:

```bash
git tag -a v-3d09bc -m "26 ago 2026 · 18:10"
git push --tags
```

**Para deshacer el último push** (lo correcto en un sitio ya publicado: crea un commit nuevo que
revierte, no reescribe historia, y pushea sin pelear):

```bash
git revert HEAD          # o: git revert <sha>
git push                 # Pages redespliega el estado anterior en 1-2 min
```

**Para volver solo el sitio a una versión vieja**, sin tocar el resto:

```bash
git checkout <sha> -- index.html && git commit -m "vuelvo a <verId>" && git push
```

⚠️ Pero eso **desincroniza el sitio del código que lo generó**. Si vas a volver atrás de verdad,
volvé el fuente y reconstruí — así lo publicado y lo que lo produce siguen siendo lo mismo:

```bash
git checkout <sha> -- src/ && .venv/bin/python src/build_all.py --test && git commit -am "..." && git push
```

**Para mirar antes de decidir:**

```bash
git log --oneline -- index.html                      # todas las versiones publicadas
git diff <sha> HEAD -- src/build_itinerary.py        # qué cambió de verdad
git show <sha>:index.html | grep -o '"verId":"[^"]*"' # qué versión era ese commit
```

> **`git revert`, no `git reset --hard` + `push --force`.** El reset reescribe la historia: si
> Thais ya tiene el sitio abierto y vos rehacés el pasado, no hay forma de reconstruir qué vio.
> El revert deja el error y la corrección, los dos, a la vista.

> **Limitación honesta:** los commits **anteriores al 26/8 22:00** tienen el `index.html`
> publicado pero **no el código que lo generó** — el fuente entró al repo recién en ese push.
> Se pueden restaurar como archivo, no reconstruir desde el fuente. De ahí en adelante, cada
> commit tiene las dos cosas.

---

## Cómo trabaja Juan

Está en `~/.claude/skills/coe-defaults/` si lo tenés instalado. Lo que más pesa acá:

- **Contestale en castellano rioplatense**, directo, sin rodeos ni preámbulos.
- **Tomá posición.** Si te pide algo que va a salir mal, decíselo y proponé la alternativa.
  Si una decisión tiene un costo, nombralo — él prefiere el costo dicho al costo escondido.
- **No inventes.** Si un horario, un precio o una disponibilidad no está verificado, decilo así.
  Los datos del viaje se verifican contra la fuente, no contra la memoria.
- **Backup y changelog antes de tocar archivos** que no creaste vos.
- Cada cambio que se ve en la app **se escribe también en `LEEME.md`**, en castellano y sin jerga:
  ese archivo lo leen él y Thais, no un programador.

---

## Rutina de trabajo sugerida

```bash
git pull                              # SIEMPRE primero
# … editar src/build_*.py o src/app_template.html …
.venv/bin/python src/build_all.py --test       # build + 66 chequeos
git add -A && git commit -m "..." && git push     # esto publica
```

Después del push, mirá que el workflow `pages-build-deployment` haya quedado verde en
https://github.com/yampo/nyc-2026/actions
