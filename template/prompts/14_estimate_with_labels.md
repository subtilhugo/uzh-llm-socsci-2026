# Prompt 14: an estimate from model labels that a referee can accept

Before pasting: a variable of your analysis comes from a model (an LLM, a classifier, a dictionary) and you have coded a sample of the same documents by hand. You know the regression or the statistic you want to report.
Suggested setting: Opus, effort `high`.

---

A variable in my analysis is measured by a model. Its errors do not wash out: for a 0/1 label they shrink the estimate when they are unrelated to X, and they can push it either way when they are. We report the estimate corrected with my hand codes, next to the naive one.

1. **The design of the hand codes.** Read how my hand-coded sample was drawn (in `PROJECT_HISTORY.md`, the scripts, or ask me). The correction needs a sample drawn at random, with a known probability for each document. If documents were chosen by hand, or the probability is unknown, stop and tell me: we draw a new random sample (prompt 11, step 2) and I code it.
2. **The variables.** `code/50_estimate.py` builds one table: the model's label, my code when it exists, an indicator that the document was hand-coded, its probability of being hand-coded, and the explanatory variables. Report the counts.
3. **Agreement first.** My codes against the model's labels: accuracy, kappa, and the confusion matrix separately for each value of the main explanatory variable. If the errors differ between groups, say so in one sentence.
4. **Three estimates**, with robust standard errors: from my hand codes only; naive, from the model's labels; corrected, with the design-based supervised learning pseudo-outcome (Egami et al. 2023): `label + (hand_coded / probability) * (my_code - label)`, regressed on the same variables. If the model was trained on my hand codes (a classifier), use cross-fitted predictions for the hand-coded documents. Save the table and a figure to `outputs/estimates/`.
5. **The section for the paper**, `notes/measurement_section.md`: the codebook and model (ID, date, settings), how the hand-coded sample was drawn and its size, who coded, the agreement, the three estimates with their intervals, and one paragraph on what changes between naive and corrected. Every number is read from the files of step 4, with the file named.
6. **I read it and decide** which estimate the paper reports. Write the decision in `PROJECT_HISTORY.md`.

Rules: never report only the naive estimate. Never drop hand-coded documents because they disagree with the model. Every number comes from a script.
