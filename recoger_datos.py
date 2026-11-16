#!/usr/bin/env python3
"""Recoge datos PUBLICOS de fincas rusticas anunciadas en el BOE.

Fuentes (todas son servicios oficiales pensados para uso automatico):
  - API de datos abiertos del BOE (sumario diario, Seccion V).
  - Servicios web del Catastro de consulta de datos NO protegidos (cultivos, superficie,
    construcciones, coordenadas) y servicio INSPIRE de parcelas (geometria).
  - WMS de ocupacion del suelo (IGN: CORINE/SIOSE) y Mapa Forestal (MITECO).

Uso personal y volumen bajo (pausas entre peticiones, limite de parcelas por ejecucion).
No se leen subastas.boe.es ni portales que lo prohiban: las paginas HTML se consultan
solo si su robots.txt lo permite.

Salida (carpeta data/): latest.json, resumen.md y diagnostico.md
"""
import datetime as dt
import html as htmlmod
import io
import json
import os
import re
import time
import traceback
import urllib.robotparser
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

import requests

try:
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
except Exception:  # shapely es opcional: sin el, no se calculan colindancias
    Polygon = None
    unary_union = None

REPO = "https://github.com/alexmateoshenrich-lang/datos-fincas-rusticas"
UA = f"datos-fincas-rusticas/1.0 (uso personal, bajo volumen; {REPO})"
DIAS = int(os.environ.get("DIAS", "14"))
MAX_RC = int(os.environ.get("MAX_RC", "120"))
MAX_WMS = int(os.environ.get("MAX_WMS", "60"))
LIMITE_SEGUNDOS = int(os.environ.get("LIMITE_SEGUNDOS", "1800"))
PAUSA = 0.4
INICIO = time.time()

BOE_API = "https://www.boe.es/datosabiertos/api/boe/sumario/{f}"
OVC_BASES = [
    "https://ovc.catastro.meh.es",
    "https://ovc.catastro.hacienda.gob.es",
    "https://ovc.catastro.minhap.es",
    "http://ovc.catastro.meh.es",
]
WMS_SERVICIOS = [
    ("Ocupacion suelo IGN (CORINE/SIOSE)", "https://servicios.idee.es/wms-inspire/ocupacion-suelo",
     ("corine", "siose", "landcover", "ocupaci", "cobertura")),
    ("Mapa Forestal MITECO", "https://wms.mapama.gob.es/sig/Biodiversidad/MFE/wms.aspx",
     ("forestal", "mfe", "arbol", "cobertura", "especie")),
]
PALABRAS_TITULO = ("subasta", "enajen", "venta", "inmueble", "finca", "parcela", "terreno", "rustic", "rústic")

MONTE = ("monte", "pinar", "encin", "alcornoc", "robl", "matorral", "frondos", "conifer", "conífer",
         "arbol", "dehesa", "sabin", "haya", "eucalipt")
NO_MONTE = ("labor", "labrad", "regad", "olivar", "viñedo", "vinedo", "frutal", "huerta", "cereal",
            "almendr", "naranj", "arroz")
DUDOSO = ("pasto", "prado", "erial")

RC20 = re.compile(r"(?<![0-9A-Z])(\d{5}[A-Z]\d{12}[A-Z]{2})(?![0-9A-Z])")
RC14 = re.compile(r"(?<![0-9A-Z])(\d{5}[A-Z]\d{8})(?![0-9A-Z])")

S = requests.Session()
S.headers.update({"User-Agent": UA})

LOG = []
ERRORES = {}
STATS = {}
FALLOS = {}
BASE_OK = {"v": None}
_ROBOTS = {}
_WMS_CACHE = {}


def log(m):
    print(m, flush=True)
    LOG.append(str(m))


def stat(k, n=1):
    STATS[k] = STATS.get(k, 0) + n


def error(servicio, mensaje):
    lista = ERRORES.setdefault(servicio, [])
    stat(f"errores_{servicio}")
    if len(lista) < 6:
        lista.append(str(mensaje)[:400])


def pedir(url, servicio, params=None, headers=None, timeout=45, reintentos=3, silenciar_404=False):
    ultimo = None
    for i in range(reintentos):
        try:
            r = S.get(url, params=params, headers=headers, timeout=timeout)
        except Exception as e:
            ultimo = repr(e)[:200]
        else:
            if r.status_code == 200:
                time.sleep(PAUSA)
                return r
            ultimo = f"HTTP {r.status_code}"
            if r.status_code == 404 and silenciar_404:
                return None
            if r.status_code in (400, 401, 403, 404):
                break
        time.sleep(1.5 * (i + 1))
    error(servicio, f"{url} {params or ''} -> {ultimo}")
    return None


def permitido(url):
    p = urlparse(url)
    base = f"{p.scheme}://{p.netloc}"
    if base not in _ROBOTS:
        rp = urllib.robotparser.RobotFileParser()
        try:
            r = S.get(base + "/robots.txt", timeout=20)
            rp.parse(r.text.splitlines() if r.status_code == 200 else [])
        except Exception:
            rp.parse([])
        _ROBOTS[base] = rp
    return _ROBOTS[base].can_fetch(UA, url)


def sin_ns(raiz):
    for e in raiz.iter():
        if isinstance(e.tag, str):
            e.tag = e.tag.split("}")[-1]
    return raiz


def aplanar(e):
    d = {}
    if e is None:
        return d
    for x in e.iter():
        if x is e:
            continue
        if len(list(x)) == 0 and x.text and x.text.strip():
            d.setdefault(x.tag, x.text.strip())
    return d


def limpiar_html(t):
    t = re.sub(r"(?is)<(script|style).*?</\1>", " ", t)
    t = re.sub(r"(?s)<[^>]+>", " ", t)
    t = htmlmod.unescape(t)
    return re.sub(r"\s+", " ", t).strip()


# ----------------------------------------------------------------------------- BOE
def buscar_items(nodo, salida):
    if isinstance(nodo, dict):
        ident = nodo.get("identificador")
        if isinstance(ident, str) and ident.startswith("BOE-B-") and "titulo" in nodo:
            salida.append(nodo)
        for v in nodo.values():
            buscar_items(v, salida)
    elif isinstance(nodo, list):
        for v in nodo:
            buscar_items(v, salida)


def url_de(v):
    if isinstance(v, str):
        return v
    if isinstance(v, dict):
        for k in ("texto", "#text", "url", "valor"):
            if isinstance(v.get(k), str):
                return v[k]
        for x in v.values():
            if isinstance(x, str) and x.startswith("http"):
                return x
    return None


def anuncios_boe():
    hoy = dt.date.today()
    encontrados = {}
    for n in range(DIAS):
        dia = hoy - dt.timedelta(days=n)
        r = pedir(BOE_API.format(f=dia.strftime("%Y%m%d")), "BOE-API",
                  headers={"Accept": "application/json"}, silenciar_404=True)
        if r is None:
            continue
        stat("boe_sumarios_leidos")
        try:
            datos = r.json()
        except Exception as e:
            error("BOE-API", f"JSON no valido {dia}: {e}")
            continue
        items = []
        buscar_items(datos, items)
        for it in items:
            titulo = it.get("titulo") or ""
            if any(p in titulo.lower() for p in PALABRAS_TITULO):
                ident = it["identificador"]
                encontrados[ident] = {
                    "id": ident,
                    "fecha": dia.isoformat(),
                    "titulo": titulo,
                    "url_html": url_de(it.get("url_html")) or f"https://www.boe.es/diario_boe/txt.php?id={ident}",
                    "url_pdf": url_de(it.get("url_pdf")) or f"https://www.boe.es/boe/dias/{dia:%Y/%m/%d}/pdfs/{ident}.pdf",
                }
    return list(encontrados.values())


def texto_anuncio(a):
    url = a["url_html"]
    if url and permitido(url):
        r = pedir(url, "BOE-texto")
        if r is not None:
            r.encoding = "utf-8"
            return limpiar_html(r.text), "html"
    else:
        stat("boe_html_no_permitido_por_robots")
    r = pedir(a["url_pdf"], "BOE-pdf")
    if r is not None:
        try:
            from pypdf import PdfReader
            lector = PdfReader(io.BytesIO(r.content))
            t = " ".join((p.extract_text() or "") for p in lector.pages)
            return re.sub(r"\s+", " ", t).strip(), "pdf"
        except Exception as e:
            error("BOE-pdf", f"{a['id']} pypdf: {e}")
    return "", "ninguno"


def extraer_rcs(texto):
    vistos = {}
    for m in RC20.finditer(texto):
        vistos.setdefault(m.group(1), texto[max(0, m.start() - 350): m.end() + 200])
    for m in RC14.finditer(texto):
        rc = m.group(1)
        if any(k.startswith(rc) for k in vistos):
            continue
        vistos.setdefault(rc, texto[max(0, m.start() - 350): m.end() + 200])
    return list(vistos.items())


# -------------------------------------------------------------------------- Catastro
def ovc(ruta, params, servicio):
    if FALLOS.get(servicio, 0) >= 5:
        stat(f"omitido_{servicio}")
        return None
    bases = [BASE_OK["v"]] if BASE_OK["v"] else OVC_BASES
    for b in bases:
        r = pedir(b + ruta, servicio, params=params, reintentos=2)
        if r is not None:
            BASE_OK["v"] = b
            FALLOS[servicio] = 0
            return r
    BASE_OK["v"] = None
    FALLOS[servicio] = FALLOS.get(servicio, 0) + 1
    return None


def clase_cultivo(nombre):
    n = nombre.lower()
    if any(p in n for p in MONTE):
        return "monte"
    if any(p in n for p in NO_MONTE):
        return "no_monte"
    if any(p in n for p in DUDOSO):
        return "dudoso"
    return "otro"


def a_float(v):
    try:
        return float(str(v).replace(",", "."))
    except Exception:
        return 0.0


def catastro_dnprc(rc):
    r = ovc("/ovcservweb/OVCSWLocalizacionRC/OVCCallejero.asmx/Consulta_DNPRC",
            {"Provincia": "", "Municipio": "", "RC": rc}, "Catastro-DNPRC")
    if r is None:
        return None
    try:
        raiz = sin_ns(ET.fromstring(r.content))
    except Exception as e:
        error("Catastro-DNPRC", f"XML no valido {rc}: {e}")
        return {"error": "xml no valido", "inicio": r.text[:300]}
    errs = [aplanar(x) for x in raiz.iter("err")]
    out = {"rc": rc, "errores_servicio": errs[:3]}
    bico = next(raiz.iter("bico"), None)
    if bico is None:
        out["inicio_respuesta"] = r.text[:600]
        listado = [aplanar(x) for x in raiz.iter("rcdnp")]
        if listado:
            out["bienes_listados"] = listado[:10]
        return out
    bi = bico.find("bi")
    dtf = aplanar(bi.find("dt")) if bi is not None else {}
    debi = aplanar(bi.find("debi")) if bi is not None else {}
    subs = [aplanar(s) for s in bico.iter("spr")]
    cons = [aplanar(c) for c in bico.iter("cons")]
    sub_compactas = []
    m2 = {"monte": 0.0, "dudoso": 0.0, "no_monte": 0.0, "otro": 0.0}
    for s in subs:
        nombre = s.get("dcc") or s.get("ccc") or ""
        sup = a_float(s.get("ssp", 0))
        m2[clase_cultivo(nombre)] += sup
        sub_compactas.append({"cultivo": nombre, "clave": s.get("ccc"), "m2": sup, "intensidad": s.get("ip")})
    total = sum(m2.values())
    sfc = a_float(debi.get("sfc", 0))
    out.update({
        "municipio": dtf.get("nm"), "provincia": dtf.get("np"), "paraje": dtf.get("npa"),
        "poligono": dtf.get("cpo"), "parcela": dtf.get("cpa"),
        "uso": debi.get("luso"), "superficie_parcela_m2": sfc or total,
        "ha": round((sfc or total) / 10000.0, 3),
        "subparcelas": sub_compactas, "construcciones": cons[:10],
    })
    if total > 0:
        out["pct_monte"] = round(100 * m2["monte"] / total)
        out["pct_dudoso"] = round(100 * m2["dudoso"] / total)
        out["pct_no_monte"] = round(100 * m2["no_monte"] / total)
        if m2["monte"] / total >= 0.6:
            out["clase_catastro"] = "monte"
        elif (m2["monte"] + m2["dudoso"]) / total >= 0.6:
            out["clase_catastro"] = "dudoso"
        else:
            out["clase_catastro"] = "no_monte"
    else:
        out["clase_catastro"] = None
    return out


def catastro_coord(rc14):
    r = ovc("/ovcservweb/OVCSWLocalizacionRC/OVCCoordenadas.asmx/Consulta_RCCOOR",
            {"SRS": "EPSG:4326", "RC": rc14}, "Catastro-coord")
    if r is None:
        return None
    try:
        raiz = sin_ns(ET.fromstring(r.content))
        x, y = raiz.find(".//xcen"), raiz.find(".//ycen")
        if x is not None and y is not None:
            return float(x.text), float(y.text)
    except Exception as e:
        error("Catastro-coord", f"{rc14}: {e}")
    return None


def catastro_poligono(rc14):
    if Polygon is None:
        return None
    r = ovc("/INSPIRE/wfsCP.aspx",
            {"service": "wfs", "version": "2.0.0", "request": "GetFeature",
             "STOREDQUERY_ID": "GetParcel", "refcat": rc14, "srsname": "EPSG:25830"},
            "Catastro-INSPIRE")
    if r is None:
        return None
    try:
        raiz = sin_ns(ET.fromstring(r.content))
        polis = []
        for pl in raiz.iter("posList"):
            nums = [float(v) for v in (pl.text or "").split()]
            pts = list(zip(nums[0::2], nums[1::2]))
            if len(pts) >= 4:
                polis.append(Polygon(pts).buffer(0))
        if polis:
            return unary_union(polis)
        error("Catastro-INSPIRE", f"{rc14}: sin geometria. Inicio: {r.text[:200]}")
    except Exception as e:
        error("Catastro-INSPIRE", f"{rc14}: {e}")
    return None


def coord_desde_geom(geom):
    """Punto interior de la parcela (ETRS89 UTM 30N) -> lon, lat WGS84."""
    try:
        from pyproj import Transformer
        c = geom.representative_point()
        t = Transformer.from_crs("EPSG:25830", "EPSG:4326", always_xy=True)
        lon, lat = t.transform(c.x, c.y)
        return lon, lat
    except Exception as e:
        error("coord-geom", repr(e))
        return None


def agrupar(parcelas):
    """parcelas: lista de dicts con rc, geom, ha. Une las que se tocan (< 2 m)."""
    n = len(parcelas)
    padre = list(range(n))

    def f(i):
        while padre[i] != i:
            padre[i] = padre[padre[i]]
            i = padre[i]
        return i

    for i in range(n):
        for j in range(i + 1, n):
            try:
                if parcelas[i]["geom"].distance(parcelas[j]["geom"]) < 2.0:
                    padre[f(i)] = f(j)
            except Exception:
                pass
    grupos = {}
    for i in range(n):
        grupos.setdefault(f(i), []).append(i)
    salida = []
    for idx in grupos.values():
        if len(idx) >= 2:
            salida.append({"rcs": [parcelas[i]["rc"] for i in idx], "n": len(idx),
                           "ha": round(sum(parcelas[i]["ha"] for i in idx), 2)})
    return sorted(salida, key=lambda g: -g["ha"])


# ------------------------------------------------------------------------------- WMS
def capas_wms(base):
    if base in _WMS_CACHE:
        return _WMS_CACHE[base]
    capas = []
    r = pedir(base, "WMS-capacidades",
              params={"service": "WMS", "request": "GetCapabilities", "version": "1.3.0"}, reintentos=2)
    if r is not None:
        try:
            raiz = sin_ns(ET.fromstring(r.content))
            for layer in raiz.iter("Layer"):
                nombre = layer.find("Name")
                if nombre is not None and nombre.text:
                    titulo = layer.find("Title")
                    q = layer.get("queryable")
                    capas.append({"name": nombre.text.strip(),
                                  "title": (titulo.text or "").strip() if titulo is not None else "",
                                  "queryable": q in (None, "1", "true")})
        except Exception as e:
            error("WMS-capacidades", f"{base}: {e}")
    _WMS_CACHE[base] = capas
    return capas


def wms_info(base, capa, lon, lat):
    d = 0.0004
    intentos = (("1.3.0", "application/json"), ("1.3.0", "text/plain"),
                ("1.3.0", "text/html"), ("1.1.1", "text/plain"))
    for version, fmt in intentos:
        p = {"service": "WMS", "request": "GetFeatureInfo", "version": version, "layers": capa,
             "query_layers": capa, "styles": "", "format": "image/png", "width": 101, "height": 101,
             "info_format": fmt, "feature_count": 5}
        if version == "1.3.0":
            p.update({"crs": "EPSG:4326", "bbox": f"{lat - d},{lon - d},{lat + d},{lon + d}", "i": 50, "j": 50})
        else:
            p.update({"srs": "EPSG:4326", "bbox": f"{lon - d},{lat - d},{lon + d},{lat + d}", "x": 50, "y": 50})
        r = pedir(base, "WMS-info", params=p, reintentos=1)
        if r is None:
            continue
        t = r.text.strip()
        if not t or "ServiceException" in t[:600]:
            continue
        return limpiar_html(t)[:500]
    return None


def consultar_capas(lon, lat):
    salida = []
    for nombre, base, claves in WMS_SERVICIOS:
        sel = [c for c in capas_wms(base)
               if c["queryable"] and any(k in (c["name"] + " " + c["title"]).lower() for k in claves)][:2]
        for c in sel:
            info = wms_info(base, c["name"], lon, lat)
            if info:
                salida.append({"servicio": nombre, "capa": c["name"], "respuesta": info})
    return salida


# ----------------------------------------------------------------------------- salida
def celda(v):
    return str(v if v not in (None, "") else "-").replace("|", "/").replace("\n", " ")


def fila(item):
    c = item.get("catastro") or {}
    co = item.get("coordenadas") or {}
    oc = "; ".join(f"{o['servicio']} [{o['capa']}]: {o['respuesta'][:140]}" for o in item.get("ocupacion_suelo") or [])
    dominante = "-"
    if c.get("subparcelas"):
        mayor = max(c["subparcelas"], key=lambda s: s["m2"])
        dominante = mayor["cultivo"] or mayor.get("clave")
    cons = len(c.get("construcciones") or [])
    pct = f"{c.get('clase_catastro')} ({c.get('pct_monte')}% monte)" if c.get("clase_catastro") else "sin datos"
    pos = f"{co['lat']:.5f},{co['lon']:.5f}" if co else "-"
    return (f"| {celda(item['rc'])} | {celda(c.get('municipio'))} ({celda(c.get('provincia'))}) "
            f"| {celda(c.get('poligono'))}/{celda(c.get('parcela'))} | {celda(c.get('ha'))} | {celda(pct)} "
            f"| {celda(dominante)} | {cons} | {pos} | {celda(oc)} |")


def construir_resumen(resultado, cuando):
    L = [f"# Datos recogidos el {cuando}",
         f"Anuncios BOE con fincas: {len(resultado)} · parcelas consultadas: {STATS.get('rc_consultadas', 0)}",
         "Fuentes: API BOE (ultimos %d dias) + Catastro (datos no protegidos) + WMS ocupacion del suelo." % DIAS,
         "Estado de los servicios (errores = fallos de red/servidor durante esta ejecucion):"]
    for s in ("BOE-API", "BOE-texto", "BOE-pdf", "Catastro-DNPRC", "Catastro-coord", "Catastro-INSPIRE",
              "WMS-capacidades", "WMS-info"):
        L.append(f"- {s}: {STATS.get('errores_' + s, 0)} errores" + (f" · ejemplo: {ERRORES[s][0]}" if s in ERRORES else " · OK"))
    L.append("")
    L.append("Importante: 'clase_catastro' sale del cultivo catastral por superficie (monte si >=60% monte/arbolado/matorral).")
    L.append("La ocupacion del suelo (WMS) es una segunda fuente: compararla con el cultivo catastral para el semaforo.")
    for a in resultado:
        L.append("")
        L.append(f"## {a['id']} · {a['fecha']} · {a['titulo']}")
        L.append(f"{a['url_html']} · {a['url_pdf']}")
        for g in a.get("agrupaciones_colindantes") or []:
            L.append(f"- Parcelas colindantes verificadas con cartografia: {g['n']} parcelas, {g['ha']} ha: {', '.join(g['rcs'])}")
        if a["rcs"]:
            L.append("| RC | municipio (prov) | pol/parc | ha | monte segun Catastro | cultivo dominante | construcciones | lat,lon | ocupacion suelo |")
            L.append("|---|---|---|---|---|---|---|---|---|")
            for item in a["rcs"]:
                L.append(fila(item))
        else:
            L.append("(sin referencias catastrales en el texto; revisar el anuncio)")
    return "\n".join(L) + "\n"


def escribir_salidas(resultado, cuando):
    os.makedirs("data", exist_ok=True)
    limpio = []
    for a in resultado:
        b = dict(a)
        b["rcs"] = [{k: v for k, v in it.items() if k != "_geom"} for it in a["rcs"]]
        limpio.append(b)
    with open("data/latest.json", "w", encoding="utf-8") as f:
        json.dump({"generado": cuando, "dias": DIAS, "stats": STATS, "errores": ERRORES, "anuncios": limpio},
                  f, ensure_ascii=False, indent=1)
    with open("data/resumen.md", "w", encoding="utf-8") as f:
        f.write(construir_resumen(resultado, cuando))


def escribir_diagnostico(cuando):
    os.makedirs("data", exist_ok=True)
    L = [f"# Diagnostico {cuando}", f"Duracion: {int(time.time() - INICIO)} s", "", "## Contadores"]
    L += [f"- {k}: {v}" for k, v in sorted(STATS.items())]
    L += ["", "## Errores por servicio (hasta 6 ejemplos)"]
    for s, lista in ERRORES.items():
        L.append(f"### {s}")
        L += [f"- {m}" for m in lista]
    capas = {b: [c["name"] for c in cs][:25] for b, cs in _WMS_CACHE.items()}
    L += ["", "## Capas WMS detectadas (primeras 25)", json.dumps(capas, ensure_ascii=False, indent=1)]
    L += ["", "## Registro"] + LOG[-80:]
    with open("data/diagnostico.md", "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def main():
    cuando = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    anuncios = anuncios_boe()
    log(f"Anuncios BOE candidatos por titulo: {len(anuncios)}")
    resultado = []
    total_rc = 0
    for a in sorted(anuncios, key=lambda x: x["fecha"], reverse=True):
        if time.time() - INICIO > LIMITE_SEGUNDOS:
            stat("cortado_por_tiempo")
            break
        texto, via = texto_anuncio(a)
        if not texto:
            continue
        rcs = extraer_rcs(texto)
        if not rcs and not re.search(r"r[úu]stic", texto, re.I):
            continue
        a.update({"texto_via": via, "texto_inicio": texto[:700], "rcs": []})
        for rc, ctx in rcs:
            if total_rc >= MAX_RC:
                stat("rc_omitidos_por_limite")
                continue
            total_rc += 1
            a["rcs"].append({"rc": rc, "contexto": ctx})
        resultado.append(a)
    log(f"Anuncios con fincas: {len(resultado)} · RC a consultar: {total_rc}")

    usadas_wms = 0
    for a in resultado:
        parcelas = []
        for item in a["rcs"]:
            if time.time() - INICIO > LIMITE_SEGUNDOS:
                stat("cortado_por_tiempo")
                break
            rc = item["rc"]
            stat("rc_consultadas")
            cat = catastro_dnprc(rc)
            item["catastro"] = cat
            geom = catastro_poligono(rc[:14])
            coord = catastro_coord(rc[:14])
            if coord is None and geom is not None:
                coord = coord_desde_geom(geom)
                if coord:
                    stat("coord_desde_geometria")
            item["coordenadas"] = {"lon": coord[0], "lat": coord[1]} if coord else None
            if geom is not None and cat and cat.get("ha"):
                parcelas.append({"rc": rc, "geom": geom, "ha": cat["ha"]})
            elif geom is not None:
                parcelas.append({"rc": rc, "geom": geom, "ha": round(geom.area / 10000.0, 3)})
            if coord and usadas_wms < MAX_WMS and not (cat and cat.get("clase_catastro") == "no_monte"):
                usadas_wms += 1
                item["ocupacion_suelo"] = consultar_capas(coord[0], coord[1])
        if len(parcelas) >= 2:
            a["agrupaciones_colindantes"] = agrupar(parcelas[:80])
        escribir_salidas(resultado, cuando)  # guardado incremental
    escribir_salidas(resultado, cuando)
    log("Terminado.")
    return cuando


if __name__ == "__main__":
    ahora = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    try:
        ahora = main()
    except Exception:
        log("EXCEPCION NO CONTROLADA:\n" + traceback.format_exc())
    finally:
        escribir_diagnostico(ahora)
