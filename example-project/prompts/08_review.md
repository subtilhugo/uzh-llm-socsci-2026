# Prompt 08: independent review

Before pasting: close the session and open a new one in the same folder. The reviewer must not have seen the code being written.
Suggested setting: Opus, effort `xhigh`.

---

You did not write the code in this project. You are its referee.

Read `notes/analysis_plan.md` (including the decisions taken at implementation), `notes/codebook.md`, every script in `code/`, `outputs/row_counts.md`, the tables and figures in `outputs/`, and `notes/insights.md`.

1. **Rerun.** Copy `outputs/row_counts.md` to `outputs/row_counts_before_review.md`, then run `python3 code/run_all.py`. Check that you get the same row counts and the same numbers.
2. **Compare the plan, the codebook and the code**, line by line. Look above all for silent errors: rows dropped or added; missing-value codes used as values; duplicates removed; identifiers read as numbers or rebuilt; a join type or a library default the plan does not state; mislabelled variables (a label in the codebook or a figure that does not match what the code computes); units, denominators, filters, weights; and matches that are technically correct but join different things (the same code for a different territory, wave or period).
3. **Check the insights**: is each number in `notes/insights.md` the one in the table it cites? Is the language descriptive?
4. **For each problem**: where (file and line), what the plan says, what the code does, the consequence (how many rows, which number changes), severity (high, medium, low), and how I can check it by hand.
5. **Write** the review to `notes/review_<YYYY-MM-DD>.md`: a table, most severe first, with an empty column "Decision" for me. End with one paragraph: what you checked and found correct.

Rules: do not fix anything. Do not soften. A list of small problems that misses the one that changes the result is a failed review.
