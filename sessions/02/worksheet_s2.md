# Worksheet, Session 2: structured data with an agent

**Course repository: https://github.com/subtilhugo/uzh-llm-socsci-2026**

**Shared document: [open it here](https://docs.google.com/document/d/1gTubrDtw8KHepmuR8dNzSeI7UypQhjzgEBJ7KX75Xq0/edit?usp=sharing).** Your row counts and your reviewer's findings go there.

**Timing.** Three blocks. In each, Hugo shows a step (10 min), you do it on your project, we check together (5 min).

| Block | Hugo shows | You do | We check |
| --- | --- | --- | --- |
| 1. Specify | 9:45 | 9:55–10:20, steps 1–2 | 10:20 |
| Break | | 10:25–10:40 | |
| 2. Implement | 10:40 | 10:50–11:10, steps 3–4 | 11:10 |
| 3. Review and decide | 11:15 | 11:25–11:40, steps 5–7 | debrief, 11:45 |

**Goal for 12:00.** In your folder: `notes/analysis_plan.md` in your words, with its open questions settled; numbered scripts in `code/` that print their row counts; a cleaned dataset in `data/processed/` and a first table or figure in `outputs/`; a review written by a fresh session, with your decision on each point; an entry in `PROJECT_HISTORY.md` with the three labels, and a commit.

**One rule for the morning: read the row counts before you look at the result.**

**Model and effort** (slide "Which model, which effort"): the plan at `medium`, the implementation at `high`, the review at `xhigh`. Type `/effort high` and so on in the agent. Tight quota: `/model opusplan` (Opus plans, Sonnet codes).

---

## Block 1. Specify

### Step 1. Prepare your folder (5 min)

1. **New prompts.** Download the course repository again (green "Code" button, "Download ZIP") and unzip it. Copy into your project, at the same places: `template/prompts/05_session_log.md` to `08_review.md`, and `template/notes/templates/analysis_plan.md`. Or ask the agent: *"Copy prompts 05 to 08 and notes/templates/analysis_plan.md from `<path of the unzipped course folder>/template/` into this project. Change nothing else."*
2. **Your data** in `data/raw/<source>/`, with one line per file in `data/raw/README.md` (where it comes from, when, under which conditions). Confidential data: a sample or a synthetic extract, as in Session 1.
3. **No data today?** Copy the example pack, `sessions/02/example_pack/`, into `data/raw/` and follow its README. **A text corpus?** Keep it for Sessions 3 and 4, and use the example pack today.

Done when: `prompts/` contains 06, 07 and 08, and `data/raw/README.md` has a line for each file.

### Step 2. The analysis plan (20 min)

Start a new session in your project folder, effort `medium`. Type `Follow @prompts/06_analysis_plan.md`.

- The agent first writes and runs an inspection script. Read its summary: number of rows, identifiers, missing-value codes, period and geography.
- Then it interviews you. Answer in your words. When you do not know, say "don't know": it goes to "Open questions". **It asks; it does not decide.**
- Read the plan before you say "ok". Is every merge given a rule for the rows that do not match?

Done when: `notes/analysis_plan.md` exists, says what one row is in each file, and has an "Open questions" section.

**Survey data?** Same steps. In the plan, settle: which weight, and for which statistics; the codes for refusal, don't know and not asked; the filter questions (who was asked what); reverse-coded items; which wave. In surveys, this is where silent decisions hide.

## Block 2. Implement

### Step 3. Implementation (15 min)

Type `/clear` (the plan is in the folder, not in the chat). Effort `high`. Type `Follow @prompts/07_implement.md`.

- First, it lists what the plan leaves open. **Answer every point before it writes any code.**
- Then it writes numbered scripts, runs them, and gives you the row-count trail (`outputs/row_counts.md`) and a first table or figure.

Done when: `outputs/row_counts.md` exists, and `data/processed/` contains a cleaned dataset.

### Step 4. Read the row counts (5 min)

Go through `outputs/row_counts.md` step by step. For each line where the number of rows changes, ask: does the plan say so?

Done when: you have written in the shared document, in one line, the step where rows changed most: *name, step, rows before → after, in the plan: yes / no.*

## Block 3. Review and decide

### Step 5. The review (7 min). Not optional.

Close the session and open a new one in the same folder: the reviewer must not have seen the code being written. Effort `xhigh`. Type `Follow @prompts/08_review.md`.

Done when: `notes/review_<date>.md` exists, with a table of discrepancies and an empty "Decision" column.

### Step 6. Decide (5 min)

For each point of the review: **fix it** (tell the agent exactly what to change, then rerun the scripts), or **accept it and write why** in the "Decision" column. A reviewer asked to find problems always finds something: deciding is your job, not the reviewer's.

Done when: every row has a decision, and every change in the row counts now follows from the plan. In the shared document, one line: *the silent decision your reviewer found (or "none"), and what you decided.*

### Step 7. Close (3 min)

Type `Follow @prompts/05_session_log.md`. Read the table of labels: for each output, origin, status, checked. Change status and checked only for what you actually checked. Then "ok" to the commit.

Done when: `git log` shows today's commit. If the time is up, do this step at home, but do it.

## Debrief

### Step 8. Two sections in your `CLAUDE.md` (2 min)

Ask the agent: *"Copy the sections 'Row counts and silent decisions' and 'Three labels on every output' from `<course folder>/template/CLAUDE.md` into my `CLAUDE.md`."* Then add one line of your own that would have caught today's error.

## Bonus 1, for the sceptics: who reviews the reviewer?

In one of your scripts, change one thing without telling anyone: an inner join instead of a left join, a filter that drops one category, `99` kept as a value. Rerun it. Open a fresh session and run prompt 08 again. Did it find your error? Write one line in the shared document: found / not found.

## Bonus 2: what does effort buy?

Run prompt 08 twice, in two fresh sessions: once with Sonnet at `low`, once with Opus at `xhigh`. Compare the two reviews: what does the cheaper one miss? Look at `/usage` after each.

---

## Before Session 3 (4 November)

- Bring one source you would like to collect from: an API, a website, a set of documents.
- Keep working in your folder. End every session with prompt 05.
- Carry-over question: an API returns 10,000 documents and the agent reports that the collection is complete. How would you know?
