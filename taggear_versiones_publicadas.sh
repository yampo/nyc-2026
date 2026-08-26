#!/bin/bash
# Taggea las versiones que ya estan publicadas, para poder volver a cualquiera por su verId
# (el sello que muestra la app en ⋯ → Version del plan). Correr una sola vez, desde el repo.
set -e
git tag -a v-74dc31 044b2fe -m "26 ago 2026 · 22:05 — saca los digitos de la tarjeta"      2>/dev/null || echo "v-74dc31 ya existe"
git tag -a v-3d09bc 9a3438b -m "26 ago 2026 · 18:10 — marca de tres estados ★/✕/☆"         2>/dev/null || echo "v-3d09bc ya existe"
git tag -a v-a1f9ad 3d44500 -m "26 ago 2026 · 16:10 — entradas del Vanguard"                2>/dev/null || echo "v-a1f9ad ya existe"
git tag -a v-d24f37 477dff7 -m "26 ago 2026 · 15:09 — scroll + imprescindibles + Vanguard"  2>/dev/null || echo "v-d24f37 ya existe"
git tag -a v-f913c4 29ccf1b -m "26 ago 2026 · 14:06 — sello de version"                     2>/dev/null || echo "v-f913c4 ya existe"
git push --tags
echo
echo "Listo. Ahora:  git tag -n   te lista las versiones publicadas"
echo "y             git checkout v-d24f37 -- index.html   vuelve el sitio a esa"
