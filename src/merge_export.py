#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Toma un plan exportado desde la app (⋯ → Exportar mi plan) y BAJA sus marcas al catálogo,
para que dejen de vivir en un solo navegador y pasen a ser el valor por defecto que ven
todos — Juan, Thais, celular, compu y el sitio publicado.

  python3 merge_export.py <archivo.json>

Qué baja al catálogo (data/overrides.json), o sea qué se replica:
  · la MARCA de cada lugar: ★ imprescindible / ✕ no imprescindible / sin marcar
  · interés JP / TH (interest)

Qué NO baja, a propósito:
  · tildes de "hecho" y notas personales → son el progreso de cada uno, no del plan.
    Si algún día las querés compartir, hay que decidirlo explícitamente: arrancar el viaje
    con bloques ya tildados o con las notas de otro sería confuso.
"""
import json, sys, os

if len(sys.argv) < 2:
    sys.exit("uso: python3 merge_export.py <plan-exportado.json>")

base = os.path.dirname(os.path.abspath(__file__))
exp = json.load(open(sys.argv[1], encoding="utf-8"))
if not isinstance(exp, dict) or "itin" not in exp:
    sys.exit("Ese archivo no parece un plan exportado por la app (no tiene 'itin').")

places = {p["id"]: p for p in json.load(open(os.path.join(base, "data/places.json")))["places"]}
ovf = os.path.join(base, "data/overrides.json")
ov = json.load(open(ovf, encoding="utf-8")) if os.path.exists(ovf) else {}

def fila(pid):
    """El override de un lugar, arrancando del valor que ya tiene el catálogo."""
    if pid not in ov:
        p = places[pid]
        ov[pid] = {"jp": p["jp"], "th": p["th"]}
    return ov[pid]

cambios_marca, cambios_int, desconocidos = [], [], []
_NOM = {1: "★ imprescindible", -1: "✕ no imprescindible", 0: "sin marcar"}

# ── MARCA (tres estados) ──
# S.must del navegador es un DELTA sobre el catalogo, no el estado completo: markOf() usa
# el valor del catalogo cuando la clave no esta (ver app_template.html). Por eso un lugar
# AUSENTE del export significa "no lo toco", NUNCA "lo desmarco" — desmarcar escribe la
# clave con 0 o -1. Barrer los ausentes borraba las estrellas que Juan no habia tocado.
#
# El 0 cambio de sentido entre versiones y la app lo estampa en s.mv:
#   mv >= 2  → 0 es "sin marcar"        (semantica actual)
#   mv < 2   → 0 era "des-marcar", o sea "no es imprescindible" = -1
_MV = exp.get("mv") or 0
def _norm(v):
    if v is True: return 1
    if isinstance(v, (int, float)):
        if v > 0: return 1
        if v < 0: return -1
        return 0 if _MV >= 2 else -1
    return 0 if _MV >= 2 else -1

marcas = exp.get("must") or {}
for pid, v in marcas.items():
    if pid not in places:
        desconocidos.append(pid); continue
    quiere = _norm(v)
    tiene = places[pid].get("must") or 0
    if quiere != tiene:
        fila(pid)["must"] = quiere
        cambios_marca.append((places[pid]["n"], tiene, quiere))

# ── INTERESES ──
for pid, v in (exp.get("interest") or {}).items():
    if pid not in places:
        desconocidos.append(pid); continue
    jp, th = int(v.get("jp", 0)), int(v.get("th", 0))
    if (jp, th) != (places[pid]["jp"], places[pid]["th"]):
        f = fila(pid)
        cambios_int.append((places[pid]["n"], (f["jp"], f["th"]), (jp, th)))
        f["jp"], f["th"] = jp, th

json.dump(ov, open(ovf, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print(f"MARCAS cambiadas ({len(cambios_marca)}):")
for n, a, b in sorted(cambios_marca):
    print(f"   {n[:44]:46s} {_NOM[a]:22s} → {_NOM[b]}")
print(f"\nIntereses cambiados ({len(cambios_int)}):")
for n, a, b in sorted(cambios_int): print(f"   {n[:44]:46s} {a} → {b}")
if desconocidos:
    print("\n⚠️ ids que ya no existen en el catálogo (ignorados):", ", ".join(sorted(set(desconocidos))))

# lo personal que quedó afuera, para poder decirlo con números
tildes = sum(1 for d in exp["itin"] for b in d["blocks"] if b.get("done"))
notas  = sum(1 for d in exp["itin"] for b in d["blocks"] if (b.get("mynote") or "").strip())
propios = sum(1 for d in exp["itin"] for b in d["blocks"] if str(b.get("id", "")).startswith("x"))
print(f"\nNO se bajaron (personales): {tildes} tildes de hecho · {notas} notas · "
      f"{propios} bloques agregados a mano · {len(exp.get('res') or {})} reservas marcadas")
print(f"overrides.json: {len(ov)} lugares")
