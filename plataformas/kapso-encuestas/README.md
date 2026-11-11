# Módulo · Encuestas por WhatsApp (Kapso dentro de Dify)

El cliente opera todo desde Dify; Kapso hace el WhatsApp por debajo y el cliente nunca entra a Kapso.

```
Cliente ──chat──> Dify "GF · Encuestas" (agente DeepSeek)
                     │  herramienta personalizada "Kapso Encuestas" (X-API-Key)
                     ▼
                  Kapso Platform API ──> WhatsApp +57 313 252 7143
```

| Puede hacer | Herramienta |
|---|---|
| Ver encuestas | `listarEncuestas`, `verEncuesta` |
| Crear y cambiar encuestas | `crearEncuesta`, `actualizarEncuesta` |
| Enviar a un número | `enviarEncuesta` |
| Ver y resumir respuestas | `listarEnvios`, `verRespuestas` |

Sin nodos de código: funciona aunque el sandbox de Dify esté caído.

## Montaje (una vez)

1. **Plantilla en Meta.** Una plantilla de invitación aprobada (WhatsApp no deja escribir primero
   sin plantilla). Su id va en `prompt.md` en lugar de `{{TEMPLATE_ID}}`.
2. **Clave de Kapso.** En Kapso → API keys, crea una clave solo para Dify. No la pegues en ningún chat.
3. **Herramienta en Dify.** Herramientas → Personalizada → Crear. Pega `kapso-encuestas.openapi.yaml`.
   Autorización: *API Key*, encabezado `X-API-Key`, valor = la clave del paso 2.
4. **App.** Crear app → Agente, nombre `GF · Encuestas`, modelo DeepSeek. Pega `prompt.md` (ya con el
   id de plantilla) como instrucciones y agrega las 7 herramientas de "Kapso Encuestas".
5. **Prueba.** Crea una encuesta de 3 preguntas, actívala y envíala solo a tu número. Revisa las
   respuestas con "resúmeme las respuestas".
6. **Acceso del cliente.** Publica y comparte con contraseña o control de acceso. No dejes el chat
   público abierto: ahí se ven datos de personas.

## Riesgos
- Cada envío cuesta (tarifa de Meta por conversación). Límite actual del número: 250 personas nuevas al día.
- La clave de Kapso da escritura sobre todo el proyecto. Si Kapso permite limitarla, limítala.
- Datos sensibles: aplica la `POLITICA-DATOS.md` del proyecto antes de salir a campo.
