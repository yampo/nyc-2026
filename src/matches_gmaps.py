#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lugares del catálogo que TAMBIÉN estaban en la lista "NY 2026" de Google Maps.
Mapeo hecho a mano (varios están en la lista con el nombre en español o abreviado),
para poder distinguir tres orígenes:

  ambas      → lo propusimos nosotros Y estaba en la lista guardada  (coincidencia)
  lista      → salió solo de la lista de Google (los 71 que se agregaron el 25/8)
  propuesta  → salió solo de nuestro trabajo conjunto

La clave es el id del catálogo; el comentario es cómo figura en la lista de Google.
"""

EN_LISTA = {
    "residenceinn":      "Residence Inn by Marriott Bridgewater Branchburg",
    "mercerlabs":        "Mercer Labs",
    "frick":             "The Frick Collection",
    "transitmuseum":     "New York Transit Museum",
    "morgan":            "The Morgan Library & Museum",
    "whitney":           "Whitney Museum of American Art",
    "thecrown":          "The Crown",
    "westlight":         "Westlight",
    "sunsetparkview":    "Sunset Park",
    "rooseveltisland":   "Roosevelt Island",
    "lincolncenter":     "Lincoln Center for the Performing Arts",
    "siferry":           "Staten Island Ferry",
    "wavehill":          "Wave Hill Public Garden & Cultural Center",
    "eldridge":          "Museum at Eldridge Street",
    "vanguard":          "Village Vanguard",
    "ornithology":       "Ornithology Jazz Club",
    "nublu":             "Nublu",
    "dizzys":            "Dizzy's Club",
    "bluenote":          "Blue Note",
    "birdland":          "Birdland Jazz Club",
    "barbes":            "Barbès",
    "lunatico":          "LunÀtico",
    "barbayeux":         "Bar Bayeux",
    "tanoreen":          "Tanoreen",
    "splunch":           "S&P Lunch",
    "lbspumoni":         "L&B Spumoni Gardens",
    "frankels":          "Frankel's Delicatessen & Appetizing",
    "essexmarket":       "Essex Market",
    "dekalb":            "Dekalb Market Hall",
    "casadellamozz":     "Casa Della Mozzarella",
    "bosbagels":         "BO's Bagels",
    "arthurmarket":      "Arthur Avenue Retail Market",
    "arthurave":         "Arthur Ave",
    "hamburgerica":      "Hamburger America",
    "vessel":            "Vessel",
    "tram":              "Teleférico Isla Roosevelt",
    "russdaughters":     "Russ & Daughters",
    "fordfoundation":    "Ford Foundation Public Atrium Garden",
    "beacon":            "Hotel Beacon",
    "ink48":             "Ink 48 Hotel",
    "cloisters":         "The Cloisters",
    "amnh":              "Museo Americano de Historia Natural",
    "highline":          "High Line",
    "chelseamarket":     "Chelsea Market",
    "tkts":              "TKTS Lincoln Center",
    "met":               "Museo Metropolitano de Arte",
    "bhpromenade":       "Brooklyn Heights Promenade",
    "timeoutmarket":     "Time Out Market New York",
    "911museum":         "National September 11 Memorial & Museum",
    "topofrock":         "Top of The Rock",
    "summit":            "SUMMIT One Vanderbilt",
    "nypl":              "Biblioteca Pública de Nueva York",
    "grandcentral":      "Grand Central Terminal",
    "edge":              "Edge NYC",
    "oculus":            "Oculus Center",
    "intrepid":          "Intrepid Sea-Air-Space Museum",
    "smalls":            "Smalls Jazz Club",
    "mezzrow":           "Mezzrow",
    "katzs":             "Katz's Delicatessen",
    "washingtonsq":      "Washington Square Park",
    "cafewha":           "Cafe Wha?",
    "peterluger":        "Peter Luger Steak House",
    "moma":              "The Museum of Modern Art",
}
