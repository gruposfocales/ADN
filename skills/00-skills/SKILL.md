---
name: skills
description: "Muestra el menú de skills del repo, ordenado por la cadena de trabajo, y sugiere cuál usar según lo que el usuario quiere hacer. Usar con /skills o al preguntar qué skills hay."
familia: 00 · Menú
version: 1.0
entra: lo que el usuario quiere hacer
sale: la skill sugerida y su siguiente paso
siguiente: —
estado: estable
---

# Menú de skills

1. Lee `.claude/skills/INDICE.md`.
2. Si el usuario solo pidió el menú, muéstralo tal cual (la tabla y la cadena).
3. Si dijo qué quiere hacer, sugiere una sola skill: su comando, qué necesita de entrada y cuál viene después.
4. Si el índice parece desactualizado (una carpeta que no aparece), corre `python3 herramientas/indexar_skills.py` y vuelve a leerlo.

No ejecutes la skill sugerida hasta que el usuario lo pida.
