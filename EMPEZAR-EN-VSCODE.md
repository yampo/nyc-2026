# Arrancar en VS Code

Seis pasos. Los tres primeros son obligatorios; el resto es para que los tests corran.

---

## 1. Abrir la carpeta

VS Code → **File → Open Folder…** → `Downloads/NYC/nyc-2026`

Tiene que ser **esa carpeta**, no `Downloads/NYC`. Es la que tiene el `.git` adentro: si abrís
la de arriba, VS Code no ve el repo y Claude no encuentra el `CLAUDE.md`.

## 2. Instalar la extensión de Claude Code

`Cmd+Shift+X` → buscar **"Claude Code"** → **Install**. Entrás con tu cuenta de Claude, no hace
falta API key. Si no aparece después de instalarla, Command Palette (`Cmd+Shift+P`) →
*Developer: Reload Window*.

Atajos que vas a usar: `Cmd+Esc` alterna entre el editor y Claude · `Cmd+Shift+Esc` abre una
conversación nueva en una pestaña.

## 3. Traer los 7 commits que te faltan

Terminal integrada (``Ctrl+` ``) y:

```bash
git pull
```

Tu clon está **7 commits atrás** — le falta todo lo de hoy. Los archivos que te dejé
(`CLAUDE.md`, `src/`, este archivo) están sin trackear, así que el pull entra limpio, sin
conflictos. Ya lo verifiqué.

Después de eso, el primer commit tuyo es el que mete el código al repo:

```bash
git add -A
git commit -m "El fuente entra al repo: build en src/, publicar pasa a ser push"
git push
```

---

## 4. Python y las dependencias

```bash
python3 -V                    # 3.9 o más
python3 -m venv .venv
source .venv/bin/activate     # esto hay que repetirlo cada vez que abrís una terminal nueva
pip install openpyxl
```

Agregá `.venv/` al `.gitignore` de la raíz después del pull, para no commitear el entorno.

Con `openpyxl` **el build ya corre entero**. Playwright es solo para los tests:

```bash
pip install playwright && playwright install chromium     # ~150 MB, opcional
```

Sin Playwright, `python3 src/build_all.py` funciona igual; lo único que no vas a poder es
`--test`. Vale la pena instalarlo: son los 53 chequeos que agarran los errores que ya rompieron
la app dos veces.

## 5. Probar que todo funciona

```bash
python3 src/build_all.py --test
```

Tiene que terminar sin ninguna línea FAIL, con `16 ok · 0 fallas` en la suite de marcas y el sello de versión. Si algo
falla acá, pasámelo antes de tocar nada.

## 6. Taggear las versiones que ya publicaste

Una sola vez, para poder volver a cualquiera por el sello que muestra la app:

```bash
bash taggear_versiones_publicadas.sh
```

Después, `git tag -n` te lista las versiones publicadas y
`git checkout v-d24f37 -- index.html` vuelve el sitio a esa.

---

## El ciclo, de acá en adelante

```bash
git pull                                   # siempre primero
# … pedirle a Claude lo que quieras cambiar …
python3 src/build_all.py --test            # reconstruye + 53 chequeos
git add -A && git commit -m "..." && git push
```

**El push publica.** No hay paso extra: GitHub Pages redespliega solo en 1-2 minutos y el sitio
queda actualizado para vos y para Thais.

## Lo primero que le podés pedir a Claude

> Leé el CLAUDE.md y decime en qué estado está el proyecto y qué quedó pendiente.

Está todo ahí: el modelo de datos, el orden del build, los pendientes reales (MoMA PS1 es el
único ★ que no entró en el itinerario) y la lista de cosas que ya costaron tiempo y no conviene
repetir.
