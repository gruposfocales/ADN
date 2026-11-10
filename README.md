# ADN · Núcleo de los agentes de GruposFocales

Este repo es la fuente de los módulos comunes. **Cada repo de proyecto es un agente**, en cualquier plataforma (Claude, Hermes, Dify, ChatGPT…). La plataforma solo lo ejecuta: todo lo que el agente es y sabe vive en GitHub.

## Cómo se arma un agente

```
SYSTEM = personalidad del proyecto  +  método común  +  reglas de la plataforma
         (repo del proyecto)           (este repo)       (este repo)
```

| Módulo | Archivo | Dónde vive |
|---|---|---|
| Personalidad (sección 0) | `agente/personalidad.md` | Repo del proyecto |
| Ficha del agente (repo, versión del núcleo, título) | `agente/agente.txt` | Repo del proyecto |
| Método del arquitecto (secciones 1-10) | `modulos/metodo.md` | Aquí |
| Manual de fases (289 ítems y gates) | `modulos/manual-fases.md` | Aquí, con copia en cada proyecto |
| ADN de GruposFocales | `modulos/adn.md` | Aquí, con copia en cada proyecto |
| Plataforma con archivos y git (Claude, Hermes, Codex) | `plataformas/con-archivos.md` | Aquí |
| Plataforma sin archivos (Dify, ChatGPT) | `plataformas/sin-archivos.md` | Aquí |

## Armar o revisar un proyecto

Con este repo y los de proyecto como carpetas hermanas:

```
python3 herramientas/armar.py ../gf-2026-002-comunicacion            # arma
python3 herramientas/armar.py ../gf-2026-002-comunicacion --revisar  # solo dice si está desalineado
```

Genera en el proyecto:
- `AGENTS.md`: versión con archivos. La leen Claude Code (vía `CLAUDE.md`), Hermes y Codex.
- `agente/SYSTEM-sin-archivos.md`: versión para pegar a mano en el SYSTEM de Dify u otra plataforma sin archivos.
- `MANUAL-FASES.md` y la copia del ADN, sincronizados con este núcleo.

## Cambiar algo

- **Lo de un proyecto** (rol, tono, qué cuida): edita `agente/personalidad.md` en su repo y vuelve a armar.
- **El método, el manual o una plataforma**: edita aquí, sube `VERSION` y vuelve a armar cada proyecto. Luego vuelve a pegar el SYSTEM en cada plataforma.

## Versiones

`VERSION` = 1.0. El método v1.0 es el `AGENTS.md` v5.2-proyecto (2026-10-23) de los proyectos gf-2026-002/003/004, sin cambios de contenido. El manual es `MANUAL-FASES.md` v4.0.

`ADN Grupos Focales.md` es el texto original subido; `modulos/adn.md` es la versión completa (misión, visión, propósito…) que usan los proyectos.
