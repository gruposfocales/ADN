# Puente Feynman (Dify ↔ Feynman ↔ GitHub)

Feynman es una app de terminal; Dify no puede correrla por dentro. Este servicio la envuelve:
Dify **encarga** una investigación, recibe un id al instante y Feynman trabaja aparte.
Cuando termina, el informe queda en GitHub, en la rama `feynman/resultados`
(carpeta `investigaciones/feynman/`). **Nunca escribe en `main`.**

## Poner en marcha (Dokploy, una vez)
1. Dokploy > Create Service > Application > fuente GitHub `gruposfocales/ADN`, rama `main`,
   build type **Dockerfile**, ruta `plataformas/feynman-puente`.
2. Environment:
   | Variable | Qué es |
   |---|---|
   | `PUENTE_TOKEN` | Clave larga inventada por ti (`openssl rand -hex 32`). La usa Dify. |
   | `GITHUB_TOKEN` | Token fine-grained **nuevo** solo para esto: Contents read+write en los repos de abajo. |
   | `REPOS_PERMITIDOS` | Opcional. Por defecto solo `gruposfocales/gf-bibliotecario`. |
   | `DEEPSEEK_API_KEY` | Tu clave de DeepSeek (platform.deepseek.com). El puente registra DeepSeek directo en Feynman al arrancar. |
   | `DEEPSEEK_MODELO` | Opcional: `deepseek-v4-pro` (por defecto) o `deepseek-v4-flash` (más barato). |
   | `FEYNMAN_MODELO` | Opcional, para forzar otro modelo (ej. `anthropic/...` con `ANTHROPIC_API_KEY`). |
   | `OPENALEX_API_KEY`, `SEMANTIC_SCHOLAR_API_KEY` | Opcionales y gratis; evitan límites de búsqueda. |
3. Domains: `feynman.gruposfocales.com`, puerto 8080, HTTPS. Deploy.
4. Prueba: `curl https://feynman.gruposfocales.com/salud` → `{"ok":true,...}`.

## Conectar a Dify
Herramientas > Crear herramienta personalizada > pega `openapi-dify.yaml` >
Autorización API Key, Bearer, valor `PUENTE_TOKEN`. Salen dos herramientas:
`encargar_investigacion` y `ver_investigacion`. Úsalas desde un nodo Agente o Herramienta.

## Límites honestos
- Una investigación a la vez (cola). `deepresearch` puede tardar 5–40 min y gastar bastantes tokens.
- La cola vive en memoria: si el contenedor se reinicia, se pierden los ids pendientes
  (lo ya subido a GitHub queda).
- El informe llega **sin revisar**: es insumo, no evidencia aprobada del proyecto.
- Solo flujos fijos; no se puede ejecutar ningún comando libre.
