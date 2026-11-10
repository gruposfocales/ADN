# Puente Telegram → Dify (GF · Agentes)

Un servicio pequeño (un archivo de Python, sin dependencias) que conecta tu bot de Telegram con la app **GF · Agentes** de Dify.

- Solo te responde a ti (lista de IDs permitidos).
- Recuerda la conversación de cada chat.
- Eliges el agente con `/agentes` y luego `/1` … `/6`. `/nuevo` empieza de cero.

## Variables de entorno

| Variable | Qué es |
|---|---|
| `TELEGRAM_TOKEN` | Token del bot (de @BotFather) |
| `DIFY_API_KEY` | API Key de la app GF · Agentes (Dify → app → *Acceso API* → *API Key*) |
| `DIFY_BASE` | `https://dify.gruposfocales.com` (por defecto) |
| `ALLOWED_IDS` | IDs de Telegram permitidos, separados por coma |
| `WEBHOOK_SECRET` | Una clave larga inventada (solo letras, números, `_` y `-`) |
| `PUBLIC_URL` | Dirección pública del puente, sin `/` final (por ejemplo `https://tg.gruposfocales.com`) |

## Desplegar en Dokploy

1. **Create Service → Application**. Fuente: GitHub, repo `gruposfocales/ADN`, rama `main`.
2. **Build Type:** Dockerfile. **Build Path / Docker context:** `puentes/telegram`.
3. **Environment:** pega las variables de arriba.
4. **Volumes / Mounts:** un volumen montado en `/data` (guarda las conversaciones).
5. **Domains:** agrega el dominio (por ejemplo `tg.gruposfocales.com`), puerto `8080`, HTTPS activado. El dominio debe tener un registro DNS A hacia la IP del VPS.
6. **Deploy.** En los logs debe salir `setWebhook: {'ok': True, ...}`.

Al arrancar, el puente registra el webhook en Telegram solo. Eso reemplaza cualquier suscripción del plugin *Telegram Trigger* de Dify (bórrala para no confundir).

## Probar

Escríbele `/agentes` al bot, toca un número y luego escribe `estado`.
