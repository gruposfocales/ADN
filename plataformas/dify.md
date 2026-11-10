# Receta · Dify

Cómo poner los agentes de GruposFocales en Dify. Es solo el "enchufe": el agente vive en su repo de GitHub y aquí no se escribe nada a mano.

## Cómo es

- **Una sola app** de tipo chatflow, llamada `GF · Agentes`.
- Al empezar la conversación, eliges el agente de una lista. Para cambiar de agente, abre una conversación nueva.
- En cada turno, la rama del agente lee en vivo de GitHub su `agente/SYSTEM-sin-archivos.md` y los archivos de `fuentes` (de su `agente/agente.txt`), y se los pasa al modelo (DeepSeek).
- Si la respuesta trae `📥 Parche` y la ficha tiene `issue_parches: N`, el parche se publica como comentario en ese issue. Nunca va a `main`. Sin `issue_parches`, el parche queda en el chat y tú lo copias.

## Las 4 piezas

| Pieza | En Dify |
|---|---|
| Instrucciones | Nodo HTTP que lee `agente/SYSTEM-sin-archivos.md` (va como primer mensaje de sistema) |
| Archivos | Un nodo HTTP por cada archivo de `fuentes`, con `Accept: application/vnd.github.raw` |
| Guardado | Nodo "¿Trae parche?" → herramienta GitHub `github_issue_comment` |
| Memoria | Ventana de 30 mensajes en el nodo del modelo |

## Armar o actualizar el chatflow

1. Si agregas un agente o cambias sus `fuentes`, actualiza `agentes.txt` o su `agente/agente.txt`.
2. Corre `python3 herramientas/dify_chatflow.py`. Escribe `plataformas/dify/chatflow.json`.
3. Súbelo al borrador de la app (`POST /console/api/apps/<id>/workflows/draft`, con el `hash` actual). **Al actualizar una app que ya tiene el token, quita `environment_variable_patch` del JSON**, o el token se borra.
4. Prueba cada agente en el borrador con `agente/pruebas.md`. Publica solo después de las pruebas.

Cambiar el texto de un agente (personalidad, método, fuentes ya existentes) **no** pide volver a subir nada: Dify lee GitHub en cada turno.

## Lo que pones a mano (una vez)

1. **Token de GitHub** en la variable de entorno `GITHUB_TOKEN` de la app (tipo secreto). Debe ser *fine-grained*, con `Contents: read` en todos los repos de `agentes.txt` y en `adn`. No lo pegues en ningún chat.
2. **Credencial del plugin GitHub** (para los parches): `Issues: write` en los repos con `issue_parches`.
3. **Modelo:** el proveedor DeepSeek con su clave.
4. **Acceso:** la app nace con el chat público apagado. Si lo enciendes, recuerda que cualquiera con el enlace ve los datos del proyecto.

## Límites conocidos

- Dify no da la fecha al modelo: el agente escribe `[fecha PENDIENTE]` si no se la dices.
- Los nodos de código y plantilla no se usan (el sandbox puede estar caído).
- Cada turno manda todos los archivos al modelo. En Vejez son unas 37 mil palabras: cuida el costo.
