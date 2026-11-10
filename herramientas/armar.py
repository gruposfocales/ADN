#!/usr/bin/env python3
"""Arma el agente de un repo de proyecto a partir de los módulos del núcleo GF.

Uso:
    python3 herramientas/armar.py ../gf-2026-002-comunicacion            # escribe los archivos
    python3 herramientas/armar.py ../gf-2026-002-comunicacion --revisar  # solo avisa si hay diferencias

El repo del proyecto necesita:
    agente/agente.txt       ficha corta (repo, núcleo, título, adn)
    agente/personalidad.md  sección 0, propia del proyecto

Genera en el repo del proyecto:
    AGENTS.md                         personalidad + método + plataforma con archivos
    agente/SYSTEM-sin-archivos.md     personalidad + método + plataforma sin archivos (para pegar en Dify, etc.)
    MANUAL-FASES.md y la copia del ADN, sincronizados con el núcleo
"""
import pathlib
import sys

NUCLEO = pathlib.Path(__file__).resolve().parent.parent


def leer(p):
    return pathlib.Path(p).read_text(encoding="utf-8")


def ficha(repo):
    datos = {}
    for linea in leer(repo / "agente" / "agente.txt").splitlines():
        if ":" in linea and not linea.lstrip().startswith("#"):
            k, v = linea.split(":", 1)
            datos[k.strip()] = v.strip()
    for clave in ("repo", "nucleo", "titulo", "adn"):
        if clave not in datos:
            sys.exit(f"Falta '{clave}' en agente/agente.txt")
    return datos


def armar(datos, personalidad, plataforma):
    aviso = (
        f"<!-- Archivo armado con gruposfocales/ADN herramientas/armar.py (núcleo v{datos['nucleo']}). "
        "No lo edites a mano: cambia agente/personalidad.md en este repo o los módulos en gruposfocales/ADN, y vuelve a armar. -->"
    )
    metodo = leer(NUCLEO / "modulos" / "metodo.md").replace("{{REPO}}", datos["repo"])
    plat = leer(NUCLEO / "plataformas" / f"{plataforma}.md")
    partes = [f"# AGENTS.md — {datos['titulo']}", aviso, personalidad.strip(), "---", metodo.strip(), plat.strip()]
    return "\n\n".join(partes) + "\n"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    revisar = "--revisar" in sys.argv
    if len(args) != 1:
        sys.exit(__doc__)
    repo = pathlib.Path(args[0]).resolve()
    datos = ficha(repo)
    version = leer(NUCLEO / "VERSION").strip()
    if datos["nucleo"] != version:
        print(f"⚠️  {repo.name} pide el núcleo v{datos['nucleo']} y aquí está la v{version}. Se arma con la v{version}.")
        datos["nucleo"] = version
    personalidad = leer(repo / "agente" / "personalidad.md")

    salidas = {
        repo / "AGENTS.md": armar(datos, personalidad, "con-archivos"),
        repo / "agente" / "SYSTEM-sin-archivos.md": armar(datos, personalidad, "sin-archivos"),
        repo / "MANUAL-FASES.md": leer(NUCLEO / "modulos" / "manual-fases.md"),
        repo / datos["adn"]: leer(NUCLEO / "modulos" / "adn.md"),
    }
    distintos = [p for p, txt in salidas.items() if not p.exists() or leer(p) != txt]
    for p in distintos:
        print(("✏️  difiere: " if revisar else "✅ escrito: ") + str(p.relative_to(repo)))
        if not revisar:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(salidas[p], encoding="utf-8")
    if not distintos:
        print(f"✅ {repo.name} está al día con el núcleo v{version}.")
    sys.exit(1 if revisar and distintos else 0)


if __name__ == "__main__":
    main()
