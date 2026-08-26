#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cruza los intereses actuales contra el itinerario y dice qué hay que cambiar.
No reescribe el itinerario solo: produce el informe para decidir con criterio.

  python3 recalc_report.py
"""
import json
from collections import defaultdict
import os
_R = os.path.dirname(os.path.abspath(__file__))   # todo se resuelve relativo a este archivo, no a donde se corra

places = json.load(open(os.path.join(_R, "data/places.json")))["places"]
P = {p["id"]: p for p in places}
days = json.load(open(os.path.join(_R, "data/itinerary.json")))["days"]

# Zona geográfica de cada día, para sugerir dónde encaja un lugar nuevo.
ZONA = {
 1: ["Hell's Kitchen", "Chelsea", "Meatpacking", "West Village", "Harlem", "Hudson Yards"],
 2: ["Financial District", "Governors Island", "Lower East Side", "East Village", "Chinatown"],
 3: ["Midtown", "Midtown East", "Financial District", "Murray Hill"],
 4: ["Lower East Side", "Chinatown", "DUMBO", "Brooklyn Heights", "West Village", "Greenwich Village"],
 5: ["Upper East Side", "East Harlem", "Central Park", "Roosevelt Island"],
 6: ["Long Island City", "Astoria", "Upper West Side", "Columbus Circle"],
 7: ["Chelsea", "Meatpacking", "West Village", "Greenwich Village", "Upper West Side"],
 8: ["Greenpoint", "Williamsburg", "Prospect Heights", "Bedford-Stuyvesant", "Park Slope",
     "Downtown Brooklyn", "Sunset Park", "Greenwood Heights", "Red Hook"],
 9: ["Upper West Side", "Central Park", "Upper East Side", "Lincoln Square"],
}
def dias_para(p):
    return [d for d, hoods in ZONA.items() if p["hood"] in hoods] or []

en_itin = defaultdict(list)
for d in days:
    for b in d["blocks"]:
        if b["pid"]: en_itin[b["pid"]].append(d["n"])

WHO = {"both": "ambos", "jp": "solo JP", "th": "Thais"}
sacar, conflicto, degradar = [], [], []
for d in days:
    for b in d["blocks"]:
        p = P.get(b["pid"])
        if not p or p["cat"] == "transporte": continue
        jp, th = p["jp"], p["th"]
        if d["who"] == "both":
            if jp == 0 and th == 0:
                sacar.append((d["n"], d["dow"], p, "los dos lo marcaron 0"))
            elif th == 0 and jp >= 1:
                conflicto.append((d["n"], d["dow"], p, "Thais 0 / JP " + str(jp)))
            elif jp == 0 and th >= 1:
                conflicto.append((d["n"], d["dow"], p, "JP 0 / Thais " + str(th)))
            elif jp == 1 and th == 1:
                degradar.append((d["n"], d["dow"], p, "ambos en 'quizás'"))
        else:  # día de JP solo
            if jp == 0:
                sacar.append((d["n"], d["dow"], p, "JP lo marcó 0"))
            elif jp == 1:
                degradar.append((d["n"], d["dow"], p, "JP en 'quizás'"))

falta_ambos, falta_jp, falta_th = [], [], []
for p in places:
    if p["id"] in en_itin or p["cat"] == "transporte": continue
    if p["jp"] == 2 and p["th"] == 2: falta_ambos.append(p)
    elif p["jp"] == 2: falta_jp.append(p)
    elif p["th"] == 2: falta_th.append(p)

def bloque(titulo, items, con_dia=True):
    print(f"\n{'═'*74}\n{titulo}  ({len(items)})\n{'═'*74}")
    if not items: print("   nada"); return
    if con_dia:
        for n, dow, p, motivo in sorted(items, key=lambda x: (x[0], x[2]["n"])):
            print(f"   Día {n} ({dow[:3]})  {p['n'][:38]:40s} {motivo}")
    else:
        for p in sorted(items, key=lambda x: (x["boro"], x["hood"], x["n"])):
            dd = dias_para(p)
            sug = f"→ entra bien en el día {', '.join(map(str, dd))}" if dd else "→ sin día natural: hay que hacerle lugar"
            print(f"   {p['n'][:34]:36s} {p['typ'][:20]:22s} {p['hood'][:18]:20s} {sug}")

bloque("SACAR DEL ITINERARIO — nadie que va ese día lo quiere", sacar)
bloque("CONFLICTO en día de a dos — uno lo quiere y el otro no", conflicto)
bloque("REVISAR — está agendado pero solo en 'quizás'", degradar)
bloque("FALTAN y los DOS los quieren (interés 2)", falta_ambos, con_dia=False)
bloque("FALTAN y los quiere JP (Thais no)", falta_jp, con_dia=False)
bloque("FALTAN y los quiere THAIS (JP no)", falta_th, con_dia=False)

print(f"\n{'═'*74}\nRESUMEN\n{'═'*74}")
tot = len([p for p in places if p["cat"] != "transporte"])
print(f"   Lugares en el catálogo (sin logística):   {tot}")
print(f"   Marcados 2 por JP:                       {sum(1 for p in places if p['jp']==2 and p['cat']!='transporte')}")
print(f"   Marcados 2 por Thais:                    {sum(1 for p in places if p['th']==2 and p['cat']!='transporte')}")
print(f"   Marcados 2 por los DOS:                  {sum(1 for p in places if p['jp']==2 and p['th']==2 and p['cat']!='transporte')}")
print(f"   Ya agendados:                            {len(en_itin)}")
print(f"   Bloques a sacar:                         {len(sacar)}")
print(f"   Conflictos en días de a dos:             {len(conflicto)}")
print(f"   Quieren ir y no están agendados:         {len(falta_ambos)+len(falta_jp)+len(falta_th)}")
