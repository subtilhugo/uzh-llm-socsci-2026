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

- Never modify or delete a data file in `data/raw/`. Raw data is read-only. Cleaned versions go in `data/processed/`, produced by a script in `code/`. The only file you may edit in `data/raw/` is its `README.md`.
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

- Scripts, not chats: every number, table and figure comes from a script in `code/`, never from an answer in the chat. `python3 code/run_all.py` reruns everything from the raw data.
- Every script prints the number of rows before and after each filter, drop, deduplication, reshape and merge. For a merge, also the number of unmatched keys on each side.
- Never take a decision that changes the sample or a variable without asking: dropping rows, treating a missing-value code, removing duplicates, choosing a join type, rebuilding an identifier, changing a unit. If `notes/analysis_plan.md` does not say, ask.
- If a row count changes and the plan does not explain why, stop and report. Do not fix it on your own.
- Write checks into the code: assertions that stop a script when a key is not unique, a value is out of range or a total is not preserved; a cross-tabulation after every recode and every merge.
- Identifiers are text, never numbers.
- Document the data: you may edit `data/raw/README.md` (provenance) and `notes/codebook.md`. Never a data file in `data/raw/`.

## Conventions of this project

- Notes, code comments and memos in English. Citations author-year: (Colantone & Stanig 2018).
- Software: Python 3.11, pandas. One script per step in `code/`.
- The municipality is identified by its INSEE code (`code_commune`): always a 5-character string, never a number. Keep leading zeros ("01001") and the Corsican codes ("2A004", "2B033").
- Paris, Lyon and Marseille are split into arrondissements in some files and not in others. Never merge without checking how each file treats them, and report the number of rows before and after every merge.
- Municipalities merge and split over time. Always state which year's municipal geography a file uses.
- Party label: "FN" for elections before June 2018, "RN" after (the party changed its name on 1 June 2018). In variable names, use `fn_rn`.
- Vote shares are computed over valid votes (exprimés) unless stated otherwise. Say which denominator you use.
- No causal language ("effect", "impact", "causes") in notes or memos until `README.md` names an identification strategy. Say "is associated with".
- Books (Coquard 2019, Ternullo 2024): write a note only from the chapters that are in `literature/`, and say which chapters.

## End of every session

Before the user leaves: write a dated entry in `PROJECT_HISTORY.md` (what was done, what was decided,
what was verified by a human, what is still open) and list the files you changed.
