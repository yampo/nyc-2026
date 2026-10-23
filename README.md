# NYC 2026

Planificador del viaje a Nueva York del 29 de agosto al 6 de septiembre de 2026.

**https://yampo.github.io/nyc-2026/**

Este repo es solo la **salida publicada**: un `index.html` autocontenido, sin
dependencias externas. Lo genera el taller de viajes, que es donde vive la
fuente (catálogo, itinerario, motor). Acá no se edita nada a mano.

El sitio se publica **saneado**: sin números de reserva ni apellidos. GitHub
Pages en cuenta gratuita obliga a que el repo sea público, así que `robots.txt`
y `noindex` le piden a los buscadores que no lo indexen — pero eso no lo hace
privado: cualquiera con la URL entra.

Para rearmarlo, desde el taller:

    python3 engine/build_all.py nyc-2026 --publicar
