# Índice de skills

> Generado por `herramientas/indexar_skills.py`. No lo edite a mano: cambie la ficha de cada `SKILL.md` y vuelva a correr el script.

## ¿Qué quiere hacer?

| Quiero… | Use |
|---|---|
| Diseñar o continuar el estudio | `/arquitecto-investigacion` |
| Montar el filtro, el bot o la encuesta en WhatsApp | `/kapso-encuestas-whatsapp` |
| Diseñar el estímulo y codificar comentarios de redes | `/escucha-social` |
| Bajar piezas, transcripciones y comentarios con Apify | `/scraping-apify` |
| Convertir transcripciones en personajes | `/arquetipos-sistemicos` |
| Escribir una serie o un guion de microdrama | `/microdrama-adictivo` |
| Producir con IA: personajes, storyboard y prompts de Seedance | `/claqueta-brief` |
| No sé qué usar | `/skills` |

## Cadena de trabajo

```
10 arquitecto-investigacion → 20 kapso-encuestas-whatsapp → 30 escucha-social → 31 scraping-apify → 40 arquetipos-sistemicos → 50 microdrama-adictivo → 60 claqueta-brief
                    ↑ 30 alimenta de vuelta a 10 (hallazgos triangulados)
```

## Catálogo

| # | Comando | Familia | Versión | Estado | Entra | Sale | Siguiente |
|---|---|---|---|---|---|---|---|
| 00 | `/skills` | 00 · Menú | 1.0 | estable | lo que el usuario quiere hacer | la skill sugerida y su siguiente paso | — |
| 10 | `/arquitecto-investigacion` | 10 · Diseño | 4.0 | estable | decisión de negocio, evidencia, archivos del proyecto | DASHBOARD.md, BITACORA.md, INSTRUMENTOS.md aprobados | 20-campo-kapso |
| 20 | `/kapso-encuestas-whatsapp` | 20 · Campo | 1.0 | estable | instrumentos aprobados (filtro, bot, encuesta) | flujos y nodos de Kapso para WhatsApp | 30-escucha-social |
| 30 | `/escucha-social` | 30 · Escucha | 0.1 | prueba | capítulo publicado con su ficha (constructo, pregunta en pantalla, códigos) | base de comentarios codificada y lectura por constructo | 31-scraping-apify |
| 31 | `/scraping-apify` | 30 · Escucha | 1.0 | estable | tema, país, plataformas, ventana de fechas, tope de gasto (o la ficha de un capítulo publicado) | un JSON por plataforma con meta, transcripciones y comentarios + reporte de costos | 30-escucha-social |
| 40 | `/arquetipos-sistemicos` | 40 · Personajes | 1.0 | prueba | transcripciones de grupos focales o entrevistas | tarjetas de arquetipo, mapa relacional, episodios para lives | 50-microdrama-adictivo |
| 50 | `/microdrama-adictivo` | 50 · Contenido | 1.0 | prueba | tarjetas de arquetipo (de 40) | biblia, escaleta y guiones de 1 min | 60-claqueta-brief |
| 60 | `/claqueta-brief` | 60 · Producción | 1.0 | estable | Claqueta de Brief del cliente (o guiones aprobados de 50) | historia aprobada, character sheets, storyboard de 9 paneles y prompts de Seedance 2.0 | 30-escucha-social |

## Para agregar una skill

1. Cree `.claude/skills/NN-nombre/SKILL.md` (NN = familia: 05 biblioteca · 10 diseño · 20 campo · 30-39 escucha · 40 personajes · 50 contenido · 60 producción).
2. Llene la ficha: `name`, `description`, `familia`, `version`, `entra`, `sale`, `siguiente`, `estado`.
3. Corra `python3 herramientas/indexar_skills.py`.
