<!-- módulo: plataforma sin-archivos · núcleo GF v1.2 -->

---

## Plataforma: sin archivos (Dify, ChatGPT, otros)

Úsalo cuando no puedes leer el disco ni hacer commit.

- Los archivos del repo te llegan después de estas instrucciones, leídos en vivo de GitHub, cada uno con su nombre (`=== ARCHIVO ===`). Esa es la fuente de verdad. Si un archivo no te llega o viene vacío, dilo: "No lo encuentro en los documentos del proyecto". No lo reconstruyas de memoria.
- Si el contexto es parcial, no cuentes el avance de memoria: usa el valor del encabezado de `DASHBOARD.md` y di que es el registrado.
- No puedes editar ni correr scripts. Si tu método guarda cambios, después de cada `ok` entrega un bloque que empiece exactamente con **📥 Parche**: qué líneas cambian en cada archivo y el commit sugerido. La plataforma lo deja en un issue de GitHub; nunca escribas en `main`.
- Si tu método es solo de lectura (por ejemplo, el orquestador), no entregues parches: informa y di qué comando correr en el repo.
