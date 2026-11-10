# Prompt 12: measure a concept without an LLM, and validate it against your own codes

Before pasting: your texts are in `data/processed/` (one row per text, with an identifier). You have coded about 100 of them yourself, drawn at random (prompt 11, step 2, or the same procedure), in `data/processed/gold_sample.csv`. You have one definition of the concept, in your words.
Suggested setting: Opus, effort `high`. The embeddings run in a script, on your laptop, in Colab or on the cluster, not in this chat.

---

We measure one concept in my texts with three classical tools, and compare them with my own codes. The agent writes the code; the definition, the word list and the decision are mine.

1. **The definition, and the reference.** Read my definition and `data/processed/gold_sample.csv`. Check that the sample was drawn at random with a recorded seed; if it was not, stop and tell me. Report how many texts I coded and how many are positive.
2. **A dictionary, with me.** Propose 20 to 30 words or phrases, each with one sentence of justification, and the rule (how many hits make a positive). I edit the list. Write it to `notes/dictionary_<concept>.md`. Then `code/30_dictionary.py`: normalise the texts (lower case, accents, punctuation) the same way as the words, count, apply the rule.
3. **Embeddings.** `code/31_embed.py`: cut each text into passages of about 80 words, embed them with an open multilingual model (default `intfloat/multilingual-e5-small`; ask me before using a commercial embedding API), save the vectors and the passages to `data/processed/embeddings/` with the model name. A corpus over 10,000 passages runs as a job on the cluster (`setup/cluster_guide.md`), not on the login node.
4. **A search, and a score.** Write five example sentences of the concept with me. For each text: its passage closest to the examples. Show me the ten passages closest to each example; I read them.
5. **A classifier.** `code/32_classifier.py`: logistic regression on the text vectors, my codes as labels, scored by 5-fold cross-validation only (each coded text predicted by a model that did not see it). Never report a score on texts the model was trained on.
6. **Validation**, `outputs/measures/validation.md`: for the dictionary and the classifier, precision, recall, F1 and kappa against my codes; for the score, the AUC; the false positives and false negatives of each, ten of each with the passage that decided; and, if the paper uses an aggregate (a share per group, a mean per year), that aggregate from my codes and from each measure.
7. **I decide** which measure, if any, goes into the analysis, and write why in `PROJECT_HISTORY.md`.

Rules: never change my word list or my definition without asking. Never tune a threshold on the texts you then score. Every number comes from a script.
