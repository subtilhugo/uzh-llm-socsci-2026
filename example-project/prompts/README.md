# The prompts

Paste them as they are, or type `Follow @prompts/<file>` in the agent. Adapt them as the project grows.
They are versioned with the project: when you change one, the change is in git.

| Prompt | What it does | When |
| --- | --- | --- |
| `01_fill_context.md` | The agent interviews you and fills `README.md` and the conventions in `CLAUDE.md`. Nothing is invented: it writes what you answer. | Once, at the start |
| `02_literature_notes.md` | One note per PDF in `literature/`, with page references and a list of claims to verify. | Each time you add papers |
| `03_research_memo.md` | A one-page memo from `README.md` and the notes only. | After you have verified the notes |
| `04_critique.md` | A hostile reviewer: five weaknesses, proposed not applied. | On any memo or draft |
| `05_session_log.md` | The entry in `PROJECT_HISTORY.md`, with the three labels on every output, and the commit. | At the end of every session |
| `06_analysis_plan.md` | The agent inspects the raw data without changing it, interviews you, and writes `notes/analysis_plan.md`. | Before any analysis code |
| `07_implement.md` | A first agent lists what the plan leaves open, then implements it in numbered scripts that print their row counts. | After the plan, in a cleared session |
| `08_review.md` | A fresh session reviews plan, code and outputs like a referee, and lists the discrepancies. You decide. | After every implementation |

Why written prompts rather than typing? Because a prompt is part of the method. In a year, you will want to know
exactly what you asked the agent to do, and so will a referee.
