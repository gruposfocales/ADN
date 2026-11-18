# Hermes · un perfil por repo

Receta para Hermes Agent (`nousresearch/hermes-agent:v0.22.7`) en el servicio **hermes2**,
con un perfil por cada repo de agente (el MCP de Dify existente no se toca). Sin `-p` responde gf-inicio (pantalla de inicio y menú).

## Cómo funciona
- `ADN/agentes.txt` (la lista única de repos): la columna `perfil` dice qué perfil va con qué repo. Para un cliente, deja solo sus líneas (y la de `default`). Perfil `-` = el repo se trae pero no lleva perfil ni atajo (ej. gf-bibliotecario, que es solo datos); si antes tenía atajo, `perfiles.sh` lo quita.
- `perfiles.sh`: clona/actualiza los repos en `/opt/data/` (donde hermes2 ya los tiene) y deja el `SOUL.md` neutro
  en cada perfil. No hay copias del AGENTS.md: un `git pull` actualiza a todos.
- **AGENTS.md es la única fuente.** El `SOUL.md` de cada perfil (el espacio de identidad de Hermes, que va primero)
  es una sola línea neutra que no habla del proyecto: "tus instrucciones están en el AGENTS.md de la carpeta".
  Al abrir con `--in <repo>` (los atajos lo hacen), Hermes carga ese `AGENTS.md` (o `CLAUDE.md`) como contexto del
  proyecto, una sola vez. No se deja vacío porque Hermes pondría su identidad por defecto, en inglés.
  Excepción: `adn` no tiene AGENTS.md ni CLAUDE.md, así que su SOUL sigue siendo un enlace a su `README.md`.
- **Telegram arranca limpio y carga a pedido.** El bot (perfil default) trabaja en `/opt/data`, que no tiene
  AGENTS.md: al abrir solo está la línea neutra del SOUL. `perfiles.sh` crea skills en `/opt/data/skills/gruposfocales/`,
  que Hermes muestra como comandos:
  `/menu` (menú de gf-inicio), `/pulso` (solo el pulso), `/inicio` y `/<proyecto>` (`/vejez`, `/comunicacion`…:
  el agente lee el AGENTS.md de ese repo y trabaja en su carpeta). Para cambiar de proyecto: `/new` y el otro comando.
  La memoria del perfil va apagada para que no se mezclen proyectos (lo importante vive en los repos).
  Una vez en el VPS: `hermes config set terminal.cwd /opt/data`, `hermes config set memory.memory_enabled false`
  y Restart del servicio en Dokploy. En la terminal no cambia nada: los atajos siguen abriendo con `--in`.
  Límite: lo que carga un comando vive en la conversación, no en las reglas fijas; en sesiones largas usa `/new` seguido.
- Comprobar: dentro de Hermes, `/context` debe mostrar `SOUL.md ✓` (pocos tokens) y `AGENTS.md ✓` (o `CLAUDE.md ✓`).
- `perfiles.sh` también crea un **atajo de una palabra** por perfil. Cada atajo abre Hermes dentro de la
  carpeta del repo y con una **sesión nueva** (sin historial anterior):

  | Atajo | Equivale a |
  |---|---|
  | `inicio` | `hermes --in /opt/data/gf-inicio` |
  | `vejez` | `hermes -p vejez --in /opt/data/inv-001-vejez` |
  | `comunicacion` | `hermes -p comunicacion --in /opt/data/inv-002-comunicacion` |
  | `noticias` | `hermes -p noticias --in /opt/data/age-001-en-efecto-noticias` |
  | `bartolinos` | `hermes -p bartolinos --in /opt/data/com-001-bartolinos` |
  | `adn`, `disenador` | igual, con su perfil y su repo |

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
   (Clona ADN: `perfiles.sh` lee `../../agentes.txt`.)

## Actualizar
`sh perfiles.sh` otra vez: hace `pull --ff-only` y rehace los enlaces.

## Validar
- `inicio` → muestra solo la lista de atajos de gf-inicio; `pulso` da el Pulso del Día.
- `hermes -p vejez` → "estado" responde con el formato de Vejez.
- `vejez` → abre en `/opt/data/inv-001-vejez` sin el historial de la sesión anterior.
- Cambia una línea del `AGENTS.md` de Vejez en GitHub, corre `perfiles.sh`, y el perfil la refleja.

## Feynman (investigación por encargo)
`perfiles.sh` crea el comando `/feynman` y el script `feynman-tarea`. Hermes encarga la investigación al
**puente Feynman** (otro servicio de Dokploy, ver `../feynman-puente/README.md`) por HTTPS y luego pregunta el estado.
El informe queda en la rama `feynman/resultados` de gf-bibliotecario.
- Token: el mismo `PUENTE_TOKEN` del puente, guardado en el contenedor de Hermes en `/opt/data/.feynman_token`
  (o como variable `FEYNMAN_TOKEN`). Nunca en el repo.
- Probar en la terminal: `feynman-tarea nueva pregunta "qué es el ahorro voluntario"` y luego `feynman-tarea estado <id>`.

## Reglas
- Hermes no escribe en `main`: los cambios van como parche en un issue.
- Nunca pongas tokens ni URLs privadas en este repo ni en el chat.

## Guardar cambios (rama + PR)
Después de un `ok`, Hermes (o tú) corre:
`sh /opt/data/ADN/plataformas/hermes/guardar.sh /opt/data/<repo> "Fase N · lote X · resumen"`
Crea una rama `hermes/<fecha-hora>`, hace commit, la sube y abre un PR contra `main`. Nunca escribe en `main`.
Requisitos: token con **Contents: Read and write** y **Pull requests: Read and write**, y `main` protegida
(Settings → Rules → Rulesets → "Require a pull request before merging") en cada repo.
