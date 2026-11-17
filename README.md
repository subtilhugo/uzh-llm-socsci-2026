# Large Language Models for Social Science Research

PhD workshop, University of Zurich, autumn 2026. Hugo Subtil (IPZ).

Five sessions, Wednesdays 9:00 to 12:00, room AFL-E-003: 14 October, 28 October, 4 November, 18 November, 2 December.

**Shared document (errors, questions, notes for the debrief): [open it here](https://docs.google.com/document/d/1gTubrDtw8KHepmuR8dNzSeI7UypQhjzgEBJ7KX75Xq0/edit?usp=sharing).**

Every participant starts their own research project in Session 1 and advances it in every session. The project lives in a git folder, and an agent (Claude Code or equivalent) works inside that folder.

## Contents

| Folder | What it is |
| --- | --- |
| `setup/` | Installation guide and the verification test to do before Session 1 |
| `template/` | The project template every participant copies in Session 1 (README, CLAUDE.md, PROJECT_HISTORY, prompts) |
| `example-project/` | The instructor's example project, **"Who votes far right? The local rise of the FN/RN in France"**. **It grows after each session.** Use it if you have no project of your own, or to catch up on a missed session. |
| `sessions/01` to `05` | Slides (PDF), worksheet, notebooks and data packs for each session |

## Session 1: setting up an agentic research project

- `sessions/01/slides_s1.pdf`
- `sessions/01/worksheet_s1.md`
- `template/`

**To get everything: green "Code" button on this page, then "Download ZIP". Or, in a terminal: `git clone https://github.com/subtilhugo/uzh-llm-socsci-2026.git`.**

## Session 2: exploring structured data with an agent

- `sessions/02/slides_s2.pdf`
- `sessions/02/worksheet_s2.md`
- `sessions/02/example_pack/`: the 2022 presidential results and the INSEE historical series by municipality, for those without data, and INSEE's history of municipalities for the bonus
- New in `template/`: prompts 06 (document and plan), 07 (clean, merge, describe), 08 (independent review) and 09 (audit one step by hand); an updated prompt 05; `notes/templates/analysis_plan.md` and `codebook.md`; and a new section of `CLAUDE.md`, "Row counts and silent decisions"

## Session 3: from an API to annotated data (remote)

- `sessions/03/slides_s3.pdf`
- `sessions/03/worksheet_s3.md`: what to install the evening before, and the steps of each block
- `sessions/03/s3_manifesto_annotation.ipynb`: the notebook of the session ([open it in Colab](https://colab.research.google.com/github/subtilhugo/uzh-llm-socsci-2026/blob/main/sessions/03/s3_manifesto_annotation.ipynb)). French party manifestos collected through the Manifesto Project API, annotated by Claude through the API and by a local model through Ollama, and compared with the Manifesto Project's human coders
- `setup/cluster_guide.md`: the UZH ScienceCluster by SSH, with an agent, and in the browser
- New in `template/`: prompt 10 (collect from an API, and prove the collection is complete) and prompt 11 (annotate with an LLM, and validate against your own coding); a new section of `CLAUDE.md`, "APIs, keys and LLM annotation"

## Session 4: from texts to variables

- `sessions/04/slides_s4.pdf`: text as data, sixty years from word lists to LLMs; three ways into the ScienceCluster; Overleaf and Dropbox; from a PDF to a table (OCR); extraction with an LLM
- `sessions/04/worksheet_s4.md`: what to do before the session, and the steps of each part
- `sessions/04/text_as_data.md`: to go further after Part 1, lectures and notebooks on text as data
- `sessions/04/s4_ocr.ipynb`: from a PDF to a table, with three readers: Tesseract, DeepSeek-OCR (free, on a Colab GPU) and GPT ([open it in Colab](https://colab.research.google.com/github/subtilhugo/uzh-llm-socsci-2026/blob/main/sessions/04/s4_ocr.ipynb)). Five historical PDFs (a 1760 manuscript, a 1793 decree, three election leaflets); Tesseract's table of words; an LLM's transcription and variables; the three readings compared, then side by side on three pages; a loop over every page
- `sessions/04/s4_extraction.ipynb`: from 300 leaflets to a table ([open it in Colab](https://colab.research.google.com/github/subtilhugo/uzh-llm-socsci-2026/blob/main/sessions/04/s4_extraction.ipynb)). The professions de foi of the 1978 legislative election (Archelec, Sciences Po) through the Internet Archive API; GPT (and Claude, if you have its key) filling in a form, checked against the Sciences Po catalogue
- `sessions/04/cluster/`: the ScienceCluster by three routes (web interface, SSH, Claude Code) with a small job in `demo/`; then, going further, a GPU job that embeds the 4,010 documents of the election and the same environment as a Jupyter kernel
- `setup/overleaf_dropbox_guide.md`: Overleaf through Git or Dropbox sync, and working with an agent in a Dropbox folder
- New in `template/`: prompt 12 (a classical measure, validated), prompt 13 (extract variables with an LLM, checked field by field) and prompt 14 (an estimate from model labels, corrected with your hand codes); a new section of `CLAUDE.md`, "Measures, extraction and estimates". Prompts 12 and 14 are used in Session 5
- The Archelec texts are under a restrictive licence (CC BY-NC-ND): the notebooks download them, and they stay out of any public repository

## Rules of the workshop

1. You delegate execution, never understanding.
2. Read before you accept.
3. Stop when you no longer know what it is doing.
