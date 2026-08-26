# NYC 2026 — contexto para trabajar este proyecto

> **PRIMERA VEZ — borrar este bloque cuando esté hecho.**
> Si existe la carpeta `setup-claude/`, el proyecto todavía no está instalado.
> Leé `setup-claude/INSTALAR.md` y hacelo vos, sin pedirle comandos a Juan.

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
python3 src/build_all.py            # cadena completa
python3 src/build_all.py --test     # cadena + las dos suites de Playwright
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

**Dependencias:** `pip install openpyxl playwright && playwright install chromium`.
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
  test_app.py              25 chequeos de la app con Playwright
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
- **`git` sobre las carpetas montadas del bridge deja `.git/*.lock` que no se pueden borrar.**
  Desde VS Code, con git nativo, esto no pasa — pero si volvés a laburar por el bridge, ojo.

---

## Cómo está hoy

Versión visible en la app en **⋯ → Versión del plan**.

- **210 lugares** · 63 en las dos listas, 71 solo de Google Maps, 76 solo nuestros.
- **34 ★ imprescindibles**, 33 de ellos ya en el itinerario.
- **9 días, 142 bloques**, 32 ítems en el checklist de reservas.
- Anclas fijas ya compradas o con horario cerrado: festival Charlie Parker (28/8),
  Birdland lun 31/8 20:30, Top of the Rock lun 31/8 ~18:00, día completo del WTC el jue 3/9,
  MO Lounge + Dizzy's jue 3/9, SUMMIT al atardecer vie 4/9 18:10,
  **Village Vanguard vie 4/9 22:00 — entradas compradas**, Peter Luger sáb 5/9 17:00,
  Café Wha sáb 5/9 23:45.

### Pendiente

1. **MoMA PS1** es el único ★ que no está en el itinerario. Necesita hueco o que Juan lo baje.
2. Cuando Juan termine de marcar ★ / ✕, **rearmar el itinerario garantizando que todos los ★
   entren**, mostrando explícitamente qué hay que sacar o mover. Ese pedido ya está hecho.
3. Verificaciones previas al viaje: orden de artistas del festival (28/8), rotonda del Guggenheim,
   alertas de NJ Transit (noche del 2/9 y mañana del 3/9), AirTrain, calendario del Lincoln Center
   Atrium, ticket con horario del Studio Museum.

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
git checkout <sha> -- src/ && python3 src/build_all.py --test && git commit -am "..." && git push
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
python3 src/build_all.py --test       # build + 41 chequeos
git add -A && git commit -m "..." && git push     # esto publica
```

Después del push, mirá que el workflow `pages-build-deployment` haya quedado verde en
https://github.com/yampo/nyc-2026/actions
