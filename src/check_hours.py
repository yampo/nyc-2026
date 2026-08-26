#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Valida cada bloque del itinerario contra el horario real de apertura del lugar."""
import json, sys
import os
_R = os.path.dirname(os.path.abspath(__file__))   # todo se resuelve relativo a este archivo, no a donde se corra
P = {p["id"]: p for p in json.load(open(os.path.join(_R, "data/places.json")))["places"]}
days = json.load(open(os.path.join(_R, "data/itinerary.json")))["days"]
DOW = {"Lunes":0,"Martes":1,"Miércoles":2,"Jueves":3,"Viernes":4,"Sábado":5,"Domingo":6}
def m(t):
    try: h,mi = t.split(":"); return int(h)*60+int(mi)
    except Exception: return None

problemas, sin_datos = [], 0
for d in days:
    wd = DOW[d["dow"]]
    for b in d["blocks"]:
        p = P.get(b["pid"])
        if not p: continue
        hrs = p.get("hrs")
        if not hrs: sin_datos += 1; continue
        w = hrs[wd]
        t = m(b["t"])
        if t is None: continue
        if w is None:
            problemas.append(f"D{d['n']} {d['dow'][:3]} {b['t']}  {p['n'][:34]:36s} CERRADO ese día")
        else:
            ap, ci = m(w[0]), m(w[1])
            if ci <= ap: ci += 24*60          # horario que cruza medianoche (ej. 05:15-02:00)
            if t < ap:
                problemas.append(f"D{d['n']} {d['dow'][:3]} {b['t']}  {p['n'][:34]:36s} abre {w[0]} → llega {ap-t} min ANTES")
            elif t >= ci:
                problemas.append(f"D{d['n']} {d['dow'][:3]} {b['t']}  {p['n'][:34]:36s} cierra {w[1]} → llega DESPUÉS del cierre")
            elif ci - t < 45:
                problemas.append(f"D{d['n']} {d['dow'][:3]} {b['t']}  {p['n'][:34]:36s} cierra {w[1]} → solo {ci-t} min de visita")
print(f"Bloques con horario cargado: {sum(1 for d in days for b in d['blocks'] if P.get(b['pid'],{}).get('hrs'))}")
print(f"Bloques sin datos de horario: {sin_datos} (parques, barrios, bares: no aplica)\n")
if problemas:
    print(f"⚠️  {len(problemas)} PROBLEMAS DE HORARIO\n" + "\n".join("   "+x for x in problemas))
else:
    print("✓ ningún bloque cae fuera del horario de apertura")
sys.exit(1 if problemas else 0)
