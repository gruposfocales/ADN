# Hermes · un perfil por repo

Receta para Hermes Agent (`nousresearch/hermes-agent:v0.22.7`) en el servicio **hermes2**,
con un perfil por cada repo de agente (el MCP de Dify existente no se toca). Sin `-p` responde el bibliotecario.

## Cómo funciona
- `perfiles.txt`: qué perfil va con qué repo. Para un cliente, deja solo su línea (y `default`).
- `perfiles.sh`: clona/actualiza los repos en `/opt/data/` (donde hermes2 ya los tiene) y enlaza el `SOUL.md` de cada
  perfil al `AGENTS.md` de su repo. No hay copias: un `git pull` actualiza a todos.
- Hermes lee `SOUL.md` solo desde el home del perfil (por eso el enlace va ahí).
- **Sin duplicado:** al abrir con `--in <repo>`, Hermes también lee el `AGENTS.md` (o `CLAUDE.md`) de esa carpeta
  como contexto del proyecto, y no lo compara con el `SOUL.md`: el mismo texto entraba dos veces (~4k tokens de más).
  Por eso `perfiles.sh` deja en cada repo un `.hermes.md` de una línea, que Hermes prefiere sobre `AGENTS.md`.
  Está en `.git/info/exclude`: no se sube ni sale como cambio sin commit. Si un repo trae su propio `.hermes.md`,
  no se toca. Telegram (perfil default, sin `--in`) no cambia.
  Comprobar: dentro de Hermes, `/context` debe mostrar `SOUL.md ✓`, `.hermes.md ✓` y `AGENTS.md ○ (not loaded)`.
- `perfiles.sh` también crea un **atajo de una palabra** por perfil. Cada atajo abre Hermes dentro de la
  carpeta del repo y con una **sesión nueva** (sin historial anterior):

  | Atajo | Equivale a |
  |---|---|
  | `inicio` | `hermes --in /opt/data/gf-inicio` |
  | `vejez` | `hermes -p vejez --in /opt/data/inv-001-vejez` |
  | `comunicacion` | `hermes -p comunicacion --in /opt/data/inv-002-comunicacion` |
  | `noticias` | `hermes -p noticias --in /opt/data/age-001-en-efecto-noticias` |
  | `bartolinos` | `hermes -p bartolinos --in /opt/data/com-001-bartolinos` |
  | `bibliotecario`, `adn`, `disenador` | igual, con su perfil y su repo |

  Dos atajos más **no abren Hermes**, así que no gastan contexto ni tokens:
  `pulso` muestra el Pulso del Día de gf-inicio, y `atajos` muestra la lista de todos los atajos.

  Se guardan en `/opt/data/bin` (el volumen) y se enlazan en `/usr/local/bin` y `~/.local/bin`.
  Aceptan más opciones de Hermes: `vejez -c` retoma la última sesión de Vejez en vez de abrir una nueva.
  Después de un redeploy, corre `perfiles.sh` otra vez para volver a enlazarlos (o usa `/opt/data/bin/vejez`).

## Instalar (Dokploy)
1. Servicio Compose con este `docker-compose.yml`.
2. Environment: `GITHUB_TOKEN` (fine-grained, Contents: read, solo los repos de la lista)
   y `DEEPSEEK_API_KEY`. Cada variable nueva debe estar también en la lista `environment:`.
3. Deploy. Luego, en la terminal del contenedor:
   `hermes model` (elige DeepSeek) y `sh /ruta/a/perfiles.sh`.
   (Copia `perfiles.sh` y `perfiles.txt` al volumen o clona ADN.)

## Actualizar
`sh perfiles.sh` otra vez: hace `pull --ff-only` y rehace los enlaces.

## Validar
- `hermes` → "estado" responde el bibliotecario.
- `hermes -p vejez` → "estado" responde con el formato de Vejez.
- `vejez` → abre en `/opt/data/inv-001-vejez` sin el historial de la sesión anterior.
- Cambia una línea del `AGENTS.md` de Vejez en GitHub, corre `perfiles.sh`, y el perfil la refleja.

## Reglas
- Hermes no escribe en `main`: los cambios van como parche en un issue.
- Nunca pongas tokens ni URLs privadas en este repo ni en el chat.

## Guardar cambios (rama + PR)
Después de un `ok`, Hermes (o tú) corre:
`sh /opt/data/ADN/plataformas/hermes/guardar.sh /opt/data/<repo> "Fase N · lote X · resumen"`
Crea una rama `hermes/<fecha-hora>`, hace commit, la sube y abre un PR contra `main`. Nunca escribe en `main`.
Requisitos: token con **Contents: Read and write** y **Pull requests: Read and write**, y `main` protegida
(Settings → Rules → Rulesets → "Require a pull request before merging") en cada repo.
