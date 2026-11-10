# Session 4, Part 1: the ScienceCluster, for real

Session 3 showed the doors. Today one task goes through two of them: **download the 4,010 professions de foi of the first round of the 1978 legislative election, and embed them on a GPU.** The same environment then serves the notebook in the browser.

You need a cluster account (your group's Science IT project; your PI adds you) and, off campus, the UZH VPN. No account: watch, and keep this page for the day you have one. Every general command is in `setup/cluster_guide.md`.

Commands marked *(course recipe)* are not from the S3IT documentation. Hugo runs them the day before the session.

## The files

| File | What it does |
| --- | --- |
| `env.yml` | The Python packages: pandas, scikit-learn, sentence-transformers, the Anthropic and OpenAI libraries, ipykernel |
| `s4.def` | The container that holds them, built from `env.yml` (the S3IT recipe for conda on the cluster) |
| `fetch_corpus.py` | Archelec through the Internet Archive API: identifiers, catalogue records, OCR texts. Checks requested = returned + missing |
| `embed_corpus.py` | Cuts each text into passages of 80 words and embeds them (multilingual-e5-small) |
| `embed.sbatch` | The batch job that runs `embed_corpus.py` on one GPU |

## Door 1. The terminal (SSH)

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

The log ends with `run.json` (model, GPU, number of passages, seconds) and the five passages closest to a local promise. The results are in `/scratch/$USER/archelec/1978-03-12/embeddings/`. Bring them home with `scp`, or open them in Door 3.

## Door 3. The browser (ScienceApps)

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
- The 4,010 embeddings of the job are already on `/scratch`: in the notebook, set `CLUSTER_EMBEDDINGS` to their folder and Part 4 works on the whole election.
- Confidential data never leave UZH: with a local model on the same node (`setup/cluster_guide.md`, "A local model on a GPU node"), nothing goes to a provider.

## Before the session (Hugo)

- [ ] Build `s4.sif`, fetch the 1978 corpus, download the model (above).
- [ ] Run `embed.sbatch` once; note the GPU and the seconds from `run.json` for the slide.
- [ ] Install the kernel; open a Jupyter session; run Part 0 of the notebook with the kernel **s4**.
- [ ] On the day: submit the job at the start of Part 1, so that it has finished by the end of it.
