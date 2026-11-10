---
name: escucha-social
description: "Diseña, captura y codifica comentarios públicos de redes (TikTok, Facebook, Instagram) provocados por un estímulo, como un microdrama, y los triangula con encuesta o grupo focal."
familia: 30 · Escucha
version: 0.1
entra: capítulo publicado con su ficha (constructo, pregunta en pantalla, códigos)
sale: base de comentarios codificada y lectura por constructo
siguiente: 31-scraping-apify
estado: prueba
---

# Escucha social por estímulo

Responde en el idioma del usuario. Lenguaje simple.

## 1. Antes de publicar: ficha del capítulo
Cada estímulo lleva: constructo (uno solo) · pregunta en pantalla · comentario fijado · códigos previos · pregunta espejo en encuesta o grupo focal.
- La pregunta en pantalla pide una experiencia ("¿Le ha pasado?") o una elección codificable ("Comente A o B y por qué"). Nunca "opine".
- Un dilema, no una moraleja: dos salidas razonables.

## 2. Captura
- Solo comentarios públicos. Texto, fecha, likes y respuestas en hilo.
- **Respuestas siempre** (decisión del usuario, 2026-10-18): prevalece sobre el Paso 5 de `/scraping-apify`. Cotiza las respuestas ×10 y muestra el costo antes de correr.
- Ventana de 14 días por video.
- Para extraer, usa `/scraping-apify` (actores probados, costos medidos, OK antes de pagar).
- Borra el usuario y asigna un ID seudónimo antes de guardar.

## 3. Codificación
- Códigos previos del constructo + códigos emergentes + "fuera de tema".
- Código de debate: acuerdo · desacuerdo · respuesta a otro.
- Las repreguntas del equipo son estímulo: codifica lo que pasa antes y después.
- Revisión humana de una muestra (10 %).

## 4. Lectura
- Por constructo: qué salidas eligen y con qué razones.
- Triangula con la pregunta espejo. Sin triangular, es señal; triangulado, vale como hallazgo.
- Límite que siempre se declara: describe el debate público en esa red, no a la población del estudio.

## Reglas
- No inventes comentarios, cifras ni citas.
- No cites textos que identifiquen a nadie.
- Confirma que la política de datos del proyecto cubre comentarios de redes antes de capturar.
