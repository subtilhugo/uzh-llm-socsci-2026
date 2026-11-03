# Worksheet, Session 3: from an API to annotated data (remote)

**Course repository: https://github.com/subtilhugo/uzh-llm-socsci-2026**

**Zoom link: in Hugo's email.** **Shared document: [open it here](https://docs.google.com/document/d/1gTubrDtw8KHepmuR8dNzSeI7UypQhjzgEBJ7KX75Xq0/edit?usp=sharing).** Your checks, your scores and your questions go there.

**The notebook:** `sessions/03/s3_manifesto_annotation.ipynb`. [Open it in Colab](https://colab.research.google.com/github/subtilhugo/uzh-llm-socsci-2026/blob/main/sessions/03/s3_manifesto_annotation.ipynb), then File, Save a copy in Drive (otherwise your changes are lost).

**Timing.**

| Part | Hugo shows | You do | We check |
| --- | --- | --- | --- |
| 1. APIs, and collecting the manifestos | 9:15 | 9:45–9:55, notebook Parts 1–2 | 9:55 |
| 2. Annotating through an API | 10:00 | 10:20–10:40, Parts 3, 4, 6 | 10:40 |
| Break | | 10:45–10:55 | |
| 3. A model on your own machine | 10:55 | 11:10–11:25, Part 5, then Part 6 again | 11:25 |
| 4. The ScienceCluster | 11:30, demo | | |
| Debrief | 11:50 | | |

**Goal for 12:00.** In your copy of the notebook (or in your project folder): the French manifestos of one election collected, with the four checks passed or explained; your own codes for 15 sentences; 200 sentences coded by Claude and by a local model; the scores of both against the Manifesto Project coders and against you; a reproducibility bundle in `outputs/annotation/<run_id>/`.

---

## The evening before (30 minutes, do it on 3 November)

Downloads on a shared Zoom connection are slow. Do these at home.

1. **Manifesto Project key.** Register at https://manifesto-project.wzb.eu (free). Registration is immediate, with no approval to wait for. On your profile page, generate an API key. The Manifesto Project forbids redistributing its data: never push the texts to a public repository.
2. **Anthropic key.** Hugo's email has a workshop key, capped. Keep it out of any file you share.
3. **Ollama**, if you will run the local part on your laptop (16 GB of memory or more recommended):
   - macOS and Windows: download from https://ollama.com/download and install.
   - Linux: `curl -fsSL https://ollama.com/install.sh | sh`
   - Then, in a terminal: `ollama pull ministral-3:8b` (6 GB; with only 8 GB of memory, ministral-3:3b instead). Check with `ollama run ministral-3:8b "Bonjour"`: it answers.
   - Less than 16 GB, or no admin rights? Use Colab for Part 5 (the notebook installs Ollama inside Colab, on a free GPU).
4. **Test the notebook**: open it in Colab, choose the GPU first (Runtime, Change runtime type, T4 GPU: changing it later erases everything you ran), then run Part 0. Put both keys in Colab Secrets (key icon in the left sidebar; names `MANIFESTO_API_KEY` and `ANTHROPIC_API_KEY`; switch on "Notebook access").

If something fails, write to Hugo before 8:30 with the error message.

---

## Part 1. APIs, and collecting the manifestos

### Step 1. The first request (5 min)

Notebook Part 1. Read the response of `list_core_versions` before going on: what does it contain? Which version will you use?

Done when: the cell prints the core dataset version and the corpus version.

### Step 2. One election, and the four checks (10 min)

Notebook Part 2. Change `ELECTION_YEAR` if the table of elections shows that another one has annotated texts.

- The raw answer is archived in `s3_work/data/raw/manifesto/` before any processing.
- Read the four checks: requested = returned + missing; no empty text; our count of quasi-sentences against the published `total`; `per504` recomputed against the published one.

Done when: you have pasted in the shared document *name, election, requested / returned / missing, check 3: match or not*.

**No Manifesto key?** Register now (https://manifesto-project.wzb.eu/signup): free, immediate, two minutes.

**Your own project.** Prompt 10 (`template/prompts/10_collect_api.md`) on the API you brought. Copy it into `prompts/` first, and put your key in `.env`.

## Part 2. Annotating through an API

### Step 3. Code 15 sentences yourself (10 min)

Notebook Part 3. Read the seven domains. Code the 15 sentences printed in `MY_CODES`, **before** running anything in Part 4. Do not look at the column `human_domain`.

Done when: `MY_CODES` has 15 entries.

### Step 4. Claude codes 200 (10 min)

Notebook Part 4. Run the single call first and read everything it returns: the domain, the reason, the stop reason, the tokens. Then the loop.

Done when: `claude: 200/200 annotated` and the cost is printed.

### Step 5. The scores (5 min)

Notebook Part 6, the first three cells. Then read five disagreements: who is right?

Done when: you have pasted *your agreement with the coders on your 15, the model's kappa, and one sentence where you think the model is right*.

## Part 3. A model on your own machine

### Step 6. The same task, locally (15 min)

Notebook Part 5.

- **Laptop**: run the notebook locally (VS Code, Cursor or Jupyter) with Ollama running. `LOCAL_MODEL` is the model you pulled.
- **Colab**: you chose the T4 GPU in Part 0; run the "Colab only" cell. It installs Ollama inside Colab and pulls the model (3 to 5 minutes).
- **Slow machine** (no GPU, old laptop): annotate `sample.head(40)` instead of the 200, as the cell says.
- Then Part 6 again: the table now has two models, and their agreement with each other.

Done when: you have pasted *model and size, laptop or Colab, seconds per sentence, kappa*.

### Exercises, if you finish early

1. Change one thing in the prompt and rerun (Exercise 1 in the notebook). Paste *what you changed, kappa before → after*.
2. Pull a second, larger model and compare speed and kappa.
3. Part 7: open `params.json`. Would a referee be able to rerun your annotation from it?

## Part 4. The ScienceCluster (demo)

Hugo shows the three doors: the terminal (SSH), an agent on the cluster, and the browser (ScienceApps). The commands are in `setup/cluster_guide.md`, for when you have an account.

## Before you leave

1. Part 7 of the notebook: download `s3_work/outputs/annotation/<run_id>/` (Colab: Files panel, right click, Download).
2. In your project: copy prompts 10 and 11 from `template/prompts/`, and the new section "APIs, keys and LLM annotation" of `template/CLAUDE.md` into yours.
3. Prompt 05: the entry in `PROJECT_HISTORY.md`, and the commit.
