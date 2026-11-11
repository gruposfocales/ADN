"""Puente Feynman: corre la CLI de Feynman como servicio HTTP para Dify.

POST /tareas        -> encola una investigación y responde al instante con un id.
GET  /tareas/{id}   -> estado (en_cola, corriendo, listo, error) y enlace al resultado.
Al terminar, el informe se sube a GitHub en una rama aparte (nunca a main).
"""
import base64, datetime as dt, os, re, subprocess, threading, uuid, queue, glob
import httpx
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

TOKEN = os.environ["PUENTE_TOKEN"]                     # lo usa Dify en Authorization: Bearer
GH_TOKEN = os.environ["GITHUB_TOKEN"]                  # fine-grained, Contents write
REPOS = set(os.environ.get("REPOS_PERMITIDOS", "gruposfocales/gf-bibliotecario").split(","))  # por defecto solo bibliotecario
RAMA = os.environ.get("RAMA_RESULTADOS", "feynman/resultados")
DS_MODELO = os.environ.get("DEEPSEEK_MODELO", "deepseek-v4-pro")  # o deepseek-v4-flash (más barato)
MODELO = os.environ.get("FEYNMAN_MODELO", f"deepseek/{DS_MODELO}" if os.environ.get("DEEPSEEK_API_KEY") else "")
LIMITE_SEG = int(os.environ.get("LIMITE_SEGUNDOS", "2700"))
FLUJOS = {"pregunta", "deepresearch", "lit", "compare", "summarize", "review"}



def configurar_deepseek():
    """DeepSeek directo: Feynman (Pi) acepta proveedores compatibles con OpenAI en models.json.
    La clave no se escribe en el archivo: va como referencia $DEEPSEEK_API_KEY."""
    if not os.environ.get("DEEPSEEK_API_KEY"):
        return
    import json
    ruta = os.path.expanduser("~/.feynman/agent/models.json")
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    datos = json.load(open(ruta)) if os.path.exists(ruta) else {}
    datos.setdefault("providers", {})["deepseek"] = {
        "baseUrl": "https://api.deepseek.com/v1", "api": "openai-completions",
        "apiKey": "$DEEPSEEK_API_KEY", "models": [{"id": DS_MODELO}]}
    with open(ruta, "w") as f:
        json.dump(datos, f, indent=2)
    os.chmod(ruta, 0o600)


configurar_deepseek()
app = FastAPI(title="Puente Feynman", version="1.0.0")
tareas: dict[str, dict] = {}
cola: "queue.Queue[str]" = queue.Queue()


class Pedido(BaseModel):
    tema: str = Field(..., min_length=3, max_length=2000, description="Pregunta o tema a investigar")
    flujo: str = Field("deepresearch", description="pregunta | deepresearch | lit | compare | summarize | review")
    repo: str = Field("gruposfocales/gf-bibliotecario", description="Repo donde se guarda el informe")


def auth(h: str | None):
    if h != f"Bearer {TOKEN}":
        raise HTTPException(401, "token inválido")


@app.get("/salud")
def salud():
    return {"ok": True, "en_cola": cola.qsize()}


@app.post("/tareas")
def crear(p: Pedido, authorization: str | None = Header(None)):
    auth(authorization)
    if p.flujo not in FLUJOS:
        raise HTTPException(400, f"flujo debe ser uno de {sorted(FLUJOS)}")
    if p.repo not in REPOS:
        raise HTTPException(400, f"repo no permitido; usa uno de {sorted(REPOS)}")
    tid = uuid.uuid4().hex[:10]
    tareas[tid] = {"id": tid, "estado": "en_cola", **p.model_dump(), "creada": dt.datetime.utcnow().isoformat()}
    cola.put(tid)
    return {"id": tid, "estado": "en_cola", "posicion": cola.qsize(),
            "mensaje": "Encargado. Suele tardar entre 5 y 40 minutos. Pregunta el estado con este id."}


@app.get("/tareas/{tid}")
def ver(tid: str, authorization: str | None = Header(None)):
    auth(authorization)
    t = tareas.get(tid)
    if not t:
        raise HTTPException(404, "no existe (el servicio pudo reiniciarse)")
    return {k: v for k, v in t.items() if k != "_log"}


def correr(tid: str):
    t = tareas[tid]
    t["estado"] = "corriendo"
    carpeta = f"/trabajo/{tid}"
    os.makedirs(carpeta, exist_ok=True)
    prompt = t["tema"] if t["flujo"] == "pregunta" else f"/{t['flujo']} {t['tema']}"
    cmd = ["feynman", "--cwd", carpeta, "--no-session", "-p", prompt]
    if MODELO:
        cmd[1:1] = ["--model", MODELO]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=LIMITE_SEG,
                           env={**os.environ, "FEYNMAN_TELEMETRY": "off"})
        if r.returncode != 0:
            raise RuntimeError((r.stderr or r.stdout)[-1500:])
        # Feynman guarda en outputs/ (y papers/); si no hay archivo, usamos la salida de la terminal.
        archivos = sorted(glob.glob(f"{carpeta}/outputs/**/*.md", recursive=True)
                          + glob.glob(f"{carpeta}/papers/**/*.md", recursive=True))
        texto = "\n\n---\n\n".join(open(a, encoding="utf-8").read() for a in archivos) or r.stdout
        t["resumen"] = texto[:1500]
        t["enlace"] = subir(t, texto)
        t["estado"] = "listo"
    except subprocess.TimeoutExpired:
        t.update(estado="error", error=f"superó {LIMITE_SEG} s")
    except Exception as e:  # noqa: BLE001
        t.update(estado="error", error=str(e)[-1500:])
    t["terminada"] = dt.datetime.utcnow().isoformat()


def subir(t: dict, texto: str) -> str:
    """Crea la rama si falta y guarda el informe. Nunca toca main."""
    api = f"https://api.github.com/repos/{t['repo']}"
    h = {"Authorization": f"Bearer {GH_TOKEN}", "Accept": "application/vnd.github+json"}
    with httpx.Client(headers=h, timeout=30) as c:
        if c.get(f"{api}/branches/{RAMA}").status_code == 404:
            base = c.get(api).json()["default_branch"]
            sha = c.get(f"{api}/git/ref/heads/{base}").json()["object"]["sha"]
            c.post(f"{api}/git/refs", json={"ref": f"refs/heads/{RAMA}", "sha": sha}).raise_for_status()
        slug = re.sub(r"[^a-z0-9]+", "-", t["tema"].lower())[:50].strip("-")
        ruta = f"investigaciones/feynman/{dt.date.today()}-{t['flujo']}-{slug}-{t['id']}.md"
        cab = f"# {t['tema']}\n\n_Feynman · flujo `{t['flujo']}` · {dt.date.today()} · sin revisar_\n\n"
        r = c.put(f"{api}/contents/{ruta}", json={
            "message": f"feynman: {t['flujo']} · {t['tema'][:60]}", "branch": RAMA,
            "content": base64.b64encode((cab + texto).encode()).decode()})
        r.raise_for_status()
        return r.json()["content"]["html_url"]


def trabajador():
    while True:
        correr(cola.get())  # una a la vez: Feynman gasta CPU y tokens


threading.Thread(target=trabajador, daemon=True).start()
