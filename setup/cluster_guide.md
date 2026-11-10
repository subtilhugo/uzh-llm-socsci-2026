# The UZH ScienceCluster: three doors

The ScienceCluster is the computing cluster of UZH, run by Science IT (S3IT): GPUs (L4 24 GB, A100 80 GB, H100, H200), long jobs, and storage that stays at UZH. This guide is what Hugo showed in Session 3. Official documentation: https://docs.s3it.uzh.ch

Checked on 3 November 2026. Commands marked *(course recipe)* are not from the S3IT documentation: test them before you rely on them.

## Getting an account

- You need a UZH AD account and to be a member of a research group that has a **Science IT project**. The project owner (usually your PI) or its technical contact adds you in the Project Dashboard (https://herd.science-it.uzh.ch/project/). A group without a project first needs a Science IT agreement. Use is billed to the project, per use. https://docs.s3it.uzh.ch/users/
- **Off campus, connect to the UZH VPN first.** SSH works only from the UZH network. https://docs.s3it.uzh.ch/cluster/quickstart/

## The rules that matter

- **Login nodes** are for light work: moving files, editing, submitting jobs. Everything else runs in a **job**, on a compute node. https://docs.s3it.uzh.ch/cluster/how_to_use_cluster_and_filesystem_nicely/
- **Storage.** `/home/$USER`: 400 GB. `/scratch/$USER`: 20 TB, but files not accessed for 30 days are deleted. `/shares/<project>`: persistent, billed. **No backups anywhere.** `quota` shows your use. https://docs.s3it.uzh.ch/cluster/data/
- **Model weights are large**: put caches on `/scratch` (or `/shares`), never in `/home`.

## Door 1. The terminal (SSH)

```bash
ssh -l <shortname> cluster.s3it.uzh.ch      # your UZH shortname and AD password
quota                                        # how much space you use
module available                             # the software you can load
```

Optional, so you stop typing your password: an SSH key, and a short name for the host.

```bash
# on your laptop
ssh-keygen -t ed25519
ssh-copy-id <shortname>@cluster.s3it.uzh.ch
# then add to ~/.ssh/config:
#   Host uzh
#       HostName cluster.s3it.uzh.ch
#       User <shortname>
ssh uzh
```

**An interactive session on a GPU node** (from the quickstart). Everything you run after it runs on the compute node, until `exit`.

```bash
module load l4                               # the L4 GPUs; also: a100, h100
srun --pty --time=1:0:0 --mem-per-cpu=7800 --cpus-per-task=2 --gpus=1 bash -l
nvidia-smi                                   # which GPU you got
exit                                         # back to the login node; the GPU is released
```

**A batch job**, for anything longer than you want to wait for: write a script, submit it, check on it.

```bash
#!/bin/bash
#SBATCH --job-name=annotate
#SBATCH --time=04:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --gpus=1
#SBATCH --output=logs/%x_%j.out
python3 code/20_annotate.py
```

```bash
module load l4
sbatch annotate.sh       # prints the job ID
squeue --me              # your jobs: pending (PD) or running (R)
scancel <jobid>          # stop one
```

GPU types: `--gpus=1` (first available), `--gpus=H100:1`, `--gpus=A100:1 --constraint=GPUMEM80GB`. Time limits: 24 h by default, up to 7 days with the `long` QoS. https://docs.s3it.uzh.ch/cluster/job_submission/ and https://docs.s3it.uzh.ch/cluster/resources/

## Door 2. An agent on the cluster (Claude Code)

The same agent as on your laptop, working in a folder on the cluster. Its best use there: writing job scripts, submitting them, reading the logs, and relaunching what failed.

```bash
# on the login node, once
curl -fsSL https://claude.ai/install.sh | bash
```

- **Logging in without a browser.** Run `claude`, press `c` to copy the login URL, open it on your laptop, and paste the code back into the terminal. https://code.claude.com/docs/en/authentication
- **Your home is shared by every node.** A self-update on one node can remove the binary a session on another node is running (it crashes with `Bus error`). Turn self-updates off in `~/.claude/settings.json`, and update by hand (`claude update`) when no session runs: https://code.claude.com/docs/en/setup

  ```json
  { "env": { "DISABLE_UPDATES": "1" } }
  ```

- **On the login node, the agent edits and submits; it does not compute.** Tell it so in your project's `CLAUDE.md`: *"This project runs on the ScienceCluster. Never run analysis code on the login node: write a job script and submit it with sbatch."*
- **Inside a job** (`srun ... bash -l`, then `claude`), it can run code on the compute node, if that node reaches the internet *(to test: `curl -sI https://api.anthropic.com` inside the session)*.
- **VS Code or Cursor over SSH**: S3IT asks you not to connect them to the login nodes. Their documentation has an advanced, unsupported recipe that connects the editor to a compute node through a job: https://docs.s3it.uzh.ch/cluster/vscode/

Claude Code needs a paid Claude plan (Pro or above) or an API key, as on your laptop.

## Door 3. The browser (ScienceApps)

https://apps.s3it.uzh.ch, with your UZH login, in a private window. Every cluster account has access. https://docs.s3it.uzh.ch/cluster/apps/overview/

- **Jupyter** and **RStudio** on a compute node, with the GPU you choose in the form (type, hours up to 168, cores, memory).
- **A desktop** (MATE or Xfce), also on GPU nodes.
- **Code Server** (VS Code in the browser), in beta, without the built-in AI features that need an external connection.
- A **file browser** (upload, download) and a **shell** in the browser.

The simplest door when you do not want a terminal: start a Jupyter session with one L4 GPU, open the Session 3 notebook, and run Part 5 against a model served on that node.

## One environment for both doors (Session 4)

The S3IT way to install Python packages on the cluster is a container built from a conda `env.yml` (https://docs.s3it.uzh.ch/cluster/how_to_use_conda/). The same container runs your batch jobs (`apptainer exec --nv env.sif python script.py`) and, installed with S3IT's `apptainer_ipykernel.py`, appears as a kernel in ScienceApps Jupyter (https://docs.s3it.uzh.ch/cluster/apps/user_guide/). A container cannot be changed from a notebook: a new package means a new build.

`sessions/04/cluster/` has the files and the full sequence: build the container, fetch the 1978 professions de foi from the Internet Archive API, embed them on a GPU with `sbatch`, then open the Session 4 notebook in ScienceApps with the same environment.

## A local model on a GPU node *(course recipe)*

S3IT has no page on LLMs. This uses Apptainer, which S3IT supports for containers (https://docs.s3it.uzh.ch/cluster/containers/), and the official Ollama image. Inside an interactive GPU session:

```bash
module load apptainer
export APPTAINER_CACHEDIR=/scratch/$USER/apptainer
export OLLAMA_MODELS=/scratch/$USER/ollama-models       # weights on scratch, not home
mkdir -p $APPTAINER_CACHEDIR $OLLAMA_MODELS
apptainer pull /scratch/$USER/ollama.sif docker://ollama/ollama
apptainer exec --nv /scratch/$USER/ollama.sif ollama serve > ollama.log 2>&1 &
sleep 5
apptainer exec --nv /scratch/$USER/ollama.sif ollama pull gemma4:26b   # 18 GB: fits an L4 (24 GB)
apptainer exec --nv /scratch/$USER/ollama.sif ollama run gemma4:26b "Bonjour"
```

Then, on the same node, the notebook's Part 5 works unchanged (Ollama answers on `localhost:11434`). For a whole corpus, put the same lines in a batch job. For many requests in parallel, vLLM serves an OpenAI-compatible API (image `vllm/vllm-openai`, port 8000), and Part 5's `make_openai_annotator` talks to it.

Do not open Ollama's port to others: UZH IT warns against exposing its API (https://www.zi.uzh.ch/en/teaching-and-research/science-it/articles/2025-ai-on-your-laptop.html).

## Beyond the cluster

- **CSCS Inference API**: open models (Apertus, Qwen, Gemma, and others) behind an OpenAI- and Anthropic-compatible endpoint, for groups with a CSCS project; billed to that allocation, prompts not logged. https://docs.cscs.ch/services/inference/api/ UZH groups get CSCS access through S3IT: https://docs.s3it.uzh.ch/supercomputer/access/
- **Apertus**, the Swiss open model (EPFL, ETH Zurich, CSCS): weights, data and training recipe published, Apache 2.0. Version 1.5, July 2026: https://huggingface.co/collections/swiss-ai/apertus-v15
