#!/usr/bin/env python3
"""Arma el agente de un repo a partir de los módulos del núcleo GF.

Uso:
    python3 herramientas/armar.py ../gf-2026-002-comunicacion            # escribe los archivos
    python3 herramientas/armar.py ../gf-2026-002-comunicacion --revisar  # solo avisa si hay diferencias
    python3 herramientas/armar.py --todos [--revisar]                    # todos los repos de agentes.txt

El repo necesita `agente/agente.txt` (ficha) y, según el método:
    metodo: arquitecto  → agente/personalidad.md (sección 0). Se generan AGENTS.md,
                          agente/SYSTEM-sin-archivos.md, MANUAL-FASES.md y la copia del ADN.
    metodo: propio      → el archivo de `instrucciones:` (por defecto AGENTS.md), escrito a mano.
                          Solo se genera agente/SYSTEM-sin-archivos.md.
Versiones: AGENTS.md y SYSTEM-sin-archivos.md llevan `versión N · fecha` en su aviso. Si el contenido
cambia, la versión anterior se archiva en agente/historial/<archivo>-vN.md y la nueva sube a N+1.
Con `skills: si`, copia las skills del núcleo (skills/) a .claude/skills/.
"""
import datetime
import pathlib
import re
import sys

from ficha import leer, leer_ficha

NUCLEO = pathlib.Path(__file__).resolve().parent.parent


def sin_frontmatter(txt):
    txt = re.sub(r"\A---\n.*?\n---\n", "", txt, flags=re.S)
    return "\n".join(l for l in txt.splitlines() if not l.strip().startswith("@")).strip()


def aviso(datos, editable):
    return (
        f"<!-- Archivo armado con gruposfocales/ADN herramientas/armar.py (núcleo v{datos['nucleo']}, versión {{VERSION}}). "
        f"No lo edites a mano: cambia {editable} en este repo o los módulos en gruposfocales/ADN, y vuelve a armar. -->"
    )


def armar_arquitecto(datos, repo, plataforma):
    personalidad = leer(repo / "agente" / "personalidad.md").strip()
    metodo = leer(NUCLEO / "modulos" / "metodo.md").replace("{{REPO}}", datos["repo"]).strip()
    plat = leer(NUCLEO / "plataformas" / f"{plataforma}.md").strip()
    partes = [f"# AGENTS.md — {datos['titulo']}", aviso(datos, "agente/personalidad.md"), personalidad, "---", metodo, plat]
    return "\n\n".join(partes) + "\n"


def armar_propio(datos, repo):
    instr = datos.get("instrucciones", "AGENTS.md")
    cuerpo = sin_frontmatter(leer(repo / instr))
    plat = leer(NUCLEO / "plataformas" / "sin-archivos.md").strip()
    partes = [f"# SYSTEM — {datos['nombre']}", aviso(datos, instr), cuerpo, plat]
    return "\n\n".join(partes) + "\n"


VERSIONADOS = ("AGENTS.md", "SYSTEM-sin-archivos.md")
MARCA = re.compile(r", versión (\d+) · \d{4}-\d{2}-\d{2}\)")


def version_de(texto):
    m = MARCA.search(texto or "")
    return int(m.group(1)) if m else 0


def versionar(p, nuevo):
    """(bytes nuevos o None si no cambió, (ruta de historial, texto viejo) o None)."""
    viejo = p.read_text(encoding="utf-8") if p.exists() else None
    if viejo is not None and MARCA.sub(", versión {VERSION})", viejo) == nuevo:
        return None, None
    n = version_de(viejo)
    sin_marca = nuevo.replace(", versión {VERSION})", ")", 1)
    if viejo is not None and not n and viejo == sin_marca:
        viejo = None  # primera versión: el texto es el mismo, no hace falta archivarlo
    final = nuevo.replace("{VERSION}", f"{n + 1} · {datetime.date.today().isoformat()}", 1)
    carpeta = (p.parent if p.parent.name == "agente" else p.parent / "agente") / "historial"
    return final.encode("utf-8"), ((carpeta / f"{p.stem}-v{n}.md", viejo) if viejo else None)


def skills(repo):
    salidas = {}
    origen = NUCLEO / "skills"
    for f in origen.rglob("*"):
        if f.is_file():
            salidas[repo / ".claude" / "skills" / f.relative_to(origen)] = f.read_bytes()
    return salidas


def salidas_de(repo, datos):
    s = {}
    if datos["metodo"] == "arquitecto":
        s[repo / "AGENTS.md"] = armar_arquitecto(datos, repo, "con-archivos")
        s[repo / "agente" / "SYSTEM-sin-archivos.md"] = armar_arquitecto(datos, repo, "sin-archivos")
        s[repo / "MANUAL-FASES.md"] = leer(NUCLEO / "modulos" / "manual-fases.md")
    else:
        s[repo / "agente" / "SYSTEM-sin-archivos.md"] = armar_propio(datos, repo)
    if datos.get("adn"):
        s[repo / datos["adn"]] = leer(NUCLEO / "modulos" / "adn.md")
    if datos.get("skills") == "si":
        s.update(skills(repo))
    return {p: (v.encode("utf-8") if isinstance(v, str) else v) for p, v in s.items()}


def procesar(repo, revisar):
    datos = leer_ficha(repo)
    version = leer(NUCLEO / "VERSION").strip()
    avisos = []
    if datos["nucleo"] != version:
        avisos.append(f"pide el núcleo v{datos['nucleo']} y aquí está la v{version}")
        datos["nucleo"] = version
    for f in datos["fuentes"]:
        otro, _, ruta = f.rpartition(":")
        base = repo.parent / otro.split("/")[-1] if otro else repo
        if not (base / ruta).exists():
            avisos.append(f"la fuente {f} no existe")
    if not (repo / "agente" / "pruebas.md").exists():
        avisos.append("falta agente/pruebas.md")
    salidas = salidas_de(repo, datos)
    historial = {}
    for p in [q for q in salidas if q.name in VERSIONADOS]:
        final, hist = versionar(p, salidas[p].decode("utf-8"))
        if final is None:
            del salidas[p]
        else:
            salidas[p] = final
            if hist:
                historial[hist[0]] = hist[1]
    distintos = [p for p, b in salidas.items() if not p.exists() or p.read_bytes() != b]
    for p in distintos:
        print(("✏️  difiere: " if revisar else "✅ escrito: ") + f"{repo.name}/{p.relative_to(repo)}")
        if not revisar:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(salidas[p])
    if not revisar:
        for h, viejo in historial.items():
            h.parent.mkdir(parents=True, exist_ok=True)
            h.write_text(viejo, encoding="utf-8")
            print(f"🗄️  archivado: {repo.name}/{h.relative_to(repo)}")
    for a in avisos:
        print(f"⚠️  {repo.name}: {a}")
    if not distintos and not avisos:
        print(f"✅ {repo.name} ({datos['tipo']}) está al día con el núcleo v{version}.")
    return bool(distintos or avisos)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    revisar = "--revisar" in sys.argv
    if "--todos" in sys.argv:
        repos = [NUCLEO.parent / l.split("#")[0].strip() for l in leer(NUCLEO / "agentes.txt").splitlines() if l.split("#")[0].strip()]
    elif len(args) == 1:
        repos = [pathlib.Path(args[0]).resolve()]
    else:
        sys.exit(__doc__)
    malos = [r for r in repos if procesar(r, revisar)]
    sys.exit(1 if revisar and malos else 0)


if __name__ == "__main__":
    main()
