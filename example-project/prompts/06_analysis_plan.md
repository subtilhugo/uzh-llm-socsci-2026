# Prompt 06: the analysis plan

Before pasting: your raw data is in `data/raw/<source>/`, and its source is written in `data/raw/README.md`.
Suggested setting: Fable (`/model fable`), effort `high`. Without access to Fable: Opus, effort `high`.

---

Before any analysis code, we write an analysis plan together. You inspect the data, you interview me, you write the plan. You do not decide anything about the analysis: I do.

1. **Inspect, read-only.** List the files in `data/raw/` and ask me which ones this analysis uses. For those files, write and run `code/00_inspect.py`. It changes nothing and prints, for each file: rows and columns; column names and types; missing values per column; values that look like missing-value codes (-9, 99, 999, "s", "NA", empty strings); the identifier columns and whether they are unique; and the period, wave or geography the file says it covers. Look at every sheet and header line, not only the data table. Show me this summary. Never print more than 10 rows of a file.
2. **Interview me**, one question at a time, to fill `notes/templates/analysis_plan.md`. Start with what the inspection revealed: anything surprising, any two files that do not describe the same units, period or geography. Keep each question short. If I answer "don't know", write the point in "Open questions". Do not choose for me.
3. **Write the plan** in `notes/analysis_plan.md`, following the template. Show it to me and wait for my "ok" before saving.

Rules: no code except the inspection script. Do not modify anything in `data/raw/`. Every choice in the plan comes from my answers; anything I did not settle is an open question, not a default.
