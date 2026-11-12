# Hermes · un perfil por repo

Receta para Hermes Agent (`nousresearch/hermes-agent:v0.22.7`) en el servicio **hermes2**,
con un perfil por cada repo de agente (el MCP de Dify existente no se toca). Sin `-p` responde el bibliotecario.

## Cómo funciona
- `perfiles.txt`: qué perfil va con qué repo. Para un cliente, deja solo su línea (y `default`).
- `perfiles.sh`: clona/actualiza los repos en `/opt/data/` (donde hermes2 ya los tiene) y enlaza el `SOUL.md` de cada
  perfil al `AGENTS.md` de su repo. No hay copias: un `git pull` actualiza a todos.
- Hermes lee `SOUL.md` solo desde el home del perfil (por eso el enlace va ahí).

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
- Cambia una línea del `AGENTS.md` de Vejez en GitHub, corre `perfiles.sh`, y el perfil la refleja.

## Reglas
- Hermes no escribe en `main`: los cambios van como parche en un issue.
- Nunca pongas tokens ni URLs privadas en este repo ni en el chat.
