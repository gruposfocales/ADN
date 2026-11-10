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

## Tipos y catálogo

- **Tipos de agente:** `modulos/tipos.md` (orquestador, investigación, activación de comunidad, proyecto de agente, diseñador).
- **Catálogo:** `agentes.txt` lista los repos; `CATALOGO.md` (generado con `herramientas/catalogo.py`) muestra tipo, método y archivos que lee cada uno. De aquí sale el chatflow único de Dify: una rama por agente.

## La carpeta `agente/` de cada repo

| Archivo | Qué es | Quién lo escribe |
|---|---|---|
| `agente.txt` | Ficha: `repo`, `tipo`, `nombre`, `metodo` (`arquitecto` o `propio`), `fuentes` (archivos que lee en vivo, `repo:ruta` si son de otro repo), `adn`, `skills` | A mano |
| `personalidad.md` | Sección 0 (solo `metodo: arquitecto`) | A mano |
| `SYSTEM-sin-archivos.md` | Instrucciones completas para Dify y otras plataformas sin archivos | `armar.py` |
| `pruebas.md` | 4-6 preguntas con lo que debe pasar. Se corren tras cada cambio | A mano |

Con `metodo: propio` (orquestador y diseñador) las instrucciones siguen escritas a mano en su `AGENTS.md` o `CLAUDE.md`; el armador solo genera su SYSTEM.

## Skills

Las skills viven en `skills/` y el armador las copia a `.claude/skills/` de los repos con `skills: si`. Se editan aquí, nunca en la copia.

## Armar o revisar un proyecto

Con este repo y los de proyecto como carpetas hermanas:

```
python3 herramientas/armar.py ../gf-2026-002-comunicacion            # arma
python3 herramientas/armar.py ../gf-2026-002-comunicacion --revisar  # solo dice si está desalineado
python3 herramientas/armar.py --todos --revisar                     # todos los del catálogo
python3 herramientas/catalogo.py                                    # regenera CATALOGO.md
```

Genera en el proyecto:
- `AGENTS.md`: versión con archivos. La leen Claude Code (vía `CLAUDE.md`), Hermes y Codex.
- `agente/SYSTEM-sin-archivos.md`: versión para pegar a mano en el SYSTEM de Dify u otra plataforma sin archivos.
- `MANUAL-FASES.md` y la copia del ADN, sincronizados con este núcleo.

## Cambiar algo

- **Lo de un proyecto** (rol, tono, qué cuida): edita `agente/personalidad.md` en su repo y vuelve a armar.
- **El método, el manual o una plataforma**: edita aquí, sube `VERSION` y vuelve a armar cada proyecto. Dify y las plataformas sin archivos leen el SYSTEM en vivo desde GitHub: no hay que pegar nada.

## Versiones

`VERSION` = 1.2. El método v1.0 era el `AGENTS.md` v5.2-proyecto (2026-10-23) de los proyectos gf-2026-002/003/004, sin cambios de contenido. El manual es `MANUAL-FASES.md` v4.0.

- **v1.1 (2026-11-10):** lenguaje sencillo, resumen ejecutivo al inicio de cada respuesta y preguntas con número y letra (`1A, 2B, 3A`).
- **v1.2 (2026-11-10):** tipos de agente, catálogo, ficha con `tipo` y `fuentes`, método `propio` (orquestador y diseñador), `pruebas.md`, skills en el núcleo y plataforma sin archivos para lectura en vivo desde GitHub.

`ADN Grupos Focales.md` es el texto original subido; `modulos/adn.md` es la versión completa (misión, visión, propósito…) que usan los proyectos.
