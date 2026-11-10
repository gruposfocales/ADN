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

MODELO = {"provider": "langgenius/deepseek/deepseek", "name": "deepseek-v4-flash", "mode": "chat",
          "completion_params": {"temperature": 0.3}}
GITHUB_PLUGIN = "langgenius/github/github"
ENV_TOKEN = {"id": "env-github-token", "name": "GITHUB_TOKEN", "value_type": "secret", "value": "",
             "description": "Token fine-grained de GitHub: Contents read en los repos de agentes.txt e Issues write para los parches."}


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


def etiqueta(d):
    return f"{d['nombre']} · {d['tipo']}"


def rama(n, d, y):
    """Nodos y aristas de la rama del agente n (prefijo a{n})."""
    p = f"a{n}"
    repo = d["repo"]
    org = repo.split("/")[0]
    nodos, aristas = [], []
    lecturas = [("SYSTEM", repo, "agente/SYSTEM-sin-archivos.md")]
    for f in d["fuentes"]:
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


def generar():
    repos = [l.split("#")[0].strip() for l in leer(NUCLEO / "agentes.txt").splitlines() if l.split("#")[0].strip()]
    fichas = [leer_ficha(NUCLEO.parent / r) for r in repos]
    opciones = [etiqueta(d) for d in fichas]
    nodos = [nodo("start", 0, 0, {"type": "start", "title": "Inicio", "variables": [{
        "variable": "agente", "label": "¿Con qué agente quieres trabajar?", "type": "select",
        "required": True, "options": opciones, "max_length": 100}]})]
    casos = [{"case_id": f"a{n}", "logical_operator": "and", "conditions": [
        {"id": f"a{n}c", "varType": "string", "variable_selector": ["start", "agente"],
         "comparison_operator": "is", "value": opciones[n]}]} for n in range(len(fichas))]
    nodos.append(nodo("elegir", 300, 0, {"type": "if-else", "title": "Elegir agente", "cases": casos}))
    aristas = [arista("start", "elegir")]
    for n, d in enumerate(fichas):
        y = n * 400
        ns, as_ = rama(n, d, y)
        nodos += ns
        aristas += as_
        aristas.append(arista("elegir", f"a{n}h0", f"a{n}"))
    nodos.append(nodo("ninguno", 600, len(fichas) * 400, {
        "type": "answer", "title": "Sin agente", "variables": [],
        "answer": "No reconozco ese agente. Empieza una conversación nueva y elige uno de la lista."}))
    aristas.append(arista("elegir", "ninguno", "false"))
    features = {
        "opening_statement": "Hola. Este es el chat de los agentes de GruposFocales. Cada agente lee en vivo "
                             "sus instrucciones y archivos desde GitHub. Para cambiar de agente, abre una conversación nueva.",
        "suggested_questions": ["abrir", "estado", "continuar"],
        "file_upload": {"enabled": False}, "retriever_resource": {"enabled": False},
        "speech_to_text": {"enabled": False}, "text_to_speech": {"enabled": False, "voice": "", "language": ""},
        "suggested_questions_after_answer": {"enabled": False}, "sensitive_word_avoidance": {"enabled": False}}
    return {"graph": {"nodes": nodos, "edges": aristas}, "features": features,
            "environment_variable_patch": {"environment_variables": [ENV_TOKEN]},
            "conversation_variables": []}


def main():
    datos = generar()
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(datos, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    ramas = sum(1 for n in datos["graph"]["nodes"] if n["data"]["type"] == "llm")
    print(f"✅ {SALIDA.relative_to(NUCLEO)}: {ramas} agentes, {len(datos['graph']['nodes'])} nodos.")


if __name__ == "__main__":
    main()
