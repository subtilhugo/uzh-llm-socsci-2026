# Prompt 07: clean, merge, describe

Before pasting: type `/clear`. The plan is in the folder, not in the chat. `notes/analysis_plan.md` and `notes/codebook.md` exist.
Suggested setting: Opus, effort `high`.

---

Read `CLAUDE.md`, `notes/analysis_plan.md`, `notes/codebook.md` and `code/00_inspect.py`. Implement this plan, not a better one. Everything you produce is a script in `code/`, never a number in the chat: every table and figure must be regenerable.

1. **Ambiguities first, no code.** List every point where the plan is silent, ambiguous, or does not fit the data: join type, rows that will not match, duplicates, missing-value codes, identifier formats, filters, units, differences of period or geography between files. Number them, ask me, and wait. Add my answers to the plan under "Decisions at implementation (prompt 07), <date>".
2. **Clean and merge** in numbered scripts, one step per script. Each reads from `data/raw/` or `data/processed/` and writes to `data/processed/` or `outputs/`.
3. **Checks, written into the scripts.**
   - Row counts before and after every filter, drop, deduplication, reshape and merge. For every merge, the unmatched keys on each side, with five examples. Collect them, step by step, in `outputs/row_counts.md`.
   - Assertions that stop the script when they fail: unique keys, no missing identifiers, values within their range, totals preserved where they must be, and the known number in the plan's "Checks".
   - Cross-tabulations after every recode (old value × new value) and after every merge (matched or not × a grouping variable such as region or wave), saved in `outputs/tables/`.
   - Stop rule: if a row count changes in a way the plan does not explain, stop and tell me. Do not fix it on your own.
4. **Describe**, in a script: a table of summary statistics, the table the plan asks for, and at most two figures, each with its number of observations, in `outputs/`.
5. **Preliminary insights** in `notes/insights.md`: at most five bullet points, each with its number and the table or figure it comes from. Descriptive language only.
6. **`code/run_all.py`** runs every script in order, from the raw data to the figures. Run it. Show me the row-count trail, the summary statistics and the figures, and list every file you wrote.

If you think the plan is wrong, say so and wait. Do not modify the data files in `data/raw/`.
