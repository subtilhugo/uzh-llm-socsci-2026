# Prompt 08: independent review

Before pasting: close the session and open a new one in the same folder. The reviewer must not have seen the code being written.
Suggested setting: Opus, effort `xhigh`.

---

You did not write the code in this project. You are its referee.

Read `notes/analysis_plan.md` (including the decisions taken at implementation), every script in `code/`, `outputs/row_counts.md`, and the outputs the plan lists.

1. **Rerun** the scripts in order. Check that you get the row counts in `outputs/row_counts.md`.
2. **Compare the plan and the code**, line by line. Look above all for silent decisions: rows dropped or added; missing-value codes used as values; duplicates removed; identifiers read as numbers or rebuilt; a join type or a library default the plan does not state; units, denominators, filters, weights; and matches that are technically correct but join different things (the same code for a different territory, wave or period).
3. **For each discrepancy**: where (file and line), what the plan says, what the code does, the consequence (how many rows, which number changes), severity (high, medium, low), and how I can check it myself.
4. **Write** the review to `notes/review_<YYYY-MM-DD>.md`: a table, most severe first, with an empty column "Decision" for me. End with one paragraph: what you checked and found correct.

Rules: do not fix anything. Do not soften. If you find nothing serious, say so and say what you checked. A list of small problems that misses the one that changes the result is a failed review.
