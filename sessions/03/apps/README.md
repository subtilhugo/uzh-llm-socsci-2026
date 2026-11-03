# Session 3: two small apps on a local model

Both talk to Ollama through its API, on `http://localhost:11434`. Nothing leaves your machine, unless you pick a cloud model (a tag ending in `cloud`).

```bash
pip install -r requirements.txt
ollama pull qwen3.5:4b        # 3.4 GB; qwen3.5:9b (6.6 GB) or ministral-3:8b (6 GB) if you have 16 GB of memory
python check_local.py --models qwen3.5:4b   # two minutes: server, model, structured answer, tool call, internet
```

## 1. `label_app.py`: label texts with one or two local models

```bash
streamlit run label_app.py
```

A browser tab opens. Pick one or two models, keep the 24 example sentences (written for this demo, not Manifesto Project data) or upload your own CSV, press **Label**. You get the labels, the speed, the agreement with your own codes and between the two models, the disagreements with the model's reasons, and `labels.csv` plus `params.json` to keep. The tab **The API call** shows the exact request the app sent and the server's answer.

## 2. `local_agent.py`: a research agent in 200 lines

```bash
python local_agent.py                                  # default task, qwen3.5:9b
python local_agent.py "your task" --model qwen3.5:4b
python local_agent.py --think                          # let the model think first
```

The loop: the model reads the task and the tool list; it answers with text (done) or with a tool call; the script runs the tool and sends the result back; repeat. Tools: `search_papers` (OpenAlex), `find_commune` (geo.api.gouv.fr), `calculate`, `list_files`, `read_file`, `write_file` (into `agent_output/` only). Every step is printed and saved in `agent_output/run_<time>.jsonl`.

The same agent with Claude, for comparison (key in `ANTHROPIC_API_KEY`):

```bash
python local_agent.py --backend openai --url https://api.anthropic.com/v1 --model claude-haiku-5-5
```

## 3. Claude Code on a local model

Ollama 0.15 or later speaks Anthropic's API, so Claude Code can run on a model on your machine:

```bash
ollama launch claude --model qwen3.5:9b
```

Set the context length to at least 64,000 tokens in Ollama's settings first. Slower and weaker than Claude, but nothing leaves the machine.
