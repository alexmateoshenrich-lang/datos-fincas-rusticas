# Diagnostico 2026-11-16 19:38 UTC
Duracion: 208 s

## Contadores
- boe_sumarios_leidos: 12
- coord_desde_geometria: 46
- errores_Catastro-coord: 5
- errores_WMS-capacidades: 1
- omitido_Catastro-coord: 41
- rc_consultadas: 46

## Errores por servicio (hasta 6 ejemplos)
### Catastro-coord
- https://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCoordenadas.asmx/Consulta_RCCOOR {'SRS': 'EPSG:4326', 'RC': '04060A04500040'} -> HTTP 500
- https://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCoordenadas.asmx/Consulta_RCCOOR {'SRS': 'EPSG:4326', 'RC': '25190A00409010'} -> HTTP 500
- https://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCoordenadas.asmx/Consulta_RCCOOR {'SRS': 'EPSG:4326', 'RC': '25190A00409009'} -> HTTP 500
- https://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCoordenadas.asmx/Consulta_RCCOOR {'SRS': 'EPSG:4326', 'RC': '25190A00409067'} -> HTTP 500
- https://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCoordenadas.asmx/Consulta_RCCOOR {'SRS': 'EPSG:4326', 'RC': '25084A00400065'} -> HTTP 500
### WMS-capacidades
- https://wms.mapama.gob.es/sig/Biodiversidad/MFE/wms.aspx {'service': 'WMS', 'request': 'GetCapabilities', 'version': '1.3.0'} -> SSLError(MaxRetryError("HTTPSConnectionPool(host='wms.mapama.gob.es', port=443): Max retries exceeded with url: /sig/Biodiversidad/MFE/wms.aspx?service=WMS&request=GetCapabilities&version=1.3.0 (Cause

## Capas WMS detectadas (primeras 25)
{
 "https://servicios.idee.es/wms-inspire/ocupacion-suelo": [
  "LC.LandCoverSurfaces",
  "LU.ExistingLandUse"
 ],
 "https://wms.mapama.gob.es/sig/Biodiversidad/MFE/wms.aspx": []
}

## Registro
Anuncios BOE candidatos por titulo: 161
Anuncios con fincas: 8 · RC a consultar: 46
Terminado.
