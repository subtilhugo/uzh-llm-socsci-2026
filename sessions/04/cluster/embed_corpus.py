"""Embed every document of a corpus fetched by fetch_corpus.py, on a GPU if there is one.

    python embed_corpus.py --download-only        # once, on a node that reaches the internet
    python embed_corpus.py --corpus /scratch/$USER/archelec/1978-03-12

Each text is cut into passages of about 80 words; each passage becomes a vector of 384 numbers
(multilingual-e5-small, MIT licence, French included). A document is the mean of its passages.

writes, in <corpus>/embeddings/:
    passages.csv        doc_id, passage number, passage text
    passages.npy        one row per passage (float16)
    docs.npy, docs.txt  one row per document, and the order of the documents
    run.json            model, device, number of passages, seconds: what a referee would ask
"""
import argparse
import datetime
import json
import pathlib
import re
import time

import numpy as np
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer


def passages(text, words=80):
    w = re.sub(r"\s+", " ", text).split(" ")
    return [" ".join(w[i:i + words]) for i in range(0, len(w), words) if len(w[i:i + words]) >= 10]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus")
    ap.add_argument("--model", default="intfloat/multilingual-e5-small")
    ap.add_argument("--words", type=int, default=80)
    ap.add_argument("--batch", type=int, default=128)
    ap.add_argument("--download-only", action="store_true", help="download the model into $HF_HOME, then stop")
    a = ap.parse_args()
    if a.download_only:
        SentenceTransformer(a.model, device="cpu")
        print("model ready:", a.model)
        return

    assert a.corpus, "--corpus is required"
    corpus = pathlib.Path(a.corpus)
    out = corpus / "embeddings"
    out.mkdir(exist_ok=True)
    rows = [(p.stem, j, s) for p in sorted((corpus / "texts").glob("*.txt"))
            for j, s in enumerate(passages(p.read_text(encoding="utf-8"), a.words))]
    df = pd.DataFrame(rows, columns=["doc_id", "passage", "text"])
    print(f"{df.doc_id.nunique()} documents, {len(df)} passages")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    gpu = torch.cuda.get_device_name(0) if device == "cuda" else None
    print("device:", device, gpu or "")
    model = SentenceTransformer(a.model, device=device)
    t0 = time.time()
    # e5 models expect a prefix; "query: " for similarity between texts of the same kind.
    emb = model.encode(["query: " + t for t in df.text], batch_size=a.batch,
                       normalize_embeddings=True, show_progress_bar=True)
    seconds = round(time.time() - t0, 1)

    df.to_csv(out / "passages.csv", index=False)
    np.save(out / "passages.npy", emb.astype(np.float16))
    docs = df.doc_id.drop_duplicates().tolist()
    doc_emb = np.vstack([emb[(df.doc_id == d).values].mean(0) for d in docs])
    doc_emb /= np.linalg.norm(doc_emb, axis=1, keepdims=True)
    np.save(out / "docs.npy", doc_emb.astype(np.float16))
    (out / "docs.txt").write_text("\n".join(docs))
    run = {"date_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "model": a.model,
           "words_per_passage": a.words, "device": device, "gpu": gpu, "documents": len(docs),
           "passages": len(df), "seconds": seconds}
    (out / "run.json").write_text(json.dumps(run, indent=1))
    print(json.dumps(run, indent=1))

    # A first look: the five passages closest to a local promise.
    q = model.encode(["query: Je me battrai pour la déviation de la route nationale qui traverse notre ville."],
                     normalize_embeddings=True)[0]
    for i in np.argsort(-emb @ q)[:5]:
        print(round(float(emb[i] @ q), 3), df.doc_id[i], "|", df.text[i][:120])


if __name__ == "__main__":
    main()
