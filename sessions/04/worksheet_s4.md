# Worksheet, Session 4: from texts to variables

**Course repository: https://github.com/subtilhugo/uzh-llm-socsci-2026**

**Room AFL-E-003, 9:00 to 12:00.** **Shared document: [open it here](https://docs.google.com/document/d/1gTubrDtw8KHepmuR8dNzSeI7UypQhjzgEBJ7KX75Xq0/edit?usp=sharing).** Your checks, your scores and your questions go there.

**Two notebooks today.** For each: open it in Colab, then File, Save a copy in Drive (otherwise your changes are lost).

- `sessions/04/s4_ocr.ipynb`: from a PDF to a table, with three readers. **Runtime: T4 GPU** (Runtime, Change runtime type). [Open it in Colab](https://colab.research.google.com/github/subtilhugo/uzh-llm-socsci-2026/blob/main/sessions/04/s4_ocr.ipynb)
- `sessions/04/s4_extraction.ipynb`: from 300 leaflets to a table you can merge. [Open it in Colab](https://colab.research.google.com/github/subtilhugo/uzh-llm-socsci-2026/blob/main/sessions/04/s4_extraction.ipynb)

| Part of the session | You do | We check: paste in the shared document |
| --- | --- | --- |
| 1. Text as data: sixty years, from word lists to LLMs | listen; `sessions/04/text_as_data.md` to go further | |
| 2. Three ways into the ScienceCluster | with an account: the small job of `sessions/04/cluster/demo/`; without: Part 0 of both notebooks | your job ID, and the node it ran on |
| 3. Your paper and your data, connected | listen; `setup/overleaf_dropbox_guide.md` for later | |
| 4. From a PDF to a table | `s4_ocr.ipynb`, Parts 1 to 7 | your document, Tesseract's confidence, the three agreements, one word a reader got right and the others did not |
| 5. Extracting with an LLM | `s4_extraction.ipynb`, Parts 1 to 3 | accuracy per field for each model you ran; one disagreement where the catalogue is wrong |

**Goal for 12:00.** Five historical PDFs read three times, by Tesseract, by DeepSeek-OCR and by GPT, in one table; 300 leaflets turned into a table by GPT (and Claude if you have its key) and checked field by field against the catalogue; both bundles downloaded.

---

## Before the session (20 minutes, at home)

1. **Keys.** Hugo's email has a capped OpenAI key (and an Anthropic key, if he sends one). Put them in Colab Secrets (key icon in the left sidebar; names `OPENAI_API_KEY` and `ANTHROPIC_API_KEY`; switch on "Notebook access"). Never in a cell, never in a file you share. Both notebooks work with the OpenAI key alone.
2. **Test both notebooks**: run Part 0 of each, and Part 1 of `s4_extraction.ipynb` (it downloads 300 documents, one or two minutes). For `s4_ocr.ipynb`, choose the T4 GPU runtime first. If something fails, write to Hugo before 8:30 with the error message.
3. **A PDF of your own** (optional): a scan from your project, for Part 8 of `s4_ocr.ipynb`.
4. **With a ScienceCluster account** (optional): the VPN if you are off campus, then the nickname and the key (`sessions/04/cluster/README.md`, Route 2). Five minutes.

---

## Part 2 of the session. Three ways into the ScienceCluster

### Step 1. Your route

- **With an account**: `sessions/04/cluster/README.md`. The nickname and the key, then the small job: copy `demo/` to the cluster, `sbatch job.sh`, `squeue`, `sacct`, `cat` the output. Then ask your agent to do the same, and read every command before you approve it.
- **Without**: Part 0 of both notebooks. Keep the README for the day you have an account (your PI adds you to the group's Science IT project).

Done when: you have pasted *your job ID, and the name of the node it ran on*.

## Part 4 of the session. From a PDF to a table

`s4_ocr.ipynb`, with the **T4 GPU** runtime. Just before the break (10:40), run Part 0 and the first cell of Part 4: it installs Ollama and downloads DeepSeek-OCR (about 7 GB, three to five minutes) while you have coffee. No GPU left in Colab? Skip Part 4: everything else works with two readers.

### Step 2. Look, and read with Tesseract

Parts 1 and 2. Hugo shows them on the 1958 leaflet; you choose **another** document: set `DOC = "decree_1793"` (old print) or `DOC = "manuscript_1760"` (handwriting) and rerun. Look at the picture, at Tesseract's table of words, at its confidence, at the words it flags in red.

### Step 3. Two more readers

Part 3: GPT reads the same page, with a form: the transcription, and five variables. Part 4: DeepSeek-OCR, a free model that only transcribes, on the GPU of your Colab. Part 5: the agreement between each pair of readings, and the words only one reader has. Read them with the picture open: who is right?

Part 6: three pages chosen to make the readers part ways (handwriting, the long s, columns), side by side. On each, which reader does best, and how does each one fail?

### Step 4. The loop

Part 7: every page of the five documents, three readers, one table. Read it by kind of document. Then the time and cost per page, and what 8,000 pages would cost.

Done when: you have pasted *your document, Tesseract's mean confidence, the three agreements, one word a reader read better than the others, one word a reader should not have written*.

**Faster?** Part 8: a PDF of your own.

## Part 5 of the session. Extracting with an LLM

`s4_extraction.ipynb`.

### Step 5. Collect, and check

Part 1. Read each check before going on: the number found, requested = returned + missing, short texts, duplicates. Open the PDF of the first document next to its OCR. Then the catalogue: someone else's coding.

### Step 6. One form, then 300

Part 2. Run the single call first and read the whole answer next to the catalogue record printed below it. Then the 300 with GPT, and with Claude if you have its key. Watch the cost lines.

### Step 7. Check against the catalogue

- The table of outcomes per field, and the accuracy where both have a value.
- `disagreements("gpt")` (and `disagreements("claude")`): open the PDF of each. Who is right?
- The offices: the model's 0/1 against the catalogue's.

Done when: you have pasted *accuracy per field for each model, and one disagreement where the catalogue, not the model, is wrong*.

### Step 8. The table and the bundle

Part 3. Download the zip. Open `params.json`: could a referee rerun your extraction from it?

**Your own project.** Prompt 13 on documents of your project.

## Before you leave

1. Both bundles downloaded.
2. In your project: copy prompt 13 from `template/prompts/`, and the new section "Measures, extraction and estimates" of `template/CLAUDE.md` into yours.
3. Prompt 05: the entry in `PROJECT_HISTORY.md`, and the commit.
4. For Session 5: ten minutes of audio or video from your project, and your 100 coded texts.

The Archelec texts are under a restrictive licence (CC BY-NC-ND): they stay out of any public repository, including yours.
