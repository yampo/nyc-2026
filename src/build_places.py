#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Base de datos de lugares para el viaje a NYC (29 ago - 6 sep 2026).
Genera data/places.json consumido por el Excel y por la app HTML.

Campos:
  id     slug unico
  n      nombre
  cat    categoria: mirador|museo|barrio|comida|musica|arq|parque|evento|teatro|transporte
  hood   barrio
  boro   borough
  sub    linea/estacion de subte mas cercana
  typ    subcategoria / tipo de lugar (segundo nivel, ver SUB abajo)
  lat,lng  coordenadas APROXIMADAS (para el mapa). El boton "Google Maps" busca por nombre+direccion.
  addr   direccion (para el link a Google Maps)
  cost   costo estimado por persona en USD (0 = gratis)
  costN  nota de costo
  dur    duracion sugerida en horas
  why    por que vale la pena
  main   True = mainstream / muy turistico
  closed dia(s) de cierre semanal
  free   ventana gratis o pay-what-you-wish
  book   nivel de reserva necesaria
  jp     interes por defecto de Juan Pablo (0 no / 1 quizas / 2 si)
  th     interes por defecto de Thais (mas bajo en lo mainstream: ya lo conoce)
  tags   etiquetas
  src    origen: propuesta (trabajo conjunto) | lista (lista de Google) | ambas (coincide)
  gname  nombre con el que figura en la lista de Google (solo si src=ambas)
  must   marca de tres estados: 1 = IMPRESCINDIBLE, -1 = NO imprescindible (descartado a proposito),
         0 = sin marcar todavia. Se edita en la app o en la columna IMPRESCINDIBLE del Excel.
"""
import os
_R = os.path.dirname(os.path.abspath(__file__))   # todo se resuelve relativo a este archivo, no a donde se corra
import json, os

P = []

def a(**kw):
    kw.setdefault("costN", ""); kw.setdefault("closed", ""); kw.setdefault("free", "")
    kw.setdefault("book", ""); kw.setdefault("main", False); kw.setdefault("tags", [])
    kw.setdefault("src", "propuesta"); kw.setdefault("addr", ""); kw.setdefault("aprox", False)
    kw.setdefault("gname", ""); kw.setdefault("must", 0)
    P.append(kw)

# ─────────────────────────────  MIRADORES Y VISTAS  ─────────────────────────────
a(id="summit", n="SUMMIT One Vanderbilt", cat="mirador", hood="Midtown East", boro="Manhattan",
  sub="Grand Central-42 St (4,5,6,7,S)", lat=40.7527, lng=-73.9787, addr="45 E 42nd St",
  cost=44, costN="desde $44 (incl. $3 fee). Atardecer $57-63. NO esta en ningun pase.",
  dur=1.5, why="El unico observatorio que es una obra de arte en si: salas de espejos infinitos de Kusama, piso de vidrio y ascensor exterior. Mas experiencia que mirador.",
  main=True, book="ticket con horario, reservar 1-2 semanas antes", jp=2, th=1, tags=["skyline","arquitectura"])

a(id="topofrock", n="Top of the Rock", cat="mirador", hood="Midtown", boro="Manhattan",
  sub="47-50 Sts-Rockefeller Ctr (B,D,F,M)", lat=40.7593, lng=-73.9793, addr="30 Rockefeller Plaza",
  cost=42, costN="desde $42, hasta $65 en horario pico. Incluido en CityPASS C3 y Go City.",
  dur=1.5, why="El unico observatorio desde el que se ve el Empire State en el encuadre, con Central Park del otro lado. Si van a pagar uno solo, es este.",
  main=True, book="ticket con horario", jp=2, th=0, tags=["skyline"])

a(id="edge", n="Edge Hudson Yards", cat="mirador", hood="Hudson Yards", boro="Manhattan",
  sub="34 St-Hudson Yards (7)", lat=40.7539, lng=-74.0011, addr="30 Hudson Yards",
  cost=34, costN="Advance Saver $34 reservando 14+ dias antes. GA $42+$2. Flex $73.",
  dur=1.25, why="Terraza triangular en voladizo con piso de vidrio. El mas espectacular fisicamente, pero la vista es la mas floja de los tres: estas demasiado al oeste.",
  main=True, book="timed entry; Advance Saver exige 14+ dias", jp=1, th=0, tags=["skyline"])

a(id="esb", n="Empire State Building", cat="mirador", hood="Midtown", boro="Manhattan",
  sub="34 St-Herald Sq (B,D,F,M,N,Q,R,W)", lat=40.7484, lng=-73.9857, addr="20 W 34th St",
  cost=49, costN="$44 + $5 booking fee (86th). 86th+102nd $79+$5.",
  dur=1.5, why="El icono. La vista es buena pero no la mejor; el valor esta en el edificio mismo y el museo art deco del segundo piso.",
  main=True, book="recomendada", jp=1, th=0, tags=["skyline","arquitectura"])

a(id="owo", n="One World Observatory", cat="mirador", hood="Financial District", boro="Manhattan",
  sub="WTC Cortlandt (1), Fulton St", lat=40.7127, lng=-74.0134, addr="117 West St",
  cost=44, costN="$44+$3.50. 50% OFF despues de las 20:00 (~$22).",
  dur=1.25, why="El punto mas alto del hemisferio occidental. Vista dominada por el puerto y Brooklyn. El truco real es entrar despues de las 20:00 a mitad de precio.",
  main=True, book="recomendada", jp=1, th=0, tags=["skyline"])

a(id="siferry", n="Staten Island Ferry", cat="mirador", hood="Financial District", boro="Manhattan",
  sub="South Ferry (1), Whitehall St (R,W), Bowling Green (4,5)", lat=40.7013, lng=-74.0134,
  addr="4 Whitehall St, Whitehall Terminal", cost=0, costN="GRATIS, 24/7",
  dur=1.5, why="Pasa a ~500 m de la Estatua de la Libertad con todo el Lower Manhattan de fondo. Sentarse a la derecha yendo, a la izquierda volviendo. Es la mejor relacion vista/precio de la ciudad.",
  jp=2, th=1, tags=["gratis","skyline","agua"])

a(id="tram", n="Roosevelt Island Tramway", cat="mirador", hood="Upper East Side", boro="Manhattan",
  sub="Lexington Av-59 St (4,5,6,N,R,W)", lat=40.7614, lng=-73.9640, addr="E 59th St & 2nd Ave",
  cost=3, costN="$3 por sentido (OMNY). Hay que pagar de nuevo para volver.",
  dur=0.75, why="Teleferico a 76 m sobre el East River con el Queensboro Bridge al lado. La vista de $50 por $3. Ir al atardecer.",
  jp=2, th=2, tags=["gratis-ish","skyline"])

a(id="bhpromenade", n="Brooklyn Heights Promenade", cat="mirador", hood="Brooklyn Heights", boro="Brooklyn",
  sub="Clark St (2,3), Borough Hall (4,5)", lat=40.6963, lng=-73.9966, addr="Columbia Heights, Brooklyn",
  cost=0, dur=0.75, why="La postal clasica del skyline de Lower Manhattan. Al atardecer, con el sol detras de Manhattan, es imbatible y gratis.",
  jp=2, th=1, tags=["gratis","skyline"])

a(id="gantry", n="Gantry Plaza State Park", cat="mirador", hood="Long Island City", boro="Queens",
  sub="Vernon Blvd-Jackson Av (7), 21 St (G)", lat=40.7472, lng=-73.9585, addr="4-09 47th Rd, LIC",
  cost=0, dur=1, why="La mejor vista frontal de Midtown que existe, desde el nivel del agua, con las gruas ferroviarias historicas y el cartel Pepsi-Cola. Practicamente sin turistas.",
  jp=2, th=2, tags=["gratis","skyline","foto"])

a(id="domino", n="Domino Park", cat="mirador", hood="Williamsburg", boro="Brooklyn",
  sub="Bedford Av (L)", lat=40.7145, lng=-73.9679, addr="300 Kent Ave, Brooklyn",
  cost=0, dur=1, why="Ex refineria de azucar. El paseo elevado pasa entre la maquinaria industrial conservada, con el Williamsburg Bridge y Midtown enfrente.",
  jp=2, th=2, tags=["gratis","skyline","industrial"])

a(id="forttryon", n="Fort Tryon Park", cat="mirador", hood="Washington Heights", boro="Manhattan",
  sub="190 St (A)", lat=40.8626, lng=-73.9327, addr="Fort Tryon Park, Manhattan",
  cost=0, dur=1.5, why="El Hudson y los Palisades sin un solo edificio a la vista. No parece Manhattan. Se combina con The Cloisters en la misma caminata.",
  jp=2, th=2, tags=["gratis","naturaleza"])

a(id="sunsetparkview", n="Sunset Park (el mirador)", cat="mirador", hood="Sunset Park", boro="Brooklyn",
  sub="25 St (R)", lat=40.6489, lng=-74.0055, addr="Sunset Park, 5th Ave & 41st St, Brooklyn",
  cost=0, dur=0.5, why="Manhattan entero, el puerto y la Estatua de la Libertad desde una loma en un barrio residencial. Cero turistas.",
  jp=2, th=2, tags=["gratis","skyline"])

a(id="govisland", n="Governors Island", cat="barrio", hood="Governors Island", boro="Manhattan",
  sub="Ferry desde Battery Maritime Bldg (10 South St)", lat=40.6895, lng=-74.0169, addr="Governors Island, New York",
  cost=5, costN="Ferry $5 ida y vuelta. GRATIS sabados y domingos antes de las 11:00 - SOLO en la ruta de Manhattan (Battery Maritime Building, 10 South St). Las rutas de Brooklyn no tienen esa ventana.",
  dur=4, why="Ex base militar sin autos. Outlook Hill da 360 grados con la Estatua de frente; Nolan Park tiene casas de oficiales del siglo XIX con arte adentro. Se siente fuera de la ciudad.",
  book="ferry con horario", jp=2, th=2, tags=["gratis-ish","arte","caminata"])

a(id="wavehill", n="Wave Hill", cat="parque", hood="Riverdale", boro="Bronx",
  sub="Metro-North a Riverdale + shuttle", lat=40.8977, lng=-73.9146, addr="4900 Independence Ave, Bronx",
  cost=10, costN="$10. GRATIS todos los jueves.", closed="lunes",
  dur=2.5, why="Jardin botanico sobre un acantilado del Hudson, con los Palisades enfrente. Es el lugar mas tranquilo de los cinco boroughs.",
  jp=1, th=1, tags=["jardin","vista"])

a(id="westlight", n="Westlight (rooftop)", cat="mirador", hood="Williamsburg", boro="Brooklyn",
  sub="Bedford Av (L)", lat=40.7211, lng=-73.9575, addr="111 N 12th St, piso 22, Brooklyn",
  cost=20, costN="Sin cover. Precio de un trago (~$20).",
  dur=1, why="Panoramica completa de Manhattan desde Brooklyn, terraza abierta, sin entrada. La alternativa honesta a pagar $60 por un observatorio.",
  jp=2, th=2, tags=["bar","skyline"])

a(id="thecrown", n="The Crown (50 Bowery)", cat="mirador", hood="Chinatown", boro="Manhattan",
  sub="Grand St (B,D), Canal St", lat=40.7166, lng=-73.9962, addr="50 Bowery, piso 21",
  cost=20, costN="Sin cover. Happy hour mar-vie 16-18h.",
  dur=1, why="Vista desde el sur con el Manhattan Bridge y los puentes en primer plano. Angulo que no da ningun observatorio pago.",
  jp=1, th=2, tags=["bar","skyline"])

a(id="valentino", n="Louis Valentino Jr. Pier", cat="mirador", hood="Red Hook", boro="Brooklyn",
  sub="sin subte: NYC Ferry o bus B61 desde Carroll St (F,G)", lat=40.6787, lng=-74.0166,
  addr="Ferris St & Coffey St, Brooklyn", cost=0,
  dur=0.5, why="La Estatua de la Libertad de frente, gratis, casi siempre vacio. La alternativa real al ferry pago.",
  jp=2, th=2, tags=["gratis","skyline"])

# ─────────────────────────────────  MUSEOS  ─────────────────────────────────
a(id="met", n="The Metropolitan Museum of Art", cat="museo", hood="Upper East Side", boro="Manhattan",
  sub="86 St (4,5,6)", lat=40.7794, lng=-73.9632, addr="1000 5th Ave",
  cost=30, costN="$30. El pay-what-you-wish alcanza a residentes del Estado de NY Y a estudiantes de NY, NJ y CT (no solo residentes): un turista extranjero paga los $30. Incluye The Cloisters el MISMO dia. NO esta en ningun pase.",
  closed="miercoles", dur=4, why="Uno de los tres museos mas importantes del mundo. Imposible de agotar: elegir dos alas y hacerlas bien (egipcio + pintura europea, o armas + arte islamico).",
  main=True, jp=2, th=1, tags=["imprescindible"])

a(id="cloisters", n="The Met Cloisters", cat="museo", hood="Fort Tryon Park", boro="Manhattan",
  sub="190 St (A)", lat=40.8649, lng=-73.9319, addr="99 Margaret Corbin Dr",
  cost=0, costN="INCLUIDO en la entrada del MET del mismo dia.", closed="miercoles",
  dur=3, why="Arte medieval en un edificio armado con claustros franceses reales, sobre un acantilado del Hudson. Casi no se cruza con el flujo turistico del MET principal.",
  jp=2, th=2, tags=["arquitectura","escondido"])

a(id="moma", n="MoMA", cat="museo", hood="Midtown", boro="Manhattan",
  sub="5 Av/53 St (E,M)", lat=40.7614, lng=-73.9776, addr="11 W 53rd St",
  cost=30, costN="$30. El cine esta INCLUIDO en la entrada general.",
  free="Viernes UNIQLO: solo residentes del Estado de NY. No aplica para turistas.",
  dur=3, why="Van Gogh, Picasso, Warhol, Rothko en un solo recorrido. Denso y muy concurrido: ir a la apertura o en las ultimas dos horas.",
  main=True, jp=2, th=1, tags=["imprescindible"])

a(id="whitney", n="Whitney Museum", cat="museo", hood="Meatpacking", boro="Manhattan",
  sub="14 St (A,C,E), 8 Av (L)", lat=40.7396, lng=-74.0089, addr="99 Gansevoort St",
  cost=30, costN="$30. Menores de 25 GRATIS siempre.", closed="martes",
  free="VIERNES 17-22h GRATIS PARA TODOS (sin restriccion de residencia) - REQUIERE TICKET RESERVADO, el cupo es limitado",
  dur=2.5, why="Arte estadounidense del siglo XX y XXI en el edificio de Renzo Piano, con terrazas escalonadas sobre el High Line. El viernes a la noche es gratis y la vista al atardecer es parte de la visita.",
  book="OBLIGATORIA para el viernes gratis: los tickets se liberan hasta 5 semanas antes y el cupo se agota. OJO: desde el 19 de agosto volvio al horario regular y CIERRA LOS MARTES.",
  jp=2, th=2, tags=["gratis-viernes","arquitectura"])

a(id="guggenheim", n="Guggenheim", cat="museo", hood="Upper East Side", boro="Manhattan",
  sub="86 St (4,5,6)", lat=40.7830, lng=-73.9590, addr="1071 5th Ave",
  cost=16, costN="~$16 reducido hasta el 17-sep-2026 por cambio de muestra en la rotonda (VERIFICAR). $30 despues.",
  free="Martes y domingos 16:00-17:30 pay-what-you-wish (sugerido $10, minimo $1) - NO CONFIRMADO en fuente oficial, solo en la oficina de turismo de NYC. LLAMAR ANTES.",
  dur=2, why="El edificio de Frank Lloyd Wright vale la entrada por si solo: se sube en ascensor y se baja caminando la rampa espiralada. OJO: la rotonda esta en montaje durante el viaje, la muestra nueva abre el 18 de septiembre.",
  main=True, book="PWYW con cupo muy limitado. VERIFICAR POR TELEFONO antes de ir: el sitio del museo no publica el precio de forma legible y la rotonda esta en montaje.", jp=1, th=1, tags=["arquitectura","verificar"])

a(id="amnh", n="American Museum of Natural History", cat="museo", hood="Upper West Side", boro="Manhattan",
  sub="81 St-Museum of Natural History (B,C)", lat=40.7813, lng=-73.9740, addr="200 Central Park West",
  cost=37, costN="$37 general; $43 con exhibicion; $48 all access.",
  dur=3, why="Dinosaurios, la ballena azul y el nuevo Gilder Center de Studio Gang. A 4 cuadras del hotel The Beacon.",
  main=True, jp=1, th=0, tags=["cerca-beacon"])

a(id="frick", n="The Frick Collection", cat="museo", hood="Upper East Side", boro="Manhattan",
  sub="68 St-Hunter College (6)", lat=40.7712, lng=-73.9673, addr="1 E 70th St",
  cost=30, costN="$30", closed="martes",
  free="MIERCOLES 13:30-17:30 pay-what-you-wish. Online el minimo es $5 y garantiza la entrada; para pagar menos hay que ir en persona, sin garantia de lugar.",
  dur=2, why="La coleccion privada de un magnate del acero, en su propia mansion: Vermeer, Rembrandt, Bellini colgados como en una casa. Reabrio en 2025 tras cinco anos de obra. Es el museo mas placentero de NYC.",
  jp=2, th=2, tags=["escondido","gratis-miercoles"])

a(id="mcny", n="Museum of the City of New York", cat="museo", hood="East Harlem", boro="Manhattan",
  sub="103 St (6)", lat=40.7924, lng=-73.9518, addr="1220 5th Ave",
  cost=23, costN="$23", free="MIERCOLES GRATIS TODO EL DIA para todos - los tickets gratis SOLO se retiran en la ventanilla del museo, no online",
  dur=2, why="La historia de la ciudad contada bien, incluida 'Timescapes'. El mejor lugar para entender NYC en las primeras 48 horas. Y los miercoles no cuesta nada.",
  jp=2, th=1, tags=["gratis-miercoles","contexto"])

a(id="tenement", n="Tenement Museum", cat="museo", hood="Lower East Side", boro="Manhattan",
  sub="Delancey-Essex St (F,J,M,Z)", lat=40.7188, lng=-73.9901, addr="103 Orchard St",
  cost=33, costN="$30 por tour + $3 fee. Cada tour se paga aparte. NO esta en ningun pase. Sin reembolso.",
  dur=1.75, why="Departamentos restaurados de familias inmigrantes reales, solo con guia. No es un museo de objetos: es la historia de la inmigracion contada dentro de la casa donde paso.",
  book="OBLIGATORIA - muchos tours se agotan; tickets extra se liberan los jueves", jp=2, th=2, tags=["escondido","historia"])

a(id="morgan", n="The Morgan Library & Museum", cat="museo", hood="Murray Hill", boro="Manhattan",
  sub="33 St (6), Grand Central", lat=40.7492, lng=-73.9814, addr="225 Madison Ave",
  cost=25, costN="$25", closed="lunes",
  free="VIERNES 17-20h GRATIS - reserva obligatoria, se liberan 1 semana antes (para el vie 4/9: reservar el vie 28/8)",
  dur=1.5, why="La biblioteca privada de J.P. Morgan: tres pisos de estanterias de nogal, una Biblia de Gutenberg y manuscritos originales. Sala pequena, impacto enorme.",
  book="obligatoria para el viernes gratis", jp=2, th=2, tags=["gratis-viernes","escondido"])

a(id="noguchi", n="The Noguchi Museum", cat="museo", hood="Long Island City", boro="Queens",
  sub="Broadway (N,W), Queensbridge (F)", lat=40.7684, lng=-73.9364, addr="9-01 33rd Rd, LIC",
  cost=16, costN="~$16 (verificar 2026)", closed="lunes y martes",
  free="1er viernes del mes GRATIS con horario extendido hasta las 20h -> viernes 4 de septiembre",
  dur=2, why="Noguchi diseno el museo el mismo alrededor de su taller, con un jardin de esculturas. Silencio absoluto. Es la visita mas serena de la ciudad.",
  book="reserva con horario", jp=2, th=2, tags=["escondido","gratis-viernes","arquitectura"])

a(id="bkmuseum", n="Brooklyn Museum", cat="museo", hood="Prospect Heights", boro="Brooklyn",
  sub="Eastern Pkwy-Brooklyn Museum (2,3)", lat=40.6712, lng=-73.9636, addr="200 Eastern Pkwy, Brooklyn",
  cost=16, costN="$16 sugerido (contribucion voluntaria); $25 con muestra temporaria",
  closed="lunes y martes", dur=3,
  why="Coleccion egipcia de primer nivel y 'The Dinner Party' de Judy Chicago en exhibicion permanente. Es el museo grande al que no va nadie, y eso lo mejora.",
  jp=2, th=2, tags=["escondido"])

a(id="momaps1", n="MoMA PS1", cat="museo", hood="Long Island City", boro="Queens",
  sub="21 St-Van Alst (G), Court Sq (7,E,M)", lat=40.7455, lng=-73.9476, addr="22-25 Jackson Ave, LIC",
  cost=0, costN="GRATIS para todos (donacion de Sonya Yu). Es la politica vigente, no una garantia escrita para todo 2026.", closed="martes y miercoles",
  dur=2.5, why="Escuela publica reconvertida en arte contemporaneo con riesgo real: lo que el MoMA no se anima a mostrar. Y en 2026 no cuesta nada.",
  jp=2, th=2, tags=["gratis","escondido","contemporaneo"])

a(id="studiomuseum", n="Studio Museum in Harlem", cat="museo", hood="Harlem", boro="Manhattan",
  sub="125 St (2,3,A,B,C,D)", lat=40.8089, lng=-73.9476, addr="144 W 125th St",
  cost=16, costN="Pay-what-you-can, sugerido $16", closed="lunes y martes",
  free="DOMINGOS GRATIS", dur=2,
  why="Reabrio en noviembre 2025 en un edificio nuevo de David Adjaye. Es la novedad arquitectonica y curatorial mas relevante de la ciudad ahora mismo, y casi ningun turista lo sabe.",
  jp=2, th=2, tags=["escondido","arquitectura","nuevo"])

a(id="momi", n="Museum of the Moving Image", cat="museo", hood="Astoria", boro="Queens",
  sub="Steinway St (M,R), 36 Av (N,W)", lat=40.7565, lng=-73.9242, addr="36-01 35th Ave, Astoria",
  cost=20, costN="$20", free="JUEVES 14-18h GRATIS -> jueves 3 de septiembre",
  closed="lunes, martes y miercoles", dur=2.5,
  why="Historia material del cine y la television, con la coleccion permanente de Jim Henson (los Muppets originales). Interactivo de verdad, no de vitrina.",
  jp=2, th=2, tags=["gratis-jueves","escondido"])

a(id="transitmuseum", n="New York Transit Museum", cat="museo", hood="Brooklyn Heights", boro="Brooklyn",
  sub="Court St-Borough Hall (2,3,4,5,R)", lat=40.6906, lng=-73.9903, addr="99 Schermerhorn St, Brooklyn",
  cost=10, closed="lunes y martes", dur=1.5,
  why="Una estacion de subte clausurada de 1936 con 20 vagones historicos en las vias originales; se puede subir a todos. AVISO: el aire acondicionado de las galerias traseras esta roto.",
  jp=2, th=2, tags=["escondido","barato"])

a(id="cityreliquary", n="The City Reliquary", cat="museo", hood="Williamsburg", boro="Brooklyn",
  sub="Metropolitan Av (G), Lorimer St (L)", lat=40.7147, lng=-73.9515, addr="370 Metropolitan Ave, Brooklyn",
  cost=7, closed="de lunes a viernes (solo abre sábados y domingos 12-18h)", dur=0.75,
  why="Museo de objetos descartados de NYC en una vidriera: fichas de subte, fragmentos de la Feria Mundial, botellas de seltzer. Absurdo y encantador.",
  jp=1, th=2, tags=["escondido","raro"])

a(id="eldridge", n="Museum at Eldridge Street", cat="arq", hood="Chinatown / LES", boro="Manhattan",
  sub="East Broadway (F), Grand St (B,D)", lat=40.7146, lng=-73.9934, addr="12 Eldridge St",
  cost=15, costN="$15. Lunes y viernes pay-what-you-wish.", closed="SABADOS (es sinagoga)",
  dur=1, why="Sinagoga de 1887 restaurada por $20 millones, con un roseton nuevo de Kiki Smith. Que hoy este en el medio de Chinatown es la mitad del punto.",
  jp=2, th=2, tags=["escondido","arquitectura"])

a(id="911museum", n="9/11 Memorial Museum", cat="museo", hood="Financial District", boro="Manhattan",
  sub="WTC Cortlandt (1), Fulton St", lat=40.7115, lng=-74.0134, addr="180 Greenwich St",
  cost=36, costN="$36 general. El memorial exterior (las fuentes) es SIEMPRE gratis.",
  closed="martes (salvo algunos)", free="los lunes hay franja gratis por la tarde (la mecanica y el horario cambian: verificar en 911memorial.org)",
  dur=2.5, why="Duro y muy bien hecho. Si el presupuesto aprieta, el memorial exterior solo ya transmite casi todo.",
  book="OBLIGATORIA - timed ticket", jp=2, th=1, tags=["intenso"])

a(id="intrepid", n="Intrepid Museum", cat="museo", hood="Hell's Kitchen", boro="Manhattan",
  sub="50 St (C,E) + caminata", lat=40.7644, lng=-74.0000, addr="Pier 86, W 46th St & 12th Ave",
  cost=38, costN="$38. Add-ons: Concorde $13, VR Apollo $13.",
  dur=2.5, why="Portaaviones de la Segunda Guerra con un transbordador espacial y un submarino. Esta a 3 cuadras del hotel Ink48.",
  jp=1, th=0, tags=["cerca-ink48"])

a(id="diabeacon", n="Dia Beacon (excursion)", cat="museo", hood="Beacon, NY", boro="Fuera de NYC",
  sub="Metro-North desde Grand Central, ~80 min", lat=41.5045, lng=-73.9843, addr="3 Beekman St, Beacon NY",
  cost=60, costN="$25 entrada + ~$35 tren ida y vuelta", closed="martes, miercoles y jueves",
  dur=8, why="Fabrica Nabisco de 1929 convertida en 28.000 m2 de minimalismo con luz cenital: Richard Serra, Walter De Maria, Agnes Martin. Es la mejor excursion de arte del estado, pero se come un dia entero.",
  jp=1, th=1, tags=["excursion","arte"])

# ─────────────────────────  BARRIOS Y CAMINATAS  ─────────────────────────
a(id="jacksonheights", n="Jackson Heights", cat="barrio", hood="Jackson Heights", boro="Queens",
  sub="74 St-Roosevelt Av (7,E,F,M,R)", lat=40.7469, lng=-73.8912, addr="74th St & Roosevelt Ave, Queens",
  cost=0, dur=4.5, why="Cuatro cuadras donde conviven el corredor indio-bangladesi de 74th St con el enclave tibetano-nepali mas denso del hemisferio occidental, mas colombianos y ecuatorianos sobre Roosevelt. Ningun otro barrio te da tres cocinas del sur de Asia caminando 300 metros.",
  jp=2, th=2, tags=["comida","etnico","caminata"])

a(id="astoria", n="Astoria", cat="barrio", hood="Astoria", boro="Queens",
  sub="Broadway o 30 Av (N,W)", lat=40.7644, lng=-73.9235, addr="30th Ave & 31st St, Astoria",
  cost=0, dur=5, why="El nucleo griego real, no la version de menu turistico. En una sola caminata: Socrates Sculpture Park, el Noguchi, tabernas griegas y Astoria Park bajo el Hell Gate Bridge al atardecer.",
  jp=2, th=2, tags=["comida","caminata","arte"])

a(id="greenpoint", n="Greenpoint", cat="barrio", hood="Greenpoint", boro="Brooklyn",
  sub="Nassau Av o Greenpoint Av (G)", lat=40.7304, lng=-73.9540, addr="Manhattan Ave & Nassau Ave, Brooklyn",
  cost=0, dur=4, why="La Polonia de Nueva York, todavia funcionando: carnicerias, panaderias y bares donde se pide en polaco. Es el ultimo barrio etnico europeo intacto; el resto se gentrifico del todo.",
  jp=2, th=2, tags=["comida","etnico","caminata"])

a(id="sunsetpark", n="Sunset Park (barrio)", cat="barrio", hood="Sunset Park", boro="Brooklyn",
  sub="45 St / 53 St (R), 8 Av (N)", lat=40.6452, lng=-74.0122, addr="5th Ave & 45th St, Brooklyn",
  cost=0, dur=4.5, why="Dos barrios paralelos: 5th Avenue es mexicana-poblana, 8th Avenue es el Chinatown fujianes (mas grande que el de Manhattan). El contraste etnico mas brusco que se puede caminar en 15 minutos.",
  jp=2, th=2, tags=["comida","etnico","caminata"])

a(id="arthurave", n="Arthur Avenue (Belmont)", cat="barrio", hood="Belmont", boro="Bronx",
  sub="Fordham Rd (B,D,4) o Metro-North a Fordham", lat=40.8546, lng=-73.8875, addr="Arthur Ave & E 187th St, Bronx",
  cost=0, dur=4.5, why="La Little Italy real. En Mulberry Street quedan ocho restaurantes para turistas; aca quedan las carnicerias, los panaderos de 1918 y la gente haciendo las compras. Encima hay un enclave albanes.",
  jp=2, th=2, tags=["comida","etnico"])

a(id="harlem", n="Harlem", cat="barrio", hood="Harlem", boro="Manhattan",
  sub="125 St (2,3,A,B,C,D)", lat=40.8090, lng=-73.9465, addr="W 125th St, Manhattan",
  cost=0, dur=4, why="El Studio Museum nuevo de Adjaye, Strivers' Row (casas de 1891 entre la 138 y la 139), Marcus Garvey Park y las brownstones de Mount Morris. Arquitectura residencial que no se parece a nada en el resto de la ciudad.",
  jp=2, th=2, tags=["arquitectura","musica","caminata"])

a(id="les", n="Lower East Side", cat="barrio", hood="Lower East Side", boro="Manhattan",
  sub="Delancey-Essex St (F,J,M,Z)", lat=40.7180, lng=-73.9880, addr="Orchard St & Delancey St",
  cost=0, dur=4, why="La unica parte de Manhattan donde tres capas de inmigracion (judia, china, dominicana) siguen visibles en la misma cuadra. Essex Market, Eldridge Street, Tenement Museum, Katz's.",
  jp=2, th=2, tags=["comida","historia","caminata"])

a(id="redhook", n="Red Hook", cat="barrio", hood="Red Hook", boro="Brooklyn",
  sub="sin subte: NYC Ferry o bus B61 desde Carroll St (F,G)", lat=40.6752, lng=-74.0110,
  addr="Van Brunt St, Brooklyn", cost=0, dur=3.5,
  why="Adoquines, gruas portuarias, ni una torre a la vista. El unico barrio de NYC que se siente como un pueblo portuario. Que no tenga subte es exactamente la razon por la que sigue asi.",
  jp=2, th=2, tags=["escondido","caminata","agua"])

a(id="ridgewood", n="Ridgewood", cat="barrio", hood="Ridgewood", boro="Queens",
  sub="Forest Av o Seneca Av (M), Myrtle-Wyckoff (L,M)", lat=40.7005, lng=-73.9057,
  addr="Forest Ave, Ridgewood, Queens", cost=0, dur=3.5,
  why="Aleman-yugoslavo historico, ahora tambien nepali, mexicano y venezolano, con manzanas enteras de casas de ladrillo amarillo protegidas. Es lo que era Bushwick hace 15 anos, sin la puesta en escena.",
  jp=2, th=2, tags=["escondido","comida"])

a(id="bayridge", n="Bay Ridge", cat="barrio", hood="Bay Ridge", boro="Brooklyn",
  sub="86 St o Bay Ridge Av (R)", lat=40.6264, lng=-74.0300, addr="5th Ave & 86th St, Brooklyn",
  cost=0, dur=3.5, why="Enclave libanes-palestino-sirio sobre 5th Avenue, mas el mejor paseo costero de la ciudad: se camina hasta quedar literalmente debajo del Verrazzano-Narrows Bridge.",
  jp=1, th=2, tags=["comida","escondido"])

a(id="flushing", n="Flushing", cat="barrio", hood="Flushing", boro="Queens",
  sub="Main St (7), ultima parada", lat=40.7596, lng=-73.8300, addr="Main St & Roosevelt Ave, Flushing",
  cost=0, dur=4, why="El Chinatown mas grande y mas regional de la ciudad: dongbei, Xi'an, uigur, taiwanes, y coreano al lado. El de Manhattan es mayormente cantones y turistico; aca se come regional de verdad. OJO: el 7 va lleno por el US Open.",
  jp=2, th=2, tags=["comida","etnico"])

a(id="inwood", n="Inwood", cat="barrio", hood="Inwood", boro="Manhattan",
  sub="Dyckman St o 207 St (A), 215 St (1)", lat=40.8677, lng=-73.9212, addr="Dyckman St, Manhattan",
  cost=0, dur=3.5, why="Inwood Hill Park es el unico bosque primario que queda en Manhattan, con cuevas de roca usadas por los Lenape. Abajo, Dyckman St es dominicana pura. Literalmente no parece Manhattan.",
  jp=2, th=2, tags=["gratis","naturaleza","comida"])

a(id="rooseveltisland", n="Roosevelt Island", cat="barrio", hood="Roosevelt Island", boro="Manhattan",
  sub="Tramway (59 St & 2 Av) o Roosevelt Island (F)", lat=40.7614, lng=-73.9500,
  addr="Roosevelt Island, New York", cost=3, dur=2.5,
  why="Se llega en teleferico por $3 y se camina hasta el FDR Four Freedoms Park de Louis Kahn, pasando por las ruinas del Smallpox Hospital. Una de las mejores obras de arquitectura moderna de la ciudad, gratis y vacia.",
  jp=2, th=2, tags=["arquitectura","gratis","vista"])

a(id="westvillage", n="West Village", cat="barrio", hood="West Village", boro="Manhattan",
  sub="Christopher St (1), W 4 St (A,B,C,D,E,F,M)", lat=40.7336, lng=-74.0027,
  addr="Bleecker St & Bank St", cost=0, dur=3,
  why="La unica grilla rota de Manhattan: calles curvas de 1800, casas bajas de ladrillo, y todos los clubes de jazz historicos a cuatro cuadras uno de otro. Se camina sin plan.",
  main=True, jp=2, th=1, tags=["caminata","jazz"])

a(id="dumbo", n="DUMBO", cat="barrio", hood="DUMBO", boro="Brooklyn",
  sub="York St (F), High St (A,C)", lat=40.7033, lng=-73.9881, addr="Washington St & Water St, Brooklyn",
  cost=0, dur=2, why="La foto del Manhattan Bridge encuadrado entre edificios (Washington y Water) y Brooklyn Bridge Park abajo. Muy turistico: ir antes de las 9 de la manana o se convierte en cola de fotos.",
  main=True, jp=2, th=0, tags=["foto","caminata"])

a(id="chinatown", n="Chinatown (Manhattan)", cat="barrio", hood="Chinatown", boro="Manhattan",
  sub="Canal St (J,N,Q,R,W,Z,6), Grand St (B,D)", lat=40.7158, lng=-73.9970, addr="Mott St & Canal St",
  cost=0, dur=2.5, why="El mas antiguo y todavia el mas denso. Vale por el paisaje urbano y las pescaderias de la calle, no tanto por los restaurantes (para eso, Flushing o Sunset Park).",
  main=True, jp=2, th=1, tags=["comida","caminata"])

# ────────────────────────────  GASTRONOMIA  ────────────────────────────
a(id="essexmarket", n="Essex Market", cat="comida", hood="Lower East Side", boro="Manhattan",
  sub="Essex St (J,M,Z), Delancey St (F)", lat=40.7189, lng=-73.9884, addr="88 Essex St",
  cost=20, dur=1, why="Mercado municipal desde 1940 en edificio nuevo. Sigue teniendo carniceros, pescaderos y verduleros de verdad, no solo puestos de comida para turistas.",
  jp=2, th=2, tags=["mercado"])

a(id="chelseamarket", n="Chelsea Market", cat="comida", hood="Chelsea", boro="Manhattan",
  sub="14 St-8 Av (A,C,E,L)", lat=40.7424, lng=-74.0061, addr="75 9th Ave",
  cost=22, dur=1.25, why="Vale, pero SOLO fuera de hora pico: el almuerzo de fin de semana es insoportable. Ir martes o miercoles 9-10h o 14:30-16h. Los Tacos No.1 y Very Fresh Noodles si valen.",
  main=True, jp=2, th=1, tags=["mercado","turistico"])

a(id="arthurmarket", n="Arthur Avenue Retail Market", cat="comida", hood="Belmont", boro="Bronx",
  sub="Fordham Rd (B,D,4)", lat=40.8541, lng=-73.8873, addr="2344 Arthur Ave, Bronx",
  cost=20, dur=1.5, why="Mercado techado de 1940 que LaGuardia construyo para sacar los carritos de la calle. Mike's Deli adentro: eggplant parm y arancini.",
  jp=2, th=2, tags=["mercado","italiano"])

a(id="newworldmall", n="New World Mall Food Court", cat="comida", hood="Flushing", boro="Queens",
  sub="Main St (7)", lat=40.7592, lng=-73.8306, addr="136-20 Roosevelt Ave, Flushing",
  cost=15, dur=1.5, why="Food court subterraneo con decenas de puestos regionales chinos. Cero concesiones al paladar occidental: ahi esta la gracia.",
  jp=2, th=2, tags=["mercado","chino","barato"])

a(id="katzs", n="Katz's Delicatessen", cat="comida", hood="Lower East Side", boro="Manhattan",
  sub="2 Av (F)", lat=40.7223, lng=-73.9874, addr="205 E Houston St",
  cost=32, costN="~$29 el sandwich de pastrami", dur=1.25,
  why="1888. El pastrami cura 30 dias y se corta a cuchillo. TRUCO: sentarse en el mostrador, dar propina al cortador, e ir un martes a las 15h en vez de un sabado al mediodia. Guardar el ticket o se paga multa.",
  main=True, jp=2, th=1, tags=["deli","clasico"])

a(id="splunch", n="S&P Lunch", cat="comida", hood="Flatiron", boro="Manhattan",
  sub="23 St (R,W,6)", lat=40.7412, lng=-73.9885, addr="174 5th Ave",
  cost=22, costN="$18-26", dur=1,
  why="Ocupa el local del Eisenberg's (1929), con pastrami cortado a mano. Es la alternativa a Katz's sin la cola ni el circo.",
  jp=2, th=2, tags=["deli","escondido"])

a(id="russdaughters", n="Russ & Daughters", cat="comida", hood="Lower East Side", boro="Manhattan",
  sub="2 Av (F)", lat=40.7226, lng=-73.9884, addr="179 E Houston St",
  cost=22, dur=0.75, why="Appetizing store de 1914, cuarta generacion de la misma familia. Salmon curado cortado a mano sobre bagel. El mostrador es mejor experiencia que el cafe de al lado.",
  main=True, jp=2, th=1, tags=["deli","clasico"])

a(id="frankels", n="Frankel's Delicatessen", cat="comida", hood="Greenpoint", boro="Brooklyn",
  sub="Nassau Av (G)", lat=40.7247, lng=-73.9509, addr="631 Manhattan Ave, Brooklyn",
  cost=20, costN="$15-25", dur=1,
  why="El pastrami-huevo-queso sobre challah entro en la lista del NYT de sandwiches que definen NYC. Deli judio version Brooklyn contemporaneo.",
  jp=2, th=2, tags=["deli","escondido"])

a(id="lhasa", n="Lhasa Fast Food", cat="comida", hood="Jackson Heights", boro="Queens",
  sub="74 St-Roosevelt Av (7,E,F,M,R)", lat=40.7480, lng=-73.8916, addr="37-50 74th St, Jackson Heights",
  cost=14, dur=1, why="Escondido al fondo de un pasillo detras de un local de celulares. Momos tibetanos y thukpa. VERIFICAR: puede figurar como 'Lhasa Tibetan Restaurant' en la misma direccion.",
  jp=2, th=2, tags=["tibetano","barato","escondido"])

a(id="nepalibhanchha", n="Nepali Bhanchha Ghar", cat="comida", hood="Jackson Heights", boro="Queens",
  sub="74 St-Roosevelt Av (7,E,F,M,R)", lat=40.7472, lng=-73.8905, addr="74-06 37th Rd, Jackson Heights",
  cost=18, dur=1.25, why="Jhol momo: dumplings de carne flotando en salsa de sesamo y tomate. Y sel roti. El mejor nepali de la ciudad segun la prensa gastronomica local.",
  jp=2, th=2, tags=["nepali","barato"])

a(id="jalapenoking", n="Jalapeno King", cat="comida", hood="Sunset Park", boro="Brooklyn",
  sub="45 St (R)", lat=40.6470, lng=-74.0090, addr="5th Ave entre 22nd y 23rd St, Brooklyn",
  cost=14, dur=1, why="Tortillas hechas en casa. La torta de bistec y las picaditas de carne. Mexicano poblano de barrio, sin traduccion al ingles.",
  jp=2, th=2, tags=["mexicano","barato"])

a(id="elbronco", n="Tacos El Bronco", cat="comida", hood="Sunset Park", boro="Brooklyn",
  sub="45 St (R)", lat=40.6480, lng=-74.0110, addr="4324 4th Ave, Brooklyn",
  cost=12, dur=0.75, why="Paso de food truck a local. Lengua, al pastor, cabeza, cueritos. Es el taco de barrio, no el de menu bilingue.",
  jp=2, th=2, tags=["mexicano","barato"])

a(id="henan", n="He Nan Mian Guan", cat="comida", hood="Flushing", boro="Queens",
  sub="Main St (7)", lat=40.7605, lng=-73.8320, addr="136-31 41st Ave, Flushing",
  cost=12, costN="~$20 para dos con bebida", dur=1,
  why="Fideos estirados a mano y rou jia mo (el 'hamburguesa' china de cerdo desmenuzado). Abre a las 6:30 de la manana.",
  jp=2, th=2, tags=["chino","barato"])

a(id="uyghur", n="New Nurlan Uyghur", cat="comida", hood="Flushing", boro="Queens",
  sub="Main St (7)", lat=40.7588, lng=-73.8290, addr="135-51 39th Ave, Flushing (subsuelo)",
  cost=22, dur=1.25, why="Cocina uigur, no china han: brochetas de cordero especiadas y dumplings de calabaza de masa finisima. Esta en el subsuelo de un hotel y no lo encuentra nadie.",
  jp=2, th=2, tags=["uigur","escondido"])

a(id="pierozek", n="Pierozek", cat="comida", hood="Greenpoint", boro="Brooklyn",
  sub="Nassau Av (G)", lat=40.7280, lng=-73.9525, addr="833 Manhattan Ave, Brooklyn",
  cost=18, dur=1, why="Bib Gourmand Michelin: el unico restaurante polaco de Estados Unidos reconocido por la guia. Pierogi ruskie y tatarskie.",
  jp=2, th=2, tags=["polaco","barato"])

a(id="karczma", n="Karczma", cat="comida", hood="Greenpoint", boro="Brooklyn",
  sub="Greenpoint Av (G)", lat=40.7305, lng=-73.9540, addr="136 Greenpoint Ave, Brooklyn",
  cost=25, dur=1.5, why="Bigos, golabki, panqueques de papa, y un plato de manteca de cerdo con pan de centeno y pepinos que es puro siglo XIX. Meseras de traje regional, y no es para turistas.",
  jp=2, th=2, tags=["polaco"])

a(id="casadellamozz", n="Casa Della Mozzarella", cat="comida", hood="Belmont", boro="Bronx",
  sub="Fordham Rd (B,D,4)", lat=40.8555, lng=-73.8858, addr="604 E 187th St, Bronx",
  cost=14, dur=0.5, why="Sandwich de mozzarella hecha esa manana con prosciutto y pimientos secos en pan de sesamo. Uno de los mejores sandwiches de la ciudad, y cuesta lo que una cerveza en Manhattan.",
  jp=2, th=2, tags=["italiano","barato"])

a(id="cosenza", n="Cosenza's Fish Market", cat="comida", hood="Belmont", boro="Bronx",
  sub="Fordham Rd (B,D,4)", lat=40.8544, lng=-73.8873, addr="2354 Arthur Ave, Bronx",
  cost=15, dur=0.5, why="Barra de ostras montada en la vereda, con los condimentos afuera. Se come parado en la calle. Es la mejor media hora de Arthur Avenue.",
  jp=2, th=2, tags=["italiano","mariscos"])

a(id="malecon", n="Malecon", cat="comida", hood="Washington Heights", boro="Manhattan",
  sub="175 St (A), 181 St (1)", lat=40.8480, lng=-73.9370, addr="4141 Broadway",
  cost=25, dur=1.25, why="Mofongo con chicharron y longaniza, y parrillada de mariscos. Dominicano de verdad, con musica latina los fines de semana.",
  jp=2, th=2, tags=["dominicano"])

a(id="tanoreen", n="Tanoreen", cat="comida", hood="Bay Ridge", boro="Brooklyn",
  sub="86 St (R)", lat=40.6229, lng=-74.0290, addr="7523 3rd Ave, Brooklyn",
  cost=35, dur=1.5, why="Palestino, en el Michelin Guide. Coliflor frita con tahini y halloumi frito. La chef Rawia Bishara es una institucion.",
  jp=1, th=2, tags=["palestino"])

a(id="kyclades", n="Taverna Kyclades", cat="comida", hood="Astoria", boro="Queens",
  sub="30 Av (N,W)", lat=40.7688, lng=-73.9130, addr="33-07 Ditmars Blvd, Astoria",
  cost=40, dur=1.5, why="Pescado griego a la parrilla, entero, con limon. La referencia del barrio desde hace decadas y en el Michelin Guide. No toman reserva: hay cola.",
  jp=2, th=2, tags=["griego"])

a(id="rudys", n="Rudy's Pastry Shop", cat="comida", hood="Ridgewood", boro="Queens",
  sub="Seneca Av (M)", lat=40.7040, lng=-73.9070, addr="905 Seneca Ave, Ridgewood",
  cost=6, dur=0.5, why="Abierta en 1934, la panaderia mas vieja de Queens. Black & white cookies a ~$4 y reposteria alemana que ya casi no existe.",
  jp=2, th=2, tags=["panaderia","barato"])

a(id="lbspumoni", n="L&B Spumoni Gardens", cat="comida", hood="Gravesend", boro="Brooklyn",
  sub="Avenue X (F)", lat=40.5945, lng=-73.9814, addr="2725 86th St, Brooklyn",
  cost=15, dur=1.25, why="La square slice siciliana con la salsa ARRIBA del queso; es su invento y sigue siendo la mejor. Y el spumoni de postre. Vale el viaje hasta el sur de Brooklyn.",
  jp=2, th=2, tags=["pizza","clasico"])

a(id="totonnos", n="Totonno's", cat="comida", hood="Coney Island", boro="Brooklyn",
  sub="Coney Island-Stillwell Av (D,F,N,Q)", lat=40.5787, lng=-73.9836, addr="1524 Neptune Ave, Brooklyn",
  cost=18, dur=1, why="Horno de carbon desde 1924, cuarta generacion. Se combina con caminar el boardwalk de Coney Island.",
  jp=2, th=2, tags=["pizza","clasico"])

a(id="lucali", n="Lucali", cat="comida", hood="Carroll Gardens", boro="Brooklyn",
  sub="Carroll St (F,G)", lat=40.6800, lng=-73.9985, addr="575 Henry St, Brooklyn",
  cost=30, costN="solo efectivo, BYOB", dur=2,
  why="Considerada por muchos la mejor pizza de NYC. SIN reservas: hay que ir a anotarse cuando abren y volver despues. Solo si tienen paciencia.",
  jp=1, th=1, tags=["pizza","cola"])

a(id="manos", n="Mano's Pizzeria", cat="comida", hood="Ridgewood", boro="Queens",
  sub="Forest Av (M)", lat=40.7035, lng=-73.9020, addr="6202 Forest Ave, Ridgewood",
  cost=5, costN="porcion $3.75-4", dur=0.5,
  why="La porcion plegable clasica de NY por cuatro dolares. Esto es lo que la gente come de verdad, no la cola de una hora en Prince Street.",
  jp=2, th=2, tags=["pizza","barato"])

a(id="lostacos", n="Los Tacos No. 1", cat="comida", hood="Chelsea", boro="Manhattan",
  sub="14 St-8 Av (A,C,E,L)", lat=40.7424, lng=-74.0061, addr="75 9th Ave (Chelsea Market)",
  cost=15, dur=0.5, why="Lo mejor de Chelsea Market y de las pocas cosas por las que vale entrar. Adobada y nopal, tortilla hecha ahi. Se come parado.",
  main=True, jp=2, th=1, tags=["mexicano","barato"])

a(id="bosbagels", n="Bo's Bagels", cat="comida", hood="Harlem", boro="Manhattan",
  sub="116 St (B,C)", lat=40.8035, lng=-73.9540, addr="235 W 116th St",
  cost=8, dur=0.5, why="El unico bagel shop dedicado de Harlem: mas chicos y densos que el estandar, con za'atar y pumpernickel-arandano.",
  jp=2, th=2, tags=["bagel","barato"])

a(id="dekalb", n="DeKalb Market Hall", cat="comida", hood="Downtown Brooklyn", boro="Brooklyn",
  sub="DeKalb Av (B,Q,R), Jay St-MetroTech", lat=40.6902, lng=-73.9832, addr="445 Albee Square W, Brooklyn",
  cost=20, dur=1, why="El food hall mas honesto de Brooklyn. Tiene una sucursal de Katz's adentro, sin la cola de Houston Street.",
  jp=1, th=2, tags=["mercado"])

a(id="timeoutmarket", n="Time Out Market", cat="comida", hood="DUMBO", boro="Brooklyn",
  sub="York St (F), High St (A,C)", lat=40.7027, lng=-73.9906, addr="55 Water St, Brooklyn",
  cost=25, dur=1.25, why="Food hall curado con terraza que da al Brooklyn Bridge. Es turistico y esta bien: la terraza al atardecer justifica la parada.",
  main=True, jp=1, th=1, tags=["mercado","vista"])

# ─────────────────────────────  JAZZ Y MUSICA  ─────────────────────────────
a(id="vanguard", n="Village Vanguard", cat="musica", hood="West Village", boro="Manhattan",
  sub="14 St (1,2,3)", lat=40.7369, lng=-74.0016, addr="178 7th Ave South",
  cost=45, costN="$45 la entrada GA (YA COMPRADA, 26/8) + minimo de UNA consumicion por persona - vale gaseosa, jugo o agua. No sirven comida. Aceptan tarjeta.",
  dur=2, why="El club de jazz en funcionamiento continuo mas antiguo del mundo. 123 asientos, sotano triangular, acustica legendaria. DEL 1 AL 6 DE SEPTIEMBRE: John Patitucci Trio con Chris Potter y Brian Blade. Si hay una sola noche de musica en el viaje, es esta.",
  book="HECHA: 2 entradas GA del viernes 4/9, set 22:00 (#18741454 y #18741456). El acomodo del segundo set arranca 21:30 y es por orden de llegada.", jp=2, th=2, tags=["jazz","imprescindible"])

a(id="smalls", n="Smalls Jazz Club", cat="musica", hood="West Village", boro="Manhattan",
  sub="Christopher St (1)", lat=40.7340, lng=-74.0022, addr="183 W 10th St",
  cost=25, costN="$25 incluye una bebida", dur=2,
  why="60 asientos, sotano. Entre semana se entra caminando. Lo mejor que tiene son las jam sessions de madrugada de jueves a sabado, desde la 1:00 AM: ahi tocan los musicos que salieron de trabajar.",
  jp=2, th=2, tags=["jazz","tarde"])

a(id="mezzrow", n="Mezzrow", cat="musica", hood="West Village", boro="Manhattan",
  sub="Christopher St (1)", lat=40.7339, lng=-74.0023, addr="163 W 10th St",
  cost=25, costN="$25 incluye una bebida", dur=1.5,
  why="35 asientos, sala de escucha centrada en el piano. El mas intimo de la ciudad. Entre semana se consigue; los fines de semana se agota.",
  book="reservar", jp=2, th=2, tags=["jazz","intimo"])

a(id="birdland", n="Birdland", cat="musica", hood="Midtown", boro="Manhattan",
  sub="42 St-Port Authority (A,C,E)", lat=40.7590, lng=-73.9905, addr="315 W 44th St",
  cost=45, costN="$20-45 cover + $20 minimo por persona por set. Solo TicketWeb.", dur=2,
  why="Menos intimo que el Vanguard, mas programacion. Los LUNES: Vince Giordano & the Nighthawks, jazz de los anos 20-30 con instrumentos de epoca. Justo el lunes 31, que es el dia que Broadway esta oscuro.",
  book="TicketWeb - unico vendedor autorizado", jp=2, th=1, tags=["jazz","cerca-ink48"])

a(id="dizzys", n="Dizzy's Club (Jazz at Lincoln Center)", cat="musica", hood="Columbus Circle", boro="Manhattan",
  sub="59 St-Columbus Circle (1,A,B,C,D)", lat=40.7684, lng=-73.9832, addr="10 Columbus Circle, piso 5",
  cost=45, costN="$20-45 + $21-25 minimo. LATE NIGHT jue-sab ~22:45 desde $10-20.", dur=2,
  why="Ventanales de piso a techo sobre Central Park detras del escenario. El truco es el set Late Night de jueves a sabado: mismo lugar, una fraccion del precio.",
  jp=2, th=1, tags=["jazz","vista"])

a(id="bluenote", n="Blue Note", cat="musica", hood="Greenwich Village", boro="Manhattan",
  sub="W 4 St (A,B,C,D,E,F,M)", lat=40.7310, lng=-74.0007, addr="131 W 3rd St",
  cost=45, costN="$20-45 + $5 minimo de mesa", dur=2,
  why="El mas grande y comercial de los clubes historicos (250 personas). 29-30 ago: MonoNeon. 4-5 sep: Chief Adjuah.",
  main=True, jp=1, th=1, tags=["jazz"])

a(id="lunatico", n="Bar LunAtico", cat="musica", hood="Bedford-Stuyvesant", boro="Brooklyn",
  sub="Halsey St (J), Kingston-Throop (C)", lat=40.6842, lng=-73.9282, addr="486 Halsey St, Brooklyn",
  cost=10, costN="$10 sugerido EN EFECTIVO - los musicos cobran de las donaciones", dur=2.5,
  why="Bar de barrio de musicos, no de publico. Dos sets todas las noches (21:00 y 22:15), cocina y cocteleria completas. Es la mejor relacion musica/precio de la ciudad. LLEVAR EFECTIVO.",
  jp=2, th=2, tags=["jazz","barato","escondido"])

a(id="barbayeux", n="Bar Bayeux", cat="musica", hood="Prospect Lefferts Gardens", boro="Brooklyn",
  sub="Sterling St (2,5)", lat=40.6620, lng=-73.9540, addr="1066 Nostrand Ave, Brooklyn",
  cost=0, costN="Frecuentemente sin cover (minimo de consumo)", dur=2,
  why="Wine bar de barrio con jazz de verdad y sin entrada. El mas barato de la lista.",
  jp=2, th=2, tags=["jazz","gratis","escondido"])

a(id="barbes", n="Barbes", cat="musica", hood="Park Slope", boro="Brooklyn",
  sub="7 Av (F,G)", lat=40.6690, lng=-73.9840, addr="376 9th St, Brooklyn",
  cost=15, costN="Donacion sugerida ~$10-20, efectivo", dur=2,
  why="No es jazz: musica latina, balcanica, brasilena y de Africa occidental. La programacion es de otro nivel y la trastienda es minuscula. Llegar temprano.",
  jp=2, th=2, tags=["musica","escondido","barato"])

a(id="ornithology", n="Ornithology Jazz Club", cat="musica", hood="Bushwick", boro="Brooklyn",
  sub="Jefferson St (L)", lat=40.7065, lng=-73.9225, addr="6 Suydam St, Brooklyn",
  cost=20, costN="$15-25", dur=2,
  why="75 asientos y regla estricta de sala de escucha: no se habla durante los sets. Es la alternativa joven al Vanguard.",
  jp=2, th=2, tags=["jazz","escondido"])

a(id="billsplace", n="Bill's Place", cat="musica", hood="Harlem", boro="Manhattan",
  sub="135 St (2,3)", lat=40.8146, lng=-73.9425, addr="148 W 133rd St",
  cost=35, costN="~$30-40 el set, entrada por la web. BYOB: se lleva la bebida propia.", dur=1.75,
  why="Speakeasy real en el living de un brownstone de la calle 133 — la cuadra que en los anos 20 era Swing Street. "
      "Bill Saxton y los Harlem All-Stars tocan VIERNES Y SABADO a las 19:00 y 21:30, a tres metros del publico. "
      "Reemplaza a Showman's, que cerro definitivamente en 2026.",
  book="OBLIGATORIA - sala diminuta, comprar el set en billsplaceharlem.com", jp=2, th=2,
  tags=["jazz","escondido","imprescindible"])

a(id="nublu", n="Nublu", cat="musica", hood="East Village", boro="Manhattan",
  sub="1 Av (L)", lat=40.7240, lng=-73.9780, addr="151 Avenue C, piso 2",
  cost=20, dur=2.5, why="Jazz experimental, afrobeat y electronica turca. Musica en vivo desde las 19:00, DJs hasta las 4:00. 'Producer Mondays' todos los lunes a las 22:00.",
  jp=1, th=2, tags=["musica","tarde"])

# ─────────────────────────────  ARQUITECTURA  ─────────────────────────────
a(id="grandcentral", n="Grand Central Terminal", cat="arq", hood="Midtown East", boro="Manhattan",
  sub="Grand Central-42 St (4,5,6,7,S)", lat=40.7527, lng=-73.9772, addr="89 E 42nd St",
  cost=0, dur=1, why="Beaux-Arts de 1913: el techo celeste pintado al reves, la Whispering Gallery frente al Oyster Bar (dos personas en esquinas opuestas se escuchan susurrar), las escaleras de marmol. AVISO: el tour gratuito semanal esta suspendido.",
  main=True, jp=2, th=1, tags=["gratis","arquitectura"])

a(id="nypl", n="New York Public Library (Schwarzman)", cat="arq", hood="Midtown", boro="Manhattan",
  sub="5 Av-Bryant Pk (7,B,D,F,M)", lat=40.7532, lng=-73.9822, addr="476 5th Ave",
  cost=0, costN="GRATIS. Tours gratuitos lun-sab 11:00 y 14:00 (edificio); 11:20, 13:30 y 15:00 (Rose Room).",
  dur=1.25, why="La Rose Main Reading Room: 90 metros de largo, techos de 15. Y no es un museo: hay gente trabajando ahi. Entrar y sentarse un rato es parte de la experiencia.",
  main=True, jp=2, th=1, tags=["gratis","arquitectura"])

a(id="chrysler", n="Lobby del Chrysler Building", cat="arq", hood="Midtown East", boro="Manhattan",
  sub="Grand Central-42 St (4,5,6,7,S)", lat=40.7516, lng=-73.9755, addr="405 Lexington Ave",
  cost=0, costN="GRATIS, lun-vie 8-18h. Fotos si, video no.", closed="sabados y domingos",
  dur=0.35, why="Art deco de 1930 en estado puro: mural del techo y puertas de ascensor con marqueteria de maderas exoticas. NO hay observatorio: el lobby es todo lo que se puede ver, y alcanza.",
  jp=2, th=2, tags=["gratis","arquitectura","escondido"])

a(id="fordfoundation", n="Ford Foundation Atrium", cat="arq", hood="Midtown East", boro="Manhattan",
  sub="Grand Central-42 St", lat=40.7500, lng=-73.9700, addr="320 E 43rd St",
  cost=0, costN="GRATIS pero requiere preinscripcion online antes de las 17h del dia anterior",
  closed="fines de semana. CIERRA el 5, 6, 7 y 9 de septiembre; cierra temprano el 4",
  dur=0.75, why="Atrio-jardin de 12 pisos de altura de Kevin Roche (1967), con ~40 especies de arboles y espejo de agua, dentro de un edificio de oficinas. En este viaje solo se puede entrar del 31 de agosto al 3 de septiembre.",
  book="preinscripcion obligatoria", jp=2, th=2, tags=["gratis","arquitectura","escondido"])

a(id="littleisland", n="Little Island", cat="arq", hood="Meatpacking", boro="Manhattan",
  sub="14 St (A,C,E), 8 Av (L)", lat=40.7420, lng=-74.0110, addr="Pier 55, Hudson River Park, W 13th St",
  cost=0, dur=1, why="Parque flotante de Heatherwick sobre 132 'macetas' de hormigon de distinta altura. Gratis; en temporada alta puede pedir entrada con horario para la tarde-noche. Pegado al extremo sur del High Line.",
  main=True, jp=2, th=1, tags=["gratis","arquitectura"])

a(id="fdrpark", n="FDR Four Freedoms Park", cat="arq", hood="Roosevelt Island", boro="Manhattan",
  sub="Tramway o Roosevelt Island (F)", lat=40.7497, lng=-73.9605, addr="1 FDR Four Freedoms Park, Roosevelt Island",
  cost=0, dur=1, why="Ultima obra de Louis Kahn, terminada 38 anos despues de su muerte: granito, platanos y una 'sala' abierta al rio apuntando a Manhattan. Arquitectura moderna de primer orden, gratis y vacia.",
  jp=2, th=2, tags=["gratis","arquitectura","escondido"])

a(id="oculus", n="Oculus / WTC Transportation Hub", cat="arq", hood="Financial District", boro="Manhattan",
  sub="WTC Cortlandt (1), Fulton St", lat=40.7115, lng=-74.0110, addr="Church St & Fulton St",
  cost=0, dur=0.35, why="Calatrava. Se puede discutir si es bueno o si costo cuatro mil millones de dolares de mas, pero hay que verlo. Se cruza caminando camino al 9/11 Memorial.",
  main=True, jp=2, th=1, tags=["gratis","arquitectura"])

a(id="cafewha", n="Cafe Wha?", cat="musica", hood="Greenwich Village", boro="Manhattan",
  sub="W 4 St (A,C,E,B,D,F,M), Christopher St (1)", lat=40.7301, lng=-74.0004, addr="115 MacDougal St",
  cost=20, costN="Reserva GRATIS por Eventbrite (es solo reserva, no entrada). $20 de music charge por cabeza se suma a la cuenta + consumo.",
  dur=1.5, why="El sotano del Village donde debutaron Dylan, Hendrix, Springsteen y Bill Cosby. La house band de fin de semana es una maquina de soul y funk. Sigue siendo un club de barrio, no un museo.",
  main=True, book="Eventbrite - la reserva NO garantiza admision: TODOS presentes 23:30 o liberan la mesa", jp=2, th=2, tags=["clasico"])

a(id="strangerthings", n="Stranger Things: The First Shadow (play)", cat="teatro", hood="Midtown", boro="Manhattan",
  sub="Times Sq-42 St", lat=40.7583, lng=-73.9866, addr="Marquis Theatre, 210 W 46th St",
  cost=90, costN="Desde ~$76-100 segun funcion. Alternativas de play esa semana: Harry Potter and the Cursed Child (Lyric), Paranormal Activity (August Wilson), The Imaginary Invalid (Roundabout).",
  dur=2.5, why="EL play-espectaculo de Broadway: la precuela de Stranger Things con la maquinaria escenica que gano el Tony. Para quien viene de Mercer Labs, es el mismo musculo llevado al teatro.",
  main=True, book="compra firme esta semana - verificar horario de funcion (19:00/19:30/20:00)", jp=2, th=2, tags=["clasico"])

a(id="hamburgerica", n="Hamburger America", cat="comida", hood="SoHo / West Village", boro="Manhattan",
  sub="Houston St (1), W 4 St (A,C,E,B,D,F,M)", lat=40.7280, lng=-74.0034, addr="155 W Houston St",
  cost=20, costN="~$15-20 con papas y bebida. SIN reservas: counter por orden de llegada.",
  dur=0.75, why="El counter de George Motz, EL historiador de la hamburguesa americana: smashburger con cebolla al estilo Oklahoma y griddle a la vista. Es la hamburguesa clasica llevada a doctrina — MUST de JP.",
  main=True, book="no acepta reservas - ir y hacer la fila", jp=2, th=1, tags=["clasico"])

a(id="molounge", n="MO Lounge — Mandarin Oriental (piso 35)", cat="mirador", hood="Columbus Circle", boro="Manhattan",
  sub="59 St-Columbus Circle (1,A,B,C,D)", lat=40.7686, lng=-73.9829, addr="80 Columbus Circle, piso 35",
  cost=30, costN="Coctel ~$26-32. Sin cover: se paga lo que se toma. Reserva por SevenRooms desde su web.",
  dur=0.75, why="Ventanales de piso a techo sobre Central Park desde el piso 35, con la ciudad de noche abajo. Y esta EN EL MISMO EDIFICIO que Dizzy's: se baja en ascensor al jazz. Alternativa mas intima en ese mismo piso: The Bar (ex speakeasy The Office), mar-sab 17-1h, 45 asientos.",
  main=True, book="recomendada (SevenRooms)", jp=2, th=2, tags=["skyline"])

a(id="lincolncenter", n="Lincoln Center (campus y plaza)", cat="arq", hood="Upper West Side", boro="Manhattan",
  sub="66 St-Lincoln Center (1)", lat=40.7725, lng=-73.9835, addr="Columbus Ave entre 62 y 66",
  cost=0, costN="La plaza es GRATIS siempre. Temporadas: la Filarmonica (Dudamel) abre el 10/9, Met Opera y City Ballet mas tarde — durante el viaje las salas grandes estan oscuras.",
  dur=0.5, why="La plaza de Revson iluminada de noche, los chandeliers del Met Opera a traves del vidrio y el espejo de agua con el Henry Moore. De noche, vacia, es puro cine. A 10 cuadras de The Beacon.",
  main=True, jp=2, th=2, tags=["gratis","arquitectura"])

a(id="mercerlabs", n="Mercer Labs — Museum of Art and Technology", cat="museo", hood="Financial District", boro="Manhattan",
  sub="Fulton St (A,C,2,3,4,5), WTC Cortlandt (1)", lat=40.7106, lng=-74.0106, addr="21 Dey St",
  cost=57, costN="Hasta $57 segun franja horaria. Timed ticket por Fever (mercerlabs.com) — los slots se agotan.",
  dur=1.25, why="15 salas inmersivas de arte y tecnologia de Roy Nachum, frente al Oculus: proyecciones, sonido espacial y salas interactivas. La visita es a tu ritmo, 60-90 min.",
  main=True, book="timed ticket online (Fever) - reservar antes", jp=2, th=2, tags=["arquitectura","intenso"])

a(id="vessel", n="The Vessel", cat="arq", hood="Hudson Yards", boro="Manhattan",
  sub="34 St-Hudson Yards (7)", lat=40.7538, lng=-74.0022, addr="20 Hudson Yards",
  cost=10, costN="$10 (flex online $15). Reabierto con redes de seguridad; algunos tramos altos hacia el Hudson siguen cerrados.",
  dur=0.75, why="La escalera infinita de Heatherwick: 154 tramos entrelazados, 2.500 escalones. Subirla es la unica forma de entenderla, y esta al pie del arranque del High Line.",
  book="timed ticket online (hay en el dia, pero mejor asegurar)", jp=2, th=1, tags=["arquitectura"])

a(id="peterluger", n="Peter Luger Steak House", cat="comida", hood="Williamsburg", boro="Brooklyn",
  sub="Marcy Av (J,Z)", lat=40.7099, lng=-73.9622, addr="178 Broadway, Brooklyn",
  cost=110, costN="Porterhouse p/2 ~$140 + sides + propina: ~$110-130 por cabeza. SIN TARJETAS DE CREDITO: efectivo, debito US o cheque.",
  dur=1.75, why="El steakhouse de 1887 con la carne dry-aged en el sotano: sigue siendo EL porterhouse contra el que se mide todo lo demas. Sala alemana, ruidosa, sin vueltas.",
  main=True, book="Resy - reservar YA: los sabados se agotan con semanas", jp=2, th=2, tags=["clasico"])

a(id="twahotel", n="TWA Hotel (terminal de Saarinen)", cat="arq", hood="JFK Airport", boro="Queens",
  sub="A o E a Howard Beach/Jamaica + AirTrain", lat=40.6459, lng=-73.7767, addr="One Idlewild Dr, JFK",
  cost=9, costN="Gratis entrar; ~$8.50 el AirTrain de JFK", dur=3,
  why="La terminal de Eero Saarinen de 1962 restaurada entera: la Sunken Lounge, el tubo de conexion y un Lockheed Constellation de 1958 convertido en bar. No hace falta ser huesped ni pagar entrada.",
  jp=1, th=1, tags=["arquitectura","excursion"])

a(id="onderdonk", n="Vander Ende-Onderdonk House", cat="arq", hood="Ridgewood", boro="Queens",
  sub="Jefferson St (L)", lat=40.7085, lng=-73.9200, addr="1820 Flushing Ave, Ridgewood",
  cost=5, costN="a voluntad", dur=0.75,
  why="Casa de piedra holandesa de 1709, la construccion mas antigua de la ciudad, rodeada de galpones industriales. El contraste es todo el punto.",
  jp=1, th=2, tags=["escondido","historia"])

a(id="striversrow", n="Strivers' Row", cat="arq", hood="Harlem", boro="Manhattan",
  sub="135 St (B,C)", lat=40.8195, lng=-73.9440, addr="W 138th-139th St entre Adam Clayton Powell y Frederick Douglass",
  cost=0, dur=0.5, why="Dos cuadras de casas de 1891 disenadas por tres estudios distintos, con callejones traseros para caballos. Es la mejor arquitectura residencial de Manhattan y no hay nadie mirandola.",
  jp=2, th=2, tags=["gratis","arquitectura","escondido"])

# ────────────────────────────  PARQUES Y PASEOS  ────────────────────────────
a(id="centralpark", n="Central Park", cat="parque", hood="Central Park", boro="Manhattan",
  sub="multiples: 72 St (B,C), 59 St-Columbus Circle, 86 St", lat=40.7812, lng=-73.9665,
  addr="Central Park, New York", cost=0, dur=3,
  why="Bethesda Terrace, el Ramble, Bow Bridge, el Reservoir. La mitad norte (arriba de la 96) esta casi vacia y es la mejor. A dos cuadras del hotel The Beacon.",
  main=True, jp=2, th=1, tags=["gratis","cerca-beacon"])

a(id="highline", n="The High Line", cat="parque", hood="Chelsea / Meatpacking", boro="Manhattan",
  sub="14 St (A,C,E), 34 St-Hudson Yards (7)", lat=40.7480, lng=-74.0048,
  addr="High Line, Gansevoort St a W 34th St", cost=0, dur=1.5,
  why="Via ferroviaria elevada convertida en parque lineal de 2,3 km. Recorrer de sur a norte por la luz. Incluye 'The Light That Shines Through the Universe' de Tuan Andrew Nguyen, un Buda de arenisca de 9 metros.",
  main=True, jp=2, th=1, tags=["gratis","caminata"])

a(id="greenwood", n="Green-Wood Cemetery", cat="parque", hood="Greenwood Heights", boro="Brooklyn",
  sub="25 St (R)", lat=40.6580, lng=-73.9940, addr="500 25th St, Brooklyn",
  cost=0, costN="Entrada libre 7-19h. Trolley tours con costo: sab 29/8 y sab 5/9, 13-15h.",
  dur=2.5, why="190 hectareas de cementerio-jardin victoriano de 1838, con la colina mas alta de Brooklyn y vista de Manhattan. Hay guia gratuita en la app Bloomberg Connects. Es un parque enorme donde no hay nadie.",
  jp=2, th=2, tags=["gratis","escondido","caminata"])

a(id="brooklynbridgepark", n="Brooklyn Bridge Park", cat="parque", hood="DUMBO / Brooklyn Heights", boro="Brooklyn",
  sub="York St (F), High St (A,C)", lat=40.7003, lng=-73.9967, addr="334 Furman St, Brooklyn",
  cost=0, dur=1.5, why="Muelles reconvertidos con el skyline de Lower Manhattan de frente. Woody De Othello, 'Guardian Spirit', en el Pier 1 hasta marzo 2027.",
  main=True, jp=2, th=1, tags=["gratis","skyline"])

a(id="socrates", n="Socrates Sculpture Park", cat="parque", hood="Long Island City", boro="Queens",
  sub="Broadway (N,W)", lat=40.7684, lng=-73.9366, addr="32-01 Vernon Blvd, LIC",
  cost=0, dur=1, why="Ex basural convertido en parque de esculturas sobre el East River. 'Homecoming' de Chakaia Booker (esculturas de neumaticos) hasta abril 2027. A 5 minutos del Noguchi.",
  jp=2, th=2, tags=["gratis","arte","escondido"])

a(id="inwoodhill", n="Inwood Hill Park", cat="parque", hood="Inwood", boro="Manhattan",
  sub="Dyckman St o 207 St (A)", lat=40.8710, lng=-73.9260, addr="Inwood Hill Park, Manhattan",
  cost=0, dur=2, why="El unico bosque primario que queda en Manhattan, con cuevas de roca usadas por los Lenape y vista del Hudson y los Palisades. Cuesta creer que sea la misma isla.",
  jp=2, th=2, tags=["gratis","naturaleza","escondido"])

a(id="astoriapark", n="Astoria Park", cat="parque", hood="Astoria", boro="Queens",
  sub="Astoria Blvd (N,W) + caminata", lat=40.7790, lng=-73.9230, addr="19th St & 23rd Ave, Astoria",
  cost=0, dur=1, why="Debajo del Hell Gate Bridge, con el Triborough al lado y Manhattan enfrente. Al atardecer es de los mejores lugares de la ciudad y solo hay vecinos corriendo.",
  jp=2, th=2, tags=["gratis","vista","escondido"])

a(id="bryantpark", n="Bryant Park", cat="parque", hood="Midtown", boro="Manhattan",
  sub="5 Av-Bryant Pk (7,B,D,F,M)", lat=40.7536, lng=-73.9832, addr="Bryant Park, New York",
  cost=0, dur=0.75, why="El patio trasero de la Biblioteca Publica. Picnic Performances gratis toda la temporada: sab 29/8 (Accordion Festival), jue 3 y vie 4/9 (Brass Festival).",
  main=True, jp=1, th=1, tags=["gratis"])

a(id="washingtonsq", n="Washington Square Park", cat="parque", hood="Greenwich Village", boro="Manhattan",
  sub="W 4 St (A,B,C,D,E,F,M), 8 St-NYU (R,W)", lat=40.7308, lng=-73.9973,
  addr="Washington Square Park", cost=0, dur=0.75,
  why="El arco, el piano ambulante, los ajedrecistas y NYU alrededor. Es el mejor lugar de la ciudad para sentarse una hora a mirar gente.",
  main=True, jp=2, th=1, tags=["gratis"])

# ─────────────────────  EVENTOS FECHADOS  ─────────────────────
a(id="charlieparker29", n="Charlie Parker Jazz Festival - Harlem", cat="evento", hood="Harlem", boro="Manhattan",
  sub="125 St (2,3)", lat=40.8042, lng=-73.9440, addr="Marcus Garvey Park, Harlem",
  cost=0, costN="GRATIS, sin reserva", dur=4,
  why="SABADO 29 DE AGOSTO, 14-19h. Joshua Redman (headliner), Nat Adderley Jr., Catherine Russell, Nicole Glover. Gratis, al aire libre, con el mismo nivel artistico que se paga $60-80 en un club. Llevar manta y llegar 1-2 h antes del headliner.",
  jp=2, th=2, tags=["evento","jazz","gratis","fecha-fija"])

a(id="charlieparker30", n="Charlie Parker Jazz Festival - East Village", cat="evento", hood="East Village", boro="Manhattan",
  sub="1 Av (L), Astor Pl (6)", lat=40.7265, lng=-73.9815, addr="Tompkins Square Park",
  cost=0, costN="GRATIS, sin reserva", dur=4,
  why="DOMINGO 30 DE AGOSTO, 15-19h. Ravi Coltrane (headliner), Billy Hart Quartet, Kassa Overall, Vanisha Gould. Segundo dia del festival, en el East Village.",
  jp=2, th=2, tags=["evento","jazz","gratis","fecha-fija"])

a(id="summerstage", n="SummerStage: Christian McBride (gratis)", cat="evento", hood="Central Park", boro="Manhattan",
  sub="72 St (B,C)", lat=40.7712, lng=-73.9695, addr="Rumsey Playfield, Central Park",
  cost=0, costN="GRATIS", dur=3,
  why="MIERCOLES 2 DE SEPTIEMBRE. Christian McBride + SAMARA JOY (Verve 70 aniversario) + Mei Semones & Friends tocando Getz/Gilberto. Puertas 18:00, show 19:00-22:00. Gratis, sin ticket, por orden de llegada: con ese cartel hay que llegar bastante antes de las 18:00.",
  jp=2, th=2, tags=["evento","jazz","gratis","fecha-fija"])

a(id="usopen", n="US Open (primeras rondas)", cat="evento", hood="Flushing Meadows", boro="Queens",
  sub="Mets-Willets Point (7)", lat=40.7500, lng=-73.8450, addr="USTA Billie Jean King NTC, Flushing",
  cost=80, costN="Grounds pass desde ~$80 segun sesion", dur=7,
  why="Cuadro principal del 30 de agosto al 13 de septiembre. Las primeras rondas (30 ago - 2 sep) son cuando mas partidos simultaneos hay y el grounds pass rinde mas: se ve a metros en las canchas exteriores. Se come un dia entero.",
  book="Ticketmaster", jp=0, th=0, tags=["evento","deporte","fecha-fija"])

a(id="carnival", n="NY Caribbean Carnival Week (Panorama)", cat="evento", hood="Prospect Heights", boro="Brooklyn",
  sub="Eastern Pkwy-Brooklyn Museum (2,3)", lat=40.6712, lng=-73.9636, addr="Brooklyn Museum, 200 Eastern Pkwy",
  cost=30, costN="precios no publicados aun - VERIFICAR en wiadcacarnival.org",
  dur=4, why="Del 3 al 7 de septiembre en el Brooklyn Museum: Blocko Mania (jue 3), Soca Fest (vie 4), Junior Carnival y Panorama (sab 5 / dom 6). El Panorama es la competencia de steel pan mas grande de Norteamerica. Fechas de fuente secundaria: VERIFICAR.",
  jp=1, th=1, tags=["evento","musica","fecha-fija","verificar"])

a(id="greenwoodtrolley", n="Green-Wood Discover Trolley Tour", cat="evento", hood="Greenwood Heights", boro="Brooklyn",
  sub="25 St (R)", lat=40.6580, lng=-73.9940, addr="500 25th St, Brooklyn",
  cost=25, costN="precio no publicado - consultar green-wood.com", dur=2,
  why="SABADO 29 DE AGOSTO y SABADO 5 DE SEPTIEMBRE, 13-15h. Recorrido en trolley por las 190 hectareas con guia. Es la forma de ver el cementerio entero sin caminar seis horas.",
  book="reservar", jp=1, th=1, tags=["evento","fecha-fija"])

# ────────────────────────────  TEATRO  ────────────────────────────
a(id="moulinrouge", n="Moulin Rouge! (ULTIMAS FUNCIONES)", cat="teatro", hood="Theater District", boro="Manhattan",
  sub="42 St-Port Authority (A,C,E)", lat=40.7593, lng=-73.9877, addr="Al Hirschfeld Theatre, 302 W 45th St",
  cost=90, costN="Loteria LuckySeat $49. Funciones de cierre suelen encarecerse.", dur=3,
  why="CIERRA EL 30 DE AGOSTO DE 2026 (ya postergo el cierre una vez, de julio a agosto: puede volver a extender). Las dos ultimas funciones caen en el fin de semana de llegada, con demanda y precios en pico. Aaron Tveit protagoniza del 18 al 29 de agosto.",
  book="urgente si lo quieren", jp=1, th=1, tags=["broadway","fecha-fija"])

a(id="maybehappy", n="Maybe Happy Ending", cat="teatro", hood="Theater District", boro="Manhattan",
  sub="49 St (N,R,W)", lat=40.7605, lng=-73.9840, addr="Belasco Theatre, 111 W 44th St",
  cost=59, costN="Promedio real pagado $59. LOTERIA $20.64 (Telecharge, cierra 15h del dia previo). Rush $49.",
  dur=2.5, why="Musical sobre dos robots obsoletos en Seul. Es la mejor relacion calidad/precio de la cartelera actual y la loteria de $20 es de las mas accesibles.",
  jp=2, th=2, tags=["broadway"])

a(id="opmincemeat", n="Operation Mincemeat", cat="teatro", hood="Theater District", boro="Manhattan",
  sub="49 St (N,R,W)", lat=40.7596, lng=-73.9846, addr="John Golden Theatre, 252 W 45th St",
  cost=63, costN="Promedio real $63. Rush $49 en boleteria a las 10h. TKTS ~40% off.", dur=2.5,
  why="Comedia musical britanica sobre una operacion de contrainteligencia real de la Segunda Guerra. Cinco actores haciendo ochenta personajes. Muy bien recibida y mas barata que los grandes musicales.",
  jp=2, th=2, tags=["broadway"])

a(id="hamilton", n="Hamilton", cat="teatro", hood="Theater District", boro="Manhattan",
  sub="50 St (1), 49 St (N,R,W)", lat=40.7593, lng=-73.9866, addr="Richard Rodgers Theatre, 226 W 46th St",
  cost=112, costN="Promedio real pagado $112. LOTERIA $10 (HamiltonMusical.com, cierra jueves 12h de la semana previa).",
  dur=3, why="Sigue siendo el show mas dificil de conseguir barato, pero la loteria de $10 es gratis de intentar y asigna butacas de primera fila. Anotarse todos los dias desde ya.",
  main=True, jp=1, th=0, tags=["broadway"])

a(id="littleshop", n="Little Shop of Horrors (Off-Broadway)", cat="teatro", hood="Theater District", boro="Manhattan",
  sub="50 St (C,E)", lat=40.7615, lng=-73.9865, addr="Westside Theatre, 407 W 43rd St",
  cost=40, costN="Loteria digital $40 (Telecharge, sorteos 10h y 15h)", dur=2,
  why="Sala chica, produccion excelente, y a un cuarto del precio de un musical grande. Off-Broadway hecho bien.",
  jp=2, th=2, tags=["off-broadway"])

a(id="tkts", n="TKTS Lincoln Center", cat="teatro", hood="Lincoln Square", boro="Manhattan",
  sub="66 St-Lincoln Center (1)", lat=40.7736, lng=-73.9830, addr="61 W 62nd St",
  cost=0, costN="Hasta 50% off (tipico 40%) + $8 de fee por ticket. Max 6 por persona.",
  closed="lunes y domingos", dur=0.75,
  why="Mismo inventario que el booth de Times Square y casi siempre sin cola. Mar-sab 11-18h. Usar la app de TKTS para ver el inventario en tiempo real ANTES de ir. A 10 cuadras del hotel The Beacon.",
  jp=2, th=2, tags=["broadway","truco"])

# ─────────────────────  LOGISTICA / TRANSPORTE  ─────────────────────
a(id="ink48", n="Hotel Ink48 (29-31 ago)", cat="transporte", hood="Hell's Kitchen", boro="Manhattan",
  sub="50 St (C,E) a ~12 min caminando", lat=40.7638, lng=-73.9971, addr="653 11th Ave",
  cost=0, dur=0, why="Base 29-31 de agosto. Esta lejos del subte (12 min al este hasta la 8va Av). Cerca: Intrepid, High Line norte, Hudson Yards, Birdland.",
  jp=2, th=2, tags=["hotel"])

a(id="jgstay", n="JGSTAY SoHo (JP: 31 ago-2 sep)", cat="transporte", hood="SoHo", boro="Manhattan",
  sub="Canal St: la del 6/J/Z esta EN la esquina (Lafayette y Canal); N/Q/R/W a 2 cuadras", lat=40.7185, lng=-73.9996, addr="120 Lafayette St, NY 10013",
  cost=0, dur=0, why="Base de JP lunes y martes a la noche: se acabaron las dos vueltas nocturnas a New Jersey. Recepcion 24 h, CONSIGNA de equipaje y desayuno incluido 7-9 AM. Canal St al lado = 6 directo al MET y Grand Central, A/C al AMNH, y el Village a 15-20 min a pie.",
  jp=2, th=0, tags=["hotel"])

a(id="beacon", n="Hotel The Beacon (3-6 sep)", cat="transporte", hood="Upper West Side", boro="Manhattan",
  sub="72 St (1,2,3) a 3 cuadras", lat=40.7810, lng=-73.9800, addr="2130 Broadway",
  cost=0, dur=0, why="Base 3-6 de septiembre. Ubicacion excelente: la 1/2/3 llega a Penn Station en 10 min. Cerca: Central Park, AMNH, TKTS Lincoln Center, Dizzy's.",
  jp=2, th=2, tags=["hotel"])

a(id="residenceinn", n="Residence Inn Branchburg (Thais 31/8-3/9 · JP solo la noche del 2)", cat="transporte",
  hood="Branchburg", boro="New Jersey", sub="Estacion Raritan (NJ Transit RVL) a 6,4 km",
  lat=40.5760, lng=-74.6790, addr="3241 US Highway 22 East, Branchburg NJ",
  cost=0, dur=0, why="Base en NJ. NO tiene shuttle (confirmado por Marriott). Estacionamiento propio gratis. Para llegar al tren hay que tomar Uber (~$14-20 por tramo a Raritan).",
  jp=2, th=2, tags=["hotel"])

out = {"places": P, "generated": "2026-08-16", "count": len(P)}
os.makedirs(os.path.join(_R, "data"), exist_ok=True)
with open(os.path.join(_R, "data/places.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

ids = [p["id"] for p in P]
assert len(ids) == len(set(ids)), "IDs duplicados: " + str([i for i in ids if ids.count(i) > 1])
cats = {}
for p in P:
    cats[p["cat"]] = cats.get(p["cat"], 0) + 1
print(f"OK - {len(P)} lugares")
for k, v in sorted(cats.items(), key=lambda x: -x[1]):
    print(f"  {k:12s} {v}")

# ══════════════════════════════════════════════════════════════════════════
#  SUBCATEGORÍA (tipo de lugar) — segundo nivel, más específico que "cat".
#  Se aplica por id para no tocar las 130 entradas de arriba.
# ══════════════════════════════════════════════════════════════════════════
# ── Lugares que estaban en la lista "NY 2026" de Google Maps y no en el catálogo ──
from places_gmaps import G as _G
_gc = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "gmaps_coords.json")))
_COORD, _APROX = _gc["coords"], set(_gc["aprox"])
_GSUB = {}
for (_pid, _n, _cat, _hood, _boro, _sub, _addr, _cost, _dur, _why, _main, _typ) in _G:
    _c = _COORD[_pid]
    a(id=_pid, n=_n, cat=_cat, hood=_hood, boro=_boro, sub=_sub or "-", lat=_c[0], lng=_c[1],
      addr=_addr, cost=_cost, dur=_dur, why=_why, main=_main, jp=1, th=1,
      src="lista", aprox=_pid in _APROX,
      tags=["lista-google"] + (["gratis"] if _cost == 0 else []))
    _GSUB.setdefault(_typ, []).append(_pid)

SUB = {
 # ── MIRADOR ──
 "Observatorio pago":   ["summit", "topofrock", "edge", "esb", "owo"],
 "Rooftop bar":         ["westlight", "thecrown", "molounge"],
 "Mirador gratis":      ["bhpromenade", "gantry", "domino", "forttryon", "sunsetparkview", "valentino"],
 "Ferry y teleférico":  ["siferry", "tram"],
 # ── MUSEO ──
 "Museo de arte":       ["met", "cloisters", "moma", "whitney", "guggenheim", "frick", "bkmuseum",
                         "momaps1", "studiomuseum", "noguchi", "diabeacon"],
 "Museo de historia":   ["mcny", "tenement", "911museum", "cityreliquary", "transitmuseum"],
 "Museo de ciencia":    ["amnh"],
 "Museo temático":      ["momi", "intrepid", "mercerlabs"],
 "Biblioteca histórica":["morgan"],
 # ── BARRIO ──
 "Barrio étnico":       ["jacksonheights", "astoria", "greenpoint", "sunsetpark", "arthurave",
                         "ridgewood", "bayridge", "flushing", "chinatown"],
 "Barrio histórico":    ["harlem", "les", "westvillage", "inwood"],
 "Waterfront":          ["redhook", "dumbo"],
 "Isla":                ["govisland", "rooseveltisland"],
 # ── COMIDA ──
 "Mercado y food hall": ["essexmarket", "chelseamarket", "arthurmarket", "newworldmall", "dekalb", "timeoutmarket"],
 "Deli y pastrami":     ["katzs", "splunch", "russdaughters", "frankels"],
 "Hamburguesería":      ["hamburgerica"],
 "Pizzería":            ["lbspumoni", "totonnos", "lucali", "manos"],
 "Restaurante étnico":  ["lhasa", "nepalibhanchha", "jalapenoking", "elbronco", "henan", "uyghur",
                         "pierozek", "karczma", "malecon", "tanoreen", "kyclades"],
 "Comida al paso":      ["casadellamozz", "cosenza", "lostacos"],
 "Panadería y bagels":  ["rudys", "bosbagels"],
 # ── MÚSICA ──
 "Club de jazz":        ["vanguard", "smalls", "mezzrow", "birdland", "dizzys", "bluenote", "ornithology", "billsplace"],
 "Play de Broadway":    ["strangerthings"],
 "Bar con música":      ["lunatico", "barbayeux", "cafewha"],
 "Música del mundo":    ["barbes"],
 "Venue alternativo":   ["nublu"],
 # ── ARQUITECTURA ──
 "Interior monumental": ["grandcentral", "nypl", "chrysler", "fordfoundation"],
 "Arquitectura moderna":["littleisland", "fdrpark", "oculus", "twahotel", "vessel", "lincolncenter"],
 "Steakhouse clásico":  ["peterluger"],
 "Templo":              ["eldridge"],
 "Casa y calle histórica": ["onderdonk", "striversrow"],
 # ── PARQUE ──
 "Parque urbano":       ["centralpark", "bryantpark", "washingtonsq", "brooklynbridgepark", "astoriapark"],
 "Paseo elevado":       ["highline"],
 "Parque de esculturas":["socrates"],
 "Naturaleza":          ["inwoodhill", "wavehill"],
 "Cementerio-jardín":   ["greenwood"],
 # ── EVENTO ──
 "Festival gratis":     ["charlieparker29", "charlieparker30", "summerstage"],
 "Festival pago":       ["carnival"],
 "Deporte":             ["usopen"],
 "Tour guiado":         ["greenwoodtrolley"],
 # ── TEATRO ──
 "Musical de Broadway": ["moulinrouge", "maybehappy", "opmincemeat", "hamilton"],
 "Off-Broadway":        ["littleshop"],
 "Tickets con descuento": ["tkts"],
 # ── LOGÍSTICA ──
 "Hotel":               ["ink48", "jgstay", "beacon", "residenceinn"],
}

# subcategorías de los lugares de la lista de Google: se suman a las existentes o crean una nueva
for _t, _ids in _GSUB.items():
    SUB.setdefault(_t, []).extend(_ids)

# ── origen de cada lugar: propuesta nuestra / lista de Google / las dos ──
from matches_gmaps import EN_LISTA as _EN_LISTA
_ids = {p["id"] for p in P}
_hu = [k for k in _EN_LISTA if k not in _ids]
assert not _hu, "ids inexistentes en matches_gmaps: " + str(_hu)
for _p in P:
    if _p["id"] in _EN_LISTA:
        _p["src"] = "ambas"                 # lo propusimos Y estaba guardado
        _p["gname"] = _EN_LISTA[_p["id"]]   # cómo figura en la lista de Google

_byid = {p["id"]: p for p in P}
_seen = set()
for sub, ids in SUB.items():
    for pid in ids:
        assert pid in _byid, "id inexistente en SUB: " + pid
        assert pid not in _seen, "id duplicado en SUB: " + pid
        _seen.add(pid)
        _byid[pid]["typ"] = sub
falta = [p["id"] for p in P if "typ" not in p]
assert not falta, "lugares sin subcategoría: " + str(falta)

# ── overrides de interés provenientes del Excel editado por el usuario ──
# Se aplican DESPUÉS de los defaults, así el catálogo sigue siendo reproducible
# y los cambios de Juan y Thais sobreviven a cualquier regeneración.
# ══════════════════════════════════════════════════════════════════════════
#  HORARIOS DE APERTURA de los lugares con horario fijo.
#  Clave: 0=lunes … 6=domingo. Valor: [apertura, cierre] en "HH:MM", o None si cierra.
#  Solo se cargan los lugares donde llegar a la hora equivocada arruina la visita.
#  Fuente: sitios oficiales, consultados el 16-ago-2026.
# ══════════════════════════════════════════════════════════════════════════
def _h(**kw):
    """lu,ma,mi,ju,vi,sa,do -> lista indexada 0..6"""
    orden = ["lu", "ma", "mi", "ju", "vi", "sa", "do"]
    return [kw.get(d) for d in orden]

HRS = {
 # ── museos ──
 "met":          _h(lu=["10:00","17:00"], ma=["10:00","17:00"], mi=None, ju=["10:00","17:00"],
                    vi=["10:00","21:00"], sa=["10:00","21:00"], do=["10:00","17:00"]),
 "cloisters":    _h(lu=["10:00","17:00"], ma=["10:00","17:00"], mi=None, ju=["10:00","17:00"],
                    vi=["10:00","17:00"], sa=["10:00","17:00"], do=["10:00","17:00"]),
 "moma":         _h(lu=["10:30","17:30"], ma=["10:30","17:30"], mi=["10:30","17:30"], ju=["10:30","17:30"],
                    vi=["10:30","20:30"], sa=["10:30","17:30"], do=["10:30","17:30"]),
 "whitney":      _h(lu=["10:30","18:00"], ma=None, mi=["10:30","18:00"], ju=["10:30","18:00"],
                    vi=["10:30","22:00"], sa=["10:30","18:00"], do=["10:30","18:00"]),
 "guggenheim":   _h(lu=["10:30","17:30"], ma=["10:30","17:30"], mi=["10:30","17:30"], ju=["10:30","17:30"],
                    vi=["10:30","17:30"], sa=["10:30","17:30"], do=["10:30","17:30"]),
 "amnh":         _h(lu=["10:00","17:30"], ma=["10:00","17:30"], mi=["10:00","17:30"], ju=["10:00","17:30"],
                    vi=["10:00","17:30"], sa=["10:00","17:30"], do=["10:00","17:30"]),
 "frick":        _h(lu=["10:30","17:30"], ma=None, mi=["10:30","17:30"], ju=["10:30","17:30"],
                    vi=["10:30","17:30"], sa=["10:30","17:30"], do=["10:30","17:30"]),
 "morgan":       _h(lu=None, ma=["10:30","17:00"], mi=["10:30","17:00"], ju=["10:30","17:00"],
                    vi=["10:30","20:00"], sa=["10:30","17:00"], do=["10:30","17:00"]),
 "momaps1":      _h(lu=["12:00","18:00"], ma=None, mi=None, ju=["12:00","18:00"],
                    vi=["12:00","18:00"], sa=["10:00","18:00"], do=["12:00","18:00"]),
 "momi":         _h(lu=None, ma=None, mi=None, ju=["14:00","18:00"],
                    vi=["14:00","20:00"], sa=["11:00","18:00"], do=["11:00","18:00"]),
 "studiomuseum": _h(lu=None, ma=None, mi=["11:00","18:00"], ju=["11:00","18:00"],
                    vi=["11:00","21:00"], sa=["11:00","18:00"], do=["11:00","18:00"]),
 "bkmuseum":     _h(lu=None, ma=None, mi=["11:00","18:00"], ju=["11:00","18:00"],
                    vi=["11:00","18:00"], sa=["11:00","18:00"], do=["11:00","18:00"]),
 "noguchi":      _h(lu=None, ma=None, mi=["11:00","18:00"], ju=["11:00","18:00"],
                    vi=["11:00","18:00"], sa=["11:00","18:00"], do=["11:00","18:00"]),
 "transitmuseum":_h(lu=None, ma=None, mi=["10:00","16:00"], ju=["10:00","16:00"],
                    vi=["10:00","16:00"], sa=["10:00","16:00"], do=["10:00","16:00"]),
 "mcny":         _h(lu=["10:00","17:00"], ma=["10:00","17:00"], mi=["10:00","21:00"], ju=["10:00","17:00"],
                    vi=["10:00","17:00"], sa=["10:00","18:00"], do=["10:00","18:00"]),
 "911museum":    _h(lu=["09:00","19:00"], ma=None, mi=["09:00","19:00"], ju=["09:00","19:00"],
                    vi=["09:00","19:00"], sa=["09:00","19:00"], do=["09:00","19:00"]),
 "mercerlabs":   _h(lu=["10:00","20:00"], ma=["10:00","20:00"], mi=["10:00","20:00"], ju=["10:00","22:00"],
                    vi=["10:00","22:00"], sa=["10:00","22:00"], do=["10:00","22:00"]),
 "eldridge":     _h(lu=["10:00","17:00"], ma=["10:00","17:00"], mi=["10:00","17:00"], ju=["10:00","17:00"],
                    vi=["10:00","17:00"], sa=None, do=["10:00","17:00"]),
 "cityreliquary":_h(sa=["12:00","18:00"], do=["12:00","18:00"]),
 "intrepid":     _h(lu=["10:00","17:00"], ma=["10:00","17:00"], mi=["10:00","17:00"], ju=["10:00","17:00"],
                    vi=["10:00","17:00"], sa=["10:00","18:00"], do=["10:00","18:00"]),
 "tenement":     _h(lu=["10:00","18:00"], ma=["10:00","17:00"], mi=["10:00","17:00"], ju=["10:00","17:00"],
                    vi=["10:00","18:00"], sa=["10:00","18:00"], do=["10:00","18:00"]),
 # ── arquitectura e interiores ──
 "chrysler":     _h(lu=["08:00","18:00"], ma=["08:00","18:00"], mi=["08:00","18:00"],
                    ju=["08:00","18:00"], vi=["08:00","18:00"]),
 "fordfoundation":_h(lu=["11:00","18:00"], ma=["11:00","18:00"], mi=["11:00","18:00"],
                    ju=["11:00","18:00"], vi=["11:00","18:00"]),
 "nypl":         _h(lu=["10:00","18:00"], ma=["10:00","20:00"], mi=["10:00","20:00"], ju=["10:00","18:00"],
                    vi=["10:00","18:00"], sa=["10:00","18:00"], do=["13:00","17:00"]),
 "grandcentral": _h(lu=["05:15","02:00"], ma=["05:15","02:00"], mi=["05:15","02:00"], ju=["05:15","02:00"],
                    vi=["05:15","02:00"], sa=["05:15","02:00"], do=["05:15","02:00"]),
 # ── mercados y comida con horario ──
 "essexmarket":  _h(lu=["08:00","20:00"], ma=["08:00","20:00"], mi=["08:00","20:00"], ju=["08:00","21:00"],
                    vi=["08:00","21:00"], sa=["08:00","21:00"], do=["10:00","18:00"]),
 "russdaughters":_h(lu=["08:00","16:00"], ma=["08:00","16:00"], mi=["08:00","16:00"], ju=["08:00","16:00"],
                    vi=["08:00","16:00"], sa=["08:00","17:00"], do=["08:00","17:00"]),
 "hamburgerica": _h(lu=["11:00","22:00"], ma=["11:00","22:00"], mi=["11:00","22:00"], ju=["11:00","22:00"],
                    vi=["11:00","23:00"], sa=["11:00","23:00"], do=["11:00","22:00"]),
 # ── miradores y teatro ──
 "molounge":     _h(lu=["07:00","23:00"], ma=["07:00","23:00"], mi=["07:00","23:00"], ju=["07:00","24:00"],
                    vi=["07:00","24:00"], sa=["07:00","24:00"], do=["07:00","23:00"]),
 "vessel":       _h(lu=["10:00","21:00"], ma=["10:00","21:00"], mi=["10:00","21:00"], ju=["10:00","21:00"],
                    vi=["10:00","21:00"], sa=["10:00","21:00"], do=["10:00","21:00"]),
 "owo":          _h(lu=["09:00","21:00"], ma=["09:00","21:00"], mi=["09:00","21:00"], ju=["09:00","21:00"],
                    vi=["09:00","21:00"], sa=["09:00","21:00"], do=["09:00","21:00"]),
 "topofrock":    _h(lu=["08:00","24:00"], ma=["08:00","24:00"], mi=["08:00","24:00"], ju=["08:00","24:00"],
                    vi=["08:00","24:00"], sa=["08:00","24:00"], do=["08:00","24:00"]),
 "summit":       _h(lu=["09:00","24:00"], ma=["09:00","24:00"], mi=["09:00","24:00"], ju=["09:00","24:00"],
                    vi=["09:00","24:00"], sa=["09:00","24:00"], do=["09:00","24:00"]),
 "tkts":         _h(ma=["11:00","18:00"], mi=["11:00","18:00"], ju=["11:00","18:00"],
                    vi=["11:00","18:00"], sa=["11:00","18:00"]),
}
for _pid, _h_ in HRS.items():
    assert _pid in _byid, "id inexistente en HRS: " + _pid
    _byid[_pid]["hrs"] = _h_

_ovf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "overrides.json")
_n_ov = 0
if os.path.exists(_ovf):
    with open(_ovf, encoding="utf-8") as f:
        _ov = json.load(f)
    for pid, v in _ov.items():
        if pid in _byid:
            if _byid[pid]["jp"] != v["jp"] or _byid[pid]["th"] != v["th"]:
                _n_ov += 1
            _byid[pid]["jp"], _byid[pid]["th"] = v["jp"], v["th"]
            if "must" in v:
                _m = v["must"]
                _byid[pid]["must"] = 1 if _m is True or _m == 1 else -1 if _m == -1 else 0
    print(f"   overrides aplicados: {_n_ov} lugares con interes distinto al default")

out = {"places": P, "generated": "2026-08-16", "count": len(P),
       "subs": {c: sorted({p["typ"] for p in P if p["cat"] == c})
                for c in dict.fromkeys(p["cat"] for p in P)}}
with open(os.path.join(_R, "data/places.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print(f"OK - {len(SUB)} subcategorías cubriendo los {len(P)} lugares")
_c = {}
for _p in P: _c[_p["src"]] = _c.get(_p["src"], 0) + 1
print(f"   origen: {_c.get('ambas',0)} en ambas · {_c.get('lista',0)} solo lista de Google · {_c.get('propuesta',0)} solo propuesta nuestra")
print(f"   imprescindibles: {sum(1 for _p in P if _p.get('must') == 1)}"
      f" · no imprescindibles: {sum(1 for _p in P if _p.get('must') == -1)}"
      f" · sin marcar: {sum(1 for _p in P if not _p.get('must'))}")
