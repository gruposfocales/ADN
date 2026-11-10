<!-- módulo: tipos de agente · núcleo GF v1.2 -->

# Tipos de agente de GruposFocales

Cada repo es un agente y declara su tipo en `agente/agente.txt`.

| Tipo (`tipo:`) | Qué hace | Qué entrega | Método |
|---|---|---|---|
| `orquestador` | Ve todos los proyectos, informa el estado y dice a qué agente ir. No diseña ni aprueba. | Estado, pendientes y bloqueos | Propio (solo lectura) |
| `investigacion` | Diseña una investigación por fases y gates hasta el paquete listo para campo. | Field-Ready Research Package | `arquitecto` (289 ítems) |
| `activacion-comunidad` | Diseña y acompaña la activación de una comunidad (memoria, encuentros, participación). | Plan y piezas de activación | `arquitecto`, con su personalidad |
| `proyecto-agente` | Su resultado final es un agente que funciona, no un informe. | Especificación y agente construido | `arquitecto` para estudiar a la gente + diseño en `disenador-de-agentes` |
| `disenador` | Entrevista por 10 capas y produce la especificación de un agente nuevo. | `ESPECIFICACION.md`, prompt y plan de construcción | Propio |

No son agentes: `ADN` (este núcleo) y el código de plataformas (por ejemplo, el repo `dify`).
