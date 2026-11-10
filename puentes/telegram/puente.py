"""Puente Telegram -> Dify (GF · Agentes).

Recibe los mensajes del bot de Telegram (webhook), los pasa a la API de
chat de la app de Dify y devuelve la respuesta al mismo chat.

- Solo responde a los IDs de Telegram en ALLOWED_IDS.
- Recuerda la conversación de cada chat (archivo JSON en /data).
- Comandos: /agentes (lista), /1 ... /9 (elige agente y empieza de cero),
  /nuevo (conversación nueva con el mismo agente).

Solo usa la biblioteca estándar de Python. Variables de entorno: ver README.md.
"""

import json
import os
import threading
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
DIFY_API_KEY = os.environ["DIFY_API_KEY"]
DIFY_BASE = os.environ.get("DIFY_BASE", "https://dify.gruposfocales.com").rstrip("/")
ALLOWED_IDS = {s.strip() for s in os.environ.get("ALLOWED_IDS", "").split(",") if s.strip()}
WEBHOOK_SECRET = os.environ["WEBHOOK_SECRET"]
PUBLIC_URL = os.environ.get("PUBLIC_URL", "").rstrip("/")
AGENT_VAR = os.environ.get("AGENT_VAR", "agente")
STATE_FILE = os.environ.get("STATE_FILE", "/data/estado.json")
PORT = int(os.environ.get("PORT", "8080"))

TG = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
_lock = threading.Lock()


# ---------- utilidades ----------

def http_json(url, data=None, headers=None, timeout=30):
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, method="POST" if body else "GET")
    req.add_header("Content-Type", "application/json")
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def load_state():
    try:
        with open(STATE_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=1)
    os.replace(tmp, STATE_FILE)


def send(chat_id, text):
    # Telegram corta en 4096 caracteres; texto plano para evitar errores de formato.
    text = text or "(sin respuesta)"
    for i in range(0, len(text), 4000):
        try:
            http_json(f"{TG}/sendMessage", {"chat_id": chat_id, "text": text[i:i + 4000]})
        except Exception as e:  # noqa: BLE001
            print("error enviando a Telegram:", e, flush=True)


def typing(chat_id):
    try:
        http_json(f"{TG}/sendChatAction", {"chat_id": chat_id, "action": "typing"})
    except Exception:  # noqa: BLE001
        pass


def dify_headers():
    return {"Authorization": f"Bearer {DIFY_API_KEY}"}


def agent_options():
    """Lee la lista de agentes desde el formulario de inicio de la app."""
    p = http_json(f"{DIFY_BASE}/v1/parameters", headers=dify_headers())
    for item in p.get("user_input_form", []):
        for field in item.values():
            if field.get("variable") == AGENT_VAR:
                return field.get("options", [])
    return []


def agents_text(opts, current=None):
    lines = ["Elige un agente (toca el número):", ""]
    for i, o in enumerate(opts, 1):
        mark = "  ← actual" if o == current else ""
        lines.append(f"/{i}  {o}{mark}")
    lines += ["", "/nuevo  empieza de cero con el mismo agente"]
    return "\n".join(lines)


# ---------- lógica ----------

def handle(update):
    msg = update.get("message") or update.get("edited_message")
    if not msg or "text" not in msg:
        return
    chat_id = msg["chat"]["id"]
    user_id = str(msg.get("from", {}).get("id", ""))
    if user_id not in ALLOWED_IDS:
        print("ignorado, ID no permitido:", user_id, flush=True)
        return

    text = msg["text"].strip()
    key = str(chat_id)
    with _lock:
        state = load_state()
    st = state.get(key, {})

    if text in ("/start", "/agentes", "/menu"):
        send(chat_id, agents_text(agent_options(), st.get("agente")))
        return

    if text == "/nuevo":
        st.pop("conversation_id", None)
        with _lock:
            state = load_state(); state[key] = st; save_state(state)
        send(chat_id, "Listo, conversación nueva" + (f" con {st['agente']}." if st.get("agente") else ". Elige agente con /agentes."))
        return

    if text.startswith("/") and text[1:].split("@")[0].isdigit():
        opts = agent_options()
        n = int(text[1:].split("@")[0])
        if 1 <= n <= len(opts):
            st = {"agente": opts[n - 1]}
            with _lock:
                state = load_state(); state[key] = st; save_state(state)
            send(chat_id, f"Agente: {opts[n - 1]}\nEscríbele lo que necesites (por ejemplo: estado).")
        else:
            send(chat_id, agents_text(opts, st.get("agente")))
        return

    if not st.get("agente"):
        send(chat_id, agents_text(agent_options()))
        return

    typing(chat_id)
    payload = {
        "inputs": {AGENT_VAR: st["agente"]},
        "query": text,
        "response_mode": "blocking",
        "user": f"tg-{user_id}",
    }
    if st.get("conversation_id"):
        payload["conversation_id"] = st["conversation_id"]

    # Mantiene el "escribiendo..." mientras Dify piensa.
    stop = threading.Event()

    def keep_typing():
        while not stop.wait(4):
            typing(chat_id)

    threading.Thread(target=keep_typing, daemon=True).start()
    try:
        r = http_json(f"{DIFY_BASE}/v1/chat-messages", payload, dify_headers(), timeout=600)
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:300]
        if e.code == 404 and st.get("conversation_id"):
            st.pop("conversation_id", None)
            with _lock:
                state = load_state(); state[key] = st; save_state(state)
            send(chat_id, "La conversación anterior ya no existe. Empecé una nueva: vuelve a enviar tu mensaje.")
        else:
            send(chat_id, f"Dify respondió con error {e.code}. {detail}")
        return
    except Exception as e:  # noqa: BLE001
        send(chat_id, f"No pude hablar con Dify: {e}")
        return
    finally:
        stop.set()

    if r.get("conversation_id"):
        st["conversation_id"] = r["conversation_id"]
        with _lock:
            state = load_state(); state[key] = st; save_state(state)
    send(chat_id, r.get("answer", ""))


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):  # chequeo de salud
        self.send_response(200); self.end_headers(); self.wfile.write(b"ok")

    def do_POST(self):
        if self.headers.get("X-Telegram-Bot-Api-Secret-Token") != WEBHOOK_SECRET:
            self.send_response(403); self.end_headers(); return
        n = int(self.headers.get("Content-Length", 0))
        try:
            update = json.loads(self.rfile.read(n) or b"{}")
        except json.JSONDecodeError:
            update = {}
        # Responde enseguida para que Telegram no reintente; procesa aparte.
        self.send_response(200); self.end_headers()
        threading.Thread(target=self._safe, args=(update,), daemon=True).start()

    @staticmethod
    def _safe(update):
        try:
            handle(update)
        except Exception as e:  # noqa: BLE001
            print("error:", e, flush=True)

    def log_message(self, *a):
        pass


def register_webhook():
    if not PUBLIC_URL:
        print("PUBLIC_URL vacío: no registro el webhook.", flush=True)
        return
    r = http_json(f"{TG}/setWebhook", {
        "url": f"{PUBLIC_URL}/telegram",
        "secret_token": WEBHOOK_SECRET,
        "allowed_updates": ["message"],
        "drop_pending_updates": True,
    })
    print("setWebhook:", r, flush=True)


if __name__ == "__main__":
    if not ALLOWED_IDS:
        raise SystemExit("ALLOWED_IDS está vacío: nadie podría usar el bot.")
    register_webhook()
    print(f"Puente escuchando en :{PORT}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
