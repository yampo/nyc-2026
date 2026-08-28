#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Construye la V2 de la app — la versión donde se trabaja la interfaz — a partir de
`app_template_v2.html`, y la deja en `v2.html` en la raíz del repo.

POR QUÉ EXISTE, y qué NO hace:
  · La v1 (`app_template.html` → `index.html`) es la que Juan y Thais usan de verdad,
    con el viaje encima. Esta cadena NO la toca: escribe un archivo aparte.
  · Se publica igual con GitHub Pages, así que la v2 se puede abrir desde el celular
    en https://yampo.github.io/nyc-2026/v2.html y compararla con la v1 lado a lado,
    sin arriesgar nada.
  · Comparte EXACTAMENTE los mismos datos: lee los JSON que ya generó la cadena
    normal. Lo único distinto entre v1 y v2 es la interfaz.
  · El estado del navegador usa OTRA clave de localStorage, para que probar la v2
    no pise las marcas y notas que Juan tiene en la v1.

  python3 build_v2.py     (correr DESPUÉS de build_app.py)
"""
import base64, json, os, hashlib, datetime

_R = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(_R, "app_template_v2.html")
LF = os.path.join(_R, "vendor/leaflet")
OUT_RAIZ = os.path.join(os.path.dirname(_R), "v2.html")

if not os.path.exists(TPL):
    raise SystemExit("falta app_template_v2.html — es la copia sobre la que se trabaja la interfaz")

pj = json.load(open(os.path.join(_R, "data/places.json"), encoding="utf-8"))
itin = json.load(open(os.path.join(_R, "data/itinerary.json"), encoding="utf-8"))["days"]
d = {
    "places": pj["places"],
    "subs": pj["subs"],
    "itinerary": itin,
    "extras": json.load(open(os.path.join(_R, "data/extras.json"), encoding="utf-8")),
    "itinHash": hashlib.md5(json.dumps(itin, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:12],
}
_MES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
_now = datetime.datetime.now()
d["ver"] = f"{_now.day} {_MES[_now.month-1]} {_now.year} · {_now:%H:%M} · V2"
tpl = open(TPL, encoding="utf-8").read()
d["verId"] = hashlib.md5(
    (json.dumps(d["places"], sort_keys=True, ensure_ascii=False)
     + json.dumps(itin, sort_keys=True, ensure_ascii=False)
     + tpl).encode()).hexdigest()[:6]

assert "/*__DATA__*/" in tpl, "el template v2 perdió el marcador /*__DATA__*/"
html = tpl.replace("/*__DATA__*/", json.dumps(d, ensure_ascii=False, separators=(",", ":")))

# La v2 NO puede compartir el estado guardado con la v1: si comparten clave, probar
# la v2 pisaría las marcas y las notas que Juan tiene en la app de verdad.
assert "nyc2026.v1" in html, "no encontré la clave de localStorage en el template v2"
html = html.replace("nyc2026.v1", "nyc2026.v2")

# Leaflet embebido, igual que en build_pages.py: por índice de string, no por regex
# (el JS de Leaflet tiene escapes que rompen las plantillas de re.sub).
CSS_URL = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">'
JS_URL = '<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>'
css = open(os.path.join(LF, "leaflet.css"), encoding="utf-8").read()
for png in ("layers-2x.png", "layers.png", "marker-icon-2x.png", "marker-icon.png", "marker-shadow.png"):
    b64 = base64.b64encode(open(os.path.join(LF, "images", png), "rb").read()).decode()
    css = css.replace(f"images/{png}", f"data:image/png;base64,{b64}")
js = open(os.path.join(LF, "leaflet.js"), encoding="utf-8").read()

for url, nuevo in ((CSS_URL, "<style>\n" + css + "\n</style>"),
                   (JS_URL, "<script>\n" + js + "\n</script>")):
    i = html.find(url)
    assert i >= 0, "no encontré en el template v2: " + url[:60]
    html = html[:i] + nuevo + html[i + len(url):]

BANNER = ('<div style="background:#c1440e;color:#fff;padding:7px 14px;font:600 12.5px/1.4 '
          'ui-sans-serif,system-ui,sans-serif;text-align:center">VERSIÓN 2 — en pruebas. '
          'La app de verdad sigue en la raíz del sitio. Lo que marques acá no se mezcla con la otra.</div>')
i = html.find("<body>")
if i >= 0:
    html = html[:i + 6] + BANNER + html[i + 6:]

with open(OUT_RAIZ, "w", encoding="utf-8") as f:
    f.write(html)
print(f"V2 ok · {round(len(html)/1024)} KB · sello {d['verId']}")
print(f"   → {OUT_RAIZ}")
print("   la v1 no se tocó · estado en localStorage: nyc2026.v2")
