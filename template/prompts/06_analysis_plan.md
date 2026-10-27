# Prompt 06: document the data, then plan the analysis

Before pasting: your raw data is in `data/raw/<source>/`.
Suggested setting: Fable (`/model fable`), effort `high`. Without access to Fable: Opus, effort `high`.

---

Before any analysis code, we document the data and write an analysis plan. You inspect, you document, you interview me, you write the plan. You decide nothing about the analysis: I do.

1. **Inspect, with a script.** List the files in `data/raw/` and ask me which ones this analysis uses. Write and run `code/00_inspect.py`. It changes nothing and prints, for each file: rows and columns; column names and types; missing values per column; values that look like missing-value codes (-9, 99, 999, "s", "NA", empty strings); the identifier columns and whether they are unique; and the period, wave or geography the file says it covers. Look at every sheet, header line and documentation tab, not only the data table. Never print more than 10 rows of a file.
2. **Document.** Complete `data/raw/README.md`: one line per file, with source, date and access conditions; write "to verify" where you do not know. It is the only file you may edit in `data/raw/`. Then write `notes/codebook.md` following `notes/templates/codebook.md`: one line per variable we will use. Only what the files or their documentation say; mark anything you inferred "inferred, to verify".
3. **Interview me**, one question at a time, to fill `notes/templates/analysis_plan.md`. Start with what the inspection revealed: anything surprising, and any two files that do not describe the same units, period or geography. If I answer "don't know", write the point in "Open questions". Do not choose for me.
4. **Write the plan** in `notes/analysis_plan.md`. Show it to me and wait for my "ok" before saving.

Rules: no code except the inspection script. Every choice in the plan comes from my answers; anything I did not settle is an open question, not a default.
