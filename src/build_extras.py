#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Transporte, análisis de pases y checklist de reservas. Genera data/extras.json"""
import os
_R = os.path.dirname(os.path.abspath(__file__))   # todo se resuelve relativo a este archivo, no a donde se corra
import json

# ══════════════════════════════ TRANSPORTE ══════════════════════════════
transport = {
 "ewr_llegada": {
  "titulo": "EWR → Ink48 · sábado 29 de agosto, 6:00 AM",
  "reco": "AirTrain + NJ Transit",
  "opciones": [
   {"m": "AirTrain + NJ Transit ✅", "costo": "$17,25", "tiempo": "~55-70 min desde terminal",
    "det": "Precio ÚNICO: ya incluye el fee de AirTrain de $8,75, no se compra aparte. Trenes sábado desde EWR: 6:00, 6:07, 6:43, 7:04, 7:15, 7:25, 7:39. Viaje 26-31 min. Comprar en la app MyTix o en máquina — a bordo cobran $5 de recargo.",
    "total": "~$30-35 p/p con el taxi de Penn Station al hotel"},
   {"m": "Taxi oficial de EWR", "costo": "~$78-90", "tiempo": "45-60 min",
    "det": "Tarifa fija por zona: Ink48 está en la calle 48 = Zona 2 = $65 fijo, + $2 de airport fee + $6,75-15,75 de peajes + $1 por valija. El recargo de hora pico ($10) rige sáb-dom 12-21h, así que a las 6-7 AM NO aplica."},
   {"m": "Uber / Lyft", "costo": "$70-110 (estimado)", "tiempo": "45-60 min",
    "det": "A las 7 AM de un sábado el tráfico es liviano. Ink48 está dentro de la zona de congestion pricing (sur de la calle 60): hay recargo adicional."},
   {"m": "Newark Airport Express ❌", "costo": "$18-19 (NO CONFIRMADO)", "tiempo": "60-80 min",
    "det": "No aporta nada frente al tren: más caro, más lento, sujeto al tráfico del Lincoln Tunnel, y deja en Port Authority a 15 min caminando del hotel. Las fuentes se contradicen sobre el precio."}],
  "secuencia": "Aterrizan 6:00 → migraciones y equipaje 45-75 min → AirTrain ~10-12 min → tren de 7:25 o 7:39 → Penn Station 7:51/8:07 → hotel 8:15-8:30. Total ≈ 2h15-2h30 desde que tocan pista.",
  "alerta": "El AirTrain de Newark está en obra de reemplazo hasta 2030. El servicio por bus solo aplica días de semana de 5:00 a 15:00 — sus dos vuelos caen en fin de semana, así que están cubiertos. Igual reverifiquen 2-3 días antes en njtransit.com."},

 "ewr_salida": {
  "titulo": "The Beacon → EWR · domingo 6 de septiembre, vuelo 23:40",
  "reco": "Subte 1/2/3 + NJ Transit — $20,25 total",
  "opciones": [
   {"m": "Subte + NJ Transit ✅", "costo": "$20,25", "tiempo": "~55 min + AirTrain",
    "det": "1/2/3 desde 72 St (a 3 cuadras del hotel) hasta 34 St-Penn Station, directo, ~10 min, $3. Después NJ Transit a EWR, $17,25. Trenes domingo: 19:51→20:12, 20:03→20:26, 20:07→20:31, 20:14→20:38, 20:55→21:16.",
    "total": "Salir del hotel 19:40 → tren de 20:14 (llega 20:38) → AirTrain → en terminal ~20:55, con 2h45 de margen. Colchón: el de 20:55 deja en terminal ~21:35, 2h05 antes."},
   {"m": "Taxi amarillo desde Manhattan", "costo": "$95-120", "tiempo": "50-75 min",
    "det": "OJO: saliendo de Manhattan NO rige la tarifa fija por zonas (esa es solo para taxis que salen de EWR). Se cobra medidor + recargo Newark de $20 + peajes + congestion charge."},
   {"m": "Uber / Lyft", "costo": "$70-110 + riesgo alto de surge", "tiempo": "50-75 min",
    "det": "El domingo 6/9 es el domingo del fin de semana largo de Labor Day: el día de mayor tráfico de retorno del año. Riesgo real de surge y de demora."}],
  "alerta": "El domingo 6 es el domingo del fin de semana largo de Labor Day: la noche de mayor tráfico de retorno del año. Eso castiga fuerte a todo lo que vaya en auto y no afecta al tren, así que esta noche puntual el tren no es solo más barato sino más confiable. Pero EWR va a estar cargado: por eso salimos con 2h45 y no con las 2h de siempre."},

 "nj_nyc": {
  "titulo": "Bridgewater/Branchburg NJ ↔ Manhattan · 31 ago al 3 sep",
  "reco": "Estación RARITAN + pasajes sueltos + Uber al tren",
  "hotel": "Residence Inn Bridgewater Branchburg, 3241 US-22 East. NO TIENE SHUTTLE (confirmado por Marriott). Estacionamiento propio gratis.",
  "estaciones": [
   {"e": "Raritan ✅", "dist": "6,4 km / 4,0 mi", "park": "$4/día", "serv": "Completo. Es cabecera: siempre hay asiento."},
   {"e": "Somerville", "dist": "8,1 km / 5,0 mi", "park": "$5/día (garage Robeson St)", "serv": "Completo. Resta 3 min de viaje pero está 1 milla más lejos."},
   {"e": "North Branch ❌", "dist": "1,7 km / 1,0 mi", "park": "GRATIS, 40 lugares", "serv": "SOLO horas pico. Es la más cercana pero no sirve."},
   {"e": "Bridgewater", "dist": "13,2 km / 8,2 mi", "park": "$4/día", "serv": "Completo, pero es la más lejana del hotel."}],
  "tarifas": [
   {"t": "Pasaje suelto Raritan → NY Penn", "p": "$18,50", "nota": "PLAN CONFIRMADO: JP hace 4 tramos = $74 (ida el 1, vuelta el 2, ida el 3, más la vuelta del 31). Thais hace 2 = $37. Total $111 ← LA OPCIÓN MÁS BARATA"},
   {"t": "Round-trip", "p": "$37,00", "nota": "Exactamente 2 × $18,50. NO hay descuento."},
   {"t": "10-trip", "p": "$185,00", "nota": "Exactamente 10 × $18,50. Más caro y sobran 2 viajes."},
   {"t": "Pase semanal", "p": "$164,00", "nota": "Más caro que 8 pasajes sueltos."},
   {"t": "FlexPass (20 viajes one-way)", "p": "$314,50", "nota": "El ÚNICO producto con descuento real: 15% off, válido 30 días. Pero son 20 viajes y ustedes hacen 8 — no sirve para este viaje."},
   {"t": "Bus 114/117 a Port Authority", "p": "$15,80", "nota": "$22 más barato en total, pero 45 min más por tramo. No compensa."}],
  "horarios": "MAÑANA (Raritan → NY Penn, todos con transbordo en Newark): 4:31→5:59, 6:23→7:37, 6:42→8:05, 6:55→8:20, 7:13→8:31. NOCHE (NY Penn → Raritan), verificado para el miércoles 2/9/2026: 19:42 con transbordo → 21:12 · 20:48 DIRECTO → 22:04 · 21:48 DIRECTO → 23:10 · 22:48 DIRECTO → 00:04 · 00:05 con transbordo → 01:31 · 01:00 con transbordo → 02:35 (último). Viaje 75-90 min.",
  "oneseat": "8 trenes DIRECTOS por sentido, solo días hábiles. HACIA EL ESTE (Raritan → NY Penn), llegadas a Penn: 10:06, 11:11, 12:07, 13:08, 14:10, 20:14, 21:16, 22:10. HACIA EL OESTE (NY Penn → Raritan), salidas: 10:40, 11:40, 12:45, 13:40, 14:40 y 20:48, 21:48, 22:48. CORRECCIÓN: yo había dicho que los directos eran solo de valle — es falso, los TRES trenes de la noche son directos y son justo los que ustedes van a usar. El resto del día (pico y madrugada) todos los trenes del RVL nacen o terminan en Newark Penn y hay que transbordar. El motivo: el RVL no está electrificado al oeste de Newark. Los fines de semana NO hay directo. Verificado en el PDF oficial de NJ Transit y en el feed GTFS para el 2 de septiembre de 2026.",
  "aviso_variantes": "Esta comparativa asume el escenario máximo (ida y vuelta los 4 días). EL PLAN CONFIRMADO es más chico: JP hace 4 tramos de tren y 4 Ubers (~$146), Thais 2 y 2 (~$73). La tabla sirve para elegir ENTRE opciones, no para el total.",
  "comparativa": [
   {"esc": "① Uber ↔ Raritan + tren ✅ (PLAN REAL)", "calc": "$111 tren (6 tramos entre los dos) + $108 Uber (6 tramos)", "tot": "~$219 los dos"},
   {"esc": "② Bus 114/117 + Uber", "calc": "$126,40 bus + $128-176 Uber", "tot": "$254-302 (pero +45 min por tramo)"},
   {"esc": "③ Auto de alquiler + park&ride", "calc": "$160-300 alquiler + $16 parking + nafta + $148 tren", "tot": "$329-469 ❌"},
   {"esc": "④ Auto hasta Newark Penn + PATH", "calc": "$160-300 alquiler + $80-120 parking + $26 PATH", "tot": "$266-446 ❌"}],
  "letra_chica": "Desde julio de 2026 los pasajes one-way de NJ Transit VENCEN a los 30 días de comprados. Y la mayoría de los trenes del Raritan Valley Line terminan en Newark Penn: el pasaje cubre el transbordo, pero el tiempo real de puerta a puerta es 70-90 minutos, no el de un tren directo.",
  "veredicto_auto": "NO conviene alquilar auto solo para llegar a la estación: sale $70-160 más caro que el Uber y sumás manejar, estacionar y devolver. Solo tiene sentido si van a usar el auto para otra cosa. Y NO manejes hasta PATH: son ~35 millas por la Ruta 78/22 en hora pico (45-70 min por tramo, o sea 1,5-2,5 h diarias al volante) y PATH te deja en downtown, no en Midtown.",
  "riesgo": "DOS RIESGOS. (1) EL HUECO DE LAS 22:48: si perdés ese tren, la próxima llegada a Raritan es a la 01:31, o sea 87 minutos después. No hay NADA en el medio. El de las 22:48 es el tren crítico de las dos noches que volvés a New Jersey. (2) Branchburg es zona semi-rural: la disponibilidad de Uber a las 6-7 AM puede ser baja y las esperas largas. Pedí el auto la noche anterior y tené plan B. AVISO: NJ Transit publica cambios por obras con ~2 semanas de anticipación — revisá njtransit.com/travel-alerts-to unos días antes."},

 "nyc_interno": {
  "titulo": "Moverse dentro de NYC",
  "cambio_clave": "EL METROCARD SE ELIMINÓ. Desde el 1 de enero de 2026 no se puede comprar ni recargar, y los pases de 7 y 30 días ilimitados ya no existen. No hay decisión que tomar: se usa OMNY.",
  "tarifa": "$3,00 por viaje de subte o bus local (subió de $2,90 en enero 2026). Bus express $7,25.",
  "capping": "Fare capping de OMNY: una vez que gastaste $35 en pasajes dentro de una ventana móvil de 7 días, el resto de esos 7 días viajás gratis. La regla es el MONTO ($35), no la cantidad de viajes — que den ~12 es aritmética ($3 × 11 = $33 y el viaje 12 cobra $2 hasta llegar a $35). La ventana arranca con el PRIMER tap, no el lunes. Los buses express, el AirTrain de JFK y los transbordos NO suman al tope.",
  "critico": "Hay que usar SIEMPRE EL MISMO plástico o dispositivo los 7 días. Si un día tapean con el celular y otro con la tarjeta física, el contador se parte en dos y nunca llegan al tope. Cada persona necesita su propio medio: no se puede tapear dos veces con la misma tarjeta. Y ojo con la tarjeta extranjera: cada tap puede generar comisión por consumo en el exterior — conviene una tarjeta sin esa comisión, o crear una cuenta OMNY.",
  "cuenta": "9 días en NYC = dos períodos de 7 días. Con uso intensivo, el techo es $35 + $35 = $70 por persona en todo el viaje. Con uso liviano pagan solo lo que usan: OMNY nunca cobra de más.",
  "hoteles": [
   {"h": "Ink48 (48th & 11th Ave)", "s": "50 St (C,E) a ~12 min caminando hacia el este. Es un hotel notoriamente lejos del subte."},
   {"h": "The Beacon (Broadway & 75th)", "s": "72 St (1,2,3) a 3 cuadras, 79 St (1) a 4. Directo a Penn Station en 10 min."}]}}

# ══════════════════════════════ PASES ══════════════════════════════
passes = {
 "veredicto": "TICKETS INDIVIDUALES. Ningún pase les cierra con este itinerario, y el ahorro real está en el calendario gratuito, no en los pases.",
 "razones": [
  "El itinerario está construido sobre días gratis y pay-what-you-wish (Whitney viernes, MCNY miércoles, Frick miércoles, Guggenheim domingo, MoMA PS1, MoMI jueves). Nada de eso está en ningún pase, y los pases no lo compensan.",
  "SUMMIT One Vanderbilt y el MET — dos de los ítems más caros y deseados — NO están en NINGÚN pase. Se pagan aparte siempre.",
  "Los precios 'desde' oficiales son bajos si se compra con anticipación (Edge $34 con Advance Saver a 14+ días, Top of the Rock $42, ESB $44). Los pases se calculan contra los precios PICO ($57-69), no contra estos.",
  "El Go City All-Inclusive es de días CONSECUTIVOS: necesitarían ~7 atracciones en 3 días seguidos para amortizarlo, lo que choca de frente con los días de cierre (miércoles cierra el MET, martes cierran Frick y 9/11).",
  "Thais ya conoce los clásicos y va a hacer bastante menos atracciones pagas. Para ella ningún pase se acerca a amortizar."],
 "opciones": [
  {"p": "New York CityPASS C3", "c": "$116 (con fee)", "v": "9 días desde el primer uso",
   "inc": "Elegís 3 de 10: Empire State, Top of the Rock, Statue of Liberty+Ellis, 9/11 Museum, Edge, AMNH, Circle Line, MoMA, Intrepid, Guggenheim",
   "an": "Con ESB + 9/11 + AMNH cubre $117 a precio 'desde'. Ahorro ≈ $1. Solo conviene si compran a último momento a precio pico (ahorro ~$20)."},
  {"p": "New York CityPASS (5 atracciones)", "c": "$164", "v": "9 días desde el primer uso",
   "inc": "Obligatorias: Empire State + AMNH. Después 3 de 6: Top of the Rock, 9/11, Statue of Liberty, Circle Line, Intrepid, Guggenheim",
   "an": "El único con ahorro defendible: ~$28 a precio 'desde', ~$47 a precio pico. PERO solo si Circle Line y la Estatua ya estaban en el plan — y en este itinerario no están."},
  {"p": "Go City Explorer (5 atracciones)", "c": "$179", "v": "30 días desde la primera atracción",
   "inc": "Elegís entre ~90 atracciones. NO incluye SUMMIT, MET, Tenement, Frick, Vessel.",
   "an": "Ahorro ~$22 + Big Bus Tour gratis (valor hasta $81, promo hasta el 7 de septiembre). Solo vale si de verdad van a usar el bus turístico. Si no, el ahorro es marginal."},
  {"p": "Go City All-Inclusive (3 días)", "c": "$269", "v": "3 días CONSECUTIVOS",
   "inc": "Todo lo del Explorer, ilimitado en 3 días seguidos",
   "an": "❌ Necesita ~7 atracciones en 3 días consecutivos. Ritmo agotador y choca con los cierres semanales. No para este viaje."},
  {"p": "The Sightseeing Pass", "c": "—", "v": "—", "inc": "—",
   "an": "🚫 NO EXISTE MÁS. La empresa suspendió operaciones en junio de 2025; el AMNH le ganó un juicio de $508.474 en marzo de 2026 por entradas impagas. El sitio sigue online. NO COMPRAR."}],
 "gratis_valor": [
  {"d": "Miércoles 2/9", "q": "MCNY gratis + Frick pay-what-you-wish", "v": "$106 (2 personas)"},
  {"d": "Viernes 4/9", "q": "Whitney gratis 17-22h", "v": "$60 (2 personas)"},
  {"d": "Viernes 4/9", "q": "Morgan Library gratis 17-20h (reserva el 28/8)", "v": "$50 (2 personas)"},
  {"d": "Viernes 4/9", "q": "Noguchi gratis (primer viernes)", "v": "$32 (2 personas)"},
  {"d": "Domingo 6/9", "q": "Guggenheim pay-what-you-wish 16-17:30", "v": "~$32-60 (2 personas)"},
  {"d": "Jueves 3/9", "q": "Museum of the Moving Image gratis 14-18h", "v": "$40 (2 personas)"},
  {"d": "Todo 2026", "q": "MoMA PS1 gratis para todos", "v": "~$40 (2 personas)"},
  {"d": "Sáb 29 y dom 30/8", "q": "Charlie Parker Jazz Festival", "v": "$240+ (equivalente en club)"},
  {"d": "Miércoles 2/9", "q": "SummerStage: Christian McBride", "v": "$120+ (equivalente en club)"}],
 "total_gratis": "El calendario gratuito de este itinerario vale aproximadamente $700-780 para los dos. Ningún pase se acerca.",
 "comprar_ahora": [
  "Edge con tarifa Advance Saver ($34): exige 14+ días de anticipación. Si lo quieren, hay que comprarlo ya.",
  "Village Vanguard (Patitucci/Potter/Blade, 1-6 sep): 123 asientos, se agota.",
  "Tenement Museum: los tours se agotan y no hay reembolso ni cambio.",
  "Estatua de la Libertad corona: se agota MESES antes. Para Labor Day weekend probablemente ya no haya.",
  "Morgan Library viernes gratis: la reserva se abre el viernes 28 de agosto, una semana antes."]}

# ══════════════════════════════ RESERVAS ══════════════════════════════
reservas = [
 {"q": "Village Vanguard — VIERNES 4/9, set de las 22:00 (Patitucci/Potter/Blade), DOS lugares", "cuando": "COMPRADAS 26/8", "url": "2 x GA $45 - #18741454 y #18741456", "hecho": True,
  "por": "LISTO. A nombre de Juan Pablo Garicoits, $90 en total. Lo que queda del dia: son asientos POR ORDEN DE LLEGADA (el acomodo del 2do set abre 21:30, no 22:00) y hay minimo de una consumicion por cabeza. No sirven comida: cenar antes.", "urg": 0},
 {"q": "MO Lounge (Mandarin Oriental, piso 35) — JUEVES 3/9 ~20:30, antes de Dizzy's", "cuando": "1 semana antes", "url": "mandarinoriental.com (SevenRooms)",
  "por": "Ventanales sobre Central Park y está en el MISMO edificio que Dizzy's: se baja en ascensor. Coctel ~$26-32, sin cover. Alternativa en el mismo piso: The Bar (mar-sáb 17-1h, 45 asientos).", "urg": 2},
 {"q": "Birdland LUNES 31/8 — Vince Giordano & the Nighthawks, set 20:30", "cuando": "YA", "url": "birdlandjazz.com",
  "por": "Es ancla fija del lunes y era la ÚNICA ancla sin ítem en este checklist (lo detectó la auditoría). Los lunes de Giordano se llenan.", "urg": 3},
 {"q": "PLAY de Broadway sáb 5/9 — COMPRA FIRME esta semana (Stranger Things: The First Shadow, o HP/Paranormal Activity/Imaginary Invalid)", "cuando": "esta semana", "url": "Telecharge / TodayTix",
  "por": "Reemplaza al musical (pedido de Juan). Desde ~$76. ⚠️ Al comprar, VERIFICAR el horario de la función del sábado (19:00/19:30/20:00): tiene que TERMINAR ~22:00 para llegar al Café Wha 23:10.", "urg": 3},
 {"q": "CAFÉ WHA sáb 5/9 — reserva GRATIS por Eventbrite (Set 2, 23:45)", "cuando": "YA (la venta cierra el 5/9 y los cupos antes)", "url": "eventbrite.com (The Cafe Wha? House Band - Saturday Set 2)",
  "por": "Es SOLO reserva, no entrada: TODOS presentes a las 23:30 o liberan los asientos al standby. $20 de music charge por cabeza en la cuenta + consumo. Grupos >10: contact@cafewha.com.", "urg": 3},
 {"q": "Dizzy's JUEVES 3/9 21:00 — solo si deciden mantenerlo", "cuando": "2-3 días antes", "url": "jazz.org/dizzys",
  "por": "Entradas con horario. CONDICIONAL: es la noche del día de ~17 horas con 5 de sueño — decidan a las 20:00 de ese día; la reserva flexible o el set Late Night (~22:45) son las opciones de bajo riesgo.", "urg": 1},
 {"q": "Dos mails operativos: early check-in Ink48 (para el sáb 29) y luggage drop en The Beacon desde las 8:45 (jue 3)", "cuando": "esta semana", "url": "mail a cada hotel",
  "por": "El día 1 y el día 6 dependen de que los dos hoteles digan que sí. Un mail de dos líneas cada uno.", "urg": 2},
 {"q": "Orden de artistas del festival Charlie Parker (¿a qué hora toca Joshua Redman?)", "cuando": "vie 28/8", "url": "cityparksfoundation.org",
  "por": "La salida obligada de las 18:30 puede o no cortar el set de cierre. Saberlo el día antes permite decidir el plan B del subte (salir 18:10) con datos.", "urg": 2},
 {"q": "Tenement Museum — SOLO SI deciden sumarlo (quedó FUERA del plan)", "cuando": "solo si lo suman", "url": "tenement.org",
  "por": "Los dos lo bajaron a 'quizás' y no está en ningún día. OJO: es sin reembolso — no reservar algo que no está agendado.", "urg": 1},
 {"q": "Edge — tarifa Advance Saver $34", "cuando": "YA (exige 14+ días)", "url": "edgenyc.com",
  "por": "FUERA del plan (lo marcaron 0/0 en la última pasada). Solo si cambian de idea; con SUMMIT y Top of the Rock ya se solapa mucho.", "urg": 1},
 {"q": "SUMMIT — VIERNES 4/9, slot ATARDECER ~18:00-18:15", "cuando": "YA", "url": "summitov.com",
  "por": "$57-63 la franja de atardecer y es LA que primero se agota. Pedido de ustedes: luz + atardecer (~19:21) + noche en un solo ticket, con los espejos de Kusama en el momento justo.", "urg": 3},
 {"q": "Ford Foundation Atrium", "cuando": "Antes de las 17h del día anterior", "url": "fordfoundation.org",
  "por": "Preinscripción obligatoria. Solo se puede entrar del 31/8 al 3/9 — cierra el 5, 6, 7 y 9 de septiembre.", "urg": 3},
 {"q": "Morgan Library — viernes gratis 17-20h", "cuando": "VIERNES 28 DE AGOSTO", "url": "themorgan.org",
  "por": "Las reservas se liberan exactamente una semana antes. Si no la sacan ese día, no entran gratis.", "urg": 3},
 {"q": "Whitney — viernes gratis 17-22h", "cuando": "YA (se liberan hasta 5 semanas antes)", "url": "whitney.org",
  "por": "OBLIGATORIA: el museo dice explícitamente que se necesita ticket y el cupo es limitado. No se entra caminando. OJO ADEMÁS: desde el 19 de agosto el Whitney volvió a su horario regular y CIERRA LOS MARTES.", "urg": 3},
 {"q": "Noguchi Museum — FUERA del plan (0/0)", "cuando": "solo si lo suman", "url": "noguchi.org",
  "por": "Lo marcaron 0/0: no reservar salvo cambio de idea. (El primer viernes del mes es gratis hasta las 20h, por si acaso.)", "urg": 1},
 {"q": "Broadway — loterías digitales", "cuando": "TODOS LOS DÍAS desde ya", "url": "Broadway Direct, Telecharge, LuckySeat, TodayTix",
  "por": "Entrar es GRATIS. Hamilton $10, Maybe Happy Ending $20,64, MJ/Hadestown/Moulin Rouge $49. Anotarse a 5-6 por día no cuesta nada.", "urg": 2},
 {"q": "Moulin Rouge! — últimas funciones", "cuando": "URGENTE si la quieren", "url": "Telecharge / LuckySeat",
  "por": "Cierra el 30 de agosto. Las funciones de cierre se agotan y se encarecen.", "urg": 3},
 {"q": "9/11 Memorial Museum — JUEVES 3/9 ~10:30", "cuando": "YA", "url": "911memorial.org",
  "por": "$36, TIMED TICKET OBLIGATORIO (el sitio oficial exige compra anticipada). Modificable hasta 24h antes. Movido del lunes gratis al jueves para hacer el WTC completo en una bajada.", "urg": 3},
 {"q": "One World Observatory — JUEVES 3/9 ~13:45", "cuando": "1-2 semanas antes", "url": "oneworldobservatory.com",
  "por": "$44 + $3,50 fee, ventana de entrada de 15 min. Los slots de la tarde se agotan en verano.", "urg": 2},
 {"q": "Top of the Rock — LUNES 31/8, slot ~18:00-18:15 (ATARDECER)", "cuando": "YA", "url": "topoftherocknyc.com",
  "por": "La franja de atardecer es la cara (~$57-65) y la que vuela. Arco completo: luz → atardecer ~19:28 → noche hasta 20:05, y Birdland queda a 12 min a pie.", "urg": 3},
 {"q": "PETER LUGER — SÁBADO 5/9 17:00 (Resy)", "cuando": "YA MISMO", "url": "Resy / peterluger.com",
  "por": "Los sábados se agotan con SEMANAS. Y ojo al pagar: SIN tarjetas de crédito — efectivo, débito US o cheque. Llevar ~$200 en cash. Plan B: almuerzo del mismo sábado.", "urg": 3},
 {"q": "Lincoln Center — revisar calendario de la semana 3-6/9 (Atrium gratis, Film at Lincoln Center)", "cuando": "1 semana antes", "url": "lincolncenter.org",
  "por": "Las salas grandes están entre temporadas (Filarmónica abre 10/9; Met Opera y Ballet después), pero el David Rubenstein Atrium suele tener shows GRATIS entre semana y Film at Lincoln Center proyecta todo el año. Si aparece algo bueno el jueves o viernes, la plaza ya está en el plan del jueves 20:30 y el cambio es trivial.", "urg": 1},
 {"q": "Mercer Labs — DOMINGO 30/8, slot 17:30 (Fever)", "cuando": "esta semana", "url": "mercerlabs.com",
  "por": "Hasta $57 por cabeza según franja; los slots del fin de semana se agotan en Fever. El domingo abre hasta las 22, así que si el 17:30 no está, cualquier slot 17:00-18:00 mantiene la cadena (Crown al atardecer 19:15).", "urg": 2},
 {"q": "The Vessel — VIERNES 4/9 10:00", "cuando": "2-3 días antes", "url": "hudsonyardsnewyork.com",
  "por": "$10 (flex $15). Suele haber en el día, pero el timed ticket de las 10:00 asegura el arranque sin fila.", "urg": 1},
 {"q": "Estatua de la Libertad — corona o pedestal", "cuando": "YA, y probablemente sea tarde", "url": "statuecitycruises.com",
  "por": "La corona se agota meses antes. SOLO por el sitio oficial: ninguna agencia vende corona.", "urg": 1},
 {"q": "JGStay SoHo — RESUELTO (JP: 31/8 → 2/9). Confirmar la CONSIGNA de equipaje por mensaje", "cuando": "esta semana", "url": "jgstay.com",
  "por": "Ya reservado por Juan: adiós a dos de las tres vueltas nocturnas a NJ. Confirmar: dejar bolso lunes ~8:35 (antes del check-in) y consigna el miércoles post-checkout hasta ~17:00. Desayuno incluido 7-9 AM; recepción 24 h; Canal St (6, N/Q/R/W, J/Z) a pasos.", "urg": 2},
 {"q": "Uber en Branchburg — quedó UNA sola mañana (jueves 3, 6:20)", "cuando": "mié 2: pedir el de Raritan→hotel ANTES de subir al tren, y programar el del jueves 6:20", "url": "app",
  "por": "Zona semi-rural: a las 0:04 y a las 6:20 puede no haber conductores. Programar con anticipación y tener plan B.", "urg": 2},
 {"q": "Guggenheim — llamar y preguntar DOS cosas: si la rotonda está abierta y si sigue el pay-what-you-wish", "cuando": "La mañana del domingo 6, antes de salir del hotel", "url": "guggenheim.org / +1 212-423-3500",
  "por": "Es la única decisión del último día y ahora tiene plan B armado. La rotonda estaría en montaje hasta el 18 de septiembre, con entrada rebajada a ~$16; el pay-what-you-wish de domingos 16-17:30 no lo pude confirmar en fuente oficial (el sitio bloquea la lectura). SI LA ROTONDA ESTÁ CERRADA: el edificio —que es la razón para ir— se ve a medias, y conviene cambiarlo por MoMA PS1, el último imprescindible que queda afuera del viaje. Es gratis, abre los domingos hasta las 18 y ese día pasan a 1,2 km. Los tiempos están en el bloque de las 15:00 del domingo y no tocan el vuelo.", "urg": 3},
 {"q": "Bill's Place — SALIÓ del plan (lo desplazó el Vanguard del viernes)", "cuando": "solo si cambian de idea", "url": "billsplaceharlem.com",
  "por": "Toca viernes y sábado nomás, y las dos noches están tomadas. Queda como la alternativa si prefieren el speakeasy de Harlem antes que el Vanguard: en ese caso el Vanguard vuelve al martes y Juan va solo.", "urg": 1},
 {"q": "Birdland sáb 29/8 — RESERVAR set 21:30: David DeJesus & the Boptet, 'Celebrating Charlie Parker'", "cuando": "YA", "url": "birdlandjazz.com",
  "por": "Cartelera verificada (22/8): tributo a Charlie Parker el día del cumpleaños de Bird, en el club que lleva su nombre, a 8 cuadras del Ink48 — encaja exacto tras los 90 min de mesa en Hudson VU (mesa cierra 21:00). Alternativa más tarde: Makoto Ozone Trio 22:30.", "urg": 2},
 {"q": "Revisar travel alerts de NJ Transit para la noche del 2/9 y la mañana del 3/9", "cuando": "2-3 días antes", "url": "njtransit.com/travel-alerts-to",
  "por": "La ÚNICA noche que queda de vuelta a New Jersey (mié 2) depende del directo de las 22:48 — si se cae, la próxima llegada a Raritan es 01:31. Y el jueves 6:55 con las maletas también es NJT.", "urg": 3},
 {"q": "Reverificar el AirTrain de Newark", "cuando": "2-3 días antes de cada vuelo", "url": "njtransit.com",
  "por": "Obra de reemplazo hasta 2030, con advisories que se renuevan mes a mes.", "urg": 2}]

# ══════════════════════════════ DECISIONES ABIERTAS ══════════════════════════════
decisiones = [
 {"t": "✅ RESUELTO — dónde duerme JP del 31 al 3",
  "d": "Confirmado por Juan: noche del 31 en New Jersey, noche del 1 en NYC (habitación propia), noche del 2 en New Jersey, "
       "y el jueves 3 viaja desde New Jersey con las maletas para dejarlas en The Beacon temprano.",
  "num": "4 tramos de tren × $18,50 = $74 + 4 Ubers Branchburg↔Raritan × ~$18 = $72. Total ~$146 para JP. "
         "Thais suma 2 tramos ($37) + 2 Ubers (~$36) por su ida el 31 y su vuelta el 3.",
  "req": "ACTUALIZADO con el JGStay SoHo: quedó UNA sola vuelta nocturna a New Jersey — el miércoles después del SummerStage, "
         "con el directo de las 22:48 que llega a Raritan ~0:04, más Uber. Sigue siendo la noche cara: el jueves hay que "
         "levantarse 5:45 para el tren de las 6:55 con las maletas. El lunes y el martes JP duerme en SoHo, sin trenes."},
 {"t": "Moulin Rouge! el domingo 30 vs Charlie Parker Festival",
  "d": "Las últimas funciones de Moulin Rouge son ese fin de semana y probablemente la de cierre sea la matinée del domingo, que choca de lleno con Ravi Coltrane en Tompkins Square.",
  "num": "Moulin Rouge: $49 por lotería, $90+ comprado. Charlie Parker: gratis.",
  "req": "Hay que confirmar el horario exacto de la función de cierre. Mi recomendación: Charlie Parker, y Broadway otro día por TKTS o lotería."},
 {"t": "¿Cuántos observatorios pagos?",
  "d": "SUMMIT, Top of the Rock, Edge, Empire State y One World se solapan mucho entre sí. El video que mandaste propone tres ($120 por persona).",
  "num": "Mi recomendación: UNO pago (Top of the Rock, el único desde el que se ve el Empire State en el encuadre) + los gratuitos: Roosevelt Island Tramway ($3), Gantry Plaza, Brooklyn Heights Promenade, Staten Island Ferry, Westlight. Si quieren la experiencia-espectáculo, SUMMIT en vez de Top of the Rock.",
  "req": "Si eligen SUMMIT: no está en ningún pase, se compra suelto."},
 {"t": "US Open",
  "d": "El cuadro principal arranca el 30 de agosto y les cae encima toda la estadía. Marcaron que no les interesa, pero lo dejo anotado.",
  "num": "Grounds pass desde ~$80. Las primeras rondas (30 ago - 2 sep) es cuando más partidos simultáneos hay.",
  "req": "Se come un día entero. Si lo quisieran, el mejor encaje sería el martes 1 o miércoles 2 (días de JP solo)."},
 {"t": "Tu lista de Google Maps",
  "d": "No pude leerla (la extensión de Chrome no conecta). Está pendiente de incorporar.",
  "num": "—",
  "req": "Pegá los nombres en el chat y los cruzo contra estos 130 lugares: marco los que ya están, agrego los que faltan y te digo cuáles chocan con el itinerario."}]

out = {"transport": transport, "passes": passes, "reservas": reservas, "decisiones": decisiones}
with open(os.path.join(_R, "data/extras.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("OK - extras.json")
