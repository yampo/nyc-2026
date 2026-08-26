#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arma pages/index.html: el build local + Leaflet 1.9.4 EMBEBIDO (js, css y sus 5 PNG
como data URI), para que GitHub Pages sirva el mapa de calles sin depender de un CDN.
Se usa reemplazo por indice, no regex: el JS de Leaflet tiene escapes que rompen las plantillas.

  python3 build_pages.py     (correr DESPUES de build_app.py)
"""
import base64, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
# Leaflet 1.9.4 vendorizado (BSD-2-Clause) para no depender de npm ni de la red.
LF   = os.path.join(BASE, "vendor/leaflet")
if not os.path.isdir(LF):
    LF = os.path.join(BASE, "node_modules/leaflet/dist")
SRC  = os.path.join(BASE, "NYC_2026_Itinerario.html")
OUT  = os.path.join(BASE, "pages/index.html")

CSS_URL = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">'
JS_URL  = '<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>'
METAS = ('<meta name="robots" content="noindex, nofollow, noarchive">\n'
         '<meta name="googlebot" content="noindex, nofollow">\n'
         '<meta name="apple-mobile-web-app-capable" content="yes">\n'
         '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n'
         '<meta name="apple-mobile-web-app-title" content="NYC 2026">\n'
         '<meta name="theme-color" content="#14293d">')

html = open(SRC, encoding="utf-8").read()

# ── CSS de Leaflet con las imagenes adentro ──
css = open(os.path.join(LF, "leaflet.css"), encoding="utf-8").read()
for png in ("layers.png", "layers-2x.png", "marker-icon.png", "marker-icon-2x.png", "marker-shadow.png"):
    b64 = base64.b64encode(open(os.path.join(LF, "images", png), "rb").read()).decode()
    css = css.replace(f"images/{png}", f"data:image/png;base64,{b64}")
js = open(os.path.join(LF, "leaflet.js"), encoding="utf-8").read()

def swap(txt, old, new):
    i = txt.index(old)                      # index, no regex
    return txt[:i] + new + txt[i+len(old):]

html = swap(html, CSS_URL, "<style>/* Leaflet 1.9.4 (BSD-2-Clause) embebido */\n" + css + "\n</style>")
html = swap(html, JS_URL,  "<script>/* Leaflet 1.9.4 (BSD-2-Clause) embebido */\n" + js + "\n</script>")
html = swap(html, '<meta name="theme-color" content="#14293d">', METAS)

for _s in (CSS_URL, JS_URL, "cdnjs.cloudflare.com"):
    assert _s not in html, f"quedo una dependencia externa: {_s}"

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(html)
destinos = [OUT]

# Si este proyecto vive dentro del repo (src/ adentro de nyc-2026), el archivo que GitHub Pages
# publica es el index.html de la RAIZ: escribirlo ahi tambien para que un commit alcance.
raiz = os.path.dirname(BASE)
if os.path.isdir(os.path.join(raiz, ".git")):
    otro = os.path.join(raiz, "index.html")
    open(otro, "w", encoding="utf-8").write(html)
    destinos.append(otro)

print(f"PAGES ok · {len(html)//1024} KB · Leaflet embebido, sin CDN")
for d in destinos: print("   →", d)
