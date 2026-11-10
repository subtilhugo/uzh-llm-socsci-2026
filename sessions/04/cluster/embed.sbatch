#!/usr/bin/bash -l
#SBATCH --job-name=embed-1978
#SBATCH --time=00:30:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --gpus=1
#SBATCH --output=logs/%x_%j.out

# Submit from the login node, in this folder:
#   module load l4
#   mkdir -p logs
#   sbatch embed.sbatch
# Then: squeue --me (PD = waiting, R = running), and tail -f logs/embed-1978_<jobid>.out

module load apptainer
export HF_HOME=/scratch/$USER/hf            # model weights on scratch, never in home
CORPUS=/scratch/$USER/archelec/1978-03-12

nvidia-smi --query-gpu=name,memory.total --format=csv
apptainer exec --nv /scratch/$USER/s4.sif python embed_corpus.py --corpus "$CORPUS"
