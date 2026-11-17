# Worksheet, Session 4: from texts to variables

**Course repository: https://github.com/subtilhugo/uzh-llm-socsci-2026**

**Room AFL-E-003, 9:00 to 12:00.** **Shared document: [open it here](https://docs.google.com/document/d/1gTubrDtw8KHepmuR8dNzSeI7UypQhjzgEBJ7KX75Xq0/edit?usp=sharing).** Your checks, your scores and your questions go there.

**Two notebooks today.** For each: open it in Colab, then File, Save a copy in Drive (otherwise your changes are lost).

- `sessions/04/s4_ocr.ipynb`: from a PDF to a table. [Open it in Colab](https://colab.research.google.com/github/subtilhugo/uzh-llm-socsci-2026/blob/main/sessions/04/s4_ocr.ipynb)
- `sessions/04/s4_extraction.ipynb`: from 300 leaflets to a table you can merge. [Open it in Colab](https://colab.research.google.com/github/subtilhugo/uzh-llm-socsci-2026/blob/main/sessions/04/s4_extraction.ipynb)

| Part of the session | You do | We check: paste in the shared document |
| --- | --- | --- |
| 1. Text as data: sixty years, from word lists to LLMs | listen; `sessions/04/text_as_data.md` to go further | |
| 2. Three ways into the ScienceCluster | with an account: the small job of `sessions/04/cluster/demo/`; without: Part 0 of both notebooks | your job ID, and the node it ran on |
| 3. Your paper and your data, connected | listen; `setup/overleaf_dropbox_guide.md` for later | |
| 4. From a PDF to a table | `s4_ocr.ipynb`, Parts 1 to 5 | your document, Tesseract's confidence, the agreement, one word each got wrong |
| 5. Extracting with an LLM | `s4_extraction.ipynb`, Parts 1 to 3 | accuracy per field for Claude and GPT; one disagreement where the catalogue is wrong |

**Goal for 12:00.** Five historical PDFs read twice, by Tesseract and by a model, in one table; 300 leaflets turned into a table by two models and checked field by field against the catalogue; both bundles downloaded.

---

## Before the session (20 minutes, at home)

1. **Keys.** Hugo's email has two workshop keys, capped: Anthropic and OpenAI. Put them in Colab Secrets (key icon in the left sidebar; names `ANTHROPIC_API_KEY` and `OPENAI_API_KEY`; switch on "Notebook access"). Never in a cell, never in a file you share.
2. **Test both notebooks**: run Part 0 of each, and Part 1 of `s4_extraction.ipynb` (it downloads 300 documents, one or two minutes). If something fails, write to Hugo before 8:30 with the error message.
3. **A PDF of your own** (optional): a scan from your project, for Part 6 of `s4_ocr.ipynb`.
4. **With a ScienceCluster account** (optional): the VPN if you are off campus, then the nickname and the key (`sessions/04/cluster/README.md`, Route 2). Five minutes.

---

## Part 2 of the session. Three ways into the ScienceCluster

### Step 1. Your route

- **With an account**: `sessions/04/cluster/README.md`. The nickname and the key, then the small job: copy `demo/` to the cluster, `sbatch job.sh`, `squeue`, `sacct`, `cat` the output. Then ask your agent to do the same, and read every command before you approve it.
- **Without**: Part 0 of both notebooks. Keep the README for the day you have an account (your PI adds you to the group's Science IT project).

Done when: you have pasted *your job ID, and the name of the node it ran on*.

## Part 4 of the session. From a PDF to a table

`s4_ocr.ipynb`.

### Step 2. Look, and read with Tesseract

Parts 1 and 2. Hugo shows them on the 1958 leaflet; you choose **another** document: set `DOC = "decree_1793"` (old print) or `DOC = "manuscript_1760"` (handwriting) and rerun. Look at the picture, at Tesseract's table of words, at its confidence, at the words it flags in red.

### Step 3. The model reads the same page

Part 3: the transcription, and the five variables. Part 4: the agreement between the two readings, the words only one of them has. Read them with the picture open: who is right?

### Step 4. The loop

Part 5: every page of the five documents, into one table. Read it by kind of document. Then the cost per page, and what 8,000 pages would cost.

Done when: you have pasted *your document, Tesseract's mean confidence, the agreement, one word the model read better, one word it should not have written*.

**Faster?** Part 6: a PDF of your own.

## Part 5 of the session. Extracting with an LLM

`s4_extraction.ipynb`.

### Step 5. Collect, and check

Part 1. Read each check before going on: the number found, requested = returned + missing, short texts, duplicates. Open the PDF of the first document next to its OCR. Then the catalogue: someone else's coding.

### Step 6. One form, then 300

Part 2. Run the single call first and read the whole answer next to the catalogue record printed below it. Then the 300 with Claude, then with GPT. Watch the cost lines.

### Step 7. Check against the catalogue

- The table of outcomes per field, and the accuracy where both have a value.
- `disagreements("claude")`, then `disagreements("gpt")`: open the PDF of each. Who is right?
- The offices: the model's 0/1 against the catalogue's.

Done when: you have pasted *accuracy per field for both models, and one disagreement where the catalogue, not the model, is wrong*.

### Step 8. The table and the bundle

Part 3. Download the zip. Open `params.json`: could a referee rerun your extraction from it?

**Your own project.** Prompt 13 on documents of your project.

## Before you leave

1. Both bundles downloaded.
2. In your project: copy prompt 13 from `template/prompts/`, and the new section "Measures, extraction and estimates" of `template/CLAUDE.md` into yours.
3. Prompt 05: the entry in `PROJECT_HISTORY.md`, and the commit.
4. For Session 5: ten minutes of audio or video from your project, and your 100 coded texts.

The Archelec texts are under a restrictive licence (CC BY-NC-ND): they stay out of any public repository, including yours.
