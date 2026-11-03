"""A research agent in 200 lines: a local model, a loop, and five tools.

    pip install requests
    python local_agent.py                                   # the default task, qwen3.5:9b
    python local_agent.py "your task" --model qwen3.5:4b    # another task, a smaller model
    python local_agent.py --think                           # let a thinking model think

An agent is nothing more than this loop: the model reads the task and the list of tools, answers either
with text (done) or with a tool call; we run the tool and send the result back; repeat.

Same agent with Claude, through Anthropic's OpenAI-compatible endpoint (key in ANTHROPIC_API_KEY):
    python local_agent.py --backend openai --url https://api.anthropic.com/v1 --model claude-haiku-5-5
Any other OpenAI-compatible server works the same way (Ollama's /v1, LM Studio, vLLM).
"""

import argparse
import ast
import json
import operator
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

OUT = Path("agent_output")
DEFAULT_TASK = ("How many inhabitants do Lyon and Marseille have, and by what percentage is Marseille larger "
                "than Lyon? Then find the three most cited papers since 2023 on large language models for "
                "text annotation in political science. Write both answers, with your sources, "
                "to the file answer.md.")
SYSTEM = ("You are a careful research assistant. Use the tools to get every fact and every number; "
          "never write a number you did not get from a tool. Use calculate for arithmetic. "
          "When the task is done, answer in a few sentences and say which tool gave each fact.")


# ---------------------------------------------------------------- the tools (plain Python functions)

def search_papers(query: str, since_year: int = 2020, n: int = 5) -> list:
    """OpenAlex, a free index of scholarly works (no key)."""
    r = requests.get("https://api.openalex.org/works", timeout=20, params={
        "search": query, "filter": f"from_publication_date:{int(since_year)}-01-01",
        "sort": "cited_by_count:desc", "per_page": min(int(n), 10),
        "select": "display_name,publication_year,cited_by_count,doi,authorships"})
    r.raise_for_status()
    return [{"title": w["display_name"], "year": w["publication_year"], "cited_by": w["cited_by_count"],
             "doi": w["doi"],
             "first_author": (w["authorships"][0]["author"]["display_name"] if w["authorships"] else None)}
            for w in r.json()["results"]]


def find_commune(name: str) -> list:
    """geo.api.gouv.fr, the French government's API of municipalities (no key)."""
    r = requests.get("https://geo.api.gouv.fr/communes", timeout=20, params={
        "nom": name, "fields": "nom,code,population,codeDepartement", "boost": "population", "limit": 3})
    r.raise_for_status()
    return r.json()


_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv,
        ast.Pow: operator.pow, ast.Mod: operator.mod, ast.USub: operator.neg, ast.UAdd: operator.pos}


def calculate(expression: str) -> float:
    """Arithmetic only: + - * / ** % and parentheses. No names, no functions."""
    def ev(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](ev(node.left), ev(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](ev(node.operand))
        raise ValueError("only numbers and + - * / ** % are allowed")
    return round(ev(ast.parse(expression, mode="eval").body), 6)


def list_files() -> list:
    """Files in the current folder (not hidden, two levels deep)."""
    return sorted(str(p) for p in Path(".").glob("*") if not p.name.startswith(".")) + \
        sorted(str(p) for p in Path(".").glob("*/*") if not any(x.startswith(".") for x in p.parts))


def read_file(path: str) -> str:
    """Read a text file inside the current folder (first 6,000 characters)."""
    p = Path(path).resolve()
    if Path(".").resolve() not in p.parents:
        raise ValueError("only files inside the current folder")
    return p.read_text(errors="replace")[:6000]


def write_file(filename: str, content: str) -> str:
    """Write a file into agent_output/ (and nowhere else)."""
    OUT.mkdir(exist_ok=True)
    p = OUT / Path(filename).name
    p.write_text(content)
    return f"wrote {len(content)} characters to {p}"


TOOLS = {f.__name__: f for f in (search_papers, find_commune, calculate, list_files, read_file, write_file)}

# What the model sees: a name, a description, the parameters as a JSON schema.
SPECS = [
    {"type": "function", "function": {"name": "search_papers", "description": search_papers.__doc__,
     "parameters": {"type": "object", "required": ["query"], "properties": {
         "query": {"type": "string", "description": "search words, in English"},
         "since_year": {"type": "integer", "description": "first publication year"},
         "n": {"type": "integer", "description": "number of results, at most 10"}}}}},
    {"type": "function", "function": {"name": "find_commune", "description": find_commune.__doc__ +
     " Returns name, INSEE code, population, department.",
     "parameters": {"type": "object", "required": ["name"], "properties": {
         "name": {"type": "string", "description": "name of the municipality, e.g. Lyon"}}}}},
    {"type": "function", "function": {"name": "calculate", "description": calculate.__doc__,
     "parameters": {"type": "object", "required": ["expression"], "properties": {
         "expression": {"type": "string", "description": "e.g. (870000 - 520000) / 520000 * 100"}}}}},
    {"type": "function", "function": {"name": "list_files", "description": list_files.__doc__,
     "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "read_file", "description": read_file.__doc__,
     "parameters": {"type": "object", "required": ["path"], "properties": {"path": {"type": "string"}}}}},
    {"type": "function", "function": {"name": "write_file", "description": write_file.__doc__,
     "parameters": {"type": "object", "required": ["filename", "content"], "properties": {
         "filename": {"type": "string"}, "content": {"type": "string"}}}}},
]


# ---------------------------------------------------------------- one call to the model, two dialects

def call_ollama(url, model, messages, think, key=None):
    payload = {"model": model, "messages": messages, "tools": SPECS, "stream": False,
               "options": {"temperature": 0, "num_ctx": 16384}}
    if think is not None:
        payload["think"] = think
    r = requests.post(url + "/api/chat", json=payload, timeout=900)
    r.raise_for_status()
    data = r.json()
    msg = data["message"]
    calls = [(c.get("id"), c["function"]["name"], c["function"].get("arguments") or {})
             for c in msg.get("tool_calls") or []]
    usage = (data.get("prompt_eval_count", 0), data.get("eval_count", 0))
    return msg, msg.get("content") or "", msg.get("thinking") or "", calls, usage


def call_openai(url, model, messages, think, key=None):
    r = requests.post(url + "/chat/completions", timeout=900,
                      headers={"Authorization": f"Bearer {key}"} if key else {},
                      json={"model": model, "messages": messages, "tools": SPECS, "temperature": 0,
                            "max_tokens": 2000})
    r.raise_for_status()
    data = r.json()
    msg = data["choices"][0]["message"]
    calls = []
    for c in msg.get("tool_calls") or []:
        try:
            args = json.loads(c["function"].get("arguments") or "{}")
        except json.JSONDecodeError:
            args = {"_malformed": c["function"].get("arguments")}
        calls.append((c.get("id"), c["function"]["name"], args))
    u = data.get("usage") or {}
    return msg, msg.get("content") or "", "", calls, (u.get("prompt_tokens", 0), u.get("completion_tokens", 0))


def tool_message(backend, call_id, name, content):
    if backend == "openai":
        return {"role": "tool", "tool_call_id": call_id, "content": content}
    return {"role": "tool", "tool_name": name, "content": content}


# ---------------------------------------------------------------- the loop

def color(code, s):
    return f"\033[{code}m{s}\033[0m" if sys.stdout.isatty() else s


def run(task, backend, url, model, think, max_steps, key):
    call = call_ollama if backend == "ollama" else call_openai
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": task}]
    OUT.mkdir(exist_ok=True)
    log_path = OUT / f"run_{datetime.now():%Y%m%d_%H%M%S}.jsonl"
    log = log_path.open("w")
    log.write(json.dumps({"task": task, "backend": backend, "url": url, "model": model, "think": think}) + "\n")
    n_calls, n_errors, tokens, t0 = 0, 0, [0, 0], time.time()
    print(color("1", f"\nTask: {task}\nModel: {model} ({backend}, {url})\n"))

    for step in range(1, max_steps + 1):
        t = time.time()
        msg, text, thinking, calls, usage = call(url, model, messages, think, key)
        tokens[0] += usage[0]
        tokens[1] += usage[1]
        messages.append(msg)
        if thinking:
            print(color("2", f"[step {step}] thinking: {thinking[:400]}{'...' if len(thinking) > 400 else ''}"))
        if not calls:
            print(color("32;1", f"[step {step}] answer ({time.time() - t:.1f} s)\n") + text)
            log.write(json.dumps({"step": step, "answer": text}) + "\n")
            break
        for call_id, name, args in calls:
            n_calls += 1
            print(color("36", f"[step {step}] tool call: {name}({json.dumps(args, ensure_ascii=False)})"))
            try:
                if name not in TOOLS:
                    raise ValueError(f"unknown tool {name}")
                result = json.dumps(TOOLS[name](**args), ensure_ascii=False)
            except Exception as e:          # the model sees the error and can correct itself
                n_errors += 1
                result = json.dumps({"error": f"{type(e).__name__}: {e}"})
            preview = result if len(result) < 300 else result[:300] + "..."
            print(color("33", f"           result: {preview}"))
            log.write(json.dumps({"step": step, "tool": name, "args": args, "result": result[:4000]},
                                 ensure_ascii=False) + "\n")
            messages.append(tool_message(backend, call_id, name, result))
        print(color("2", f"           ({time.time() - t:.1f} s)"))
    else:
        print(color("31;1", f"\nStopped after {max_steps} steps without a final answer."))

    print(color("1", f"\n{n_calls} tool calls, {n_errors} errors, {tokens[0]:,} tokens in, {tokens[1]:,} out, "
                     f"{time.time() - t0:.0f} s. Transcript: {log_path}"))
    log.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("task", nargs="?", default=DEFAULT_TASK)
    ap.add_argument("--model", default="qwen3.5:9b")
    ap.add_argument("--backend", choices=["ollama", "openai"], default="ollama")
    ap.add_argument("--url", default="http://localhost:11434")
    ap.add_argument("--think", action="store_true", help="let a thinking model think (slower)")
    ap.add_argument("--max-steps", type=int, default=10)
    ap.add_argument("--key-env", default="ANTHROPIC_API_KEY", help="env variable with the key (openai backend)")
    a = ap.parse_args()
    key = os.environ.get(a.key_env) if a.backend == "openai" else None
    think = None
    try:
        if a.backend == "ollama":
            shown = requests.post(a.url.rstrip("/") + "/api/show", json={"model": a.model}, timeout=10)
            if shown.status_code == 404:
                sys.exit(f"{a.model} is not on this machine. In a terminal: ollama pull {a.model}")
            caps = shown.json().get("capabilities", [])
            if "tools" not in caps:
                sys.exit(f"{a.model} cannot call tools (capabilities: {caps}). Try qwen3.5:9b or ministral-3:8b.")
            think = a.think if "thinking" in caps else None
        run(a.task, a.backend, a.url.rstrip("/"), a.model, think, a.max_steps, key)
    except requests.ConnectionError:
        sys.exit(f"No server at {a.url}. Start Ollama (the app, or `ollama serve`).")
    except requests.HTTPError as e:
        body = e.response.text[:300] if e.response is not None else ""
        sys.exit(f"The server refused the request: {e}\n{body}")
