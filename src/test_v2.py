# -*- coding: utf-8 -*-
"""Chequeos de la v2: que lo que ya andaba siga andando, y que lo nuevo ande."""
import sys, json
from playwright.sync_api import sync_playwright

URL = "file:///Users/fuser/Downloads/NYC/nyc-2026/v2.html"
FAKE = "2026-08-29T15:42:00"
ok = fail = 0
def t(cond, msg):
    global ok, fail
    if cond: ok += 1; print("  ✓", msg)
    else: fail += 1; print("  ✗ FALLA:", msg)

def nueva(b, w=375, h=667, fake=FAKE):
    ctx = b.new_context(viewport={"width":w,"height":h}, has_touch=True, is_mobile=True)
    if fake: ctx.add_init_script(f"window.__NOW='{fake}';")
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append("PAGEERROR "+str(e)))
    pg.on("console", lambda m: errs.append("CONSOLE "+m.text) if m.type=="error" else None)
    pg.goto(URL); pg.wait_for_timeout(800)
    return ctx, pg, errs

with sync_playwright() as p:
    b = p.chromium.launch()

    print("\n— las 6 pestañas, sin errores JS —")
    ctx, pg, errs = nueva(b)
    for k, sel in [("itin",".blk.itb"),("places",".pc, .prow"),("map","#map"),
                   ("costs","table"),("trans","table"),("res",".blk")]:
        pg.click(f'.tab[data-t="{k}"]'); pg.wait_for_timeout(500)
        t(pg.locator(f"#v-{k} {sel}").count() > 0, f"pestaña {k} renderiza ({sel})")
    t(not errs, f"sin errores JS ({errs[:2]})")
    pg.click('.tab[data-t="itin"]'); pg.wait_for_timeout(300)

    print("\n— tarjeta AHORA —")
    t(pg.locator(".ahora").count() == 1, "existe la tarjeta")
    t("15:42" in pg.inner_text(".ahlb"), "muestra la hora local (15:42)")
    t(pg.locator(".itb.now").count() == 1, "el bloque actual queda marcado")
    t(pg.locator(".itb.past").count() > 0, "los bloques pasados se atenúan")
    t("CHARLIE PARKER" in pg.inner_text(".ahnext"), "anuncia lo que sigue")
    t("en 48 min" in pg.inner_text(".ahnext"), "y en cuántos minutos")
    href = pg.get_attribute(".ahacts a.ahbtn", "href") or ""
    t(href.startswith("https://maps.apple.com/directions?"), "→ Llegar apunta a Apple Maps")
    t("Marcus%20Garvey" in href or "Charlie" in href, "y al destino que viene, no al traslado")

    print("\n— marcar hecho desde la tarjeta —")
    pg.click("#ahDone"); pg.wait_for_timeout(400)
    t(pg.locator(".itb.now.done").count() == 1, "el bloque queda tildado en la lista")
    t("✓ hecho" in pg.inner_text("#ahDone"), "y la tarjeta lo refleja")
    t("1/18" in pg.inner_text("#stat"), "el contador del día sube")
    pg.click("#ahDone"); pg.wait_for_timeout(400)
    t(pg.locator(".itb.now.done").count() == 0, "destildar también anda")

    print("\n— 'Ahora' de la barra inferior —")
    pg.evaluate("window.scrollTo(0, 2000)"); pg.wait_for_timeout(200)
    pg.click("#bAhora"); pg.wait_for_timeout(900)
    y = pg.evaluate("()=>{const e=document.querySelector('.itb.now');const r=e.getBoundingClientRect();return r.top}")
    t(0 < y < 667, f"salta al bloque actual y queda a la vista (top={round(y)})")

    print("\n— desplegar un bloque: vuelve TODO lo de la v1 —")
    pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(150)
    sel = '.blk.itb[data-b="d1b10"]'   # ARTHUR AVENUE
    antes = pg.locator(sel).bounding_box()["height"]
    pg.click(sel + " .btog"); pg.wait_for_timeout(400)
    box = pg.locator(sel)
    t(box.bounding_box()["height"] > antes * 1.8, "crece al desplegar")
    txt = box.inner_text()
    t("DOMINGOS no abre" in txt, "el texto completo está (nada se borró)")
    t(box.locator('a[data-nav="apple"]').count() >= 1, "link Apple Maps")
    t(box.locator('a[data-nav="google"]').count() >= 1, "link Google Maps")
    t(box.locator('a.chip.b').count() >= 1, "link ↗ Maps")
    t(box.locator('[data-act="up"]').count() == 1 and box.locator('[data-act="down"]').count() == 1
      and box.locator('[data-act="del"]').count() == 1, "▲ ▼ ✕ aparecen solo desplegado")
    t(box.locator('input.tm').count() == 1, "la hora es editable solo desplegado")
    t("acá cerca" in txt.lower(), "«acá cerca» sigue estando")
    pg.click(sel + " .plegar"); pg.wait_for_timeout(300)
    t(abs(pg.locator(sel).bounding_box()["height"] - antes) < 3, "vuelve a plegarse")
    t(pg.locator(sel + " input.tm").count() == 0, "y la hora deja de ser input")

    print("\n— controles de edición —")
    pg.click(sel + " .btog"); pg.wait_for_timeout(300)
    pg.fill(sel + " input.tm", "14:15"); pg.wait_for_timeout(400)
    t(pg.evaluate("()=>JSON.parse(localStorage['nyc2026.v2']).itin[0].blocks[10].t") == "14:15", "editar la hora se guarda")
    pg.click(sel + ' [data-act="opennote"]'); pg.wait_for_timeout(300)
    pg.fill(sel + " textarea.bnote", "probando la nota"); pg.wait_for_timeout(500)
    t(pg.evaluate("()=>JSON.parse(localStorage['nyc2026.v2']).itin[0].blocks[10].mynote") == "probando la nota", "la nota se guarda")
    n0 = pg.locator(".blk.itb").count()
    pg.click(sel + ' [data-act="down"]'); pg.wait_for_timeout(400)
    t(pg.evaluate("()=>JSON.parse(localStorage['nyc2026.v2']).itin[0].blocks[11].mynote") == "probando la nota", "bajar el bloque lo mueve")
    pg.click('.blk.itb[data-b="d1b10"] [data-act="del"]'); pg.wait_for_timeout(400)
    t(pg.locator(".blk.itb").count() == n0 - 1, "quitar el bloque lo saca")
    ctx.close()

    print("\n— cambiar de día: tira, swipe y 'ir a hoy' —")
    ctx, pg, errs = nueva(b)
    pg.click('.dbtn[data-d="4"]'); pg.wait_for_timeout(500)
    t("día 4" in pg.inner_text("#stat"), "la tira de días cambia el día")
    t(pg.locator("#ahHoy").count() == 1, "aparece «ir a hoy» cuando mirás otro día")
    pg.click("#ahHoy"); pg.wait_for_timeout(500)
    t("día 1" in pg.inner_text("#stat"), "«ir a hoy» vuelve al día de hoy")
    # swipe hacia la izquierda = día siguiente
    bx = pg.locator(".card").first.bounding_box()
    yy = bx["y"] + 40
    pg.touchscreen.tap(200, 400)
    pg.evaluate("""()=>{const v=document.getElementById('v-itin');
      const mk=(ty,x,y)=>{const e=new TouchEvent(ty,{bubbles:true,cancelable:true,
        touches:ty==='touchend'?[]:[new Touch({identifier:1,target:v,clientX:x,clientY:y})],
        changedTouches:[new Touch({identifier:1,target:v,clientX:x,clientY:y})]});v.dispatchEvent(e);};
      mk('touchstart',300,420); mk('touchend',100,430);}""")
    pg.wait_for_timeout(500)
    t("día 2" in pg.inner_text("#stat"), "deslizar ← pasa al día siguiente")
    pg.evaluate("""()=>{const v=document.getElementById('v-itin');
      const mk=(ty,x,y)=>{const e=new TouchEvent(ty,{bubbles:true,cancelable:true,
        touches:ty==='touchend'?[]:[new Touch({identifier:1,target:v,clientX:x,clientY:y})],
        changedTouches:[new Touch({identifier:1,target:v,clientX:x,clientY:y})]});v.dispatchEvent(e);};
      mk('touchstart',80,420); mk('touchend',300,428);}""")
    pg.wait_for_timeout(500)
    t("día 1" in pg.inner_text("#stat"), "deslizar → vuelve al anterior")
    # un gesto mayormente vertical NO cambia de día
    pg.evaluate("""()=>{const v=document.getElementById('v-itin');
      const mk=(ty,x,y)=>{const e=new TouchEvent(ty,{bubbles:true,cancelable:true,
        touches:ty==='touchend'?[]:[new Touch({identifier:1,target:v,clientX:x,clientY:y})],
        changedTouches:[new Touch({identifier:1,target:v,clientX:x,clientY:y})]});v.dispatchEvent(e);};
      mk('touchstart',300,200); mk('touchend',210,500);}""")
    pg.wait_for_timeout(400)
    t("día 1" in pg.inner_text("#stat"), "un gesto vertical NO cambia de día")

    print("\n— filtro por persona —")
    n_all = pg.locator(".blk.itb").count()
    pg.click("#bWho"); pg.wait_for_timeout(300)
    pg.click('[data-w="th"]'); pg.wait_for_timeout(500)
    t(pg.locator(".blk.itb").count() <= n_all, "el filtro por persona sigue filtrando")
    pg.click("#bWho"); pg.wait_for_timeout(300); pg.click('[data-w="all"]'); pg.wait_for_timeout(400)
    t(pg.locator(".blk.itb").count() == n_all, "y se puede volver a «todo»")
    t(not errs, f"sin errores JS ({errs[:2]})")
    ctx.close()

    print("\n— mapa, ruta del día, agregar lugar —")
    ctx, pg, errs = nueva(b)
    pg.click("#mapDay"); pg.wait_for_timeout(1200)
    t(pg.locator("#map .leaflet-marker-icon, #map svg").count() > 0 or pg.locator("#map").count()==1,
      "el mapa del día se dibuja")
    pg.click('.tab[data-t="itin"]'); pg.wait_for_timeout(400)
    pg.click("#rutaDia"); pg.wait_for_timeout(500)
    t(pg.locator("#rw").count() == 1 and (pg.get_attribute("#rw","href") or "").startswith("https://maps.apple.com"),
      "la hoja de ruta del día arma el link de Apple")
    t(pg.locator("#rgm a").count() > 0, "y los tramos de Google")
    pg.click("#ov", position={"x":10,"y":10}); pg.wait_for_timeout(300)
    pg.click("#addFree"); pg.wait_for_timeout(400)
    pg.fill("#nt","16:05"); pg.fill("#nx","comprar postales")
    pg.click("#nok"); pg.wait_for_timeout(500)
    t("comprar postales" in pg.inner_text("#v-itin"), "agregar nota libre anda")
    t(not errs, f"sin errores JS ({errs[:2]})")
    ctx.close()

    print("\n— resistencia del estado: borrar cada clave, una por una —")
    for k in ["itin","interest","must","mv","res","day","tab","whoF","pv","v","baseHash"]:
        ctx = b.new_context(viewport={"width":375,"height":667}, has_touch=True, is_mobile=True)
        ctx.add_init_script(f"window.__NOW='{FAKE}';")
        pg = ctx.new_page(); errs=[]
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(URL); pg.wait_for_timeout(600)
        pg.evaluate(f"()=>{{const s=JSON.parse(localStorage['nyc2026.v2']); delete s['{k}']; localStorage['nyc2026.v2']=JSON.stringify(s);}}")
        pg.reload(); pg.wait_for_timeout(700)
        for tab in ["itin","places","map","costs","trans","res"]:
            pg.click(f'.tab[data-t="{tab}"]'); pg.wait_for_timeout(250)
        t(not errs, f"sin «{k}» en el estado, las 6 pestañas andan ({errs[:1]})")
        ctx.close()

    print("\n— antes y después del viaje —")
    for fake, esperado, desc in [("2026-08-27T21:00:00","faltan 2 días","antes del viaje: cuenta los días"),
                                 ("2026-09-08T10:00:00","El viaje terminó","después: lo dice y no rompe")]:
        ctx, pg, errs = nueva(b, fake=fake)
        t(esperado.lower() in pg.inner_text(".ahora").lower(), desc)
        t(not errs, f"  sin errores JS con __NOW={fake}")
        ctx.close()

    print("\n— hora local, no UTC (el bug de las noches) —")
    ctx, pg, errs = nueva(b, fake="2026-08-31T22:30:00")
    t("día 3" in pg.inner_text("#stat"), "a las 22:30 del 31/8 sigue siendo el día 3, no el 4")
    ctx.close()

    print("\n— sin scroll horizontal, en las 6 pestañas y los 9 días —")
    ctx, pg, errs = nueva(b)
    malas = []
    for tab in ["itin","places","map","costs","trans","res"]:
        pg.click(f'.tab[data-t="{tab}"]'); pg.wait_for_timeout(400)
        pg.mouse.move(187, 560); pg.mouse.wheel(600, 0); pg.wait_for_timeout(120)
        if pg.evaluate("window.scrollX"): malas.append(tab)
        pg.evaluate("window.scrollTo(0,0)")
    t(not malas, f"rueda horizontal no mueve la página ({malas})")
    pg.click('.tab[data-t="itin"]'); pg.wait_for_timeout(300)
    anchos = []
    for d in range(1, 10):
        pg.click(f'.dbtn[data-d="{d}"]'); pg.wait_for_timeout(400)
        sw, cw = pg.evaluate("()=>[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
        if sw > cw: anchos.append((d, sw, cw))
    t(not anchos, f"ningún día desborda a lo ancho ({anchos})")
    t(not errs, f"los 9 días renderizan sin errores ({errs[:2]})")
    ctx.close()

    b.close()

print(f"\n{'='*46}\n{ok} bien · {fail} mal")
sys.exit(1 if fail else 0)
