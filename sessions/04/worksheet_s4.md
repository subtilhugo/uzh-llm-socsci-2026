# Worksheet, Session 4: from texts to variables, with and without an LLM

**Course repository: https://github.com/subtilhugo/uzh-llm-socsci-2026**

**Room AFL-E-003, 9:00 to 12:00.** **Shared document: [open it here](https://docs.google.com/document/d/1gTubrDtw8KHepmuR8dNzSeI7UypQhjzgEBJ7KX75Xq0/edit?usp=sharing).** Your checks, your scores and your questions go there. **The sheet for your hand codes**: its link is at the top of the Session 4 part of the shared document.

**The notebook:** `sessions/04/s4_extraction.ipynb`. [Open it in Colab](https://colab.research.google.com/github/subtilhugo/uzh-llm-socsci-2026/blob/main/sessions/04/s4_extraction.ipynb), then File, Save a copy in Drive (otherwise your changes are lost).

**Your number**: the one next to your name in Hugo's email. It decides which documents you code by hand.

**Today's question.** In the first round of the 1978 legislative election, do candidates who already hold a local office talk more about local issues? 300 professions de foi from Archelec (Sciences Po), measured six ways, then one coefficient.

| Part | You do | We check: paste in the shared document |
| --- | --- | --- |
| 1. The ScienceCluster | with an account: `sessions/04/cluster/README.md`; without: notebook Part 0 | the job ID, the GPU, the seconds |
| 2. Measuring without an LLM | notebook Parts 1 to 3 | found / requested / returned / missing; your dictionary's precision and recall, before and after; the AUC; the classifier's kappa |
| 3. Extracting with an LLM | Part 4 | accuracy per field for Claude and GPT; one disagreement where the catalogue is wrong |
| 4. From labels to an estimate | Parts 5 and 6 | for Claude: the coefficient naive and corrected, with the intervals |

**Goal for 12:00.** In your copy of the notebook (or in your project folder): 300 documents collected with their checks; your six hand codes in the class's sheet; a dictionary, an embedding score and a classifier scored against the class's codes; a table extracted by two models and checked field by field; the coefficient, naive and corrected; the bundle downloaded.

---

## Before the session (30 minutes, at home)

1. **Keys.** Hugo's email has two workshop keys, capped: Anthropic and OpenAI. Put them in Colab Secrets (key icon in the left sidebar; names `ANTHROPIC_API_KEY` and `OPENAI_API_KEY`; switch on "Notebook access"). Never in a cell, never in a file you share.
2. **Test the notebook**: open it in Colab, run Part 0 and Part 1. Part 0 installs the packages; Part 1 downloads 300 documents from the Internet Archive (one or two minutes). If something fails, write to Hugo before 8:30 with the error message.
3. **Your 100 texts.** The texts you coded yourself, as a CSV with a column `text` and a column `label` (0 or 1). Part 7 of the notebook and prompt 12 use them.
4. **With a ScienceCluster account** (optional): copy `sessions/04/cluster/` to the cluster and start building the container (README, "Once"). It takes 10 to 20 minutes; better done the day before.

---

## Part 1. The ScienceCluster

### Step 1. Follow, or prepare

- **With an account**: `sessions/04/cluster/README.md`, step by step: the container, the corpus (and its check), the model, then `sbatch embed.sbatch`. The job runs while we move on.
- **Without**: notebook Part 0. Keep the README for the day you have an account (your PI adds you to the group's Science IT project).

Done when: you have pasted *the job ID, the GPU named in the log, the seconds in `run.json`* (with an account), or Part 0 printed `ready`.

## Part 2. Measuring without an LLM

### Step 2. Collect, and check

Notebook Part 1. Read each check before going on: the number found, requested = returned + missing, short texts, duplicates. Open the PDF of the first document next to its OCR.

Done when: you have pasted *found, requested, returned, missing*.

### Step 3. Code six documents by hand

Notebook Part 2. Set `MY_NUMBER` in Part 0 and rerun that cell. Then:

- Read the definition of `local_offer` (printed in the notebook, and on slide 17).
- Read each of your six documents: the common one, then your five. The PDF is easier than the OCR.
- Write your six codes in `MY_CODES`, in the order printed (1 = a local offer, 0 = none).
- Paste the six lines printed by the next cell into the class's sheet.

Do this **before** anything else in the notebook: your codes must not be influenced by a measure.

Done when: your six rows are in the sheet. Then put the sheet's CSV link (in the shared document) in `GOLD_SHEET_CSV`, Part 0, and run "The class's codes".

### Step 4. A dictionary

Notebook Part 3a. Run the three cells, read the precision and recall, then read the contexts of a false positive.

**Exercise**: remove one word, add two, rerun the three cells.

Done when: you have pasted *precision and recall, before and after, and the words you changed*.

### Step 5. Embeddings and a classifier

Notebook Parts 3b and 3c. Run the search with a sentence of your own. Read the AUC of the score. Run the classifier once the sheet has enough codes.

Done when: you have pasted *the AUC, the classifier's kappa, and your search sentence with the best passage it found*.

**Your own project.** Part 7 with your 100 texts, or prompt 12 in your folder.

## Part 3. Extracting with an LLM

### Step 6. One form, then 300

Notebook Part 4. Run the single call first and read the whole answer next to the catalogue record printed below it. Then the 300 with Claude, then with GPT. Watch the cost lines.

### Step 7. Check against the catalogue

- The table of outcomes per field, and the accuracy where both have a value.
- `disagreements("claude")`, then `disagreements("gpt")`: open the PDF of each. Who is right?
- The offices: the model's 0/1 against the catalogue's.

Done when: you have pasted *accuracy per field for both models, and one disagreement where the catalogue, not the model, is wrong*.

**Your own project.** Prompt 13 on documents of your project.

## Part 4. From labels to an estimate

### Step 8. Naive and corrected

Notebook Part 5. Every measure against the class's codes, then the coefficient of `local_mandate`, naive and corrected, and the figure.

Done when: you have pasted *for Claude, the coefficient naive and corrected, with their intervals, and whether the conclusion changes*.

### Step 9. The bundle

Notebook Part 6. Open `params.json`: could a referee rerun your analysis from it? Download the zip.

## Before you leave

1. The bundle downloaded (Part 6).
2. In your project: copy prompts 12, 13 and 14 from `template/prompts/`, and the new section "Measures, extraction and estimates" of `template/CLAUDE.md` into yours.
3. Prompt 05: the entry in `PROJECT_HISTORY.md`, and the commit.

The Archelec texts are under a restrictive licence (CC BY-NC-ND): they stay out of any public repository, including yours.
