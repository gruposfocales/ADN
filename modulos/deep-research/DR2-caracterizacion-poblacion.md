# Momento DR2 · Deep research para caracterizar la población (v1.0)

> Versión cerrada. Sale de la conversación con grupos focales del 2026-11-13.
> v0.2: auditoría del prompt v0.1 y nueva versión orientada a un **expediente de referencia del investigado**, que se pueda consultar durante horas y que sirva para diseñar dinámicas de campo.
> v1.0: grupos focales eligió la opción A el 2026-11-13 (una sola corrida tras G1, reutilizada en la Fase 14).

## Cuándo se lanza

Al aprobar el **gate G1** (tras la Fase 6) y antes de la **Fase 7**, con 3.4, 3.11, 3.13, 3.14, 3.15, 6.1 y 6.4 aprobados.

## Corridas

- **Principal (obligatoria):** una sola corrida tras G1 con el prompt de abajo. El informe se reutiliza en las Fases 11 y 14.
- **DR2b (opcional):** corrida corta antes de la Fase 14, solo si la muestra aprobada en la Fase 10 difiere mucho de la población investigada (otro segmento, otro territorio u otros roles). Cubre únicamente roles, relaciones y acceso de lo que cambió. El agente la propone y el usuario decide.

## Qué alimenta

| Uso | Ítems |
|---|---|
| Variables y relaciones | 7.6-7.12 conductas, percepciones, motivaciones, barreras, facilitadores, experiencias y contextos · 7.14 relaciones esperadas |
| Hipótesis | 6.6-6.8 explicaciones rivales y evidencia a favor o en contra (revisión, no aprobación) |
| Evidencia | 8.5 segmentos requeridos |
| Población y muestra | 10.4 segmentos · 10.7 variables · 10.8-10.10 casos críticos, extremos y negativos · 10.12-10.14 canales, disponibilidad y reclutamiento |
| Instrumentos (Fase 11) | 11.4 participantes · 11.9 estímulos · 11.10 técnicas proyectivas o interactivas · 11.11 lenguaje |
| Campo | 14.5-14.7 reclutamiento, contacto y filtros · roles en las sesiones |
| Skills | `40-arquetipos-sistemicos` (roles, relaciones y bucles) · `30-escucha-social` (estímulos e imaginarios) |

## Auditoría del prompt v0.1

1. **Pedía un inventario, no un retrato.** Solo tablas: útil para decidir la muestra, pero no se puede leer ni consultar durante horas.
2. **Fuentes demasiado estrechas.** arXiv casi no tiene estudios sobre poblaciones; 2024-2026 corta la historia y la cultura; quedaban fuera los estudios cualitativos y las voces públicas, que son la fuente del lenguaje y de las citas.
3. **Faltaba la vida cotidiana y el lenguaje del investigado,** que es lo que más sirve para diseñar dinámicas y para que las preguntas suenen naturales.
4. **Faltaban los imaginarios:** cómo se ve a esta población y cómo se ve ella misma. Estereotipos y narrativas en disputa son materia prima de estímulos.
5. **T4 era operación, no caracterización.** El acceso pasa a ser una sección del informe que alimentan T1 y T3, y el eje queda libre para imaginarios.
6. **No había puente a las dinámicas.** Se agrega un banco de tensiones, dilemas, escenarios por rol y estímulos. [RIESGO] Regla de oro 8: son insumos, no preguntas de instrumento; el agente solo los usa desde la Fase 11.
7. **Campos sin origen en el DASHBOARD:** `{fenómeno}` y `{6.x}`. Ahora salen de 3.13, 6.1 y 6.4, y se pide contraevidencia a las hipótesis.
8. **Riesgo de estereotipar.** Se pide diversidad y casos que contradigan el perfil dominante, y se prohíbe identificar a personas privadas.

## Qué hace el agente

1. Arma el comando con la plantilla de abajo y rellena cada `{campo}` con lo **aprobado** (`[x]`) en el DASHBOARD.
2. Ajusta lo que busca cada eje al proyecto. El usuario lo aprueba con `ok` antes de lanzar.
3. Entrega **solo** el bloque con el comando, listo para pegar en la consola de Feynman.
4. Cuando vuelve el informe, lo guarda en `evidencia/`, cruza cada afirmación con su fuente y propone los ítems de la tabla. El informe es evidencia por verificar y no aprueba nada por sí solo.
5. En las Fases 11 y 14 vuelve a leer las partes 9-11 para proponer estímulos, dinámicas, reclutamiento y roles en campo.

## Plantilla del comando

Regla de formato (igual que en DR1): el comando **empieza siempre** con `/deepresearch "` y todo el prompt va dentro de las comillas. Si el texto del proyecto trae comillas dobles, el agente las cambia por comillas simples.

```text
/deepresearch "Caracterización de la población: {título del estudio (0.1)}. Quiero un expediente de referencia del investigado: un retrato vivo, denso y citado de {población (3.4)} en {territorio (3.11)} frente a {temas (3.13)}, que sirva como libro de consulta durante todo el estudio y como base para diseñar dinámicas de campo. Problema: {3.15}. Pregunta principal: {6.1}. Hipótesis a contrastar: {6.4}. Decisión que apoya: {2.1}. Fuera de alcance: {3.14}.

Divide la investigación en exactamente 4 ejes temáticos independientes, uno por agente, en paralelo. Cada agente entrega hallazgos concretos (casos, cifras, citas textuales, ejemplos), no generalidades:
T1 · Quiénes son: segmentos y diversidad interna; trayectorias de vida típicas y atípicas; hitos, crisis y transiciones; cifras clave y cómo varían por territorio, edad, género, ingreso y otras variables relevantes; dónde y cómo se les encuentra.
T2 · Cómo viven {temas (3.13)}: un día y un año en su vida frente al tema; rutinas, rituales, objetos y espacios; momentos de verdad; emociones; contradicciones entre lo que dicen y lo que hacen; y su vocabulario propio (palabras, dichos, eufemismos) con ejemplos de uso.
T3 · El sistema de roles: todos los actores que intervienen, incluidos los que no son la población (familia, pares, instituciones, mercado, medios); el papel, los intereses, los miedos y el poder de cada uno; y las relaciones entre ellos (flujos de dinero, información, cuidado, poder o afecto), con conflictos, alianzas, dependencias y bucles que se refuerzan o se equilibran.
T4 · Imaginarios y conversación pública: cómo se habla de esta población y cómo habla ella de sí misma en medios, redes, cultura popular y política; estereotipos, mitos, narrativas en disputa, referentes que los representan, temas tabú y debates abiertos.

Organiza el entregable final en estas partes, con encabezados claros:
1. Retrato en una página: quiénes son, qué los mueve y qué tensión los define.
2. Ficha de cifras: tabla dato, valor, año, territorio y fuente.
3. Segmentos: tabla de lo que distingue a cada uno y un perfil narrativo breve por segmento, sin nombres reales.
4. Vida cotidiana: línea de tiempo del día y del año, momentos de verdad y contradicciones entre decir y hacer.
5. Glosario del investigado: palabras y expresiones propias, con significado y un ejemplo citado.
6. Catálogo de roles: función, intereses, miedos, poder y fuentes.
7. Mapa de relaciones: tabla origen, tipo de relación, destino, intensidad y evidencia; más una lista de bucles sistémicos, uno por frase.
8. Imaginarios: estereotipo frente a evidencia, narrativas en disputa y temas tabú.
9. Voces: citas textuales de fuentes públicas (testimonios, entrevistas publicadas, estudios cualitativos), cada una con fuente, fecha y segmento.
10. Banco para dinámicas: tensiones y dilemas que dividen a la población; escenarios reales por rol que podrían representarse; estímulos posibles (noticias, piezas, datos sorprendentes); temas que abren conversación y temas que la cierran. Son insumos, no preguntas de instrumento.
11. Acceso y campo: por segmento, dónde están, por qué canales se llega, cómo hablan, cuándo están disponibles y qué les impide participar.
12. Contraevidencia y vacíos: qué contradice las hipótesis, qué no se sabe y qué debe cubrir el campo.

Reglas de evidencia: usa esta jerarquía y etiqueta cada afirmación con su nivel. (A) Estadísticas oficiales, encuestas nacionales y reportes institucionales. (B) Estudios académicos y cualitativos publicados (OpenAlex, SciELO, Redalyc, repositorios universitarios). (C) Periodismo de investigación, crónica, testimonios públicos y conversación en redes, solo para voces, lenguaje e imaginarios. Cifras de 2024 a 2026, o la más reciente disponible con su año. Contexto histórico y cultural sin límite de fecha, con su año. Cada cita con URL verificada; sin URLs rotas ni fuentes inventadas. Marca como [INFERENCIA] todo lo que no tenga fuente directa. Busca diversidad e incluye casos que contradigan el perfil dominante. No identifiques a personas privadas: cita solo testimonios ya publicados y sin datos de contacto.

Salida: consolida el informe final en outputs/{slug}.md y su registro de procedencia en outputs/{slug}.provenance.md."
```

## Pendiente

- `{slug}`: propuesta `poblacion-{código del proyecto}` (por ejemplo `poblacion-gf-2026-002`).
- Probar el prompt con un proyecto real y ver si Feynman respeta las 12 partes. Si el informe sale corto, partirlo en dos corridas: retrato (partes 1-9) y uso (partes 10-12).
- La conversación en redes que encuentre Feynman es indirecta (artículos que la citan). Para un corpus propio se usan las skills `30-escucha-social` y `31-scraping-apify`.

## [HISTÓRICO] v0.1

Prompt con 4 ejes (perfiles y segmentos, roles, relaciones sistémicas, acceso y contexto de campo), 6 partes de entregable en tablas y fuentes primarias 2024-2026 incluyendo arXiv. Reemplazado por la v0.2 tras la auditoría de arriba.
