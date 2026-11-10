#!/usr/bin/env python3
"""Escribe CATALOGO.md con los agentes de agentes.txt (tipo, nombre, método y archivos que lee).

Uso: python3 herramientas/catalogo.py [--revisar]
"""
import pathlib
import sys

from ficha import leer, leer_ficha

NUCLEO = pathlib.Path(__file__).resolve().parent.parent


def main():
    repos = [l.split("#")[0].strip() for l in leer(NUCLEO / "agentes.txt").splitlines() if l.split("#")[0].strip()]
    filas = []
    for nombre in repos:
        d = leer_ficha(NUCLEO.parent / nombre)
        filas.append(f"| {d['nombre']} | `{d['tipo']}` | `{d['repo']}` | {d['metodo']} | {', '.join(f'`{f}`' for f in d['fuentes'])} |")
    txt = "\n".join([
        "# Catálogo de agentes",
        "",
        "> Generado por `herramientas/catalogo.py` desde `agentes.txt` y el `agente/agente.txt` de cada repo. No lo edites a mano.",
        "> Tipos: ver `modulos/tipos.md`. Cada agente se ejecuta con `agente/SYSTEM-sin-archivos.md` más sus archivos, leídos en vivo de GitHub.",
        "",
        "| Agente | Tipo | Repo | Método | Archivos que lee |",
        "|---|---|---|---|---|",
        *filas,
        "",
    ])
    destino = NUCLEO / "CATALOGO.md"
    if "--revisar" in sys.argv:
        ok = destino.exists() and leer(destino) == txt
        print("✅ CATALOGO.md al día." if ok else "✏️  CATALOGO.md difiere.")
        sys.exit(0 if ok else 1)
    destino.write_text(txt, encoding="utf-8")
    print(f"✅ CATALOGO.md con {len(filas)} agentes.")


if __name__ == "__main__":
    main()
