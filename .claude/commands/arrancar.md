---
name: arrancar
description: Deja el proyecto listo para trabajar: sincroniza con GitHub, instala lo que falte, reconstruye y verifica. Correr una sola vez, la primera.
disable-model-invocation: true
---

Poné el proyecto en marcha. Hacé los pasos vos, no se los pidas al usuario. Contá al final en
castellano rioplatense qué pasó y qué quedó pendiente, sin recitar cada comando.

1. `git pull`. El clon arranca varios commits atrás; los archivos nuevos están sin trackear, así
   que el pull debería entrar limpio. Si hubiera conflicto, PARÁ y explicá qué chocó.

2. Dependencias. `python3 -V` y probá `python3 -c "import openpyxl"`.
   Si falta: creá `.venv` con `python3 -m venv .venv`, instalá `openpyxl` con
   `.venv/bin/pip`, y usá `.venv/bin/python3` de ahí en adelante.
   En macOS `pip install` a secas puede fallar con *externally-managed-environment*: el venv lo
   resuelve. Agregá `.venv/` al `.gitignore` de la raíz si no está.
   `playwright` es opcional (solo para los tests, ~150 MB): preguntá antes de bajarlo.

3. `.venv/bin/python src/build_all.py --test` — o sin `--test` si no hay playwright.
   Tiene que cerrar sin ninguna línea `FAIL` y con `16 ok · 0 fallas` en la suite de marcas.
   Si algo falla, PARÁ y mostrá qué.

4. Si el build dejó cambios sin commitear, commiteá el fuente:
   `git add -A && git commit -m "El fuente entra al repo: build en src/, publicar pasa a ser push"`
   **No pushees**: avisale y esperá que te diga.

5. `bash taggear_versiones_publicadas.sh` para poder volver a cualquier versión ya publicada por
   su sello. El script pushea tags: pedí confirmación antes.

6. Leé `CLAUDE.md` y cerrá contándole en qué estado está el viaje y qué decisiones le quedan
   abiertas.
