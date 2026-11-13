# Momento DR1 · Deep research para el mapa de conocimiento (v1.0)

> Regla general del método desde el 2026-11-13 (instrucciones de grupos focales).
> Cubre los 5 puntos: formato de invocación, 4 ejes, mapa estructurado, restricciones de evidencia y salida.

## Cuándo se lanza

Al cerrar la **Fase 3**, con 3.13 (alcance temático) y 3.15 (formulación del problema) aprobados.
El informe alimenta **4.14 Mapa de conocimiento** y sirve de evidencia para 3.3, 3.8, 3.9 y 8.11.

## Qué hace el agente

1. Arma el comando `/deepresearch` con la plantilla de abajo, rellenando cada `{campo}` con lo **aprobado** (`[x]`) en el DASHBOARD.
2. Propone los 4 ejes (T1-T4) a partir del problema y la ontología del proyecto; el usuario los aprueba con `ok` antes de lanzar.
3. Entrega **únicamente** el bloque de texto con el comando, listo para copiar y pegar en la consola de Feynman.
4. Cuando vuelve el informe: lo guarda en `evidencia/`, hace la lectura cruzada afirmación ↔ fuente y propone 4.14. El informe es evidencia por verificar; no aprueba nada por sí solo.

## Regla de los 4 ejes

Feynman elige entre búsqueda simple (1 agente) o profunda (4 agentes en paralelo) según la estructura del prompt.
Para forzar la profunda, el mapa se divide en **exactamente 4 ejes temáticos independientes**, derivados de la ontología y los problemas del proyecto. Ejemplo:

- **T1** Marco teórico y taxonomía
- **T2** Enfoques y métodos actuales
- **T3** Evidencia empírica y casos de uso
- **T4** Vacíos, brechas y controversias

## Plantilla del comando

Regla de formato: el comando **empieza siempre** con `/deepresearch "` y todo el prompt va dentro de las comillas, abriendo con el título y el alcance. Si el texto del proyecto trae comillas dobles, el agente las cambia por comillas simples.

```text
/deepresearch "Mapa de conocimiento: {título del estudio (0.1)}. Alcance: {3.15 problema en una frase}; población {3.4}; territorio {3.11}; temas {3.13}; fuera de alcance {3.14}.

Contexto: {1.2 necesidad}. Decisión que apoya: {2.1}.

Divide la investigación en exactamente 4 ejes temáticos independientes, uno por agente, en paralelo:
T1 · {eje 1 aprobado}: {qué buscar}
T2 · {eje 2 aprobado}: {qué buscar}
T3 · {eje 3 aprobado}: {qué buscar}
T4 · {eje 4 aprobado}: {qué buscar}

Organiza el entregable como un mapa de conocimiento estructurado con: (1) taxonomía jerárquica de conceptos; (2) matriz de relaciones entre las entidades de la ontología: {conceptos clave del proyecto}; (3) citas verificadas, cada afirmación con su fuente; (4) tabla de estado del arte.

Restricciones de evidencia: solo fuentes primarias (papers en arXiv u OpenAlex, documentación técnica, repositorios y reportes institucionales); periodo 2024 a 2026; cada cita con URL verificada, sin URLs rotas ni fuentes inventadas.

Salida: consolida el informe final en outputs/{slug}.md y su registro de procedencia en outputs/{slug}.provenance.md."
```

## Pendiente

- `{slug}`: propuesta `mapa-{código del proyecto}` (por ejemplo `mapa-gf-2026-002`).
