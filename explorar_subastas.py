#!/usr/bin/env python3
"""Exploracion puntual del portal de subastas: guarda su robots.txt y el HTML de las
paginas de busqueda SOLO si el robots.txt las permite. Pocas peticiones, con pausa."""
import os
import time
import urllib.robotparser

import requests

BASE = "https://subastas.boe.es"
UA = "datos-fincas-rusticas/1.0 (uso personal, bajo volumen; https://github.com/alexmateoshenrich-lang/datos-fincas-rusticas)"
PAGINAS = ["/", "/subastas_ava.php", "/reg/subastas_ava.php"]
OUT = "data/subastas_exploracion"
os.makedirs(OUT, exist_ok=True)

s = requests.Session()
s.headers.update({"User-Agent": UA})
informe = []

robots = s.get(BASE + "/robots.txt", timeout=30)
informe.append(f"robots.txt -> HTTP {robots.status_code}")
with open(f"{OUT}/robots.txt", "w", encoding="utf-8") as f:
    f.write(robots.text)
rp = urllib.robotparser.RobotFileParser()
rp.parse(robots.text.splitlines() if robots.status_code == 200 else [])

for ruta in PAGINAS:
    url = BASE + ruta
    permitido = rp.can_fetch(UA, url)
    informe.append(f"{ruta}: robots permite={permitido}")
    if not permitido:
        continue
    time.sleep(2)
    try:
        r = s.get(url, timeout=45)
    except Exception as e:
        informe.append(f"{ruta}: error {e!r}")
        continue
    informe.append(f"{ruta}: HTTP {r.status_code}, {len(r.text)} caracteres")
    nombre = ruta.strip("/").replace("/", "_") or "inicio"
    with open(f"{OUT}/{nombre}.html", "w", encoding="utf-8") as f:
        f.write(r.text[:150000])

with open(f"{OUT}/informe.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(informe) + "\n")
print("\n".join(informe))
