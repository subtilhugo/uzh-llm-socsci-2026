# The prompts

Paste them as they are, or type `Follow @prompts/<file>` in the agent. Adapt them as the project grows.
They are versioned with the project: when you change one, the change is in git.

| Prompt | What it does | When |
| --- | --- | --- |
| `01_fill_context.md` | The agent interviews you and fills `README.md` and the conventions in `CLAUDE.md`. Nothing is invented: it writes what you answer. | Once, at the start |
| `02_literature_notes.md` | One note per PDF in `literature/`, with page references and a list of claims to verify. | Each time you add papers |
| `03_research_memo.md` | A one-page memo from `README.md` and the notes only. | After you have verified the notes |
| `04_critique.md` | A hostile reviewer: five weaknesses, proposed not applied. | On any memo or draft |
| `05_session_log.md` | The entry in `PROJECT_HISTORY.md` and the commit. | At the end of every session |
| `06_analysis_plan.md` | The agent inspects the raw data with a script, completes `data/raw/README.md`, writes `notes/codebook.md`, interviews you, and writes `notes/analysis_plan.md`. | Before any analysis code |
| `07_implement.md` | A first agent lists what the plan leaves open, then cleans, merges and describes in numbered scripts, with row counts, assertions and cross-tabulations, summary statistics, figures, preliminary insights and `code/run_all.py`. | After the plan, in a cleared session |
| `08_review.md` | A fresh session reviews plan, codebook, code and outputs like a referee, and lists the problems. You decide. | After every implementation |
| `09_audit_by_hand.md` | You audit one step yourself: the agent explains the code line by line and points you to three units in the raw data; you read and compute their values by hand. | After the review |
| `10_collect_api.md` | The agent reads the API documentation and its terms, asks you what to collect, proposes checks against numbers the provider publishes, then writes a collector that archives every raw response and a parser that reports the checks. | When you collect from an API |
| `11_annotate_llm.md` | Codebook with you, your own coding of 100 texts first, then a pipeline (prompt in a file, JSON schema, every raw answer kept), a pilot on 20, a validation against your codes, and the full run only after your decision. | Before you put model labels in a paper |
| `12_classical_measure.md` | A dictionary you edit, embeddings, a search, a classifier scored by cross-validation, all validated against your random hand codes. | Before you reach for an LLM, or to check one |
| `13_extract_llm.md` | A form with you, a reference for each field (or your own extraction of 30 documents), a pipeline with a JSON schema, a pilot, a check field by field, then the merge. | When you turn documents into a table |
| `14_estimate_with_labels.md` | The hand-coded sample checked for randomness, agreement by group, and three estimates (hand codes only, naive, corrected), then the measurement section of the paper. | Before a coefficient built on model labels goes in a paper |

Why written prompts rather than typing? Because a prompt is part of the method. In a year, you will want to know
exactly what you asked the agent to do, and so will a referee.
