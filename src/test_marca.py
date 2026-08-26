import os as _os
_BASE = _os.path.dirname(_os.path.abspath(__file__))
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prueba la marca de tres estados: ciclo, filtros, banner, persistencia y compatibilidad
   con los estados guardados por la version anterior (donde 0 significaba 'des-marcado')."""
from playwright.sync_api import sync_playwright
import json, sys

URL = "file://" + _os.path.join(_BASE, "pages/index.html")
ok = fail = 0
def chk(n, c, extra=""):
    global ok, fail
    print(("  ok    " if c else "  FALLA ") + n + (("  " + extra) if extra and not c else ""))
    ok, fail = ok + (1 if c else 0), fail + (0 if c else 1)

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1180, "height": 900})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(URL, wait_until="load"); pg.wait_for_timeout(1200)
    pg.get_by_text("Lugares", exact=True).first.click(); pg.wait_for_timeout(700)

    st = lambda: pg.evaluate("() => { const b=document.querySelector('.mustbtn'); "
                             "return [b.textContent.trim(), b.className]; }")
    t0, c0 = st()
    chk("arranca en ★ (viene del catálogo)", t0.startswith("★") and "on" in c0, f"{t0} / {c0}")
    pg.click(".mustbtn"); pg.wait_for_timeout(400); t1, c1 = st()
    chk("★ → ✕", t1.startswith("✕") and "off" in c1, f"{t1} / {c1}")
    pg.click(".mustbtn"); pg.wait_for_timeout(400); t2, c2 = st()
    chk("✕ → sin marcar", t2.startswith("☆") and "on" not in c2 and "off" not in c2, f"{t2} / {c2}")
    pg.click(".mustbtn"); pg.wait_for_timeout(400); t3, c3 = st()
    chk("sin marcar → ★", t3.startswith("★") and "on" in c3, f"{t3} / {c3}")

    # ── contadores y filtros ──
    cnt = lambda: pg.evaluate("() => [mustCount(), outCount(), PLACES.length]")
    m, o, tot = cnt()
    chk("contadores coherentes", m + o <= tot, f"{m}+{o}>{tot}")
    opts = pg.eval_on_selector_all("#fmk option", "e=>e.map(x=>x.textContent.trim())")
    chk("el filtro ofrece los tres estados", len(opts) == 4 and "✕" in opts[2], str(opts))

    def filtra(v):
        pg.select_option("#fmk", v); pg.wait_for_timeout(600)
        return pg.eval_on_selector_all(".pc, .prow", "e=>e.length")
    pg.click(".mustbtn"); pg.wait_for_timeout(300)          # dejar uno en ✕
    m, o, tot = cnt()
    chk("filtro ★ muestra sólo imprescindibles", filtra("si") == m, f"esperaba {m}")
    chk("filtro ✕ muestra sólo descartados", filtra("no") == o, f"esperaba {o}")
    chk("filtro «sin marcar» cierra la cuenta", filtra("sin") == tot - m - o, f"esperaba {tot-m-o}")
    filtra("")

    # ── banner de descartados que siguen en el itinerario ──
    pid = pg.evaluate("() => { const k = Object.keys(DAYMAP)[0]; S.must[k]=-1; save(); rPlaces(); return k; }")
    pg.wait_for_timeout(600)
    chk("avisa si un ✕ sigue en el itinerario",
        "siguen en el itinerario" in pg.inner_text("#v-places"), pid)

    # ── persistencia entre recargas ──
    pg.evaluate("() => { S.must['met']=-1; S.must['moma']=1; delete S.must['summit']; save(); }"); pg.wait_for_timeout(500)
    pg.reload(wait_until="load"); pg.wait_for_timeout(1200)
    got = pg.evaluate("() => [markOf('met'), markOf('moma'), markOf('summit')]")
    chk("sobrevive a la recarga", got[0] == -1 and got[1] == 1, str(got))

    # ── compatibilidad: la versión vieja guardaba 0 = des-marcado ──
    pg.evaluate("""() => { const s = JSON.parse(localStorage.getItem(KEY));
        s.must = {met: 0, moma: 1}; delete s.mv; localStorage.setItem(KEY, JSON.stringify(s)); }""")
    pg.reload(wait_until="load"); pg.wait_for_timeout(1200)
    got = pg.evaluate("() => [markOf('met'), markOf('moma')]")
    chk("un 0 viejo se lee como ✕, no como ★", got == [-1, 1], str(got))

    # ── el estado 'sin marcar' NO se guarda como basura ──
    # 'met' es ★ en el catálogo: tres toques tienen que dar la vuelta entera y pasar por ☆
    vuelta = pg.evaluate("""() => { S.must={}; const r=[markOf('met')];
        for (let i=0;i<3;i++){ cycleMark('met'); r.push(markOf('met')); } return r; }""")
    chk("la vuelta completa es ★ → ✕ → ☆ → ★", vuelta == [1, -1, 0, 1], str(vuelta))
    chk("un 0 explícito es «sin marcar», NO el ★ del catálogo",
        pg.evaluate("() => { S.must={met:0}; return markOf('met'); }") == 0)
    pg.evaluate("() => save()"); pg.wait_for_timeout(500)
    left = pg.evaluate("() => JSON.parse(localStorage.getItem(KEY)).must")
    chk("y ese «sin marcar» queda guardado", left.get("met") == 0, str(left))

    chk("sin errores JS", not errs, str(errs))
    b.close()

print(f"\n{ok} ok · {fail} fallas")
sys.exit(1 if fail else 0)
