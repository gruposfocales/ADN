# Módulo · Encuestas por WhatsApp (Kapso dentro de Dify)

**Decisión (2026-11-11):** va DENTRO de la app `GF · Agentes`, como la opción "Encuestas" de la lista.
La encuesta se construye conversando en Dify y, con "publicar", Dify la exporta a Kapso (borrador).
Activar y enviar a personas es un paso aparte, siempre con "sí" explícito.

```
GF · Agentes ─ opción "Encuestas" ─> LLM arma la encuesta con el usuario
     └─ "publicar" → LLM produce JSON de Kapso → HTTP POST /platform/v1/workflows
                     (X-API-Key = variable de entorno KAPSO_API_KEY, secreta)
```

Igual que los parches a GitHub: un nodo "¿Trae 📤 Publicar?" decide y un nodo HTTP envía.
`prompt.md` trae la receta del grafo. La herramienta OpenAPI de abajo sirve si luego se quiere
un agente con más acciones (enviar, leer respuestas).

## Cómo funciona (v1)

1. En GF · Agentes eliges **📋 Encuestas WhatsApp → Kapso**.
2. El módulo lee en vivo `SYSTEM.md` (este folder) y el `INSTRUMENTOS.md` de cada proyecto.
3. Pides un instrumento ("filtro de Vejez"): te muestra cada mensaje tal como llega por WhatsApp,
   con una auditoría corta.
4. Correcciones → `📥 Parche` al `INSTRUMENTOS.md` (GitHub manda). `ok` → `📤 Kapso` + JSON.
5. El nodo "¿Trae 📤 Kapso?" saca el JSON y lo manda con POST a `api.kapso.ai/platform/v1/workflows`
   (clave en la variable de entorno secreta `KAPSO_API_KEY`). Queda en **borrador** en Kapso.
6. Activar y enviar: aparte, con la plantilla `invitacion_encuesta` (id Meta 1605684120779922,
   pedida el 2026-11-11, MARKETING, en revisión).

Límites v1: grafo lineal; los saltos quedan escritos en el nombre de cada nodo y se montan a mano en
Kapso. El JSON lo arma el modelo: si Kapso responde 422, se ve el error en el chat.

Generado por `herramientas/dify_chatflow.py` (función `rama_encuestas`).

## Herramienta OpenAPI (para después)

`kapso-encuestas.openapi.yaml` sirve si luego se quiere un agente con más acciones:

| Puede hacer | Herramienta |
|---|---|
| Ver encuestas | `listarEncuestas`, `verEncuesta` |
| Crear y cambiar encuestas | `crearEncuesta`, `actualizarEncuesta` |
| Enviar a un número | `enviarEncuesta` |
| Ver y resumir respuestas | `listarEnvios`, `verRespuestas` |

Sin nodos de código: funciona aunque el sandbox de Dify esté caído.

## Montaje (una vez)

1. Kapso → API keys: crea una clave solo para Dify. No la pegues en ningún chat.
2. Dify → GF · Agentes → Variables de entorno: agrega `KAPSO_API_KEY` (tipo secreto) con esa clave.
3. Al subir el chatflow a una app que ya tiene secretos, quita `environment_variable_patch`.

## Riesgos
- Cada envío cuesta (tarifa de Meta). Límite actual del número: 250 personas nuevas al día.
- La clave de Kapso da escritura sobre todo el proyecto.
- Datos sensibles: aplica la `POLITICA-DATOS.md` del proyecto antes de salir a campo.
