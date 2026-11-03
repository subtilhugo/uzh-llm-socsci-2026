# Prompt 11: annotate texts with an LLM, and validate against your own coding

Before pasting: your texts are in `data/processed/` (one row per text, with an identifier). You have written, in your words, what you want to code: the categories and one sentence of definition each. You have decided where the texts may go: a commercial API, or only a model on your machine or on the cluster (confidential data: local only).
Suggested setting: Opus, effort `high`. The annotation itself runs on a small model through a script, not in this chat.

---

We annotate a corpus with an LLM. The agent writes the pipeline; the codebook and the validation are mine. An annotation is usable when it agrees with careful human coding at least as well as two humans agree with each other.

1. **The codebook, with me.** From my categories, write `notes/codebook_annotation.md`: each category with its definition, one example that belongs, one that does not, and the rule for borderline cases. Ask me about every ambiguity. Do not add a category I did not ask for. Wait for my "ok".
2. **My gold standard first.** Draw a random sample of 100 texts with a fixed seed, stratified if I ask, and write it to `data/processed/gold_sample.csv` with an empty column `my_code`. I code them myself, before seeing any model output. Wait until I tell you it is done.
3. **The pipeline**, `code/20_annotate.py`. The prompt (the codebook) lives in `prompts/annotation_prompt.md`, not in the code. The answer follows a JSON schema (structured output), with a short reason before the label. The backend is a parameter: a commercial API (key from `.env`) or an OpenAI-compatible local server (Ollama, LM Studio, vLLM). Every raw answer is appended to `outputs/annotation/<run_id>/raw.jsonl` as it arrives, so a rerun never pays twice. It records the model ID (and for a local model, the digest and the quantization), the parameters, the date, and the tokens used.
4. **Pilot on 20 texts.** Show me the 20 answers with their reasons and the cost or time per text. Estimate the cost and time for the whole corpus. Wait.
5. **Validate**, `code/21_validate.py`, on my 100: accuracy, macro-F1 and Cohen's kappa against my codes; the confusion matrix; the 15 disagreements with the model's reasons; agreement with a second run of the same model on 30 texts; and, if the paper will use an aggregate (a share per party, a mean per year), that aggregate computed from my codes and from the model's. Write `outputs/annotation/<run_id>/validation.md`.
6. **I decide.** I read the disagreements and decide, for each, who is right. If I change the codebook, it is a new `run_id`: we rerun steps 4 and 5, and keep both runs.
7. **Only after my decision**: the full corpus, with `code/20_annotate.py`. Then the bundle in `outputs/annotation/<run_id>/`: the prompt, the schema, `params.json`, the raw answers, the validation.

Rules: never annotate the full corpus before step 6. Never send a text to a commercial API if I said the data is local only. Never present the model's labels as human coding. Every number comes from a script.
