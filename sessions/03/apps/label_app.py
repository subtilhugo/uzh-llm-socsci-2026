"""Label texts with local models, through the Ollama API.

    pip install streamlit pandas requests scikit-learn
    streamlit run label_app.py

Every label comes from one HTTP request to the Ollama server on this machine (http://localhost:11434).
Nothing leaves the machine, unless you pick a cloud model (a tag ending in "cloud").
The app shows the exact request and response, so you can see what "calling an API" means.
"""

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests
import streamlit as st
from sklearn.metrics import accuracy_score, cohen_kappa_score, f1_score

HERE = Path(__file__).parent

LABELS = ["external_relations", "freedom_democracy", "political_system", "economy",
          "welfare_quality_of_life", "fabric_of_society", "social_groups", "no_category"]

CODEBOOK = """You are an expert coder for the Manifesto Project (MARPOR). You code quasi-sentences of party
manifestos into policy domains. The texts are in French; reason about the meaning, not the words.

Assign exactly one domain to the text:
- external_relations: other countries, the military, peace, internationalism, the European Union.
- freedom_democracy: freedom and human rights, democracy, constitutionalism.
- political_system: decentralisation, administrative efficiency, corruption, political authority.
- economy: markets, regulation, planning, protectionism, growth, infrastructure, budget discipline.
- welfare_quality_of_life: environment, culture, equality, welfare state, education.
- fabric_of_society: national way of life, traditional morality, law and order, multiculturalism.
- social_groups: workers, farmers, middle class, minorities, women, the elderly, the young.
- no_category: no policy content.

Give a one-sentence reason in English, then the label."""


# ---------------------------------------------------------------- the API, in five functions

def api(url, path, payload=None, timeout=600):
    """One request to the Ollama server. GET if no payload, POST otherwise."""
    if payload is None:
        r = requests.get(url + path, timeout=10)
    else:
        r = requests.post(url + path, json=payload, timeout=timeout)
    r.raise_for_status()
    return r.json()


def schema(labels):
    """The JSON schema the answer must follow: a reason first, then one label from the list."""
    return {"type": "object",
            "properties": {"reason": {"type": "string"}, "label": {"type": "string", "enum": labels}},
            "required": ["reason", "label"]}


def build_request(model, system, text, labels, temperature, seed, num_ctx, think):
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": text}],
        "format": schema(labels),       # structured output: the server forces valid JSON
        "options": {"temperature": temperature, "seed": seed, "num_ctx": num_ctx},
        "stream": False,
    }
    if think is not None:               # only for models that can think (Qwen 3.5, gpt-oss, ...)
        payload["think"] = think
    return payload


def label_one(url, payload):
    t0 = time.time()
    data = api(url, "/api/chat", payload)
    seconds = time.time() - t0
    out = json.loads(data["message"]["content"])
    tok_s = data.get("eval_count", 0) / max(data.get("eval_duration", 1), 1) * 1e9
    return {"label": out.get("label"), "reason": out.get("reason"), "seconds": round(seconds, 2),
            "tokens_in": data.get("prompt_eval_count"), "tokens_out": data.get("eval_count"),
            "tokens_per_s": round(tok_s, 1)}, data


@st.cache_data(ttl=30, show_spinner=False)
def server_state(url):
    version = api(url, "/api/version")["version"]
    models = api(url, "/api/tags")["models"]
    return version, models


@st.cache_data(show_spinner=False)
def model_card(url, model):
    s = api(url, "/api/show", {"model": model})
    det = s.get("details", {})
    ctx = next((v for k, v in s.get("model_info", {}).items() if k.endswith("context_length")), None)
    return {"capabilities": s.get("capabilities", []), "parameters": det.get("parameter_size"),
            "quantization": det.get("quantization_level"), "family": det.get("family"), "max_context": ctx}


# ---------------------------------------------------------------- the page

st.set_page_config(page_title="Local labeller", layout="wide")
st.title("Local labeller")

with st.sidebar:
    st.header("Server")
    url = st.text_input("Ollama URL", "http://localhost:11434").rstrip("/")
    try:
        version, models = server_state(url)
    except requests.RequestException as e:
        st.error(f"No Ollama server at {url}.\n\nStart it: open the Ollama app, or run `ollama serve` "
                 f"in a terminal.\n\n{type(e).__name__}")
        st.stop()
    st.caption(f"Ollama {version}, {len(models)} models on this machine")
    names = [m["name"] for m in models]
    if not names:
        st.warning("No model yet. In a terminal: `ollama pull qwen3.5:4b`")
        st.stop()
    default = [n for n in ("qwen3.5:4b", "ministral-3:8b") if n in names] or names[:1]
    chosen = st.multiselect("Models (pick two to compare them)", names, default=default)
    st.header("Parameters")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.0, 0.1)
    seed = st.number_input("Seed", value=42, step=1)
    num_ctx = st.select_slider("Context window (tokens)", [2048, 4096, 8192, 16384, 32768], value=4096)
    think = st.toggle("Let thinking models think", value=False,
                      help="Qwen 3.5 and gpt-oss think before answering: slower, sometimes better.")
    for m in chosen:
        card = model_card(url, m)
        digest = next(x["digest"] for x in models if x["name"] == m)
        cloud = m.endswith("cloud")
        st.markdown(f"**{m}**{' :red[cloud: your texts leave this machine]' if cloud else ''}  \n"
                    f"{card['parameters']}, {card['quantization']}, digest `{digest[:12]}`  \n"
                    f"{', '.join(card['capabilities'])}")

tab_data, tab_codebook, tab_results, tab_api = st.tabs(["1. Data", "2. Codebook", "3. Results", "The API call"])

with tab_codebook:
    labels_txt = st.text_input("Labels, comma separated", ", ".join(LABELS))
    labels = [x.strip() for x in labels_txt.split(",") if x.strip()]
    system = st.text_area("Codebook (the system prompt)", CODEBOOK, height=360)
    st.caption(f"sha256 {hashlib.sha256(system.encode()).hexdigest()[:16]}: goes into params.json")

with tab_data:
    up = st.file_uploader("A CSV, one text per row", type="csv")
    if up is not None:
        df = pd.read_csv(up)
    else:
        df = pd.read_csv(HERE / "example_sentences.csv")
        st.caption("No file: 24 example sentences, written for this demo (not Manifesto Project data), "
                   "with the label I would give.")
    cols = list(df.columns)
    text_col = st.selectbox("Text column", cols, index=cols.index("text") if "text" in cols else 0)
    gold_opts = ["(none)"] + cols
    gold_col = st.selectbox("Your own codes, if any (to validate)", gold_opts,
                            index=gold_opts.index("my_label") if "my_label" in cols else 0)
    n = st.slider("How many rows", 1, len(df), min(len(df), 24))
    st.dataframe(df.head(n), height=240)
    go = st.button("Label", type="primary", disabled=not chosen)

if go:
    rows, examples = [], {}
    bar = st.progress(0.0)
    total = n * len(chosen)
    k = 0
    for m in chosen:
        card = model_card(url, m)
        can_think = "thinking" in card["capabilities"]
        for i, text in enumerate(df[text_col].head(n).astype(str)):
            payload = build_request(m, system, text, labels, temperature, int(seed), num_ctx,
                                    think if can_think else None)
            try:
                res, raw = label_one(url, payload)
            except (requests.RequestException, json.JSONDecodeError, KeyError) as e:
                res, raw = {"label": None, "reason": f"ERROR {type(e).__name__}: {e}"[:200]}, None
            rows.append({"row": i, "model": m, "text": text, **res})
            if m not in examples and raw is not None:
                examples[m] = (payload, raw)
            k += 1
            bar.progress(k / total, text=f"{m}: {i + 1}/{n}")
    st.session_state["results"] = pd.DataFrame(rows)
    st.session_state["examples"] = examples
    st.session_state["params"] = {
        "date_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "server": url, "ollama_version": version,
        "models": {m: {"digest": next(x["digest"] for x in models if x["name"] == m), **model_card(url, m)}
                   for m in chosen},
        "options": {"temperature": temperature, "seed": int(seed), "num_ctx": num_ctx, "think": think},
        "labels": labels, "codebook_sha256": hashlib.sha256(system.encode()).hexdigest(),
        "n_texts": n, "text_column": text_col,
    }
    bar.empty()
    st.success("Done. See the tab 3. Results.")

with tab_results:
    res = st.session_state.get("results")
    if res is None:
        st.info("Run the labelling first (tab 1).")
    else:
        wide = res.pivot(index="row", columns="model", values="label")
        speed = res.groupby("model")[["seconds", "tokens_per_s"]].mean().round(2)
        st.subheader("Speed")
        st.dataframe(speed)
        st.subheader("Labels")
        show = df.head(n)[[text_col]].copy()
        if gold_col != "(none)":
            show["mine"] = df.head(n)[gold_col].values
        for m in wide.columns:
            show[m] = wide[m].values
        st.dataframe(show, height=300)

        scores = []
        if gold_col != "(none)":
            gold = df.head(n)[gold_col].astype(str).values
            for m in wide.columns:
                pred = wide[m].astype(str).values
                ok = pred != "None"
                scores.append({"comparison": f"{m} vs mine", "n": int(ok.sum()),
                               "accuracy": round(accuracy_score(gold[ok], pred[ok]), 2),
                               "macro_F1": round(f1_score(gold[ok], pred[ok], average="macro",
                                                          labels=sorted(set(gold[ok])), zero_division=0), 2),
                               "kappa": round(cohen_kappa_score(gold[ok], pred[ok]), 2)})
        if len(wide.columns) == 2:
            a, b = (wide[c].astype(str).values for c in wide.columns)
            scores.append({"comparison": f"{wide.columns[0]} vs {wide.columns[1]}", "n": len(a),
                           "accuracy": round((a == b).mean(), 2), "macro_F1": None,
                           "kappa": round(cohen_kappa_score(a, b), 2)})
        if scores:
            st.subheader("Agreement")
            st.dataframe(pd.DataFrame(scores), hide_index=True)
        if gold_col != "(none)":
            m = st.selectbox("Confusion matrix for", list(wide.columns))
            st.dataframe(pd.crosstab(pd.Series(df.head(n)[gold_col].values, name="mine"),
                                     pd.Series(wide[m].values, name=m)))
            dis = show[show["mine"].astype(str) != show[m].astype(str)]
            reasons = res[res.model == m].set_index("row")["reason"]
            st.subheader(f"Disagreements with {m}: who is right?")
            for i, r in dis.iterrows():
                st.markdown(f"- *{r[text_col]}*  \n  mine **{r['mine']}**, model **{r[m]}**: {reasons.get(i, '')}")

        st.subheader("Take it with you")
        c1, c2 = st.columns(2)
        c1.download_button("labels.csv", res.to_csv(index=False).encode(), "labels.csv", "text/csv")
        c2.download_button("params.json", json.dumps(st.session_state["params"], indent=2).encode(),
                           "params.json", "application/json")

with tab_api:
    ex = st.session_state.get("examples")
    if not ex:
        st.info("Run the labelling first: the first request and response of each model appear here.")
        st.code(f"curl {url}/api/tags", language="bash")
    else:
        m = st.selectbox("Model", list(ex))
        payload, raw = ex[m]
        st.markdown(f"**What the app sent** (`POST {url}/api/chat`)")
        st.code(json.dumps(payload, indent=2, ensure_ascii=False), language="json")
        st.markdown("**What the server answered**")
        st.code(json.dumps(raw, indent=2, ensure_ascii=False), language="json")
        st.markdown("**The same request from a terminal**: save the JSON above as `request.json`, then")
        st.code(f"curl {url}/api/chat -d @request.json", language="bash")
        st.download_button("request.json", json.dumps(payload, indent=2, ensure_ascii=False).encode(),
                           "request.json", "application/json")
