# Instructions for the agent

You are working inside a social science research project. This file is read at the start of
every session. Follow it. If something here conflicts with a request, say so before acting.

## Start of every session

1. Read `README.md` (what the project is) and the last entry of `PROJECT_HISTORY.md` (where it stands).
2. Summarise the state of the project in three lines before doing anything else.
3. If the request is unclear, ask one question. Do not guess the research question.

## What you may do

- Read anything in the folder.
- Create and edit files in `notes/`, `code/`, `outputs/`, `data/processed/`, `paper/`.
- Run scripts in `code/` and report what they did, including errors.
- Propose a change and wait, when the request says "propose" or "suggest".

## What you may not do

- Never modify or delete anything in `data/raw/`. Raw data is read-only. Cleaned versions go in `data/processed/`, produced by a script in `code/`.
- Never modify anything in `literature/`.
- Never invent a reference, a number, a quotation or a result. If you did not find it in the folder, say "not found in the project" and stop.
- Never delete files. Move them to `_trash/` if asked and say so.
- Never send data outside this folder (no uploads, no external API calls on data) unless a script in `code/` explicitly does so and the user has asked for it.
- Never run `git push`. Commits are fine when asked.

## How to write

- Short sentences. No filler. No praise of the user or of the project.
- Every factual claim about a paper must be traceable: cite the file name and, when possible, the page or section.
- When uncertain, say so with the words "uncertain" or "to verify", and say what would settle it.
- Literature notes follow `notes/templates/literature_note.md`.
- Code: Python 3.11+, one script per step, numbered (`01_clean.py`, `02_describe.py`). Each script reads from `data/raw/` or `data/processed/`, writes to `data/processed/` or `outputs/`, and prints the number of rows it read and wrote.

## Row counts and silent decisions

- Every script prints the number of rows before and after each filter, drop, deduplication, reshape and merge. For a merge, also the number of unmatched keys on each side.
- Never take a decision that changes the sample or a variable without asking: dropping rows, treating a missing-value code, removing duplicates, choosing a join type, rebuilding an identifier, changing a unit. If `notes/analysis_plan.md` does not say, ask.
- If a row count changes and the plan does not explain why, stop and report. Do not fix it on your own.
- Identifiers are text, never numbers.

## Three labels on every output

Every file you write in `data/processed/`, `outputs/` or `notes/` carries three labels, listed in the session entry of `PROJECT_HISTORY.md`:

- Origin: agent, user, or agent then user.
- Status: exploratory or polished.
- Checked: "not yet", or who checked it and against what.

You write the origin, "exploratory" and "not yet". Only the user changes status and checked.

## Conventions of this project

<!-- The agent fills this section with the user during Session 1 (prompt 01). Examples:
language of the notes (English), citation style (author-year), unit of analysis, main variable names,
file naming, anything the user keeps repeating. -->

## End of every session

Before the user leaves: write a dated entry in `PROJECT_HISTORY.md` (what was done, what was decided,
what was verified by a human, what is still open, and the three labels of every output) and list the files you changed.
