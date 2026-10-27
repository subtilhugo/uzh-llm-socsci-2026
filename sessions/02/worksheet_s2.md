# Worksheet, Session 2: exploring structured data with an agent

**Course repository: https://github.com/subtilhugo/uzh-llm-socsci-2026**

**Shared document: [open it here](https://docs.google.com/document/d/1gTubrDtw8KHepmuR8dNzSeI7UypQhjzgEBJ7KX75Xq0/edit?usp=sharing).** Your row counts, your audit and your reviewer's findings go there.

**Timing.** Three blocks. In each, Hugo shows a step (10 min), you do it on your project, we check together (5 min).

| Block | Hugo shows | You do | We check |
| --- | --- | --- | --- |
| 1. Document and specify | 9:45 | 9:55–10:20, steps 1–2 | 10:20 |
| Break | | 10:25–10:40 | |
| 2. Clean, merge, describe | 10:40 | 10:50–11:10, steps 3–4 | 11:10 |
| 3. Audit and decide | 11:15 | 11:25–11:40, steps 5–8 | 11:40, then debrief |

**Goal for 12:00.** In your folder: `data/raw/README.md` and `notes/codebook.md`; `notes/analysis_plan.md` in your words, with its open questions settled; numbered scripts in `code/` that print their row counts and check themselves, and `code/run_all.py`; a cleaned dataset, summary statistics, two figures and `notes/insights.md`; a review by a fresh session, and one step you audited by hand; an entry in `PROJECT_HISTORY.md` and a commit.

**Scripts, not chats.** Every number, table and figure comes from a script in `code/`. If the agent gives you a number in the chat, ask for the script that produces it.

**When the agent says a request conflicts with your `CLAUDE.md`**, it is doing its job. Read why, then answer explicitly: yes, for this request; or no.

**Model and effort** (slide "Which model, which effort, for which task"): the plan with Fable at `high` (`/model fable`; without access to Fable, Opus); the cleaning and the review with Opus, at `high` and `xhigh`. Type `/model` and `/effort` in the agent.

---

## Block 1. Document and specify

### Step 1. Prepare your folder (5 min)

1. **New prompts and templates.** Download the course repository again (green "Code" button, "Download ZIP") and unzip it. Copy into your project, at the same places: prompts 05 to 09 from `template/prompts/`, and the two files of `template/notes/templates/` (`analysis_plan.md`, `codebook.md`). Or ask the agent: *"Copy prompts 05 to 09 and the files in notes/templates/ from `<path of the unzipped course folder>/template/` into this project. Change nothing else."*
2. **Your data** in `data/raw/<source>/`. Confidential data: a sample or a synthetic extract, as in Session 1.
3. **No data today?** Copy the `elections/` and `insee/` folders of `sessions/02/example_pack/` into your `data/raw/`, and follow the pack's README. **A text corpus?** Keep it for Sessions 3 and 4, and use the example pack today.

Done when: `prompts/` contains 05 to 09, `notes/templates/` contains `analysis_plan.md` and `codebook.md`, and your data is in `data/raw/`.

**Python packages.** The agent will need some (pandas, matplotlib, xlrd for old `.xls` files). Let it create a virtual environment in `.venv` and install them there.

### Step 2. Document, then plan (20 min)

Start a new session in your project folder: `/model fable` (or Opus), effort `high`. Type `Follow @prompts/06_analysis_plan.md`.

- A script inspects your files without changing them. Read its summary: rows, identifiers, missing-value codes, period and geography.
- The agent completes `data/raw/README.md` and writes `notes/codebook.md`. Your `CLAUDE.md` from Session 1 forbids touching `data/raw/`: if the agent says so, answer *"yes, the README only"*.
- Then it interviews you. Answer in your words. When you do not know, say "don't know": it goes to "Open questions". **It asks; it does not decide.**
- Read the codebook and the plan before you say "ok". Is every missing-value code documented? Does every merge have a rule for the rows that do not match?

Done when: `data/raw/README.md` has one line per file, `notes/codebook.md` one line per variable you will use, and `notes/analysis_plan.md` an "Open questions" section.

**Survey data?** Same steps. The codebook records the weight variable and when to use it, the filter questions (who was asked what), reverse-coded items, and the codes for refusal, don't know and not asked. In surveys, this is where silent errors hide.

## Block 2. Clean, merge, describe

### Step 3. Scripts that check themselves (15 min)

Type `/clear` (the plan is in the folder, not in the chat). `/model opus`, `/effort high`. Type `Follow @prompts/07_implement.md`.

- First, it lists what the plan leaves open. **Answer every point before it writes any code.**
- Then it writes numbered scripts with row counts, assertions and cross-tabulations; then summary statistics, at most two figures, and `notes/insights.md`; and `code/run_all.py`, which reruns everything.

Done when: `python3 code/run_all.py` runs from start to end, and `outputs/row_counts.md` exists.

Still running at 11:10? Let it finish. Read the row counts as they arrive, and start Block 3 as soon as it is done.

### Step 4. Read in this order (5 min)

1. The row counts (`outputs/row_counts.md`): for each line where rows change, does the plan say so?
2. The assertions: did one fail? What did the agent do about it?
3. The cross-tabulations in `outputs/tables/`: does every recode do what the codebook says?
4. Only then the figures and the insights.

Done when: you have pasted in the shared document each step where rows changed without the plan saying so, or "none": *name, step, rows before → after, in the plan: yes / no.*

## Block 3. Audit and decide

### Step 5. The review (2 min to start)

Close the session and open a new one in the same folder: the reviewer must not have seen the code being written. `/model opus`, `/effort xhigh`. Type `Follow @prompts/08_review.md`.

While it runs (several minutes), go to Step 6 at once, in a second session: sidebar, new session, same folder. The two do not interfere: the reviewer reruns the scripts, the audit only reads.

### Step 6. Audit one step by hand (8 min). Not optional.

Choose your riskiest step (usually the merge, a recode or a filter), and type `Follow @prompts/09_audit_by_hand.md for code/<your script>.py`.

- The agent explains the script line by line, and points you to three units in the raw data: one ordinary, one edge case, one dropped or unmatched. It does not tell you their values.
- **Open the raw file yourself** (Excel, a text editor) and read the three units. Compute their result by hand. Give your numbers to the agent: it compares them with the processed data.

Done when: `notes/audit_<date>.md` exists, with your three units and your values. In the shared document, one line: *name, step audited, match / no match, what you learned.*

### Step 7. Decide (3 min)

For each point of the review and of your audit: **fix it** (tell the agent exactly what to change, then `python3 code/run_all.py`), or **accept it and write why** in the "Decision" column of the review. A reviewer asked to find problems always finds something: deciding is your job. In the shared document, one line: *the silent decision your reviewer found (or "none"), and what you decided.*

### Step 8. Close (2 min)

Type `Follow @prompts/05_session_log.md`. Under "Verified by a human", only what you actually checked. Then "ok" to the commit. If the time is up, do this step at home, but do it.

## Debrief

### Step 9. One section in your `CLAUDE.md` (2 min)

Ask the agent: *"Copy the section 'Row counts and silent decisions' from `<course folder>/template/CLAUDE.md` into my `CLAUDE.md`."* Then add one line of your own that would have caught today's error.

## Bonus 1, for the sceptics: who reviews the reviewer?

In one of your scripts, change one thing without telling anyone: an inner join instead of a left join, a filter that drops one category, `99` kept as a value. Rerun it. Open a fresh session and run prompt 08 again. Did it find your error? Write one line in the shared document: found / not found.

## Bonus 2: what does effort buy?

Run prompt 08 twice, in two fresh sessions: once with Sonnet at `low`, once with Opus at `xhigh`. Compare the two reviews: what does the cheaper one miss? Look at `/usage` after each.

## Bonus 3, example pack only: put both files in the same geography

The election file and the INSEE file do not describe the same municipalities. Use `example_pack/extra/v_mvt_commune_2026.csv` (INSEE's history of municipalities) to add up the municipalities that merged, so that both files use the geography of the 2022 election. Assert that the national totals do not change. Careful: the file also lists events after 2022.

---

## Before Session 3 (4 November)

- Bring one source you would like to collect from: an API, a website, a set of documents.
- Keep working in your folder. End every session with prompt 05.
- Carry-over question: an API returns 10,000 documents and the agent reports that the collection is complete. How would you know?
