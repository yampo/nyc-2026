#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera NYC_2026_Itinerario.html inyectando los datos + hash de versión del itinerario."""
import json, hashlib, pathlib

base = pathlib.Path(__file__).parent
pj = json.load(open(base / "data/places.json"))
itin = json.load(open(base / "data/itinerary.json"))["days"]
d = {
    "places": pj["places"],
    "subs": pj["subs"],
    "itinerary": itin,
    "extras": json.load(open(base / "data/extras.json")),
    # hash del itinerario base: si cambia, la app migra el estado guardado
    "itinHash": hashlib.md5(json.dumps(itin, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:12],
}
# Sello de versión: fecha de generación + huella del contenido. Sirve para que Juan y Thais,
# que abren la MISMA URL, puedan confirmar si están viendo la última o una cacheada.
import datetime, os as _os
_MES = ["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"]
_now = datetime.datetime.now()
d["ver"] = f"{_now.day} {_MES[_now.month-1]} {_now.year} · {_now:%H:%M}"
d["verId"] = hashlib.md5(
    (json.dumps(d["places"], sort_keys=True, ensure_ascii=False)
     + json.dumps(itin, sort_keys=True, ensure_ascii=False)
     + json.dumps(d["extras"], sort_keys=True, ensure_ascii=False)).encode()
).hexdigest()[:6]
tpl = (base / "app_template.html").read_text(encoding="utf-8")
assert "/*__DATA__*/" in tpl
out = tpl.replace("/*__DATA__*/", json.dumps(d, ensure_ascii=False, separators=(",", ":")))
(base / "NYC_2026_Itinerario.html").write_text(out, encoding="utf-8")
print(f"HTML ok · itinHash={d['itinHash']} · {round(len(out)/1024)} KB")

# ── Versión WEB (para publicar como sitio) ────────────────────────────────────
# El hosting de Claude aplica un CSP estricto: bloquea recursos de otros dominios.
# Por eso esta versión sale SIN Leaflet (mapa de calles) y usa el esquema SVG propio,
# que no necesita ni librerías ni internet. Todo lo demás es idéntico.
import re
web = out
web = re.sub(r'\s*<link rel="stylesheet" href="https://cdnjs[^>]*>', '', web)
web = re.sub(r'\s*<script src="https://cdnjs[^<]*</script>', '', web)
assert 'cdnjs' not in web, "quedaron referencias a CDN"
assert 'tile.openstreetmap.org' in web  # queda en el código del mapa, que en el artifact no corre
# el Artifact envuelve el contenido: se entrega sin doctype/html/head/body
m = re.search(r'<head>(.*?)</head>.*?<body[^>]*>(.*)</body>', web, re.S)
assert m, "no pude separar head/body"
head, body = m.group(1), m.group(2)
head = re.sub(r'<meta charset[^>]*>|<meta name="viewport"[^>]*>', '', head)
head = head.replace('<title>NYC 2026 · JP &amp; Thais</title>', '<title>NYC 2026</title>')
head = head.replace('<title>NYC 2026 · JP & Thais</title>', '<title>NYC 2026</title>')
(base / "NYC_2026_web.html").write_text(head.strip() + "\n" + body.strip(), encoding="utf-8")
print(f"WEB ok · {round(len((base / 'NYC_2026_web.html').read_text(encoding='utf-8'))/1024)} KB · sin dependencias externas")
