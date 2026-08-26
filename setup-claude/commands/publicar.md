---
name: publicar
description: Reconstruye, verifica y publica el sitio en GitHub Pages. Es el único camino para que un cambio llegue al celular de Juan y de Thais.
disable-model-invocation: true
---

Publicá el estado actual.

1. `git status` y `git diff --stat`: mostrá qué cambió antes de tocar nada.
2. `python3 src/build_all.py --test`. Si falla un chequeo, PARÁ. No se publica en rojo.
3. Commiteá con un mensaje que diga **qué cambia para el que usa la app**, no qué archivo tocaste,
   y con el sello de versión entre corchetes — `build_all.py` lo imprime al final.
   Taggeá con `git tag -a v-<verId> -m "<sello>"`.
4. `git push && git push --tags`. **Pedí confirmación antes del push**: publica en un sitio público
   que Thais también mira.
5. Después del push, decile que verifique que
   https://github.com/yampo/nyc-2026/actions quedó en verde (1-2 min), y con qué sello quedó el
   sitio para que lo compare con lo que ve en ⋯ → Versión del plan.
6. Si el cambio se ve en la app, escribilo también en `LEEME.md`: castellano, sin jerga. Ese
   archivo lo leen Juan y Thais.
