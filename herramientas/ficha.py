"""Lee la ficha `agente/agente.txt` de un repo. La usan armar.py y catalogo.py."""
import pathlib
import sys

TIPOS = ("orquestador", "investigacion", "activacion-comunidad", "proyecto-agente", "disenador")
OBLIGATORIOS = ("repo", "tipo", "nombre", "nucleo", "metodo", "fuentes")


def leer(p):
    return pathlib.Path(p).read_text(encoding="utf-8")


def leer_ficha(repo):
    datos = {}
    for linea in leer(pathlib.Path(repo) / "agente" / "agente.txt").splitlines():
        if ":" in linea and not linea.lstrip().startswith("#"):
            k, v = linea.split(":", 1)
            datos[k.strip()] = v.strip()
    faltan = [k for k in OBLIGATORIOS if k not in datos]
    if datos.get("metodo") == "arquitecto" and "titulo" not in datos:
        faltan.append("titulo")
    if faltan:
        sys.exit(f"{pathlib.Path(repo).name}: falta {', '.join(faltan)} en agente/agente.txt")
    if datos["tipo"] not in TIPOS:
        sys.exit(f"{pathlib.Path(repo).name}: tipo '{datos['tipo']}' no válido. Usa uno de: {', '.join(TIPOS)}")
    if datos["metodo"] not in ("arquitecto", "propio"):
        sys.exit(f"{pathlib.Path(repo).name}: metodo debe ser 'arquitecto' o 'propio'")
    datos["fuentes"] = [f.strip() for f in datos["fuentes"].split(",") if f.strip()]
    return datos
