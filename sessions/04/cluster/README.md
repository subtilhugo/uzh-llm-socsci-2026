# Session 4, Part 2: three ways into the ScienceCluster

The same machines, reached three ways: the web interface, the terminal, and Claude Code. Start with the small job in `demo/`. The second half of this page ("Going further") is a real task: a GPU job that embeds 4,010 documents, and the same environment as a Jupyter kernel.

You need a cluster account (your group's Science IT project; your PI adds you). Every general command is also in `setup/cluster_guide.md`.

## Step zero: off campus, the UZH VPN

Install Ivanti Secure Access from the UZH VPN download page, add a connection with the server `remoteaccess.uzh.ch/vpn`, connect with your UZH account and approve the MFA prompt. Without it the cluster does not answer (`Network is unreachable`). On campus Wi-Fi (eduroam) you are already inside.

## Route 1. The web interface

https://apps.s3it.uzh.ch, with your UZH login. Nothing to install. **Files** (browse, upload, download; "Open in Terminal" gives a shell in the browser), **Jobs** (what is running), **Interactive Apps** (Jupyter, RStudio, VS Code on a compute node: choose hours, cores, memory and a GPU in a form, then Launch). Delete idle sessions: they are billed while they run.

## Route 2. The terminal (SSH)

```bash
ssh <you>@cluster.s3it.uzh.ch      # your UZH shortname and password
hostname                            # u24-login-...: you are on the login node
```

Two time-savers, once. A nickname, in `~/.ssh/config` on your laptop:

```
Host scicluster
  HostName cluster.s3it.uzh.ch
  User <you>
  ServerAliveInterval 60
```

And a key instead of a password (an agent cannot type passwords):

```bash
ssh-keygen -t ed25519
ssh-copy-id scicluster
```

The small job. `demo/job.sh` is a booking form (the `#SBATCH` lines: time, cores, memory) and a recipe (load Python, run the script):

```bash
scp -r sessions/04/cluster/demo scicluster:demo_cours_llm     # from the repository, on your laptop
ssh scicluster
cd demo_cours_llm
sbatch job.sh                 # Submitted batch job 1234567
squeue -u $USER               # R = running, PD = pending
sacct -j 1234567 -X           # once it is done: COMPLETED, and the node it ran on
cat demo_1234567.out
```

The output names the machine: a compute node, not the login node.

## Route 3. Claude Code

Claude Code runs on your laptop and reaches the cluster through the same `ssh scicluster`. It needs the VPN, the nickname, the key, and you approving each command. What Hugo typed:

> Connect to scicluster, create a folder demo_cours_llm, write a small Python script that counts the words in three sentences, run it as a Slurm job with 1 CPU and 1 GB for 5 minutes, and show me the output.

It failed first (`module: command not found`: the job script needs `#!/bin/bash -l`; and quotes mangled while writing the file remotely: write locally, then `scp`), read the error, and fixed it. Read what it runs before you approve: it sends what it reads to Anthropic, and it can delete files as fast as it writes them.

## Do and don't

| Do | Don't |
| --- | --- |
| Send heavy work to Slurm (`sbatch`, or a session in ScienceApps). | Run heavy code on the login node: it is shared by everyone. |
| Ask for what the job needs (time, cores, memory, GPUs): small requests start sooner. | Ask for more GPUs than your code uses: you wait much longer in the queue, your group pays, and the job runs no faster. |
| Copy what you want to keep from `scratch` to `home` or `shares`. | Leave the only copy on `scratch`: files untouched for 30 days are deleted, with no backup. |
| Delete Jupyter sessions you no longer use. | Show an agent interview transcripts or personal data. |
| Read what an agent runs before you approve. | Approve a command you do not understand. |

## When it breaks

| Message | Cause, fix |
| --- | --- |
| `Network is unreachable` | The VPN is off. |
| `Permission denied (publickey,password)` | No key installed: `ssh-copy-id scicluster`. |
| `REMOTE HOST IDENTIFICATION HAS CHANGED` | The server's key was renewed. Check with IT, then `ssh-keygen -R cluster.s3it.uzh.ch`. |
| `module: command not found` | Job script without a login shell. First line: `#!/bin/bash -l`. |

---

# Going further: a GPU job, and the same environment in Jupyter

One task through two routes: **download the 4,010 professions de foi of the first round of the 1978 legislative election, and embed them on a GPU.** The same environment then serves the notebook in the browser. Commands marked *(course recipe)* are not from the S3IT documentation: test them before you rely on them.

## The files

| File | What it does |
| --- | --- |
| `env.yml` | The Python packages: pandas, scikit-learn, sentence-transformers, the Anthropic and OpenAI libraries, ipykernel |
| `s4.def` | The container that holds them, built from `env.yml` (the S3IT recipe for conda on the cluster) |
| `fetch_corpus.py` | Archelec through the Internet Archive API: identifiers, catalogue records, OCR texts. Checks requested = returned + missing |
| `embed_corpus.py` | Cuts each text into passages of 80 words and embeds them (multilingual-e5-small) |
| `embed.sbatch` | The batch job that runs `embed_corpus.py` on one GPU |

## By SSH

### Once: copy the files and build the environment

```bash
# on your laptop, from the repository
scp -r sessions/04/cluster <shortname>@cluster.s3it.uzh.ch:~/s4

# on the cluster
ssh -l <shortname> cluster.s3it.uzh.ch
cd ~/s4
srun --pty -n 1 -c 2 --time=01:00:00 --mem=16G bash -l     # building is work: not on the login node
module load apptainer
export APPTAINER_CACHEDIR=/scratch/$USER/apptainer
APPTAINER_BINDPATH="" apptainer build /scratch/$USER/s4.sif s4.def    # 10 to 20 minutes
```

### Fetch the corpus, and check it

Still in the interactive session (it is a compute node). Does this node reach the internet? *(course recipe: test it first)*

```bash
curl -sI https://archive.org | head -1                      # HTTP/2 200 : yes
apptainer exec /scratch/$USER/s4.sif python fetch_corpus.py --date 1978-03-12 --out /scratch/$USER/archelec
# 4010 documents found, 4010 to fetch ... requested 4010 = returned ... + missing ...
cat /scratch/$USER/archelec/1978-03-12/fetch_log.json | head -8
```

Read the list of missing documents before you go on. The texts are under a restrictive licence: they stay on `/scratch`, never in a public repository.

Download the embedding model once, so that the job does not depend on the network *(course recipe)*:

```bash
export HF_HOME=/scratch/$USER/hf
apptainer exec /scratch/$USER/s4.sif python embed_corpus.py --download-only
exit                                                         # leave the compute node
```

### Submit the job

```bash
cd ~/s4
mkdir -p logs
module load l4
sbatch embed.sbatch          # Submitted batch job 1234567
squeue --me                  # PD = waiting for a GPU, R = running
tail -f logs/embed-1978_1234567.out
```

The log ends with `run.json` (model, GPU, number of passages, seconds) and the five passages closest to a local promise. The results are in `/scratch/$USER/archelec/1978-03-12/embeddings/`. Bring them home with `scp`, or open them in ScienceApps.

## In the browser (ScienceApps)

https://apps.s3it.uzh.ch, with your UZH login.

### Once: the same container as a Jupyter kernel

In ScienceApps: **Clusters → ScienceCluster Shell Access** (or by SSH), then:

```bash
srun --pty -n 1 -c 2 --time=00:30:00 --mem=7G bash -l
cd ~/s4
curl -O https://gitlab.uzh.ch/s3it/docs/-/snippets/271/raw/main/apptainer_ipykernel.py
module load apptainer
python apptainer_ipykernel.py install /scratch/$USER/s4.sif --name s4
python apptainer_ipykernel.py list
exit
```

The container cannot be changed from the notebook: no `pip install` in a cell. A missing package means editing `env.yml` and building again.

### Every time: a Jupyter session on a GPU

1. **Interactive Apps → Jupyter.** Hours: 3. Cores: 4. RAM: 16 GB. GPU: L4.
2. **My Interactive Sessions**: wait for "Running", then **Connect to Jupyter**.
3. Upload `s4_extraction.ipynb` (file browser, or `git clone` the repository in the shell), open it, choose the kernel **s4**.
4. The API keys: not in the notebook. Put them in `~/.env` (`ANTHROPIC_API_KEY=...`, `OPENAI_API_KEY=...`), then `chmod 600 ~/.env`. The notebook reads that file when it is not in Colab.
5. Delete the session when you are done: the GPU is billed to your group while it runs.

### What it buys you

- The notebook runs next to the data, on a GPU, without Colab's time limits.
- The 4,010 embeddings of the job are already on `/scratch`: in the notebook, set `CLUSTER_EMBEDDINGS` to their folder and Part 5 works on the whole election.
- Confidential data never leave UZH: with a local model on the same node (`setup/cluster_guide.md`, "A local model on a GPU node"), nothing goes to a provider.

## Before the session (Hugo)

- [ ] Build `s4.sif`, fetch the 1978 corpus, download the model (above).
- [ ] Run `embed.sbatch` once; note the GPU and the seconds from `run.json` for the slide.
- [ ] Install the kernel; open a Jupyter session; run Part 0 of the notebook with the kernel **s4**.
- [ ] Run the small job of `demo/` by the three routes, once.
