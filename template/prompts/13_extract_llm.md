# Prompt 13: extract variables from documents with an LLM, and check them field by field

Before pasting: your documents are in `data/raw/` or `data/processed/` (one file or one row per document, with an identifier). You know which variables you want from each document, and whether a reference exists for some of them (a catalogue, metadata, an official register, a dataset someone else coded). You have decided where the documents may go: a commercial API, or only a model on your machine or on the cluster.
Suggested setting: Opus, effort `high`. The extraction itself runs on a small model through a script, not in this chat.

---

We turn documents into a table. The agent writes the pipeline; the form and the checks are mine. An empty field is an answer; an invented value is an error.

1. **The form, with me.** From my list of variables, write `notes/extraction_form.md`: each field, its type (text, number, date, a closed list, a list), what counts, what does not, and an example from a real document. Ask me about every ambiguity, in particular who is who when a document names several people or organisations, and past versus current. Do not add a field I did not ask for. Wait for my "ok".
2. **The reference.** Tell me which fields can be checked against an existing source, and how to get it (an API, a file). If no field can, draw 30 documents at random with a fixed seed into `data/processed/extraction_check.csv`; I fill in the fields by hand before seeing any model output. Wait until I tell you it is done.
3. **The pipeline**, `code/40_extract.py`. The instructions live in `prompts/extraction_prompt.md`, the form is a JSON schema (structured output) generated from `notes/extraction_form.md`. The instructions say: copy as printed, leave empty rather than guess, the evidence before any judgement. The backend is a parameter (a commercial API, key from `.env`, or an OpenAI-compatible local server). Long documents: say how many are cut, and where. Every raw answer is appended to `outputs/extraction/<run_id>/raw.jsonl` as it arrives; record the model ID, the date, the parameters and the tokens.
4. **Pilot on 20 documents**, two models if I have two keys. Show me the 20 forms next to the reference, and the cost per document. Wait.
5. **Check, field by field**, `code/41_check_extraction.py`: for each field, match, mismatch, model only (the reference is empty), reference only (the model left it empty), both empty. Names compared after normalisation; free text by word overlap, which you report as such. Then ten disagreements per field with the passage of the document. Write `outputs/extraction/<run_id>/check.md`.
6. **I decide**, field by field: keep, fix the form and rerun (a new `run_id`), or drop the field.
7. **Only after my decision**: the whole corpus, then `data/processed/extracted.csv`, merged with the rest of the project on keys I approve, with the row counts before and after the merge.

Rules: never run the whole corpus before step 6. Never send a document to a commercial API if I said the data is local only. Never fill a field from your own knowledge rather than from the document. Every number comes from a script.
