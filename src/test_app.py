import os
_R = os.path.dirname(os.path.abspath(__file__))   # todo se resuelve relativo a este archivo, no a donde se corra
import os as _os
_BASE = _os.path.dirname(_os.path.abspath(__file__))
#!/usr/bin/env python3
"""Prueba la app: errores de consola, navegación entre pestañas, interacciones y capturas."""
from playwright.sync_api import sync_playwright
import pathlib, sys, json

BASE = sum(len(d["blocks"]) for d in json.load(open(os.path.join(_R, "data/itinerary.json")))["days"])

URL = "file://" + _os.path.join(_BASE, "NYC_2026_Itinerario.html")
errors, console = [], []

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 430, "height": 940})   # iPhone-ish
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.on("console", lambda m: console.append(f"{m.type}: {m.text}") if m.type in ("error", "warning") else None)
    pg.goto(URL); pg.wait_for_timeout(1200)

    def check(label, fn):
        n0 = len(errors)
        try: fn()
        except Exception as e: errors.append(f"[{label}] excepción: {e}")
        pg.wait_for_timeout(450)
        print(f"  {'FAIL' if len(errors) > n0 else 'ok  '}  {label}")

    print("── navegación ──")
    for tab, name in [("itin","Itinerario"),("places","Lugares"),("map","Mapa"),
                      ("costs","Costos"),("trans","Transporte"),("res","Reservas")]:
        check(name, lambda t=tab: pg.click(f'.tab[data-t="{t}"]'))
        if tab == "map": pg.wait_for_timeout(1800)
        pg.screenshot(path=f"/tmp/shot_{tab}.png", full_page=(tab not in ("map",)))

    print("── interacciones ──")
    pg.click('.tab[data-t="itin"]'); pg.wait_for_timeout(300)
    check("cambiar de día (día 5)", lambda: pg.click('.dbtn[data-d="5"]'))
    check("marcar bloque hecho", lambda: pg.click('.blk .ck'))
    check("mover bloque abajo", lambda: pg.click('.blk .mini[data-act="down"]'))
    check("abrir ficha de lugar", lambda: pg.click('.blk .chip[data-act="info"]'))
    check("cerrar ficha", lambda: pg.click('#ov', position={"x": 10, "y": 10}))
    check("abrir campo de nota", lambda: pg.click('.blk .notebtn'))
    check("escribir nota", lambda: pg.fill('.blk .bnote', 'probando nota'))
    check("agregar lugar al día", lambda: (pg.click('#addBlk'), pg.wait_for_timeout(400),
                                           pg.click('#pl .opt')))
    pg.click('.tab[data-t="places"]'); pg.wait_for_timeout(400)
    check("buscar 'jazz'", lambda: pg.fill('#q', 'jazz'))
    check("filtro no turístico", lambda: pg.click('#th'))
    check("filtro gratis", lambda: pg.click('#tf'))
    check("toggle de interés", lambda: pg.click('.pc .ib[data-w="jp"]'))
    check("filtro categoría", lambda: pg.select_option('#fc', 'museo'))
    pg.click('.tab[data-t="map"]'); pg.wait_for_timeout(1500)
    check("mapa: filtrar por día", lambda: pg.select_option('#mday', '2'))
    pg.wait_for_timeout(1500)
    pg.screenshot(path="/tmp/shot_mapday.png")
    pg.click('.tab[data-t="res"]'); pg.wait_for_timeout(300)
    check("marcar reserva", lambda: pg.click('#v-res [data-r="0"]'))
    check("menú de datos", lambda: pg.click('#bMenu'))
    check("cerrar menú", lambda: pg.click('#ov', position={"x": 10, "y": 10}))
    check("filtro por persona", lambda: (pg.click('#bWho'), pg.wait_for_timeout(350),
                                         pg.click('#sheet [data-w="jp"]')))

    print("── persistencia ──")
    CNT = ("(()=>{const s=JSON.parse(localStorage.getItem('nyc2026.v1'));"
           "return {done:s.itin.reduce((a,d)=>a+d.blocks.filter(b=>b.done).length,0),"
           "notes:s.itin.reduce((a,d)=>a+d.blocks.filter(b=>b.mynote).length,0),"
           "res:Object.values(s.res).filter(Boolean).length,"
           "ints:Object.keys(s.interest).length,"
           "blocks:s.itin.reduce((a,d)=>a+d.blocks.length,0)}})()")
    a = pg.evaluate(CNT)
    pg.reload(); pg.wait_for_timeout(1200)
    b2 = pg.evaluate(CNT)
    ok = a == b2 and a["done"] == 1 and a["notes"] == 1 and a["res"] == 1 and a["ints"] == 1 and a["blocks"] == BASE + 1
    print(f"  {'ok  ' if ok else 'FAIL'}  persistencia {a} → {b2}")
    print(f"        esperado: done=1 notes=1 res=1 ints=1 blocks={BASE+1} ({BASE} base + 1 agregado)")
    if not ok: errors.append(f"persistencia/doble-disparo: {a}")

    # sanidad de datos
    st = pg.evaluate("({p: PLACES.length, d: S.itin.length, "
                     "blocks: S.itin.reduce((a,x)=>a+x.blocks.length,0), "
                     "nocoord: PLACES.filter(p=>!p.lat).length})")
    print(f"\n  datos: {st['p']} lugares · {st['d']} días · {st['blocks']} bloques · sin coordenadas: {st['nocoord']}")
    b.close()

print("\n── errores JS ──")
print("\n".join(errors) if errors else "  ninguno ✓")
if console: print("\n── consola (error/warning) ──\n  " + "\n  ".join(console[:12]))
sys.exit(1 if errors else 0)
