---
name: kapso-encuestas-whatsapp
description: "Sugerencias técnicas para diseñar encuestas y entrevistas por WhatsApp con agentes y workflows de Kapso: nodos, ramificación, audio, almacenamiento y configuración sencilla."
familia: 20 · Campo
version: 1.0
entra: instrumentos aprobados (filtro, bot, encuesta)
sale: flujos y nodos de Kapso para WhatsApp
siguiente: 30-escucha-social
estado: estable
---

# Kapso · Encuestas avanzadas por WhatsApp (configuración sencilla)

Usa esta skill cuando el usuario quiera convertir un cuestionario, filtro, entrevista o módulo de investigación en un sistema que corra en WhatsApp con Kapso, o pida sugerencias técnicas sobre qué puede hacer Kapso.

Idioma: español, lenguaje claro. Cada respuesta termina con un bloque **💬 En pocas palabras** (máx. 3 líneas, sin jerga).

## 1. Reglas de honestidad técnica

- Marca cada capacidad como **[DOC]** (confirmada en docs.kapso.ai), **[INFERIDO]** (deducido, no confirmado) o **[PROBAR]** (hay que verificar en el entorno o con soporte de Kapso).
- No inventes nombres de campos, límites ni precios. Si no está en el mapa de abajo, consulta https://docs.kapso.ai/llms.txt (índice completo) con WebFetch antes de afirmarlo.
- Nunca pidas ni escribas la API key en el chat; se usa como variable de entorno `KAPSO_API_KEY`.
- Las decisiones metodológicas (qué preguntar, a quién, consentimiento) son del investigador; tú sugieres la implementación.

## 2. Mapa de capacidades verificado (docs, oct-2026)

**Acceso**
- CLI: `npm install -g @kapso/cli` → `kapso login` → `kapso setup`. Gestiona números, mensajes y webhooks; aún no gestiona Functions. [DOC]
- MCP remoto: `https://api.kapso.ai/mcp` con bearer `KAPSO_API_KEY`. Herramientas: workflows (crear, actualizar, publicar, triggers), workflow_executions (iniciar, reanudar), functions, WhatsApp Flows, mensajes, conversaciones, contactos, plantillas, números, webhooks, broadcasts. [DOC]
- SDK TypeScript y API REST. [DOC]

**Workflows** (grafo de nodos; un solo Start) [DOC]
| Nodo | Uso en encuestas |
|---|---|
| Start | Disparo por mensaje entrante, por API o por evento. |
| Send text / template / interactive | Preguntas; interactive = botones o listas; template = primer contacto fuera de la ventana de 24 h. |
| Wait for response | Guarda la respuesta como texto en `{{last_user_input}}` o en `save_response_to`. Timeout de 10 s a 7 días; `{{system.last_resume.reason}}` = `timeout` o `user_input`. |
| Decide | Modo `ai` (interpreta intención con descripciones) o `function` (devuelve `next_edge`). Para reglas exactas (edad, sexo, cortes) usa **function**. Las etiquetas deben coincidir con las aristas. |
| Function | JavaScript en Cloudflare Workers; lee el contexto y devuelve `vars`. |
| Set variable | Guarda valores derivados (cohorte, ruta, segmento). |
| Call workflow | Encadena módulos (filtro → bot → módulo adicional). |
| Agent | Conversación multiturno con herramientas; sale con `complete_task`. Ideal para entrevista semiestructurada. |
| Webhook | Envía datos a sistemas externos. |
| Handoff | Pasa la conversación a una persona. |
| Emit event | Dispara eventos de proyecto (p. ej., `encuesta_completada`). |

**Variables** [DOC]: `vars` (por ejecución), `context.phone_number`, `context.contact.*`, `system.*`, `${ENV:NOMBRE}` (proyecto o workflow). Las `vars` NO persisten entre ejecuciones: lo que deba durar se guarda en KV o D1.

**Functions** [DOC]: `handler(request, env)`; `fetch()`; secretos en `env.NOMBRE`; **KV** por proyecto (con TTL) y **D1** (`env.DB`, SQL). D1 es la base natural de respuestas.

**Audio entrante** [DOC]: el webhook `whatsapp.message.received` con `type: audio` trae `media_url` y, en el ejemplo, `transcript.text`. [PROBAR]: si la transcripción llega siempre, si llega al Wait (que guarda solo texto) y cuánto dura disponible la URL del medio.

**WhatsApp Flows** [DOC]: formularios nativos de varias pantallas; respuestas por webhook o guardadas en Kapso. Requiere portafolio de Meta Business verificado.

**Broadcasts** [DOC]: envíos masivos con plantillas, carga por CSV y programación; opt-out de marketing.

## 3. Patrones recomendados (de lo simple a lo avanzado)

1. **Una pregunta = Send + Wait (+ guardar variable).** Botones si hay 3 opciones o menos; lista si hay más [INFERIDO de límites de WhatsApp: verificar].
2. **Validación barata:** Decide en modo function tras cada respuesta cerrada; si no es válida, una repregunta y después seguir (no bloquear).
3. **Ramificación por reglas:** una sola Function `enrutar` que lee `vars` (edad, sexo, cotización) y devuelve `next_edge`. Las reglas viven en una tabla de configuración (KV o D1), no dentro del código, para que el investigador cambie umbrales sin programar.
4. **Módulos encadenados:** cada instrumento es un workflow propio (filtro, bot, módulo pensionados, díada) unido con Call workflow. Así se prueban y versionan por separado.
5. **Abiertas y audio:** Wait guarda el texto; un webhook o Function guarda `media_url`, descarga el audio a almacenamiento propio y registra `transcript`. Siempre guardar texto, transcripción y referencia al audio.
6. **Entrevista profunda:** nodo Agent con guion por bloques, herramienta `guardar_respuesta` (Function → D1) y `complete_task` al cubrir los bloques. El agente no inventa preguntas fuera del guion.
7. **Abandono:** Wait con timeout (p. ej. 24 h) → recordatorio con plantilla → segundo timeout → cierre y marca `incompleto`.
8. **Persistencia:** tabla `respuestas(id_participante, instrumento, item, valor_texto, valor_codigo, media_url, transcripcion, ts, version_instrumento)`. Un participante = hash del teléfono, nunca el número en claro en los análisis.
9. **Formularios largos y cerrados:** WhatsApp Flow en lugar de 10 mensajes, si la cuenta está verificada en Meta.
10. **Trazabilidad:** cada ítem lleva un código (F1, B3…) igual al de la matriz de trazabilidad del proyecto; Emit event al completar cada módulo.

## 4. Ética y privacidad (señalar siempre)

- Consentimiento como primer nodo; si dice No → fin sin guardar más datos.
- Comando de salida (p. ej., SALIR) revisado en cada Wait.
- Declarar que el asistente es automático.
- Audio = dato de voz: definir retención, acceso y borrado. [PROBAR] dónde se aloja y por cuánto tiempo.
- Menores o personas fuera de criterio: despedida y no persistir respuestas.

## 5. Cómo responder

Cuando el usuario traiga un ítem o un módulo:
1. **Mapeo:** tabla `Ítem | Nodo(s) Kapso | Variable | Validación | Rama`.
2. **Configuración mínima:** pasos concretos (canvas, CLI o MCP) para dejarlo funcionando.
3. **Mejora avanzada opcional:** máximo 2 ideas, con su coste de configuración.
4. **Por verificar:** lista de [PROBAR].
5. **💬 En pocas palabras.**

Si el usuario pide implementar y el MCP de Kapso está conectado, propone el cambio y pide confirmación antes de crear o publicar workflows, enviar mensajes o broadcasts.

## 6. Fuentes

- Índice: https://docs.kapso.ai/llms.txt
- Workflows: https://docs.kapso.ai/docs/workflows/introduction
- Nodos: https://docs.kapso.ai/docs/flows/step-types/ (wait-for-response-node, decide-node, agent-node, function-node, call-workflow-node)
- Variables: https://docs.kapso.ai/docs/flows/variables-and-context
- Functions: https://docs.kapso.ai/docs/functions/overview
- Webhooks de mensajes: https://docs.kapso.ai/docs/platform/webhooks/message-events
- WhatsApp Flows: https://docs.kapso.ai/docs/whatsapp/flows/overview
- MCP: https://docs.kapso.ai/docs/whatsapp/mcp