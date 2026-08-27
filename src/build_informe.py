#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convierte los tres informes de exploración (docs/informe_*.md) en UNA página
para revisarlos desde el celular y decidir qué entra al catálogo.

No es un documento de lectura: es la misma mecánica de tres estados que ya usa
la app — ★ lo quiero / ✕ no / sin marcar — con las marcas guardadas en el
navegador y un botón para exportarlas. Lo que Juan marque vuelve como lista y
entra al catálogo por el camino de siempre.

  python3 build_informe.py   →  informe_exploracion.html
"""
import os, re, json, html

_R = os.path.dirname(os.path.abspath(_file_ := __file__))
DOCS = os.path.join(os.path.dirname(_R), "docs")

FUENTES = [
    ("agenda", "Qué pasa esos días", "informe_1_agenda_29ago_6sep.md",
     "Muestras temporales, ópera gratis, festivales y cierres que caen entre el 29/8 y el 6/9. "
     "Es lo más perecedero: nada de esto lo puede saber un catálogo."),
    ("joyas", "Joyas por barrio", "informe_2_joyas_por_barrio.md",
     "56 lugares que no están en el catálogo, en los barrios que ya recorren. "
     "Interiores públicos, pocket parks, museos chicos, miradores gratis."),
    ("comida", "Comida", "informe_3_comida.md",
     "35 lugares atados a los huecos reales del itinerario: las cenas sin definir, "
     "los desayunos cerca de cada hotel, lo que abre a las 6 y lo que abre a las 3."),
]

# los mismos colores con que la app pinta cada categoría, para que un tipo de
# lugar se lea igual acá que allá
TONO = [
    (r"museo|galer|exposici|muestra|colecci", "#6741d9"),
    (r"ópera|opera|jazz|música|musica|concierto|festival|club", "#2b8a3e"),
    (r"comida|bar|café|cafe|restaurant|pizza|bagel|deli|panader|brunch|cena|desayuno", "#c2255c"),
    (r"parque|jardín|jardin|garden|plaza", "#5c940d"),
    (r"mirador|vista|rooftop|observator|torre", "#0b7285"),
    (r"iglesia|catedral|templo|edificio|arquitect|lobby|puente|calle", "#1864ab"),
    (r"cerrad|cierra|obra|alerta|sacar", "#b8283a"),
]


def tono(texto):
    t = texto.lower()
    for patron, color in TONO:
        if re.search(patron, t):
            return color
    return "#66707d"


def parsea(ruta):
    """Cada `## sección` con sus `### ítems`, y cada ítem con sus campos."""
    seccion, items = "", []
    for linea in open(ruta, encoding="utf-8"):
        if linea.startswith("## "):
            seccion = linea[3:].strip()
        elif linea.startswith("### "):
            items.append({"n": linea[4:].strip(), "sec": seccion, "campos": [], "cuerpo": []})
        elif items:
            m = re.match(r"\s*-\s+\*\*(.+?)\*\*:?\s*(.*)", linea)
            if m:
                items[-1]["campos"].append([m.group(1).strip(), m.group(2).strip()])
            elif linea.strip() and items[-1]["campos"]:
                # continuación del campo anterior (los informes envuelven a 95 columnas)
                items[-1]["campos"][-1][1] += " " + linea.strip()
            elif linea.strip():
                items[-1]["cuerpo"].append(linea.strip())
    return [i for i in items if i["campos"] or i["cuerpo"]]


def limpia(s):
    """Markdown mínimo a HTML: negrita, itálica, enlaces y código."""
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*([^*]+?)\*(?![\w*])", r"<i>\1</i>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    s = re.sub(r"(https?://[^\s<)]+)", r'<a href="\1" target="_blank" rel="noopener">\1</a>', s)
    return s


DATOS, n_items = [], 0
for clave, titulo, archivo, bajada in FUENTES:
    ruta = os.path.join(DOCS, archivo)
    if not os.path.exists(ruta):
        raise SystemExit("falta el informe: " + ruta)
    items = parsea(ruta)
    n_items += len(items)
    DATOS.append({"k": clave, "t": titulo, "d": bajada, "items": items})

# ── el HTML ────────────────────────────────────────────────────────────────
tarjetas = []
idx = 0
for grupo in DATOS:
    for it in grupo["items"]:
        idx += 1
        c = tono(it["n"] + " " + it["sec"])
        conf = next((v for k, v in it["campos"] if k.lower().startswith("confianza")), "")
        fuente = next((v for k, v in it["campos"] if k.lower().startswith("fuente")), "")
        campos = "".join(
            f'<div class="f"><dt>{html.escape(k)}</dt><dd>{limpia(v)}</dd></div>'
            for k, v in it["campos"]
            if not k.lower().startswith(("fuente", "confianza")))
        cuerpo = "".join(f"<p>{limpia(x)}</p>" for x in it["cuerpo"])
        pill = ""
        if conf:
            nivel = "alta" if "alta" in conf.lower() else "baja" if "baja" in conf.lower() else "media"
            pill = f'<span class="conf {nivel}">{html.escape(conf.split(chr(40))[0].strip())}</span>'
        tarjetas.append(f'''
<article class="it" data-g="{grupo['k']}" data-sec="{html.escape(it['sec'], quote=True)}" id="i{idx}">
  <div class="hd">
    <div class="marca" role="group" aria-label="Decisión">
      <button class="m si" data-v="1" title="Lo quiero">★</button>
      <button class="m no" data-v="-1" title="Descartado">✕</button>
    </div>
    <div class="ti">
      <h3 style="--c:{c}">{limpia(it['n'])}</h3>
      <div class="meta"><span class="sec">{html.escape(it['sec'])}</span>{pill}</div>
    </div>
  </div>
  <dl class="cs">{campos}</dl>
  {cuerpo}
  {f'<a class="src" href="{html.escape(fuente, quote=True)}" target="_blank" rel="noopener">fuente ↗</a>' if fuente.startswith('http') else ''}
</article>''')

secciones = "".join(
    f'''<section class="grupo" data-g="{g['k']}">
  <header class="gh"><h2>{html.escape(g['t'])}</h2><p>{html.escape(g['d'])}</p>
  <span class="cuenta">{len(g['items'])} propuestas</span></header>
</section>''' for g in DATOS)

HTML = f'''<title>Explorar Nueva York</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700&display=swap">
<style>
/* La paleta sale del design system que ya tiene la app del viaje: mismo crema,
   misma tinta, mismos colores por categoría. Que se sienta el mismo proyecto. */
:root{{
  --bg:#f7f5f1; --card:#fff; --ink:#16202b; --mut:#66707d; --line:#e3ddd4;
  --navy:#14293d; --accent:#c1440e; --gold:#c8891b; --green:#2e7d4f; --red:#b8283a;
  --chip:#f0ece4; --sh:0 1px 2px rgba(20,41,61,.06),0 4px 14px rgba(20,41,61,.06);
}}
@media (prefers-color-scheme: dark){{
  :root:not([data-theme="light"]){{
    --bg:#14161a; --card:#1c1f25; --ink:#eceae6; --mut:#9aa2ad; --line:#2c313a;
    --navy:#c8d4e2; --accent:#e8703a; --gold:#e0a63c; --green:#5fbe86; --red:#e0687a;
    --chip:#252a32; --sh:0 1px 2px rgba(0,0,0,.3),0 4px 14px rgba(0,0,0,.25);
  }}
}}
:root[data-theme="dark"]{{
  --bg:#14161a; --card:#1c1f25; --ink:#eceae6; --mut:#9aa2ad; --line:#2c313a;
  --navy:#c8d4e2; --accent:#e8703a; --gold:#e0a63c; --green:#5fbe86; --red:#e0687a;
  --chip:#252a32; --sh:0 1px 2px rgba(0,0,0,.3),0 4px 14px rgba(0,0,0,.25);
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);
  font:15px/1.55 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  -webkit-text-size-adjust:100%}}
h1,h2,h3{{font-family:Archivo,ui-sans-serif,system-ui,sans-serif;text-wrap:balance;margin:0}}
a{{color:var(--navy)}}
code{{background:var(--chip);padding:1px 5px;border-radius:5px;font-size:.88em}}
.wrap{{max-width:760px;margin:0 auto;padding:0 16px 96px}}

header.top{{padding:30px 0 18px}}
header.top h1{{font-size:29px;font-weight:700;letter-spacing:-.02em;line-height:1.12}}
header.top .sub{{color:var(--mut);margin-top:9px;max-width:62ch}}
.avisos{{display:flex;flex-direction:column;gap:8px;margin-top:16px}}
.aviso{{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--accent);
  border-radius:11px;padding:10px 13px;font-size:13.5px;box-shadow:var(--sh)}}
.aviso b{{color:var(--accent)}}

.barra{{position:sticky;top:0;z-index:9;background:var(--bg);
  padding:11px 0 10px;border-bottom:1px solid var(--line);margin-bottom:16px}}
.filtros{{display:flex;gap:7px;flex-wrap:wrap;align-items:center}}
.bt{{font:inherit;font-size:13px;font-weight:600;padding:6px 12px;border-radius:99px;cursor:pointer;
  background:var(--chip);color:var(--ink);border:1px solid transparent;white-space:nowrap}}
.bt.on{{background:var(--navy);color:var(--bg);border-color:var(--navy)}}
.bt:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
#q{{flex:1;min-width:150px;font:inherit;font-size:14px;padding:7px 12px;border-radius:99px;
  border:1px solid var(--line);background:var(--card);color:var(--ink)}}
.tot{{font-size:12.5px;color:var(--mut);margin-top:8px;font-variant-numeric:tabular-nums}}

.gh{{margin:26px 0 12px;padding-top:18px;border-top:2px solid var(--line)}}
.gh h2{{font-size:20px;font-weight:700;letter-spacing:-.01em}}
.gh p{{color:var(--mut);font-size:13.5px;margin:5px 0 0;max-width:62ch}}
.cuenta{{display:inline-block;margin-top:7px;font-size:11px;text-transform:uppercase;
  letter-spacing:.07em;color:var(--mut)}}

.it{{background:var(--card);border:1px solid var(--line);border-radius:13px;
  padding:13px 15px;margin-bottom:9px;box-shadow:var(--sh)}}
.it[data-m="1"]{{border-color:var(--green);box-shadow:0 0 0 1px var(--green)}}
.it[data-m="-1"]{{opacity:.42}}
.hd{{display:flex;gap:11px;align-items:flex-start}}
.marca{{display:flex;flex-direction:column;gap:4px;flex:none}}
.m{{width:31px;height:27px;border-radius:8px;border:1px solid var(--line);background:var(--bg);
  cursor:pointer;font-size:13px;line-height:1;color:var(--mut);padding:0}}
.m:focus-visible{{outline:2px solid var(--accent);outline-offset:1px}}
.it[data-m="1"] .m.si{{background:var(--green);border-color:var(--green);color:#fff}}
.it[data-m="-1"] .m.no{{background:var(--red);border-color:var(--red);color:#fff}}
.ti{{flex:1;min-width:0}}
.ti h3{{font-size:16px;font-weight:600;line-height:1.3;color:var(--c,var(--ink))}}
.meta{{display:flex;gap:7px;flex-wrap:wrap;align-items:center;margin-top:4px}}
.sec{{font-size:11.5px;color:var(--mut)}}
.conf{{font-size:10.5px;font-weight:600;padding:1px 7px;border-radius:99px;
  text-transform:uppercase;letter-spacing:.05em}}
.conf.alta{{background:color-mix(in srgb,var(--green) 16%,transparent);color:var(--green)}}
.conf.media{{background:color-mix(in srgb,var(--gold) 20%,transparent);color:var(--gold)}}
.conf.baja{{background:color-mix(in srgb,var(--red) 15%,transparent);color:var(--red)}}

.cs{{margin:11px 0 0;display:flex;flex-direction:column;gap:5px}}
.f{{display:grid;grid-template-columns:88px 1fr;gap:10px;font-size:13.5px}}
.f dt{{color:var(--mut);font-size:11.5px;text-transform:uppercase;letter-spacing:.04em;
  padding-top:2px}}
.f dd{{margin:0;min-width:0;overflow-wrap:anywhere}}
.it p{{font-size:13.5px;color:var(--mut);margin:8px 0 0}}
.src{{display:inline-block;margin-top:9px;font-size:12px;color:var(--mut);
  overflow-wrap:anywhere}}
@media (max-width:520px){{
  .f{{grid-template-columns:1fr;gap:1px}}
  header.top h1{{font-size:24px}}
}}

.pie{{position:fixed;left:0;right:0;bottom:0;background:var(--card);border-top:1px solid var(--line);
  padding:10px 16px;display:flex;gap:10px;align-items:center;z-index:10;
  box-shadow:0 -3px 14px rgba(20,41,61,.07)}}
.pie .n{{flex:1;min-width:0;font-size:13px;font-variant-numeric:tabular-nums;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.pie .n b{{color:var(--green)}}
.bt.exp{{background:var(--accent);color:#fff}}
@media (prefers-reduced-motion:no-preference){{.it{{transition:opacity .15s,border-color .15s}}}}
</style>

<div class="wrap">
<header class="top">
  <h1>Explorar Nueva York</h1>
  <p class="sub">{n_items} propuestas que <b>no están</b> en el catálogo de 256 lugares, buscadas y
  verificadas contra fuente el 27 de agosto. Marcá ★ lo que quieras y ✕ lo que no; al final tocá
  <b>Exportar</b> y pasame el resultado. Lo que elijas entra al plan como referencia de paso.</p>
  <div class="avisos">
    <div class="aviso"><b>Ya aplicado al plan:</b> la rotonda del Guggenheim está cerrada hasta el
    17/9 · el jueves hay ópera gratis en Lincoln Center y despejan la plaza desde las 18:00 ·
    Charlie Parker cierra con Joshua Redman el sábado 29 · la Neue Galerie está cerrada y salió del catálogo.</div>
    <div class="aviso"><b>Cada ficha dice su confianza.</b> «Alta» es fuente oficial. Lo que no se
    pudo confirmar está marcado, no escondido: varios sitios cargan la cartelera por JavaScript
    y no se dejan leer.</div>
  </div>
</header>

<div class="barra">
  <div class="filtros">
    <button class="bt on" data-f="todo">Todo</button>
    <button class="bt" data-f="agenda">Esos días</button>
    <button class="bt" data-f="joyas">Joyas</button>
    <button class="bt" data-f="comida">Comida</button>
    <button class="bt" data-f="marcados">★ Marcados</button>
    <input id="q" type="search" placeholder="Buscar barrio, nombre, día…" aria-label="Buscar">
  </div>
  <div class="tot" id="tot"></div>
</div>

{secciones}
{"".join(tarjetas)}
</div>

<div class="pie">
  <div class="n" id="cuenta"></div>
  <button class="bt" id="limpiar">Borrar marcas</button>
  <button class="bt exp" id="exportar">Exportar</button>
</div>

<script>
const K='nyc2026.informe.v1';
let S={{}}; try{{ S=JSON.parse(localStorage.getItem(K))||{{}}; }}catch(e){{ S={{}}; }}
const guardar=()=>{{ try{{ localStorage.setItem(K,JSON.stringify(S)); }}catch(e){{}} }};
const items=[...document.querySelectorAll('.it')];
const grupos=[...document.querySelectorAll('.grupo')];

/* el nombre es la clave: sobrevive a que se reordene o regenere el informe */
const clave=el=>el.querySelector('h3').textContent.trim();
items.forEach(el=>{{ const v=S[clave(el)]; if(v) el.dataset.m=v; }});

let filtro='todo', busca='';
function pinta(){{
  let vis=0;
  items.forEach(el=>{{
    const m=el.dataset.m||'0';
    const okF = filtro==='todo' ? true : filtro==='marcados' ? m==='1' : el.dataset.g===filtro;
    const okQ = !busca || el.textContent.toLowerCase().includes(busca);
    const ok = okF && okQ;
    el.style.display = ok ? '' : 'none';
    if(ok) vis++;
  }});
  grupos.forEach(g=>{{
    const suyos=items.filter(el=>el.dataset.g===g.dataset.g && el.style.display!=='none');
    g.style.display = suyos.length ? '' : 'none';
  }});
  const si=items.filter(el=>el.dataset.m==='1').length;
  const no=items.filter(el=>el.dataset.m==='-1').length;
  document.getElementById('tot').textContent =
    vis+' a la vista · '+items.length+' en total';
  const corto = window.innerWidth < 560;
  document.getElementById('cuenta').innerHTML = corto
    ? '<b>'+si+' ★</b> · '+no+' ✕'
    : '<b>'+si+' marcados</b> · '+no+' descartados · '+(items.length-si-no)+' sin decidir';
}}
document.addEventListener('click',e=>{{
  const b=e.target.closest('.m'); if(!b) return;
  const el=b.closest('.it'), v=b.dataset.v;
  const nuevo = el.dataset.m===v ? '' : v;      /* volver a tocar lo deshace */
  if(nuevo) el.dataset.m=nuevo; else delete el.dataset.m;
  if(nuevo) S[clave(el)]=nuevo; else delete S[clave(el)];
  guardar(); pinta();
}});
document.querySelectorAll('[data-f]').forEach(b=>b.onclick=()=>{{
  document.querySelectorAll('[data-f]').forEach(x=>x.classList.toggle('on',x===b));
  filtro=b.dataset.f; pinta();
}});
document.getElementById('q').oninput=e=>{{ busca=e.target.value.toLowerCase().trim(); pinta(); }};
document.getElementById('limpiar').onclick=()=>{{
  if(!confirm('¿Borrar todas las marcas?')) return;
  S={{}}; guardar(); items.forEach(el=>delete el.dataset.m); pinta();
}};
document.getElementById('exportar').onclick=()=>{{
  const si=items.filter(el=>el.dataset.m==='1').map(el=>'★ '+clave(el)+'  ['+el.dataset.g+']');
  const no=items.filter(el=>el.dataset.m==='-1').map(el=>'✕ '+clave(el));
  if(!si.length && !no.length){{ alert('Todavía no marcaste nada.'); return; }}
  const txt='LO QUE QUIERO ('+si.length+')\\n'+si.join('\\n')+
            '\\n\\nDESCARTADOS ('+no.length+')\\n'+no.join('\\n');
  navigator.clipboard.writeText(txt).then(
    ()=>alert('Copiado al portapapeles: '+si.length+' marcados y '+no.length+' descartados.\\n\\nPegámelo en el chat.'),
    ()=>prompt('Copiá esto y pasámelo:', txt));
}};
pinta();
addEventListener('resize', pinta);
</script>'''

salida = os.path.join(os.path.dirname(_R), "informe_exploracion.html")
with open(salida, "w", encoding="utf-8") as f:
    f.write(HTML)
print(f"INFORME ok · {n_items} propuestas · {round(len(HTML)/1024)} KB")
print(f"   → {salida}")
