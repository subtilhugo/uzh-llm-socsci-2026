# Demo: labelling through an API, written by the agent

This folder holds 24 invented sentences in the style of French manifestos (`example_sentences.csv`, with my own label in `my_label`) and the codebook (`codebook.md`). It is the same task as the Colab notebook `s3_live_annotation`, done by an agent instead of by hand.

Rules:
- The codebook is `codebook.md`, used word for word as the system prompt (the instructions). Never edit it.
- Keys are in `.env`. Never print a key, never write it to a file, never put it in an error message.
- Labels come from a script that calls the API, never typed in this chat.
- Every raw answer is saved in `outputs/` as it arrives, before any processing.
- Scripts go in `code/`. Show me a script before running it the first time.
- Every number you report comes from a file you computed, not from memory.
