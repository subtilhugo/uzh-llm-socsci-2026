# Worksheet, Session 4: from texts to variables, with and without an LLM

**Course repository: https://github.com/subtilhugo/uzh-llm-socsci-2026**

**Room AFL-E-003, 9:00 to 12:00.** **Shared document: [open it here](https://docs.google.com/document/d/1gTubrDtw8KHepmuR8dNzSeI7UypQhjzgEBJ7KX75Xq0/edit?usp=sharing).** Your checks, your scores and your questions go there. **The sheet for your hand codes**: its link is at the top of the Session 4 part of the shared document.

**The notebook:** `sessions/04/s4_extraction.ipynb`. [Open it in Colab](https://colab.research.google.com/github/subtilhugo/uzh-llm-socsci-2026/blob/main/sessions/04/s4_extraction.ipynb), then File, Save a copy in Drive (otherwise your changes are lost).

**Your number**: the one next to your name in Hugo's email. It decides which documents you code by hand.

**Today's question.** In the first round of the 1978 legislative election, do candidates who already hold a local office talk more about local issues? 300 professions de foi from Archelec (Sciences Po).

| Part of the session | You do | We check: paste in the shared document |
| --- | --- | --- |
| 1. Text as data: from word counts to black boxes | listen | |
| 2. Three ways into the ScienceCluster | with an account: the small job of `sessions/04/cluster/demo/`; without: notebook Parts 0 and 1 | your job ID, and the node it ran on |
| 3. Your paper and your data, connected | listen; `setup/overleaf_dropbox_guide.md` for later | |
| 4. From a scan to a text: OCR | notebook Parts 1 and 2 | surnames found by the old OCR and by the model; one word each got wrong |
| 5. Extracting with an LLM | notebook Part 3 | accuracy per field for Claude and GPT; one disagreement where the catalogue is wrong |
| 6. Classifying text, and the coefficient | notebook Parts 4 to 7 | your dictionary before and after; for Claude, the coefficient naive and corrected |

**Goal for 12:00.** In your copy of the notebook: 300 documents collected with their checks; twelve scans read twice; a table extracted by two models and checked field by field; your six hand codes in the class's sheet; four measures scored against the class's codes; the coefficient, naive and corrected; the bundle downloaded.

---

## Before the session (30 minutes, at home)

1. **Keys.** Hugo's email has two workshop keys, capped: Anthropic and OpenAI. Put them in Colab Secrets (key icon in the left sidebar; names `ANTHROPIC_API_KEY` and `OPENAI_API_KEY`; switch on "Notebook access"). Never in a cell, never in a file you share.
2. **Test the notebook**: open it in Colab, run Part 0 and Part 1. Part 0 installs the packages; Part 1 downloads 300 documents from the Internet Archive (one or two minutes). If something fails, write to Hugo before 8:30 with the error message.
3. **Your 100 texts.** The texts you coded yourself, as a CSV with a column `text` and a column `label` (0 or 1). Part 8 of the notebook and prompt 12 use them.
4. **With a ScienceCluster account** (optional): the VPN if you are off campus, then the nickname and the key (`sessions/04/cluster/README.md`, Route 2). Five minutes.

---

## Part 2 of the session. Three ways into the ScienceCluster

### Step 1. Your route

- **With an account**: `sessions/04/cluster/README.md`. The nickname and the key, then the small job: copy `demo/` to the cluster, `sbatch job.sh`, `squeue`, `sacct`, `cat` the output. Then ask your agent to do the same, and read every command before you approve it.
- **Without**: notebook Parts 0 and 1. Keep the README for the day you have an account (your PI adds you to the group's Science IT project).

Done when: you have pasted *your job ID, and the name of the node it ran on* (with an account), or Part 1 printed its checks.

## Part 4 of the session. From a scan to a text

### Step 2. Collect, and check

Notebook Part 1. Read each check before going on: the number found, requested = returned + missing, short texts, duplicates. Open the PDF of the first document next to its OCR.

### Step 3. Read a scan twice

Notebook Part 2. One page first: read the model's version, then the 2021 version, with the PDF open. Then the other eleven.

- Check 1: how much do the versions differ, and what did only the model write?
- Check 2: is the candidate's surname (from the catalogue) in each version?

Done when: you have pasted *surnames found by the old OCR and by the model, out of twelve; one word the model got right; one word it should not have written*.

## Part 5 of the session. Extracting with an LLM

### Step 4. One form, then 300

Notebook Part 3. Run the single call first and read the whole answer next to the catalogue record printed below it. Then the 300 with Claude, then with GPT. Watch the cost lines.

### Step 5. Check against the catalogue

- The table of outcomes per field, and the accuracy where both have a value.
- `disagreements("claude")`, then `disagreements("gpt")`: open the PDF of each. Who is right?
- The offices: the model's 0/1 against the catalogue's.

Done when: you have pasted *accuracy per field for both models, and one disagreement where the catalogue, not the model, is wrong*.

**Your own project.** Prompt 13 on documents of your project.

## Part 6 of the session. Classifying text, and the coefficient

### Step 6. Code six documents by hand

Notebook Part 4. Set `MY_NUMBER` in Part 0 and rerun that cell. Then:

- Read the definition of `local_offer` (printed in the notebook, and on the slide "Four Ways to Say Yes or No").
- Read each of your six documents: the common one, then your five. The PDF is easier than the OCR.
- Write your six codes in `MY_CODES`, in the order printed (1 = a local offer, 0 = none).
- Paste the six lines printed by the next cell into the class's sheet.

Do this **before** you look at any measure of Part 5: your codes must not be influenced by one.

Done when: your six rows are in the sheet. Then put the sheet's CSV link (in the shared document) in `GOLD_SHEET_CSV`, Part 0, and run "The class's codes".

### Step 7. Four measures

Notebook Part 5. The dictionary and its precision and recall; the contexts of a false positive; then the **exercise**: remove one word, add two, rerun. The third OCR check: does the dictionary change with the model's text? One search of your own. The classifier, once the sheet has enough codes. Then the LLMs' label, and all measures against the class's codes.

Done when: you have pasted *precision and recall before and after, the words you changed, the AUC, the classifier's kappa*.

### Step 8. Naive and corrected

Notebook Part 6. The coefficient of `local_mandate`, naive and corrected, and the figure.

Done when: you have pasted *for Claude, the coefficient naive and corrected, with their intervals, and whether the conclusion changes*.

### Step 9. The bundle

Notebook Part 7. Open `params.json`: could a referee rerun your analysis from it? Download the zip.

**Your own project.** Part 8 with your 100 texts; prompt 12 (a classical measure) and prompt 14 (an estimate from labels) in your folder.

## Before you leave

1. The bundle downloaded (Part 7).
2. In your project: copy prompts 12, 13 and 14 from `template/prompts/`, and the new section "Measures, extraction and estimates" of `template/CLAUDE.md` into yours.
3. Prompt 05: the entry in `PROJECT_HISTORY.md`, and the commit.

The Archelec texts are under a restrictive licence (CC BY-NC-ND): they stay out of any public repository, including yours.
