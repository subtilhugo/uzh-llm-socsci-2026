# Prompt 09: audit one step by hand

Before pasting: choose the step you will audit, the riskiest one (usually the merge, a recode or a filter). Type `Follow @prompts/09_audit_by_hand.md for code/<your script>.py`.
Suggested setting: Opus, effort `high`. Same session as the review, or a new one.

---

I will audit one step of this project by hand: the script I named in my message. If I did not name one, ask me which. You assist; I check.

1. **Explain the script line by line**, in plain words. Mark every line that changes the number of rows or the value of a variable.
2. **Pick three units for me to follow**: one ordinary, one edge case, and one that is dropped, recoded or left unmatched. For each, tell me exactly where to find it in the raw data (file, sheet, row, column) and what the script does to it. **Do not tell me its values**: I will read them in the raw file myself.
3. **Wait** until I give you the values I read and the result I computed by hand. Then compare them with `data/processed/` and `outputs/`, and write `notes/audit_<YYYY-MM-DD>.md`: the step, the three units, my values, the script's values, match or not, and my conclusion in my words.

Do not change any code. If my numbers and the script's differ, say where the difference comes from, and let me decide.
