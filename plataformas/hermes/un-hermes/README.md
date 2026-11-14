# Un solo Hermes que carga el agente desde GitHub

Reemplaza los perfiles (`perfiles.sh`). Un solo Hermes; en el chat (web o Telegram) escribes
`agentes` para ver el menú y `agente vejez` (o `agente 2`) para cambiar. Hermes lee el `AGENTS.md`
de ese repo y lo sigue.

## Qué vive en GitHub
- `SOUL.md`: el menú y las reglas de cambio de agente.
- `arranque.sh`: en cada reinicio trae los repos (`pull --ff-only`) y enlaza el `SOUL.md`.
- `config.yaml` (paso 2, opcional): si lo agregas aquí, se copia al servidor en cada arranque.
  Sin claves: usa `${DEEPSEEK_API_KEY}`, `${DIFY_MCP_URL}`. Deja respaldo en `config.yaml.antes`.

## Instalar (una vez, en Dokploy → hermes2 → Compose)
Cambia la línea `command:` por:
```yaml
    command: sh -c "sh /opt/data/ADN/plataformas/hermes/un-hermes/arranque.sh; exec hermes gateway run"
```
Guarda y Deploy. Desde ahí no hace falta volver al servidor.

## Uso diario
- Editar un agente: cambia su `AGENTS.md` en GitHub; en el chat escribe `actualizar`.
- Editar el menú o las reglas: cambia `SOUL.md` aquí; `actualizar` (o reinicia en Dokploy).

## Validar
1. Tras el deploy, en el chat: `agentes` → sale la tabla de 7.
2. `agente vejez` y luego `estado` → responde con el formato de Vejez.
3. Cambia una línea del SOUL en GitHub, `actualizar`, `cual` → se nota el cambio.

## Límite
Hermes mezcla el SOUL fijo con el agente leído en el chat: funciona bien, pero en conversaciones muy
largas conviene empezar una nueva (`/new`) y volver a pedir el agente.
