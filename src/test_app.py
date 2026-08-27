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

    print("── símbolos ──")
    def simbolos_seguros():
        """La brújula 🧭 (U+1F9ED, Emoji 11 / 2018) salía como un glyph roto: el botón
        estaba y no se veía. Ningún icono de la app puede depender de un emoji tan
        nuevo. Esta lista blanca es todo lo no-ASCII que la app tiene derecho a usar:
        símbolos Unicode de los 90 y emojis de Emoji 1.0 (2015). Para agregar uno
        nuevo, primero comprobalo en el aparato de Juan y después sumalo acá."""
        import unicodedata
        PERMITIDOS = set(
            "═─—–…“”‘’·«»⋯"          # tipografía y separadores
            "★☆✕✓✔→←↑↓↗↔▸▾▲▼●⊞☰＋"    # símbolos Unicode, todos anteriores a 2000
            "⚠❌✅📍🚇📅👥🕐🚫🔴"        # emojis, todos de Emoji 1.0 (2015)
            "\ufe0f"                  # variation selector-16
        )
        tpl = open(_os.path.join(_BASE, "app_template.html"), encoding="utf-8").read()
        malos = {}
        for ch in tpl:
            if ord(ch) < 0x2000 or ch in PERMITIDOS: continue
            if unicodedata.category(ch).startswith("L"): continue   # letras acentuadas
            malos[ch] = malos.get(ch, 0) + 1
        assert not malos, "símbolos sin verificar en el aparato: " + ", ".join(
            f"{c} (U+{ord(c):04X}, {malos[c]} usos)" for c in malos)
    check("sin símbolos que el aparato pueda no tener", simbolos_seguros)

    print("── ruta a Apple Maps ──")
    # El dia 7 es todo "both", asi que el filtro por persona que dejo el bloque
    # anterior no le esconde bloques.
    pg.click('.tab[data-t="itin"]'); pg.wait_for_timeout(300)
    pg.click('.dbtn[data-d="7"]'); pg.wait_for_timeout(300)

    def q(url):
        from urllib.parse import urlparse, parse_qsl
        u = urlparse(url); return u.path, parse_qsl(u.query)

    def chips_por_bloque():
        """Cada bloque con lugar tiene los DOS mapas: el plan B tiene que estar donde
        se lo necesita, parado en la calle, no solo en la hoja del día."""
        ap = pg.locator('#v-itin a.chip[data-nav="apple"]')
        go = pg.locator('#v-itin a.chip[data-nav="google"]')
        assert ap.count() >= 5, f"pocos chips de Apple: {ap.count()}"
        assert go.count() == ap.count(), f"Apple {ap.count()} vs Google {go.count()}"
        path, ps = q(ap.first.get_attribute("href")); d = dict(ps)
        assert path == "/directions", path
        assert d.get("mode") == "walking", d
        assert "destination" in d and "," in d["destination"], d
        assert "waypoint" not in d, "un bloque suelto no lleva waypoints"
        gu, gp = q(go.first.get_attribute("href")); gd = dict(gp)
        assert "google.com" in go.first.get_attribute("href"), gu
        assert gd.get("travelmode") == "walking", gd
        assert "destination" in gd, gd
        assert gd.get("destination") == d.get("destination"), "los dos mapas van a destinos distintos"
    check("cada bloque tiene los dos mapas, al mismo destino", chips_por_bloque)

    check("abre la hoja de ruta del día", lambda: pg.click('#rutaDia'))

    def lista_paradas():
        n = pg.locator('#rlist [data-rp]').count()
        assert n >= 5, f"paradas listadas: {n}"
    check("lista las paradas del día", lista_paradas)

    def ruta_pie():
        path, ps = q(pg.locator('#rw').get_attribute("href"))
        n = pg.locator('#rlist [data-rp]:checked').count()
        wp = [v for k, v in ps if k == "waypoint"]
        dest = [v for k, v in ps if k == "destination"]
        assert path == "/directions", path
        assert len(wp) == n - 1, f"{len(wp)} waypoints para {n} paradas"
        assert len(dest) == 1, dest
        assert ("mode", "walking") in ps, ps
        # nombre + direccion, NO coordenadas crudas: daddr/destination=lat,lng se
        # rompio en iOS 18.4 y un pin mudo no dice adonde va.
        import re as _re
        crudas = [t for t in wp + dest if _re.fullmatch(r"-?\d+\.\d+,-?\d+\.\d+", t)]
        assert not crudas, f"paradas como coordenadas crudas: {crudas}"
    check("ruta a pie: waypoints en orden + destino + mode", ruta_pie)

    def ruta_transporte():
        _, ps = q(pg.locator('#rt').get_attribute("href"))
        assert ("mode", "transit") in ps, ps
        assert any(k == "transit-preferences" for k, _ in ps), ps
    check("ruta en transporte: mode=transit + preferencias", ruta_transporte)

    def destildar():
        antes = len([1 for k, _ in q(pg.locator('#rw').get_attribute("href"))[1] if k == "waypoint"])
        pg.uncheck('#rlist [data-rp="0"]'); pg.wait_for_timeout(250)
        ahora = len([1 for k, _ in q(pg.locator('#rw').get_attribute("href"))[1] if k == "waypoint"])
        assert ahora == antes - 1, f"{antes} → {ahora}"
    check("destildar una parada la saca de la ruta", destildar)

    def sin_paradas():
        for c in pg.locator('#rlist [data-rp]').all():
            if c.is_checked(): c.uncheck()
        pg.wait_for_timeout(250)
        assert pg.locator('#rw').get_attribute("aria-disabled"), "el botón debería quedar deshabilitado"
        assert pg.locator('#raviso .banner').count() == 1, "falta el aviso"
    check("sin paradas elegidas no se puede abrir", sin_paradas)

    def gm_tramos():
        # volver a tildar todo: el chequeo anterior dejo la lista vacia
        for c in pg.locator('#rlist [data-rp]').all():
            if not c.is_checked(): c.check()
        pg.wait_for_timeout(300)
        filas = pg.locator('#rgm > div')
        assert filas.count() >= 1, "no arma tramos de Google"
        sel = pg.locator('#rlist [data-rp]:checked').count()
        cubiertas, mx = 0, 0
        for i in range(filas.count()):
            _, ps = q(filas.nth(i).locator('a.chip').first.get_attribute("href"))
            d = dict(ps)
            assert d.get("api") == "1", d
            assert d.get("travelmode") == "walking", d
            wps = d.get("waypoints", "").split("|") if d.get("waypoints") else []
            mx = max(mx, len(wps)); cubiertas += len(wps) + 1
        # 3 waypoints es el tope de Google en navegador movil, que es donde lo va a abrir
        assert mx <= 3, f"un tramo lleva {mx} waypoints"
        # los tramos tienen que cubrir TODAS las paradas elegidas: ni perder ni repetir
        assert cubiertas == sel, f"los tramos cubren {cubiertas} de {sel} paradas"
    check("Google Maps: tramos dentro del límite y sin perder paradas", gm_tramos)

    def gm_transporte():
        _, ps = q(pg.locator('#rgm > div').first.locator('a.chip').nth(1).get_attribute("href"))
        assert ("travelmode", "transit") in ps, ps
    check("Google Maps: el segundo link va en transporte", gm_transporte)


    check("cerrar la hoja", lambda: pg.click('#ov', position={"x": 10, "y": 10}))

    def plan_b_a_la_vista():
        """El plan B no sirve enterrado: la primera versión quedaba a 1025px en una
        pantalla de 844 y no se veía. Se mide achicando a un iPhone SE —la pantalla
        más chica— y recorriendo los 9 días, porque los que tienen más paradas son
        los que empujan la sección de Google fuera de la vista."""
        pg.set_viewport_size({"width": 375, "height": 667})
        try:
            for d in range(1, 10):
                pg.click(f'.dbtn[data-d="{d}"]'); pg.wait_for_timeout(120)
                pg.click('#rutaDia'); pg.wait_for_timeout(320)
                r = pg.evaluate("""() => {const g = document.querySelector('#rgm');
                    if (!g) return null;
                    const b = g.getBoundingClientRect();
                    return {bot: Math.round(b.bottom), vh: window.innerHeight};}""")
                assert r, f"D{d}: no existe la sección de Google"
                assert r["bot"] <= r["vh"], \
                    f"D{d}: Google termina en {r['bot']}px y la pantalla mide {r['vh']}px"
                pg.click('#ov', position={"x": 10, "y": 10}); pg.wait_for_timeout(120)
        finally:
            pg.set_viewport_size({"width": 430, "height": 940})
            pg.click('.dbtn[data-d="7"]'); pg.wait_for_timeout(150)
    check("el plan B se ve sin scrollear, en pantalla chica y los 9 días", plan_b_a_la_vista)

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
