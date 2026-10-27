# Prompt 07: implement the plan

Before pasting: type `/clear`. The plan is in the folder, not in the chat. `notes/analysis_plan.md` exists.
Suggested setting: Opus, effort `high`.

---

Read `CLAUDE.md`, `notes/analysis_plan.md` and `code/00_inspect.py`. Your job is to implement this plan, not a better one.

1. **Ambiguities first, no code yet.** List every point where the plan is silent, ambiguous, or does not fit the data: join type, rows that will not match, duplicates, missing-value codes, identifier formats, filters, units, differences of period or geography between files. Number them. Ask me about each one and wait for my answers. Add my answers to the plan under a heading "Decisions at implementation (prompt 07), <date>".
2. **Implement** in numbered scripts in `code/`, one step per script (for example `01_clean_<source>.py`, `02_merge.py`, `03_describe.py`). Each script reads from `data/raw/` or `data/processed/` and writes to `data/processed/` or `outputs/`.
3. **Row counts.** Every script prints the number of rows before and after every filter, drop, deduplication, reshape and merge. For every merge, it also prints the number of unmatched keys on each side, with five examples of each. Collect these lines, step by step, in `outputs/row_counts.md`.
4. **Stop rule.** If a row count changes in a way the plan does not explain, stop and tell me. Do not fix it on your own.
5. **Run** the scripts in order. Show me the row-count trail and the first table or figure the plan asks for.
6. **Labels.** List every file you wrote with three labels: origin "agent", status "exploratory", checked "not yet". Only I change status and checked.

If you think the plan is wrong, say so and wait. Do not modify anything in `data/raw/`.
