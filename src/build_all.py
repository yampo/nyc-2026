#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Corre TODA la cadena de build en el orden correcto y, si el proyecto esta dentro del repo,
deja el index.html publicable en la raiz.

    python3 build_all.py            # build completo
    python3 build_all.py --test     # build + las dos suites de Playwright

El orden NO es negociable: places -> itinerary -> extras -> app -> pages -> xlsx.
Cada paso lee el JSON que escribio el anterior.
"""
import subprocess, sys, os

BASE = os.path.dirname(os.path.abspath(__file__))
PASOS = [
    ("build_places.py",    "catalogo de lugares  → data/places.json"),
    ("build_itinerary.py", "9 dias de itinerario → data/itinerary.json"),
    ("build_extras.py",    "transporte/reservas  → data/extras.json"),
    ("build_app.py",       "app local + web      → NYC_2026_Itinerario.html, NYC_2026_web.html"),
    ("build_pages.py",     "sitio con Leaflet    → pages/index.html (+ index.html de la raiz)"),
    ("build_xlsx.py",      "planilla             → NYC_2026_Planificador.xlsx"),
]
TESTS = [("test_app.py", "43 chequeos generales"), ("test_marca.py", "16 chequeos de la marca ★/✕/☆")]

def corre(script, que):
    print(f"\n── {script}  ({que})")
    r = subprocess.run([sys.executable, os.path.join(BASE, script)], cwd=BASE)
    if r.returncode:
        sys.exit(f"\n✗ FALLO {script} (codigo {r.returncode}). La cadena se corta acá: "
                 f"los pasos siguientes leerian datos viejos.")

for s, q in PASOS: corre(s, q)

# Los entregables salen dentro de src/ porque cada script trabaja relativo a si mismo.
# Si estamos adentro del repo, subirlos a la raiz: es donde Juan y Thais los buscan,
# y donde GitHub Pages lee el index.html.
RAIZ = os.path.dirname(BASE)
if os.path.isdir(os.path.join(RAIZ, ".git")):
    import shutil
    for f in ("NYC_2026_Itinerario.html", "NYC_2026_Planificador.xlsx", "NYC_2026_web.html"):
        o = os.path.join(BASE, f)
        if os.path.exists(o):
            shutil.copy2(o, os.path.join(RAIZ, f)); print(f"   → {f} a la raiz")

if "--test" in sys.argv:
    for s, q in TESTS: corre(s, q)

# El sello que la app muestra en ⋯ → Version del plan. Ponerlo en el commit y en un tag deja
# la version que ve Juan en el celular apuntando a un commit exacto: "vuelvo a 3d09bc" pasa a
# ser una orden ejecutable en vez de una arqueologia.
try:
    import json, re
    _h = open(os.path.join(BASE, "pages/index.html"), encoding="utf-8").read(400_000)
    _m = re.search(r'"ver":"([^"]*)","verId":"([^"]*)"', _h)
    ver, vid = _m.group(1), _m.group(2)
    print(f"\n✓ Listo · version {ver} · {vid}")
    print(f"\n  git add -A && git commit -m \"<que cambiaste> [{vid}]\"")
    print(f"  git tag -a v-{vid} -m \"{ver}\"")
    print(f"  git push && git push --tags")
except Exception:
    print("\n✓ Listo. Para publicar: git add -A && git commit && git push")
