"""Lee la ficha `agente/agente.txt` de un repo y la lista única `agentes.txt`. La usan armar.py y catalogo.py."""
import pathlib
import sys

NUCLEO = pathlib.Path(__file__).resolve().parent.parent

TIPOS = ("orquestador", "investigacion", "activacion-comunidad", "proyecto-agente", "disenador")
OBLIGATORIOS = ("repo", "tipo", "nombre", "nucleo", "metodo", "fuentes")


def leer(p):
    return pathlib.Path(p).read_text(encoding="utf-8")


def lista(clase=None):
    """Filas de agentes.txt como (repo, clase, perfil). Con clase, solo esa (o esas, si es una tupla)."""
    filas = []
    for l in leer(NUCLEO / "agentes.txt").splitlines():
        c = l.split("#")[0].split()
        if not c:
            continue
        fila = (c[0], c[1] if len(c) > 1 else "sistema", c[2] if len(c) > 2 else "-")
        if clase is None or fila[1] in ((clase,) if isinstance(clase, str) else clase):
            filas.append(fila)
    return filas


def agentes():
    """Repos que son agentes (todo menos el núcleo y los repos de datos), en el orden de agentes.txt."""
    return [r for r, clase, _ in lista() if clase not in ("nucleo", "datos")]


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
