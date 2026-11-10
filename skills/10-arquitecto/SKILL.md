---
name: arquitecto-investigacion
description: "Diseña o continúa una investigación completa (cualitativa, cuantitativa o mixta) por fases y gates hasta un paquete listo para campo. Usar con 'continuar', 'estado', 'ir a fase N' o al abrir el repo del proyecto."
familia: 10 · Diseño
version: 4.0
entra: decisión de negocio, evidencia, archivos del proyecto
sale: DASHBOARD.md, BITACORA.md, INSTRUMENTOS.md aprobados
siguiente: 20-campo-kapso
estado: estable
---

# Arquitecto de Investigación Estratégica

Esta skill no repite las reglas: las reglas vigentes viven en la raíz del repo, para que haya una sola versión.

1. Lee `AGENTS.md` (cómo trabajas) y `MANUAL-FASES.md` (las 289 preguntas y los gates).
2. Lee `DASHBOARD.md` (en la raíz de este repo).
3. Sigue el ciclo de `AGENTS.md` §5: lote → auditoría → `ok`.
4. Cuenta el avance con `python3 herramientas/contar_avance.py DASHBOARD.md`.

Las carpetas de `pruebas/` no son evidencia de ningún proyecto.
