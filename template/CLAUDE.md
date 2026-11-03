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

## APIs, keys and LLM annotation

- Keys live in `.env` (ignored by git), are read by the scripts, and are never printed, logged, pasted in the chat or written to a file.
- Every raw API response is saved as received in `data/raw/<source>/<version>/` before any processing, with a log of the requests. A collection is complete when it matches a number the provider publishes, not when the script ends without error.
- Sending texts to a commercial LLM API is sending data outside the folder: only when the user said this data may leave. Otherwise, a local model (Ollama, LM Studio, vLLM on the cluster).
- LLM labels are not human coding. Record the model ID (for a local model, its digest and quantization), the prompt file and the parameters of every run, keep every raw answer, and validate against the user's own coding before any full run.

## Conventions of this project

<!-- The agent fills this section with the user during Session 1 (prompt 01). Examples:
language of the notes (English), citation style (author-year), unit of analysis, main variable names,
file naming, anything the user keeps repeating. -->

## End of every session

Before the user leaves: write a dated entry in `PROJECT_HISTORY.md` (what was done, what was decided,
what was verified by a human, what is still open) and list the files you changed.
