# Receta · Usar un agente en Claude o ChatGPT (proyecto o chat)

La tercera forma de usar un agente, sin servidor: el repo del agente se lleva a un **Proyecto** de Claude o de ChatGPT, o a un chat suelto. No hay que instalar nada. El agente responde igual que en Dify. Como no puede escribir en GitHub, cada "ok" sale como un **📥 Parche** en el chat.

## Qué archivos se usan

- **Instrucciones:** `agente/SYSTEM-sin-archivos.md` del repo del agente, completo. Su aviso de arriba dice la versión.
- **Archivos:** los de la línea `fuentes:` de `agente/agente.txt`. En Vejez son `index.md`, `DASHBOARD.md`, `MANUAL-FASES.md`, `ADN.md`, `POLITICA-DATOS.md`, `INSTRUMENTOS.md`, `BITACORA.md` y `evidencia/mapa-conocimiento.md`.

## A. Proyecto de Claude (claude.ai) · recomendado

1. Crea un proyecto con el nombre del agente (por ejemplo, "Vejez · INV-001").
2. En **Instrucciones del proyecto**, pega `agente/SYSTEM-sin-archivos.md`.
3. En **Conocimiento del proyecto**, agrega los archivos de `fuentes:`. Lo mejor es usar **Agregar desde GitHub**: eliges el repo y marcas esos archivos. Así puedes sincronizarlos cuando cambien, sin volver a subirlos.
4. Abre un chat dentro del proyecto y escribe `abrir`.

## B. Proyecto de ChatGPT (OpenAI)

1. Crea un proyecto con el nombre del agente.
2. En **Instrucciones**, pega `agente/SYSTEM-sin-archivos.md`. Si no cabe, pega allí solo la sección 0 y el §1, y sube el archivo completo como archivo del proyecto con la indicación "sigue `SYSTEM-sin-archivos.md`".
3. En **Archivos**, sube los archivos de `fuentes:`. Descárgalos de GitHub: abre cada archivo y usa **Download raw file**.
4. Abre un chat dentro del proyecto y escribe `abrir`.

Un GPT personalizado se arma igual: las instrucciones van en *Instructions* y los archivos en *Knowledge*.

## C. Un chat suelto (Claude, ChatGPT u otro)

Para una consulta rápida. En el primer mensaje, pega el contenido de `SYSTEM-sin-archivos.md` y adjunta los archivos de `fuentes:`. Después escribe `abrir`. Al cerrar el chat se pierde el contexto, pero no se pierde nada aprobado, porque lo aprobado vive en el repo.

## Guardar lo aprobado

- Tras cada "ok", el agente entrega un **📥 Parche**. Pégalo en el issue de parches del repo (el número está en `issue_parches:` de `agente/agente.txt`), o pídele a Claude Code o a Hermes que lo aplique.
- Después de aplicar el parche en GitHub, actualiza los archivos del proyecto: en Claude, usa **Sincronizar**; en ChatGPT, vuelve a subir los archivos que cambiaron.
- Trabaja cada lote en una sola plataforma a la vez. Antes de cambiar de plataforma, confirma que el último parche ya está en `main`.

## Cuándo usar cada forma

| Forma | Ventaja | Límite |
|---|---|---|
| Proyecto de Claude | Sin servidor; sincroniza desde GitHub | Los parches se aplican a mano |
| Proyecto de ChatGPT | Sin servidor; el cliente ya lo tiene | Hay que volver a subir archivos tras cada cambio |
| Chat suelto | Inmediato | No guarda contexto entre chats |
| Dify (`dify.md`) | Lee GitHub en vivo y deja el parche en un issue | Requiere VPS |
| Hermes (`hermes/`) | Lee el repo y puede usar git | Requiere VPS |
