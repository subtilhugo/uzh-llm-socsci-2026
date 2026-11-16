#!/bin/bash -l
#SBATCH --job-name=demo_cours
#SBATCH --time=00:05:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --output=demo_%j.out

# The first line ends with -l: a login shell, so that `module` exists inside the job.
module load miniforge3
python hello_cluster.py
