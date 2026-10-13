# Worksheet, Session 1: setting up an agentic research project

**Course repository: https://github.com/subtilhugo/uzh-llm-socsci-2026**

**Goal for 12:00.** A git folder for your own project containing a filled `CLAUDE.md`, three to five literature notes, a one-page research memo, a critique of that memo, and a first commit. And you have caught at least one error the agent made.

Work on your own project. If you have no project or no PDFs today, use the example project: **its question and its literature are in `example-project/README.md`; ask Hugo for the PDFs**.

Each step has a prompt to paste (in `template/prompts/`) and a "done when" criterion. Do the steps in order. Steps 1 to 3 are mandatory before anything else. If you get stuck for more than five minutes, paste your error message in the shared document and ask your neighbour.

One rule for the whole morning: **read what the agent writes before you accept it.** Everything it produces is a draft until you have checked it.

---

## Step 0. Check your agent (5 min)

In a terminal, create an empty folder, start your agent inside it, and ask it to create a file `hello.md` containing today's date.

Done when: the file exists and contains today's date. If not: see `setup/install_guide.md`, or raise your hand.

## Step 1. Copy the template (5 min)

**On the course repository page, click the green "Code" button, then "Download ZIP", and unzip it.** Copy the contents of its `template/` folder into a new folder named after your project (for example `thesis-chapter-2/`). Keep the hidden file `.gitignore` **(on macOS, `Cmd+Shift+.` shows hidden files in Finder)**.

Then, in a terminal inside that folder:

```
git init
git add .
git commit -m "Project template"
```

Done when: `git log` shows one commit.

## Step 2. Start the agent in the folder (2 min)

Start your agent inside the project folder (`claude` in the terminal, or open the folder in the desktop app, or in Cursor / VS Code and start Claude Code there).

Ask: "What does CLAUDE.md tell you to do?"

Done when: the agent summarises the rules in `CLAUDE.md` (read-only raw data, no invented references, log at the end of the session).

## Step 3. Fill the context (15 min)

Paste `prompts/01_fill_context.md`. Answer the agent's questions out loud or in writing. Say "skip" when you do not know yet. Read `README.md` and the conventions in `CLAUDE.md` before you confirm.

Done when: `README.md` has a research question in your words, and `CLAUDE.md` has at least three conventions you actually care about.

## Step 4. Literature notes (10 min)

Put three to five PDFs in `literature/`. Paste `prompts/02_literature_notes.md`.

If the agent says it cannot read a PDF: run `pdftotext file.pdf file.txt` in the terminal (or ask the agent to install and use `pymupdf`), put the `.txt` next to the PDF, and ask again.

Done when: one note per PDF in `notes/literature/`, each with a "Claims to verify" section.

## Step 5. Verify (10 min). This is the step that matters.

Open one note next to its PDF. Pick two claims in "Main results" and find them in the PDF: the number, the page, the table.

- Correct: change "Verified by: not yet verified" to your name and the date.
- Wrong or approximate: tell the agent exactly what is wrong and where the right version is. Make it fix the note. Then re-check.

Done when: at least one note has your name in "Verified by", and you have written in the shared document, in one line, what kind of error you found (wrong number, wrong paper, wrong page, invented finding, nothing wrong).

## Step 6. Research memo (10 min)

Paste `prompts/03_research_memo.md`. Read the memo. Rewrite at least one paragraph in your own words.

Done when: `notes/research_memo.md` reads like something you would show your supervisor.

## Step 7. Critique (10 min)

Paste `prompts/04_critique.md`. Read the five weaknesses. Decide for each whether you agree. Write your decisions as a short list at the end of the memo under "Response to critique".

Done when: the memo contains your responses, in your words.

## Step 8. Log and commit (5 min)

Paste `prompts/05_session_log.md`. Check the list of files before saying "ok" to the commit.

Then close the agent, start a fresh session in the same folder, and ask: "Where does this project stand?"

Done when: the agent answers from `PROJECT_HISTORY.md` without you explaining anything.

## Bonus, if you finish early

Drop your dataset (or the example dataset) in `data/raw/<source>/` and ask the agent to fill `data/raw/README.md` with the provenance table and the quirks it notices (separator, encoding, missing-value codes, identifiers). This is the first step of Session 2.

---

## Before Session 2 (28 October)

- Bring your dataset as a file the agent can open (CSV, Excel, Stata, SPSS, Parquet). If it is confidential, bring a sample or an anonymised extract. If it is large, bring a subset.
- If you have no dataset, you will use the example pack (French election results and local indicators at the municipality level).
- Keep working in your folder. End every session with prompt 05.
