#!/usr/bin/env python3
"""Genera el chatflow único de Dify a partir del catálogo (agentes.txt + cada agente/agente.txt).

Uso:
    python3 herramientas/dify_chatflow.py            # escribe plataformas/dify/chatflow.json

El chatflow tiene una rama por agente. Al empezar, el usuario elige el agente de una lista.
Cada turno, la rama lee de GitHub, en vivo, el `agente/SYSTEM-sin-archivos.md` del repo y sus
`fuentes`, y se los pasa al modelo. Si la respuesta trae "📥 Parche" y la ficha tiene
`issue_parches: N`, el parche se publica como comentario en ese issue (nunca en main).

El archivo generado no lleva secretos: el token va en la variable de entorno GITHUB_TOKEN,
que se llena a mano en Dify. Ver plataformas/dify.md.
"""
import json
import pathlib

from ficha import leer, leer_ficha

NUCLEO = pathlib.Path(__file__).resolve().parent.parent
SALIDA = NUCLEO / "plataformas" / "dify" / "chatflow.json"
SALIDA_MINIMO = NUCLEO / "plataformas" / "dify" / "chatflow-minimo.json"
# Modo --minimo: cada turno lee solo el SYSTEM y el archivo de estado del agente (el primero que exista
# en sus fuentes). El repo no cambia; lo demás (Manual, bitácora, evidencia) se trabaja fuera de Dify.
ESTADO = ("DASHBOARD.md", "INDICE_MAESTRO.md", "organizacion/ESTADO-NEGOCIO.md")
MINIMO = False

MODELO = {"provider": "langgenius/deepseek/deepseek", "name": "deepseek-v4-flash", "mode": "chat",
          "completion_params": {"temperature": 0.3}}
GITHUB_PLUGIN = "langgenius/github/github"
ENV_TOKEN = {"id": "env-github-token", "name": "GITHUB_TOKEN", "value_type": "secret", "value": "",
             "description": "Token fine-grained de GitHub: Contents read en los repos de agentes.txt e Issues write para los parches."}
ENV_KAPSO = {"id": "env-kapso-api-key", "name": "KAPSO_API_KEY", "value_type": "secret", "value": "",
             "description": "Clave de API del proyecto Kapso GruposFocales, para exportar encuestas (módulo Encuestas)."}
ENCUESTAS = "📋 Encuestas WhatsApp → Kapso"
ENCUESTAS_SYSTEM = ("gruposfocales/ADN", "plataformas/kapso-encuestas/SYSTEM.md")
TIPOS_CON_INSTRUMENTOS = ("investigacion", "activacion-comunidad", "proyecto-agente")


def nodo(i, x, y, data):
    return {"id": i, "type": "custom", "position": {"x": x, "y": y}, "data": data}


def arista(s, t, handle="source"):
    return {"id": f"{s}-{handle}-{t}", "source": s, "sourceHandle": handle, "target": t,
            "targetHandle": "target", "type": "custom", "data": {}}


def http(titulo, repo, ruta):
    return {"type": "http-request", "title": titulo, "method": "get",
            "url": f"https://api.github.com/repos/{repo}/contents/{ruta}?ref=main",
            "authorization": {"type": "no-auth", "config": None},
            "headers": "Accept:application/vnd.github.raw\nAuthorization:Bearer {{#env.GITHUB_TOKEN#}}\n"
                       "X-GitHub-Api-Version:2022-11-28\nUser-Agent:dify-gf-agentes",
            "params": "", "body": {"type": "none", "data": []},
            "timeout": {"max_connect_timeout": 10, "max_read_timeout": 30, "max_write_timeout": 10},
            "retry_config": {"retry_enabled": True, "max_retries": 2, "retry_interval": 1000},
            "ssl_verify": True, "variables": []}


ICONOS = {"orquestador": "🧭", "investigacion": "🔎", "activacion-comunidad": "🤝",
          "proyecto-agente": "📰", "disenador": "🛠️"}


def etiqueta(d):
    return f"{ICONOS.get(d['tipo'], '•')} {d['nombre']}"


def rama(n, d, y):
    """Nodos y aristas de la rama del agente n (prefijo a{n})."""
    p = f"a{n}"
    repo = d["repo"]
    org = repo.split("/")[0]
    nodos, aristas = [], []
    lecturas = [("SYSTEM", repo, "agente/SYSTEM-sin-archivos.md")]
    fuentes = d["fuentes"]
    if MINIMO:
        fuentes = [f for e in ESTADO for f in fuentes if f == e][:1]
    for f in fuentes:
        otro, _, ruta = f.rpartition(":")
        lecturas.append((f, f"{org}/{otro}" if otro else repo, ruta))
    anterior, x = None, 600
    ids = []
    for k, (titulo, r, ruta) in enumerate(lecturas):
        i = f"{p}h{k}"
        nodos.append(nodo(i, x, y, http(f"{d['nombre'][:20]} · {titulo}", r, ruta)))
        if anterior:
            aristas.append(arista(anterior, i))
        anterior, x = i, x + 260
        ids.append((titulo, i))
    archivos = "\n\n".join(f"=== {t} ===\n{{{{#{i}.body#}}}}" for t, i in ids[1:])
    llm = f"{p}llm"
    nodos.append(nodo(llm, x, y, {
        "type": "llm", "title": f"{d['nombre'][:24]} · modelo", "model": MODELO,
        "prompt_template": [
            {"id": f"{p}s1", "role": "system", "text": f"{{{{#{ids[0][1]}.body#}}}}"},
            {"id": f"{p}s2", "role": "system", "text":
                "Archivos vigentes, leídos en vivo desde GitHub en este turno (fuente de verdad). "
                "Si un archivo dice 404 o Not Found, di \"No lo encuentro\" y sigue.\n\n" + archivos},
        ],
        "context": {"enabled": False, "variable_selector": []},
        "memory": {"window": {"enabled": True, "size": 30}, "query_prompt_template": "{{#sys.query#}}",
                   "role_prefix": {"user": "", "assistant": ""}},
        "vision": {"enabled": False}, "variables": [], "reasoning_format": "separated"}))
    aristas.append(arista(anterior, llm))
    resp = f"{p}ans"
    nodos.append(nodo(resp, x + 300, y, {"type": "answer", "title": f"{d['nombre'][:24]} · respuesta",
                                         "answer": f"{{{{#{llm}.text#}}}}", "variables": []}))
    aristas.append(arista(llm, resp))
    issue = d.get("issue_parches", "").strip()
    if issue and d["tipo"] != "orquestador":
        si, pub = f"{p}if", f"{p}pub"
        nodos.append(nodo(si, x + 300, y + 160, {"type": "if-else", "title": "¿Trae parche?", "cases": [
            {"case_id": "true", "logical_operator": "and", "conditions": [
                {"id": f"{p}c1", "varType": "string", "variable_selector": [llm, "text"],
                 "comparison_operator": "contains", "value": "📥 Parche"}]}]}))
        nodos.append(nodo(pub, x + 600, y + 160, {
            "type": "tool", "title": f"Parche al issue #{issue}", "desc": "",
            "provider_id": GITHUB_PLUGIN, "provider_type": "builtin", "provider_name": GITHUB_PLUGIN,
            "tool_name": "github_issue_comment", "tool_label": "Comentar issue", "tool_description": "",
            "tool_configurations": {}, "tool_node_version": "2", "is_team_authorization": True, "paramSchemas": [],
            "tool_parameters": {
                "owner": {"type": "mixed", "value": org},
                "repo": {"type": "mixed", "value": repo.split("/")[1]},
                "issue_number": {"type": "constant", "value": int(issue)},
                "body": {"type": "mixed", "value": f"{{{{#{llm}.text#}}}}\n\n---\n_Enviado desde Dify · {d['nombre']}_"}}}))
        aristas += [arista(llm, si), arista(si, pub, "true")]
    return nodos, aristas


def rama_encuestas(n, fichas, y):
    """Módulo Encuestas: lee los INSTRUMENTOS.md, muestra la vista previa, pide ok y exporta a Kapso."""
    p = f"a{n}"
    lecturas = [("SYSTEM",) + ENCUESTAS_SYSTEM]
    lecturas += [(f"{d['nombre']} · INSTRUMENTOS.md", d["repo"], "INSTRUMENTOS.md")
                 for d in fichas if d["tipo"] in TIPOS_CON_INSTRUMENTOS]
    nodos, aristas, ids, anterior, x = [], [], [], None, 600
    for k, (titulo, r, ruta) in enumerate(lecturas):
        i = f"{p}h{k}"
        nodos.append(nodo(i, x, y, http(f"Encuestas · {titulo[:24]}", r, ruta)))
        if anterior:
            aristas.append(arista(anterior, i))
        anterior, x = i, x + 260
        ids.append((titulo, i))
    archivos = "\n\n".join(f"=== {t} ===\n{{{{#{i}.body#}}}}" for t, i in ids[1:])
    llm = f"{p}llm"
    nodos.append(nodo(llm, x, y, {
        "type": "llm", "title": "Encuestas · modelo", "model": MODELO,
        "prompt_template": [
            {"id": f"{p}s1", "role": "system", "text": f"{{{{#{ids[0][1]}.body#}}}}"},
            {"id": f"{p}s2", "role": "system", "text":
                "Instrumentos vigentes de cada proyecto, leídos en vivo desde GitHub (fuente de verdad):\n\n" + archivos}],
        "context": {"enabled": False, "variable_selector": []},
        "memory": {"window": {"enabled": True, "size": 30}, "query_prompt_template": "{{#sys.query#}}",
                   "role_prefix": {"user": "", "assistant": ""}},
        "vision": {"enabled": False}, "variables": [], "reasoning_format": "separated"}))
    aristas.append(arista(anterior, llm))
    resp, si, js, post, fin = (f"{p}{s}" for s in ("ans", "if", "json", "post", "fin"))
    nodos.append(nodo(resp, x + 300, y, {"type": "answer", "title": "Encuestas · respuesta",
                                         "answer": f"{{{{#{llm}.text#}}}}", "variables": []}))
    nodos.append(nodo(si, x + 300, y + 160, {"type": "if-else", "title": "¿Trae 📤 Kapso?", "cases": [
        {"case_id": "true", "logical_operator": "and", "conditions": [
            {"id": f"{p}c1", "varType": "string", "variable_selector": [llm, "text"],
             "comparison_operator": "contains", "value": "📤 Kapso"}]}]}))
    nodos.append(nodo(js, x + 600, y + 160, {
        "type": "llm", "title": "Encuestas · sacar JSON",
        "model": {**MODELO, "completion_params": {"temperature": 0}},
        "prompt_template": [
            {"id": f"{p}j1", "role": "system", "text":
                "Copia exactamente el objeto JSON que aparece después de la línea '📤 Kapso'. "
                "Responde solo con ese JSON: sin ```, sin comentarios, sin texto antes ni después."},
            {"id": f"{p}j2", "role": "user", "text": f"{{{{#{llm}.text#}}}}"}],
        "context": {"enabled": False, "variable_selector": []},
        "vision": {"enabled": False}, "variables": [], "reasoning_format": "separated"}))
    nodos.append(nodo(post, x + 900, y + 160, {
        "type": "http-request", "title": "Exportar a Kapso", "method": "post",
        "url": "https://api.kapso.ai/platform/v1/workflows",
        "authorization": {"type": "no-auth", "config": None},
        "headers": "X-API-Key:{{#env.KAPSO_API_KEY#}}\nContent-Type:application/json",
        "params": "",
        "body": {"type": "json", "data": [{"id": f"{p}b1", "key": "", "type": "text", "value": f"{{{{#{js}.text#}}}}"}]},
        "timeout": {"max_connect_timeout": 10, "max_read_timeout": 60, "max_write_timeout": 30},
        "retry_config": {"retry_enabled": False, "max_retries": 0, "retry_interval": 1000},
        "ssl_verify": True, "variables": []}))
    nodos.append(nodo(fin, x + 1200, y + 160, {
        "type": "answer", "title": "Resultado Kapso", "variables": [],
        "answer": f"\n\n---\n**Kapso respondió {{{{#{post}.status_code#}}}}** (201 = creada en borrador).\n"
                  f"Revísala en https://app.kapso.ai → Workflows.\n\n{{{{#{post}.body#}}}}"}))
    aristas += [arista(llm, resp), arista(llm, si), arista(si, js, "true"), arista(js, post), arista(post, fin)]
    return nodos, aristas


def generar():
    repos = [l.split("#")[0].strip() for l in leer(NUCLEO / "agentes.txt").splitlines() if l.split("#")[0].strip()]
    fichas = [leer_ficha(NUCLEO.parent / r) for r in repos]
    opciones = [etiqueta(d) for d in fichas] + [ENCUESTAS]
    nodos = [nodo("start", 0, 0, {"type": "start", "title": "Inicio", "variables": [{
        "variable": "agente", "label": "Elige tu agente", "type": "select",
        "required": True, "options": opciones, "max_length": 100}]})]
    casos = [{"case_id": f"a{n}", "logical_operator": "and", "conditions": [
        {"id": f"a{n}c", "varType": "string", "variable_selector": ["start", "agente"],
         "comparison_operator": "is", "value": opciones[n]}]} for n in range(len(opciones))]
    nodos.append(nodo("elegir", 300, 0, {"type": "if-else", "title": "Elegir agente", "cases": casos}))
    aristas = [arista("start", "elegir")]
    for n, d in enumerate(fichas):
        y = n * 400
        ns, as_ = rama(n, d, y)
        nodos += ns
        aristas += as_
        aristas.append(arista("elegir", f"a{n}h0", f"a{n}"))
    n = len(fichas)
    ns, as_ = rama_encuestas(n, fichas, n * 400)
    nodos += ns
    aristas += as_
    aristas.append(arista("elegir", f"a{n}h0", f"a{n}"))
    nodos.append(nodo("ninguno", 600, (n + 1) * 400, {
        "type": "answer", "title": "Sin agente", "variables": [],
        "answer": "No reconozco ese agente. Empieza una conversación nueva y elige uno de la lista."}))
    aristas.append(arista("elegir", "ninguno", "false"))
    features = {
        "opening_statement": "Hola 👋 Soy tu equipo de agentes de GruposFocales.\n\n"
                             "Cada agente trabaja con los archivos vigentes de su proyecto. Tú solo apruebas o corriges.\n\n"
                             "Para empezar, toca una opción. Para cambiar de agente, abre una conversación nueva.",
        "suggested_questions": ["estado", "continuar", "pendientes"],
        "file_upload": {"enabled": False}, "retriever_resource": {"enabled": False},
        "speech_to_text": {"enabled": False}, "text_to_speech": {"enabled": False, "voice": "", "language": ""},
        "suggested_questions_after_answer": {"enabled": False}, "sensitive_word_avoidance": {"enabled": False}}
    return {"graph": {"nodes": nodos, "edges": aristas}, "features": features,
            "environment_variable_patch": {"environment_variables": [ENV_TOKEN, ENV_KAPSO]},
            "conversation_variables": []}


def main():
    global MINIMO, SALIDA
    import sys
    if "--minimo" in sys.argv:
        MINIMO, SALIDA = True, SALIDA_MINIMO
    datos = generar()
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(datos, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    ramas = sum(1 for n in datos["graph"]["nodes"] if n["data"]["type"] == "llm")
    print(f"✅ {SALIDA.relative_to(NUCLEO)}: {ramas} agentes, {len(datos['graph']['nodes'])} nodos.")


if __name__ == "__main__":
    main()
