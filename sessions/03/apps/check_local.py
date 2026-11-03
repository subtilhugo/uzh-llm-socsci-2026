"""Check, the evening before, that everything for Part 3 works on this machine. Two to five minutes.

    python check_local.py
    python check_local.py --models qwen3.5:4b ministral-3:8b    # other models

It tests the Ollama server, each model (a plain answer, a structured answer, a tool call), the APIs the
agent uses, and the command-line tools. Paste the summary at the end into the chat if something fails.
"""

import argparse
import importlib.util
import json
import shutil
import subprocess
import time

import requests

URL = "http://localhost:11434"
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, ok, detail))
    print(f"{'OK  ' if ok else 'FAIL'}  {name}  {detail}")


def chat(payload):
    t = time.time()
    r = requests.post(URL + "/api/chat", json={"stream": False, "options": {"temperature": 0, "seed": 1},
                                                **payload}, timeout=600)
    r.raise_for_status()
    return r.json(), time.time() - t


def test_model(m):
    caps = requests.post(URL + "/api/show", json={"model": m}, timeout=10).json().get("capabilities", [])
    think = False if "thinking" in caps else None
    base = {"model": m} | ({"think": think} if think is not None else {})

    # 1. A plain answer (the first call also loads the model into memory: slower)
    try:
        d, s = chat(base | {"messages": [{"role": "user", "content": "Réponds en un mot : capitale de la Suisse ?"}]})
        check(f"{m}: plain answer", True, f"{s:.1f} s (includes loading): {d['message']['content'].strip()[:40]!r}")
    except Exception as e:
        check(f"{m}: plain answer", False, str(e)[:120])
        return

    # 2. A structured answer: the schema of the labelling app
    schema = {"type": "object", "required": ["reason", "label"], "properties": {
        "reason": {"type": "string"},
        "label": {"type": "string", "enum": ["economy", "welfare_quality_of_life", "fabric_of_society"]}}}
    try:
        d, s = chat(base | {"format": schema, "messages": [
            {"role": "system", "content": "Classify the policy domain of the French manifesto sentence."},
            {"role": "user", "content": "Nous recruterons 10 000 policiers supplémentaires."}]})
        out = json.loads(d["message"]["content"])
        tok_s = d.get("eval_count", 0) / max(d.get("eval_duration", 1), 1) * 1e9
        check(f"{m}: structured answer", out.get("label") in schema["properties"]["label"]["enum"],
              f"{s:.1f} s, {tok_s:.0f} tokens/s, label={out.get('label')} (expected fabric_of_society)")
    except Exception as e:
        check(f"{m}: structured answer", False, str(e)[:120])

    # 3. A tool call: the agent needs this
    if "tools" not in caps:
        check(f"{m}: tool call", False, f"no 'tools' capability ({caps})")
        return
    tool = {"type": "function", "function": {"name": "calculate", "description": "Arithmetic.",
            "parameters": {"type": "object", "required": ["expression"],
                           "properties": {"expression": {"type": "string"}}}}}
    try:
        d, s = chat(base | {"tools": [tool], "messages": [
            {"role": "user", "content": "Use the calculate tool: what is 17.5% of 2340?"}]})
        calls = d["message"].get("tool_calls") or []
        args = calls[0]["function"]["arguments"] if calls else None
        check(f"{m}: tool call", bool(calls) and "expression" in (args or {}), f"{s:.1f} s, {args}")
    except Exception as e:
        check(f"{m}: tool call", False, str(e)[:120])


def main():
    global URL
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="*", default=["ministral-3:8b", "qwen3.5:4b", "qwen3.5:9b"])
    ap.add_argument("--url", default=URL)
    a = ap.parse_args()
    URL = a.url.rstrip("/")

    print("\n== Ollama server")
    try:
        v = requests.get(URL + "/api/version", timeout=5).json()["version"]
        major_minor = tuple(int(x) for x in v.split(".")[:2])
        check("server running", True, f"version {v}")
        check("version >= 0.15 (ollama launch claude)", major_minor >= (0, 15),
              "" if major_minor >= (0, 15) else "update: https://ollama.com/download")
        have = [m["name"] for m in requests.get(URL + "/api/tags", timeout=5).json()["models"]]
    except requests.RequestException:
        check("server running", False, "open the Ollama app, or run `ollama serve`")
        return summary()
    print("   models here:", ", ".join(have) or "none")

    print("\n== Models")
    for m in a.models:
        if m not in have:
            check(f"{m}: pulled", False, f"ollama pull {m}")
            continue
        test_model(m)

    print("\n== APIs (internet)")
    for name, url in [("OpenAlex (agent)", "https://api.openalex.org/works?per_page=1"),
                      ("geo.api.gouv.fr (agent)", "https://geo.api.gouv.fr/communes?nom=Lyon&limit=1"),
                      ("Manifesto Project API", "https://manifesto-project.wzb.eu/api/v1/list_core_versions"),
                      ("Anthropic API", "https://api.anthropic.com/v1/models")]:
        try:
            r = requests.get(url, timeout=10)
            check(name, r.status_code < 500, f"HTTP {r.status_code} (401 or 403 without a key is fine)")
        except requests.RequestException as e:
            check(name, False, type(e).__name__)

    print("\n== Command-line tools and packages")
    for cmd in ["ollama", "claude"]:
        path = shutil.which(cmd)
        if path:
            out = subprocess.run([cmd, "--version"], capture_output=True, text=True, timeout=20)
            check(f"{cmd} on PATH", True, (out.stdout or out.stderr).strip().splitlines()[0][:60])
        else:
            check(f"{cmd} on PATH", False, "not found")
    for pkg in ["streamlit", "pandas", "sklearn", "requests"]:
        check(f"python package {pkg}", importlib.util.find_spec(pkg) is not None,
              "" if importlib.util.find_spec(pkg) else f"pip install {'scikit-learn' if pkg == 'sklearn' else pkg}")
    try:
        loaded = requests.get(URL + "/api/ps", timeout=5).json().get("models", [])
        for m in loaded:
            print(f"   loaded now: {m['name']}, context {m.get('context_length', '?')} tokens, "
                  f"{m.get('size_vram', 0) / 1e9:.1f} GB in GPU memory")
    except requests.RequestException:
        pass
    summary()


def summary():
    bad = [r for r in RESULTS if not r[1]]
    print(f"\n== Summary: {len(RESULTS) - len(bad)} OK, {len(bad)} FAIL")
    for name, _, detail in bad:
        print(f"   FAIL {name}: {detail}")


if __name__ == "__main__":
    main()
