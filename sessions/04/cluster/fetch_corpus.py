"""Download the professions de foi of one French legislative election from Archelec (Internet Archive).

Archelec is the electoral archive of Sciences Po (CEVIPOF), published on Internet Archive.
Each document comes with a catalogue record written by Sciences Po (candidate, profession,
current mandates, party support, substitute) and an OCR text.

    python fetch_corpus.py --date 1978-03-12 --out /scratch/$USER/archelec

writes, in <out>/<date>/:
    ids.json            every identifier the search returned, with numFound and the query
    metadata.jsonl      the catalogue record of each document, raw, one per line
    texts/<id>.txt      the OCR text of each document
    fetch_log.json      requested / returned / missing, and the time of the collection

Rerun it after a failure: what is already on disk is not downloaded again.
The texts are under a restrictive licence (CC BY-NC-ND, rights "RESTRICTED"): keep them
out of any public repository.
"""
import argparse
import datetime
import json
import pathlib
import random
import time
from concurrent.futures import ThreadPoolExecutor

import requests

SEARCH = "https://archive.org/advancedsearch.php"
COLLECTION = "archiveselectoralesducevipof"
HEADERS = {"User-Agent": "uzh-llm-socsci-2026 (course; contact hugo.subtil@ipz.uzh.ch)"}


def get(url, params=None, tries=5):
    """GET with retries. Raises after the last try: a silent failure is the worst kind."""
    for i in range(tries):
        try:
            r = requests.get(url, params=params, headers=HEADERS, timeout=60)
            if r.status_code == 200:
                return r
            if r.status_code == 404:
                return None
        except requests.RequestException:
            pass
        time.sleep(2 ** i)
    raise RuntimeError(f"failed after {tries} tries: {url}")


def search_ids(date, doc_type="profession de foi"):
    q = f'collection:{COLLECTION} AND date:{date} AND type:"{doc_type}"'
    params = {"q": q, "fl[]": "identifier", "sort[]": "identifier asc", "rows": 10000, "output": "json"}
    resp = get(SEARCH, params).json()["response"]
    ids = [d["identifier"] for d in resp["docs"]]
    return {"query": q, "numFound": resp["numFound"], "ids": ids}


def fetch_one(identifier, folder):
    """Catalogue record and OCR text of one document. Returns (identifier, metadata or None, ok)."""
    txt = folder / "texts" / f"{identifier}.txt"
    meta = get(f"https://archive.org/metadata/{identifier}")
    meta = meta.json().get("metadata") if meta is not None else None
    if not txt.exists():
        r = get(f"https://archive.org/download/{identifier}/{identifier}_djvu.txt")
        if r is not None:
            txt.write_text(r.text, encoding="utf-8")
    return identifier, meta, txt.exists() and txt.stat().st_size > 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default="1978-03-12", help="election day, e.g. 1978-03-12 (first round, 1978)")
    ap.add_argument("--out", default="archelec")
    ap.add_argument("--sample", type=int, default=0, help="0 = every document; N = a random sample of N")
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()

    folder = pathlib.Path(a.out) / a.date
    (folder / "texts").mkdir(parents=True, exist_ok=True)

    found = search_ids(a.date)
    ids = found["ids"]
    # Check 1: the search returned every document it found (no silent truncation).
    assert len(ids) == found["numFound"], f"search returned {len(ids)} of {found['numFound']}: paginate"
    (folder / "ids.json").write_text(json.dumps(found, indent=1))
    if a.sample:
        ids = sorted(random.Random(a.seed).sample(ids, a.sample))
    print(f"{found['numFound']} documents found, {len(ids)} to fetch")

    done = {}
    meta_path = folder / "metadata.jsonl"
    if meta_path.exists():
        for line in meta_path.read_text().splitlines():
            rec = json.loads(line)
            done[rec["identifier"]] = rec
    todo = [i for i in ids if i not in done or not (folder / "texts" / f"{i}.txt").exists()]

    with ThreadPoolExecutor(a.workers) as pool, meta_path.open("a") as f:
        for k, (identifier, meta, ok) in enumerate(pool.map(lambda i: fetch_one(i, folder), todo), 1):
            if meta is not None and identifier not in done:
                f.write(json.dumps(meta, ensure_ascii=False) + "\n")
                done[identifier] = meta
            if k % 200 == 0:
                print(f"  {k}/{len(todo)}")

    texts = {p.stem for p in (folder / "texts").glob("*.txt") if p.stat().st_size > 0}
    missing = [i for i in ids if i not in done or i not in texts]
    log = {"date_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "query": found["query"],
           "numFound": found["numFound"], "requested": len(ids), "returned": len(ids) - len(missing),
           "missing": missing}
    (folder / "fetch_log.json").write_text(json.dumps(log, indent=1))
    # Check 2: requested = returned + missing. Read the list of missing before you go on.
    print(f"requested {log['requested']} = returned {log['returned']} + missing {len(missing)}")


if __name__ == "__main__":
    main()
