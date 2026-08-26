# NYC 2026

Planificador del viaje a Nueva York (29 ago – 6 sep 2026), para Juan Pablo y Thais.

**El sitio:** https://yampo.github.io/nyc-2026/ — abrilo en el celular, Compartir → Añadir a
pantalla de inicio. Tiene el mapa de calles y guarda tus cambios en ese teléfono.

**Cómo leerlo:** `LEEME.md` explica qué hace cada pestaña, en castellano y sin jerga.

## Para desarrollar

El sitio se genera; `index.html` **no se edita a mano**.

```bash
python3 src/build_all.py --test       # reconstruye todo y corre los 41 chequeos
git add -A && git commit -m "..." && git push
```

El push dispara `pages-build-deployment` y el sitio queda actualizado en 1-2 minutos.

`CLAUDE.md` tiene el contexto completo del proyecto: modelo de datos, orden del build,
y la lista de cosas que ya rompieron una vez y no conviene repetir.

Requiere `pip install openpyxl playwright && playwright install chromium`.
