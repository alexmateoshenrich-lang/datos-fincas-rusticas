# Datos recogidos el 2026-11-16 19:21 UTC
Anuncios BOE con fincas: 8 · parcelas consultadas: 46
Fuentes: API BOE (ultimos 14 dias) + Catastro (datos no protegidos) + WMS ocupacion del suelo.
Estado de los servicios (errores = fallos de red/servidor durante esta ejecucion):
- BOE-API: 0 errores · OK
- BOE-texto: 0 errores · OK
- BOE-pdf: 0 errores · OK
- Catastro-DNPRC: 0 errores · OK
- Catastro-coord: 5 errores · ejemplo: https://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCoordenadas.asmx/Consulta_RCCOOR {'SRS': 'EPSG:4326', 'RC': '04060A04500040'} -> HTTP 500
- Catastro-INSPIRE: 0 errores · OK
- WMS-capacidades: 0 errores · OK
- WMS-info: 0 errores · OK

Importante: 'clase_catastro' sale del cultivo catastral por superficie (monte si >=60% monte/arbolado/matorral).
La ocupacion del suelo (WMS) es una segunda fuente: compararla con el cultivo catastral para el semaforo.

## BOE-B-2026-37672 · 2026-11-16 · Resolución de la Delegación de Economía y Hacienda en Teruel, por la que se anuncia subasta de bienes propiedad del Estado.
https://www.boe.es/diario_boe/txt.php?id=BOE-B-2026-37672 · https://www.boe.es/boe/dias/2026/11/16/pdfs/BOE-B-2026-37672.pdf
(sin referencias catastrales en el texto; revisar el anuncio)

## BOE-B-2026-37018 · 2026-11-12 · Anuncio de la Delegación Territorial de Economía, Hacienda, Fondos Europeos, Universidad, Industria, Energía e Innovación de la Junta de Andalucía en Almería por el que se convoca levantamiento de actas previa a la ocupación de la finca con referencia catastral 04060A045000400000GA afectada por el proyecto denominado "Línea de evacuación 132 kV de la PSFV Tabernas I y PSFV Tabernas II", sito en los términos municipales de Tabernas y de Lucainena de las Torres (Almería). Expediente: LAT 6860.
https://www.boe.es/diario_boe/txt.php?id=BOE-B-2026-37018 · https://www.boe.es/boe/dias/2026/11/12/pdfs/BOE-B-2026-37018.pdf
| RC | municipio (prov) | pol/parc | ha | monte segun Catastro | cultivo dominante | construcciones | lat,lon | ocupacion suelo |
|---|---|---|---|---|---|---|---|---|
| 04060A045000400000GA | LUCAINENA DE LAS TORRES (ALMERÍA) | 45/40 | 6.536 | no_monte (0% monte) | LABOR O LABRADÍO SECANO | 0 | - | - |

## BOE-B-2026-36911 · 2026-11-11 · Anuncio de los Servicios Territoriales del Departamento de Territorio, Vivienda y Transición Ecológica en Lleida, por el que se hace pública la convocatoria para la redacción de las actas previas a la ocupación de los bienes y/o derechos afectados por el procedimiento de expropiación derivado de la ejecución del proyecto de la infraestructura de evacuación, líneas soterradas a 25 kV y la LAT subterránea a 25KV, de la planta solar fotovoltaica denominada 22CER, de 4,5 MW, sobre terreno en suelo no urbanizable, en los términos municipales de Les Oluges y Cervera, en la comarca de La Segarra (exp. FUE-2021-02341200).
https://www.boe.es/diario_boe/txt.php?id=BOE-B-2026-36911 · https://www.boe.es/boe/dias/2026/11/11/pdfs/BOE-B-2026-36911.pdf
- Parcelas colindantes verificadas con cartografia: 2 parcelas, 3.61 ha: 25084A00400065, 25084A00409069
- Parcelas colindantes verificadas con cartografia: 3 parcelas, 0.45 ha: 25190A00409010, 25190A00409009, 25190A00409067
| RC | municipio (prov) | pol/parc | ha | monte segun Catastro | cultivo dominante | construcciones | lat,lon | ocupacion suelo |
|---|---|---|---|---|---|---|---|---|
| 25190A00409010 | LES OLUGES (LLEIDA) | 4/9010 | 0.065 | no_monte (0% monte) | VÍA DE COMUNICACIÓN DE DOMINIO PÚBLICO | 0 | - | - |
| 25190A00409009 | LES OLUGES (LLEIDA) | 4/9009 | 0.249 | no_monte (0% monte) | VÍA DE COMUNICACIÓN DE DOMINIO PÚBLICO | 0 | - | - |
| 25190A00409067 | LES OLUGES (LLEIDA) | 4/9067 | 0.131 | no_monte (0% monte) | VÍA DE COMUNICACIÓN DE DOMINIO PÚBLICO | 0 | - | - |
| 25084A00400065 | CERVERA (LLEIDA) | 4/65 | 1.596 | monte (98% monte) | MATORRAL | 0 | - | - |
| 25084A00409069 | CERVERA (LLEIDA) | 4/9069 | 2.011 | no_monte (0% monte) | VÍA DE COMUNICACIÓN DE DOMINIO PÚBLICO | 0 | - | - |

## BOE-B-2026-36914 · 2026-11-11 · Resolución de la Delegación Territorial de la Consejería Economía, Hacienda y Fondos Europeos y de Universidad, Industria, Energía e Innovación de la Junta de Andalucía en Córdoba, por la que se concede Autorización Administrativa Previa, Autorización Administrativa de Construcción y Declaración, en concreto, de Utilidad Pública, para las instalaciones eléctricas de alta tensión recogidas en el proyecto denominado: Nueva línea de media tensión 15 kV entre el apoyo A553610 y el apoyo A556998 para cierre de las línea denominadas "FTE_PA_2" y "PALMA_RÍO", sito en parajes Ochavillo Bajo, Las Monjas, Casablanca, en los términos municipales de Fuente Palmera y Hornachuelos (Córdoba), y se convoca para el levantamiento de actas previas a la ocupación de las fincas afectadas. (AT 36/20-1).
https://www.boe.es/diario_boe/txt.php?id=BOE-B-2026-36914 · https://www.boe.es/boe/dias/2026/11/11/pdfs/BOE-B-2026-36914.pdf
- Parcelas colindantes verificadas con cartografia: 9 parcelas, 55.74 ha: 14036A037000110000FO, 14036A037090060000FD, 14036A037000120001GL, 14036A038090050000FL, 14036A038000240000FX, 14036A038000250000FI, 14036A038090030000FQ, 14036A038000260000FJ, 14030A013000280000DE
| RC | municipio (prov) | pol/parc | ha | monte segun Catastro | cultivo dominante | construcciones | lat,lon | ocupacion suelo |
|---|---|---|---|---|---|---|---|---|
| 14036A037000110000FO | HORNACHUELOS (CÓRDOBA) | 37/11 | 0.017 | no_monte (0% monte) | NARANJO | 1 | - | - |
| 14036A037090060000FD | HORNACHUELOS (CÓRDOBA) | 37/9006 | 0.417 | no_monte (0% monte) | VÍA DE COMUNICACIÓN DE DOMINIO PÚBLICO | 0 | - | - |
| 14036A037000120001GL | HORNACHUELOS (CÓRDOBA) | 37/12 | 0.029 | sin datos | - | 3 | - | - |
| 14036A038090050000FL | HORNACHUELOS (CÓRDOBA) | 38/9005 | 2.689 | no_monte (0% monte) | VÍA DE COMUNICACIÓN DE DOMINIO PÚBLICO | 0 | - | - |
| 14036A038000240000FX | HORNACHUELOS (CÓRDOBA) | 38/24 | 6.294 | no_monte (0% monte) | OLIVAR | 0 | - | - |
| 14036A038000250000FI | HORNACHUELOS (CÓRDOBA) | 38/25 | 14.691 | no_monte (0% monte) | OLIVAR | 0 | - | - |
| 14036A038090030000FQ | HORNACHUELOS (CÓRDOBA) | 38/9003 | 4.441 | no_monte (0% monte) | VÍA DE COMUNICACIÓN DE DOMINIO PÚBLICO | 0 | - | - |
| 14036A038000260000FJ | HORNACHUELOS (CÓRDOBA) | 38/26 | 22.128 | no_monte (0% monte) | LABOR O LABRADÍO REGADÍO | 0 | - | - |
| 14030A013000280000DE | FUENTE PALMERA (CÓRDOBA) | 13/28 | 5.035 | no_monte (0% monte) | LABOR O LABRADÍO REGADÍO | 0 | - | - |

## BOE-B-2026-36156 · 2026-11-05 · Resolución de la Delegación de Economía y Hacienda de Segovia por la que se anuncia la celebración de subasta pública al alza de 27 fincas rústicas propiedad de la Administración General del Estado en la provincia de Segovia, con admisión simultánea de ofertas en sobre cerrado.
https://www.boe.es/diario_boe/txt.php?id=BOE-B-2026-36156 · https://www.boe.es/boe/dias/2026/11/05/pdfs/BOE-B-2026-36156.pdf
| RC | municipio (prov) | pol/parc | ha | monte segun Catastro | cultivo dominante | construcciones | lat,lon | ocupacion suelo |
|---|---|---|---|---|---|---|---|---|
| 40143B001000480000GJ | MATABUENA (SEGOVIA) | 1/48 | 1.102 | dudoso (0% monte) | PASTOS | 0 | - | - |
| 40143B001000930000GA | MATABUENA (SEGOVIA) | 1/93 | 0.851 | dudoso (0% monte) | PASTOS | 0 | - | - |
| 40143B001001270000GQ | MATABUENA (SEGOVIA) | 1/127 | 0.469 | dudoso (0% monte) | PASTOS | 0 | - | - |
| 40143B001001490000GU | MATABUENA (SEGOVIA) | 1/149 | 1.241 | dudoso (0% monte) | PASTOS | 0 | - | - |
| 40143B002000830000GO | MATABUENA (SEGOVIA) | 2/83 | 0.415 | dudoso (0% monte) | PRADOS O PRADERAS | 0 | - | - |
| 40143B002001770000GO | MATABUENA (SEGOVIA) | 2/177 | 0.855 | dudoso (0% monte) | PASTOS | 0 | - | - |
| 40143B002101610000GL | MATABUENA (SEGOVIA) | 2/10161 | 1.369 | no_monte (0% monte) | PASTIZAL | 0 | - | - |
| 40143B003000730000GU | MATABUENA (SEGOVIA) | 3/73 | 0.453 | dudoso (0% monte) | PRADOS O PRADERAS | 0 | - | - |
| 40143B003001020000GZ | MATABUENA (SEGOVIA) | 3/102 | 0.799 | dudoso (0% monte) | PRADOS O PRADERAS | 0 | - | - |
| 40143B004000190000GB | MATABUENA (SEGOVIA) | 4/19 | 3.866 | dudoso (0% monte) | PASTOS | 0 | - | - |
| 40143B004000440000GE | MATABUENA (SEGOVIA) | 4/44 | 1.434 | dudoso (0% monte) | PASTOS | 0 | - | - |
| 40143B004000530000GA | MATABUENA (SEGOVIA) | 4/53 | 0.694 | dudoso (0% monte) | PRADOS O PRADERAS | 0 | - | - |
| 40143B004000710000GR | MATABUENA (SEGOVIA) | 4/71 | 1.526 | dudoso (0% monte) | PASTOS | 0 | - | - |
| 40143B004001050000GJ | MATABUENA (SEGOVIA) | 4/105 | 1.308 | dudoso (0% monte) | PASTOS | 0 | - | - |
| 40143B004001110000GZ | MATABUENA (SEGOVIA) | 4/111 | 6.302 | dudoso (0% monte) | PASTOS | 0 | - | - |
| 40143B004001120000GU | MATABUENA (SEGOVIA) | 4/112 | 2.241 | dudoso (0% monte) | PASTOS | 0 | - | - |
| 40143B004001190000GQ | MATABUENA (SEGOVIA) | 4/119 | 0.376 | dudoso (0% monte) | PASTOS | 0 | - | - |
| 40143B005000570000GH | MATABUENA (SEGOVIA) | 5/57 | 3.017 | dudoso (0% monte) | PASTOS | 0 | - | - |
| 40143B005000720000GT | MATABUENA (SEGOVIA) | 5/72 | 0.629 | dudoso (0% monte) | PASTOS | 0 | - | - |
| 40143B005000770000GR | MATABUENA (SEGOVIA) | 5/77 | 0.877 | dudoso (0% monte) | PASTOS | 0 | - | - |
| 40143B006000290000GZ | MATABUENA (SEGOVIA) | 6/29 | 2.904 | dudoso (0% monte) | PRADOS O PRADERAS | 0 | - | - |
| 40143B006000550000GD | MATABUENA (SEGOVIA) | 6/55 | 1.569 | dudoso (0% monte) | PASTOS | 0 | - | - |
| 40143B006000600000GI | MATABUENA (SEGOVIA) | 6/60 | 0.234 | dudoso (0% monte) | PASTOS | 0 | - | - |
| 40143B006000610000GJ | MATABUENA (SEGOVIA) | 6/61 | 1.83 | dudoso (0% monte) | PASTOS | 0 | - | - |
| 40143B006000690000GB | MATABUENA (SEGOVIA) | 6/69 | 0.698 | dudoso (0% monte) | PASTOS | 0 | - | - |
| 40143B006000960000GZ | MATABUENA (SEGOVIA) | 6/96 | 0.413 | dudoso (0% monte) | PASTOS | 0 | - | - |
| 40143B008000150000GZ | MATABUENA (SEGOVIA) | 8/15 | 4.766 | dudoso (0% monte) | PASTOS | 0 | - | - |

## BOE-B-2026-36158 · 2026-11-05 · Anuncio de la Delegación de Economía y Hacienda en Alicante, por el que se hace público el acuerdo de inicio del procedimiento de investigación patrimonial relativo a la parcela 26 del polígono 19, paraje Fontcalent, del término municipal de Alicante.
https://www.boe.es/diario_boe/txt.php?id=BOE-B-2026-36158 · https://www.boe.es/boe/dias/2026/11/05/pdfs/BOE-B-2026-36158.pdf
| RC | municipio (prov) | pol/parc | ha | monte segun Catastro | cultivo dominante | construcciones | lat,lon | ocupacion suelo |
|---|---|---|---|---|---|---|---|---|
| 03900A019000260000OY | ALICANTE/ALACANT (ALICANTE) | 19/26 | 0.28 | dudoso (0% monte) | PASTOS | 0 | - | - |

## BOE-B-2026-36193 · 2026-11-05 · Resolución de la Dirección General de Transición Energética y Economía Circular por la que se convoca para el levantamiento de Actas Previas a la Ocupación de las fincas afectadas por el proyecto de la nueva subestación transformadora STR FUENTIDUEÑA 66/20kV (ISE300), en el término municipal de Fuentidueña de Tajo (Madrid). EXE 11/26.
https://www.boe.es/diario_boe/txt.php?id=BOE-B-2026-36193 · https://www.boe.es/boe/dias/2026/11/05/pdfs/BOE-B-2026-36193.pdf
- Parcelas colindantes verificadas con cartografia: 2 parcelas, 2.87 ha: 28060A103003670000KG, 28060A103004670000KL
| RC | municipio (prov) | pol/parc | ha | monte segun Catastro | cultivo dominante | construcciones | lat,lon | ocupacion suelo |
|---|---|---|---|---|---|---|---|---|
| 28060A103003670000KG | FUENTIDUEÑA DE TAJO (MADRID) | 103/367 | 1.303 | no_monte (0% monte) | LABOR -TIERRA ARABLE | 0 | - | - |
| 28060A103004670000KL | FUENTIDUEÑA DE TAJO (MADRID) | 103/467 | 1.565 | no_monte (0% monte) | LABOR -TIERRA ARABLE | 0 | - | - |

## BOE-B-2026-36016 · 2026-11-04 · Anuncio de la Confederación Hidrográfica del Miño-Sil, O.A. de información pública del expediente de autorización para la ejecución del "Plan de cortas para o aproveitamento forestal na parcela catastral 27047A08000351", en las márgenes de varios cauces, parcela 351-polígono 80 de la C.M.V.M.C. de Lamaigrexa e lugares de Domiz e Pereiro da parroquia de Salcedo, parroquia de Lamaigrexa (San Pedro) , del T.M. de A Pobra do Brollón (Lugo).
https://www.boe.es/diario_boe/txt.php?id=BOE-B-2026-36016 · https://www.boe.es/boe/dias/2026/11/04/pdfs/BOE-B-2026-36016.pdf
| RC | municipio (prov) | pol/parc | ha | monte segun Catastro | cultivo dominante | construcciones | lat,lon | ocupacion suelo |
|---|---|---|---|---|---|---|---|---|
| 27047A08000351 | A POBRA DO BROLLON (LUGO) | 80/351 | 106.065 | monte (83% monte) | PINAR MADERABLE | 0 | - | - |
