---
name: estado
description: Dónde está el viaje y qué decisiones quedan abiertas.
disable-model-invocation: true
---

Contale en qué estado está esto. Mirá, en este orden:

1. `CLAUDE.md`, sección *Cómo está hoy*.
2. `git log --oneline -8` y `git status -sb`: si el repo está atrás o adelante de origin, decilo primero.
3. `.venv/bin/python src/recalc_report.py`: qué quieren ir y no está agendado, conflictos, huecos.
4. Los ★ imprescindibles que NO están en el itinerario (los calcula el reporte del punto 3).

Cerrá con las decisiones que dependen de él, no con un resumen de archivos.
