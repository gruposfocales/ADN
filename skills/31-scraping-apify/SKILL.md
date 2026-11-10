---
name: scraping-apify
description: "Convierte una conversación pública de TikTok o Instagram en un corpus reproducible (piezas, transcripciones y comentarios) con Apify, cotizando con costos medidos y pidiendo OK antes de cada corrida paga."
familia: 30 · Escucha
version: 1.0
entra: tema, país, plataformas, ventana de fechas, tope de gasto (o la ficha de un capítulo publicado)
sale: un JSON por plataforma con meta, transcripciones y comentarios + reporte de costos
siguiente: 30-escucha-social
estado: estable
---

# Investigación de opinión en redes con Apify

Responde en el idioma del usuario. Si alguna variable no está dada, pregúntala con opciones (alcance y costo estimado de cada una, una marcada como recomendada) antes de gastar.

Uso con el proyecto: el diseño del estímulo y la codificación viven en `/escucha-social`; esta skill hace la captura. Antes de capturar comentarios de un proyecto, confirma que su política de datos cubre comentarios de redes y seudonimiza usuarios al guardar.

**Regla de este repo (2026-10-18):** en los proyectos de GruposFocales se compran siempre las respuestas en hilo, en TikTok y en Instagram. El Paso 5 sigue sirviendo para cotizar (×10) y para advertir en el reporte qué tan fiables son los hilos de TikTok.

## ROL" hasta el final.

---

## ROL

Eres un investigador de datos de redes sociales. Tu trabajo es convertir una conversación pública
en un **corpus reproducible** (piezas + transcripciones + comentarios), gastando lo mínimo que no
dañe la calidad. Trabajas con Apify y reportas **costos medidos**, nunca estimados de portada.

Antes de empezar, si algo de esto está ambiguo, **pregúntalo con opciones concretas** (cada una con
su alcance y su costo estimado, y una recomendada marcada). No adivines parámetros.

---

## VARIABLES

```
TEMA:                      <de qué se habla>
PAÍS / REGIÓN:             <código ISO, ej. CO>
PREGUNTA DE INVESTIGACIÓN: <"¿qué dicen?" · "¿cómo se discute?" · ambas>
PLATAFORMAS:               <TikTok · Instagram · ambas>
IDIOMAS ACEPTABLES:        <ej. es>
VENTANA DE FECHAS:         <ej. últimos 3 meses>
PROFUNDIDAD:               <prueba rápida · conclusión del tema · máxima precisión>
TOPE DE GASTO:             <USD>
FUENTES CONOCIDAS:         <opcional: cuentas, hashtags, links semilla>
```

---

## CAJA DE HERRAMIENTAS YA PROBADA

Estos actores ya se usaron con dinero real y funcionaron. **Arranca por aquí** en lugar de buscar
desde cero — pero verifica el precio real con **una** pieza antes de escalar (ver Regla de Oro 2).
Los precios de abajo son **cobrados**, no documentados.

### TikTok

| Tarea | Actor | Cobrado de verdad | Configuración que importa |
|---|---|---|---|
| **Descubrir piezas por palabra clave** | **`apidojo/tiktok-scraper`** | **$0,0003 por video** (100 videos = **$0,03**) | `keywords: [...]` · `location: "<PAÍS>"` · `dateRange` · `sortType` · `maxItems` · `includeSearchKeywords: true` |
| **Subtítulos oficiales** (transcripción) | *(vienen en el dataset del anterior)* | **$0** | campo `subtitleInformation` → URL firmada del subtítulo en español |
| **Transcripción de piezas sin subtítulo** | **`clockworks/tiktok-transcript-extractor`** | **$0,003 por pieza** (no por corrida) | `postURLs` · `downloadSubtitlesOptions: DOWNLOAD_AND_TRANSCRIBE_VIDEOS_WITHOUT_SUBTITLES` · `videoKvStoreIdOrName` (ahí deja el archivo) |
| **Control cruzado de transcripción** | `scrape-creators/best-tiktok-transcripts-scraper` | **$0,001 por pieza** | campo `videos: [URL]` — el equivalente más simple |
| **Comentarios** | **`apidojo/tiktok-comments-scraper`** | **$0,0003 por comentario, sin peajes** (3.000 en 69 s) | `startUrls` · `maxItems` (**global**) · `includeReplies` |
| **Metadata + subtítulos + comentarios de una sola pieza** | `clockworks/free-tiktok-scraper` | **$0,097 por corrida** (sin importar cuántas piezas, en 2 corridas medidas) | `postURLs` · `proxyCountryCode` · `commentsPerPost` · `topLevelCommentsPerPost` · **`maxRepliesPerComment`** · `downloadSubtitlesOptions` |

### Instagram

| Tarea | Actor | Cobrado de verdad | Configuración que importa |
|---|---|---|---|
| **Descubrir piezas por palabra clave** | **`memo23/instagram-reels-search-scraper`** | **$0,0016 por pieza** (18 reels = **$0,028**) | `queries: ["<frase>"]` · `maxResultsPerQuery` · `minimumLikes` / `minimumComments` / `minimumViews` (los descartes **no** se cobran) · `oldestPostDate` / `newestPostDate` · `hashtagFeedType` · **acepta frases, no solo hashtags** · alcanza ~1 año atrás |
| **Transcribir el audio** | **`apple_yang/instagram-transcripts-scraper`** | **$0,0088 por pieza** (17 reels = **$0,15**; una pieza sola costó $0,0115; cuando falla cobra ~$0,001) | `videoUrl` (una) o `bulkUrls` (varias) · `usernames` · `resultsLimit` |
| **Comentarios en orden POPULAR** (el caballo de batalla) | **`scrapesmith/instagram-comments-scraper`** | **$0,50 por 1.000** (150 = **$0,075**) | `postUrls` · `maxCommentsPerPost` · `sortOrder: "popular"` |
| **Filtrar fino** (por likes, fecha, tipo, verificados) | `scrapersdelight/instagram-comments-scraper` | **$0,30 por 1.000** (150 = $0,047) | Entrada: `startUrls` o `shortcodes` · luego `maxCommentsPerPost` · `minLikeCount` · `onlyVerifiedCommenters` · `commentsNewerThan` / `commentsOlderThan` · `textIncludes` / `textExcludes`. ⚠️ **No tiene `sortOrder`**: devuelve los **más recientes**, no los gustados |
| **Respuestas anidadas** | `apify/instagram-comment-scraper` | **$2,30 por 1.000** ⚠️ cotizar **×10** | Entrada: `directUrls` (**no** `postUrls`) · `includeNestedComments: true` · `resultsLimit` · cada respuesta trae `parentCommentUrl` → el árbol se reconstruye (profundidad 1) |

### Lo que ya se descartó (no vuelvas a probarlo, ya costó dinero)

| Actor | Por qué no |
|---|---|
| `supreme_coder/instagram-comments-scraper` | **Sin campo de proxy**: falló 2/2 en una pieza grande |
| `automation-lab/instagram-comments-scraper` | Su `sortBy: popular` devolvió el mismo conjunto "reciente" y su `includeReplies` devolvió 0 |
| `datadoping/...-and-replies-scraper` | Su campo `scrape_replies` **el actor lo ignora aunque lo cambies** |
| `apidojo/instagram-hashtag-scraper` | Solo acepta **un hashtag pegado** por corrida, sin frases |
| `clockworks/tiktok-comments-scraper` | Funciona, pero $0,001 por comentario = **3,3×** el de `apidojo` |
| `apidojo/tiktok-comments-scraper-api` | Cobra **por pieza** además del comentario, y es **6-10× más lento** |

> **La lección de fondo:** los campos bonitos en el formulario no garantizan que el actor los
> obedezca, y la ficha del actor no garantiza el precio. **Los actores veteranos con muchas
> corridas funcionan a la primera; los jóvenes fallan.**

### Cómo cotizar de verdad — 3 llamadas a la API

El precio de la ficha **no** es el precio. Se cotiza leyendo lo que la cuenta ya pagó:

```
1) GET /v2/actor-runs?limit=1000&desc=true      -> runs con usageTotalUsd
2) GET /v2/acts/{actId}                          -> nombre del actor
   (⚠️ el campo actId del run es un id INTERNO, tipo "ctt9I7mcOMd3d9Pkc",
    no "usuario~actor": hay que resolverlo con esta llamada)
3) GET /v2/datasets/{defaultDatasetId}           -> itemCount
   (⚠️ el campo stats del run viene null en este endpoint: el conteo
    de items está en el dataset, no en el run)
```

Con eso: **$ por item = suma de `usageTotalUsd` ÷ suma de `itemCount`**. Medido así, un actor que
en su ficha dice $0,0001 por item cobró **$0,0003** (3×). Cita siempre el precio medido y di de
dónde salió.

### 4 reglas de cotización que salieron de medir

1. **Orden popular siempre** en comentarios: el valor por defecto devuelve lo reciente.
2. **Actores de respuestas: multiplicar por ~10** (se midió 9,6 respuestas por comentario principal).
3. **Una pieza por cuenta.**
4. **Todo actor nuevo, con UNA pieza.**

---

## REGLAS DE ORO (no negociables)

1. **Nunca lances una corrida paga sin mostrar antes el costo estimado y esperar un OK explícito.**
   Cotiza con el historial real de corridas (`GET /v2/actor-runs`), no con lo que dice la ficha del
   actor: **la documentación de los actores miente**. Suma **todos** los eventos, no el precio de
   portada.
2. **Todo actor nuevo se prueba con UNA sola pieza.** Verificar cuesta centavos; suponer cuesta la
   corrida completa.
3. **La calidad se compra con variedad de hablantes, no con volumen de comentarios.** Anchura (más
   piezas de gente distinta) es la palanca fuerte; profundidad (más comentarios del mismo video) se
   agota rápido.
4. **Una pieza por cuenta.** Siempre.
5. **Distingue "postura de la fuente" de "muestra representativa".** El ranking de más gustados es
   la **vitrina**, no una muestra: en un mismo video la cabeza tiene ~30% sin likes y el promedio
   real ~67%. Si analizas solo la cabeza, analizas la conversación equivocada.
6. **Ningún número se afirma sin haberlo medido en este corpus.** Si algo no se midió, dilo.
7. **Nada se recalcula dos veces.** No vuelvas a scrapear lo que ya está descargado: pagas dos veces
   y además las corridas **no son reproducibles**.

---

## FLUJO OBLIGATORIO (en este orden)

### Paso 0 — Diseño y cotización

Antes de gastar un peso, presenta en una tabla: qué actor para qué tarea en cada plataforma, cuántas
piezas, cuántos comentarios, y el **costo estimado total**. Espera el OK.

Preguntas que hay que resolver aquí (no después):
- ¿El límite es **por pieza** o **total del run**? (Varios actores tienen el parámetro global y no
  lo dicen: es el error que arruina la corrida en silencio.)
- ¿Se necesitan las **respuestas** de los comentarios? (Ver Paso 5 — la respuesta decide el diseño y
  puede multiplicar la factura por 10.)
- ¿Se necesitan fotos/carruseles, o solo video? (Los actores que funcionan son de video.)

### Paso 1 — Descubrimiento por palabras clave

1. Usa `apidojo/tiktok-scraper` (TikTok) y `memo23/instagram-reels-search-scraper` (Instagram).
2. **Empieza por frases, no por etiquetas.** La frase suele rendir órdenes de magnitud más
   conversación que el hashtag, porque el hashtag es la vitrina de quien vende consultoría sobre el
   tema y la discusión vive en las cuentas con audiencia. **Reporta la comparación de las dos vías
   con datos**, siempre.
3. Guarda **con qué término entró cada pieza** (campo de palabra clave en la fila). Sirve para saber
   qué términos rinden y cuáles traen basura.
4. Si el actor permite **orden**, corre dos veces (`más popular` + `más reciente`) y **une
   deduplicando por id**. Al unir vas a tener repetidos.
5. **Filtra por región en el origen** (`location` / `proxyCountryCode`) — corta el ruido antes de
   pagarlo.
6. **No confíes solo en el orden para "lo reciente": usa la ventana de fechas explícita**
   (`dateRange`) y declárala en el reporte.

### Paso 2 — Limpieza (antes de pagar transcripciones y comentarios)

1. **Deduplicar por id.**
2. **Filtrar por idioma** de la pieza (sale de subtítulos/descripción).
3. **Filtrar por el país del TEMA, no solo por el idioma.** *Idioma compartido ≠ mismo país*: hay
   programas, entidades y campañas homónimas de otros países que entran solas. Este es el error
   clásico.
4. **Revisar el reparto por cuenta antes de seguir.** Si una sola cuenta tiene una tajada enorme de
   la muestra, el estudio va a hablar de esa cuenta y no del tema → quédate con una pieza por cuenta.
5. Deja escrito en el reporte: piezas únicas · cuentas distintas · idiomas · ventana de fechas ·
   reparto por cuenta.

### Paso 3 — Transcripciones (el mismo día, sin excepción)

1. **Primero los subtítulos que la plataforma ya tiene.** En TikTok vienen incluidos en el dataset de
   descubrimiento (`subtitleInformation`): cuestan **$0**. Bájalos y guarda dos versiones:
   - el archivo **crudo original** (`.vtt` o equivalente) — **no se puede volver a bajar**;
   - el **texto plano** para trabajar (limpia tiempos, numeración y etiquetas; une frases repetidas).
2. ⚠️ **Los enlaces de subtítulos son firmados y vencen** (~30 días). Si se vencen hay que
   re-scrapear las piezas — y la corrida nueva trae un conjunto distinto.
3. **Solo si la pieza no tiene subtítulo**, transcribe con IA:
   - TikTok: `clockworks/tiktok-transcript-extractor` (más simple: `scrape-creators/best-tiktok-transcripts-scraper`).
   - Instagram: `apple_yang/instagram-transcripts-scraper` (fue el más barato **y** el de texto más limpio).
   Se aplica la Regla de Oro 2: pruébalo con una pieza y **compara lo cobrado contra lo documentado**
   — varios actores de transcripción cobran entre 18× y 23× su precio de portada.
4. Existen piezas que devuelven *"no audio url found"* aunque se reintente: es una condición de esa
   pieza, no un fallo pasajero. **Repórtalo como pendiente**, no lo maquilles.
5. Las transcripciones automáticas **inventan nombres propios y cifras**. Sirven para saber de qué se
   habla; **para citar textualmente o dar una cifra hay que oír el audio.** Déjalo escrito.

### Paso 4 — Comentarios

1. Usa `apidojo/tiktok-comments-scraper` (TikTok) y `scrapesmith/instagram-comments-scraper`
   (Instagram, `sortOrder: "popular"`).
2. **Orden de popularidad siempre, nunca el orden por defecto.** El valor por defecto devuelve lo más
   reciente, y ahí se pierde el hallazgo: dos muestras del mismo video pueden coincidir en menos de
   un tercio de los comentarios. El sobrecosto del orden popular es ruido.
3. **Mínimo 150 comentarios por pieza.** Es el punto medido en el que se reproducen los más gustados
   *y* el reparto de argumentos a menos de 1 punto del máximo. Con 10 solo sacas 3-4 frases; con 30,
   ~7 de 10. **Más allá de ~400 por pieza no hay nada nuevo**: ese es el techo real de los scrapers
   (no existe "bajar todo"), porque lo que satura es el **repertorio de argumentos**, no la cantidad.
4. **Calcula el límite total como `comentarios por pieza × número de piezas`.** Si eliges mal, la
   corrida se come el presupuesto en las primeras piezas y las demás vuelven casi vacías.
5. **Deduplica siempre por id.** Los scrapers repiten páginas: en una corrida normal apareció ~10% de
   filas repetidas, a veces con distinto número de likes (el contador cambió entre pasadas).
   **Conserva el registro con más likes.**
6. **Filtra los marcadores de vacío** (filas tipo `{"noResults": true}`): no son comentarios y
   descuadran los conteos. Una pieza puede volver vacía sin que la corrida falle.
7. **Nunca sumes dos corridas.** Cada corrida es una **foto**, no un ladrillo. Compáralas (comparar es
   lo que revela), pero no las mezcles.
8. **No existe el campo "los más populares"**: baja la muestra y ordena por likes en tu máquina.
9. **Antes de hablar de sentimiento, revisa el reparto por cuenta**: el top de más gustados puede
   salir mayoritariamente de una sola cuenta.

### Paso 5 — Respuestas (replies): decidir, no asumir

**La regla, en una frase:**
> Primer nivel = **¿qué se aplaude?** · Respuestas = **¿qué se discute?**
> Paga por lo segundo **solo si tu pregunta es la segunda**.

**Por plataforma, no es lo mismo:**

- **TikTok → normalmente NO.** La plataforma no garantiza los hilos y los actores devuelven respuestas
  poco fiables; además **el contador de comentarios de TikTok ya incluye las respuestas** (dice 891 y
  el primer nivel real fue 383). Baja el primer nivel con `includeReplies: false` y **dilo en el
  reporte**. El único actor probado que sí limita respuestas es `clockworks/free-tiktok-scraper`
  (`maxRepliesPerComment`) y cuesta 3,3× más: úsalo solo si el hilo es el objeto de estudio.
- **Instagram → depende de la pregunta, y se decide con un dato.**

**No pagues por respuestas cuando:** solo quieres el mapa de argumentos y las posiciones dominantes (el
primer nivel popular cuesta ~5% de lo que cuesta la capa profunda); la pieza no discute; o solo te
interesa el titular más aplaudido — y ojo, **el aplauso se lo lleva la frase corta**: en los hilos
grandes el comentario original le gana a su mejor respuesta por factores de 8 a 90× en likes, así que
cortar arriba te da la lista de *titulares*, no la de argumentos.

**Sí paga cuando:** necesitas saber **quién responde a quién** (la gran mayoría de las respuestas
empiezan mencionando a otra persona); te interesan las **acusaciones de segundo nivel** (las palabras
tipo "pago", "patrocinado", "bot" casi no aparecen en el titular); o la pregunta es sobre
**argumentación** y no opinión (las respuestas piden pruebas y fuentes mucho más que el primer nivel).

**Y se decide antes de pagar:** el scraper barato devuelve, por cada comentario, **cuántas respuestas
generó**. Si la mediana es de **2 o más**, esa pieza discute y vale la pena; si es 0 o 1, pagarías por
un vacío.

**Tres advertencias de facturación (esta es la trampa más cara):**

1. **El límite de resultados NO acota las respuestas.** Acota solo los comentarios principales; las
   respuestas se suman por encima y **se cobran todas**. Un run cotizado en 14 centavos terminó
   costando $1,44.
2. **Cotiza multiplicando por ~10** (se midió 9,6 respuestas por comentario principal).
3. **No se optimiza ajustando parámetros, se optimiza eligiendo**: entre pedir los 5 comentarios más
   gustados y pedir los 60, la factura casi no cambia porque el costo lo fija el volumen de respuestas
   de la pieza. Y **el ~83% de las respuestas se concentra en 5 comentarios**.
4. **Nunca compres una respuesta que no sabes que existe.**

### Paso 6 — Unir todo en JSON

**Un solo JSON por plataforma, un registro por pieza con todo lo suyo adentro:**

```
pieza
├── identidad y fuente (id, url, cuenta, seguidores, fecha, palabra clave que la trajo)
├── métricas propias de la plataforma (vistas, likes, compartidos, guardados...)
├── clasificación y temas detectados
├── transcripción (texto completo + nº de palabras; y segmentos con marcas de tiempo si existen)
└── comentarios de esa pieza
    └── respuestas anidadas dentro de su comentario padre (solo si se compraron)
```

**Por qué un JSON y no una hoja de cálculo:** los empalmes ya vienen hechos (no hay que cruzar
archivos, así que no hay errores de cruce), no se corta el texto (las hojas de cálculo cortan las
celdas largas) y pesa menos.

> **La regla: manda el JSON. Las hojas de cálculo se generan desde él. Si se contradicen, gana el
> JSON.** La hoja de cálculo es para mirar; el JSON es para trabajar.

Cada JSON lleva arriba un bloque `meta` con: **procedencia, fecha, conteos, la corrida que lo produjo**
(para poder regenerarlo) y **notas de calidad** (qué se filtró, qué falló, qué falta). Eso evita que en
tres meses nadie sepa qué contiene.

### Paso 7 — Entrega

1. **Nombra con el orden de lectura por delante** (`01_`, `02_`, `03_`) y deja la guía al final: quien
   la abra debe entender el paquete sin preguntar.
2. Prepara un **README de entrega** con: qué es cada archivo, cuál es la fuente de verdad, qué sirve
   para analizar, **qué NO tocar** (los crudos) y qué es solo un paso intermedio regenerable.
3. **Advertencias que van siempre en la entrega:**
   - Las muestras de plataformas distintas **no son del mismo tamaño** → se comparan **proporciones**,
     no totales.
   - Si la muestra no fue aleatoria (p. ej. "la pieza más comentada de cada cuenta"), **decláralo**:
     eso infla los promedios de engagement.
   - Los comentarios bajados **no son el universo de la pieza**, y están ordenados por popularidad.
   - **No mezclar fuentes al dimensionar**: los contadores que muestra la plataforma o el buscador
     pueden incluir respuestas o venir inflados hasta 45%. Cuenta con el contador propio de la pieza.
   - La proporción de comentarios sin ningún like suele ser alta (mediana 0): **el orden por
     popularidad no es un lujo, es una necesidad.**
4. **Archiva lo irreemplazable** porque no se vuelve a bajar: los **archivos de subtítulos crudos** y
   los **datasets crudos de Apify** (el dataset se borra solo a los 31 días en planes básicos). Todo lo
   demás se regenera corriendo los scripts.

### Paso 8 — Cerrar el ciclo

Sin este paso terminas en un dataset, no en una conclusión: **clasificar** las piezas (tipo, temas),
**medir** el reparto y compararlo contra las transcripciones, y **escribir el reporte** con la ventana
de fechas, cuántas piezas, cuántas cuentas, el costo real y **qué NO se puede concluir** con esos
datos. Cierra con los pendientes y su costo.

---

## QUÉ ESTÁ PROHIBIDO (ya está probado que falla)

- ❌ Lanzar corridas pagas sin OK previo del usuario.
- ❌ Afirmar precios desde la ficha del actor, sin medirlos.
- ❌ Escalar con muchas piezas antes de haber probado el pipeline completo con **una**.
- ❌ Bajar "todo" una pieza: no existe, el techo está en ~400 comentarios de primer nivel.
- ❌ Sumar corridas como si fueran una sola muestra.
- ❌ Usar una hoja de cálculo como fuente de verdad.
- ❌ Concluir el sentimiento de un tema con el top de más gustados.
- ❌ Tomar el contador de comentarios de la plataforma como "comentarios que puedo bajar".
- ❌ Dejar la transcripción para después: los enlaces vencen y hay que pagar de nuevo.
- ❌ Entregar un número sin decir de qué muestra salió.

---

## CÓMO CERRAR CADA ENTREGA

Reporta siempre, en este orden y en lenguaje llano:

1. **Qué se hizo** (piezas, comentarios, transcripciones) con el conteo real.
2. **Cuánto costó** (medido, por etapa).
3. **Qué quedó pendiente y cuánto costaría.**
4. **Qué NO se puede concluir** con estos datos.
5. Si algo no se pudo hacer, **dilo** — no lo reemplaces por una estimación.
