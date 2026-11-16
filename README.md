# datos-fincas-rusticas

Recoge cada lunes datos **publicos** de fincas rusticas anunciadas en el BOE (subastas y enajenaciones),
para que un asistente los analice despues.

- `recoger_datos.py`: lee el sumario del BOE por su API de datos abiertos, extrae referencias
  catastrales y consulta los servicios web oficiales del Catastro (cultivos, superficie, construcciones,
  geometria) y servicios WMS de ocupacion del suelo.
- `.github/workflows/semanal.yml`: lo ejecuta los lunes y cuando cambia el script.
- `data/resumen.md`: resumen compacto de la ultima ejecucion.
- `data/latest.json`: datos completos.
- `data/diagnostico.md`: que servicios respondieron y que errores hubo.

Uso personal, volumen bajo y pausas entre peticiones. No se leen portales que lo prohiban en su `robots.txt`.
