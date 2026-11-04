# Session 3: the Colab annotation, done by Claude Code

Same 24 sentences, same codebook (sha256 `588f3e7e…`), same model as the Colab notebook. The difference: here the agent writes the script; you check it against the notebook.

1. Copy this folder to your Desktop (e.g. `~/Desktop/demo-annotation`).
2. Create `.env` with one line: `OPENAI_API_KEY=...` (or `ANTHROPIC_API_KEY=...` for Claude). Check: `git init && git check-ignore .env` prints `.env`.
3. `pip install openai pandas` (or `anthropic pandas`).
4. Claude Desktop, Code tab, Local, select this folder, mode Manual. Paste the prompts of the demo sheet, one at a time.

What to check in the script it writes: the endpoint and the model are the ones you asked for; the system prompt is `codebook.md` word for word (`params.json` must show sha256 `588f3e7e…`); the key is read from `.env` and never printed; every raw answer is in `outputs/raw.jsonl`.
