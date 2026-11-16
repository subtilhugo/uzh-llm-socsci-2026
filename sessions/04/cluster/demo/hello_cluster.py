"""The smallest job: count the words of three sentences, and say where it ran."""
import os
import platform
import socket

SENTENCES = [
    "Le parlement a adopté la réforme des retraites.",
    "Les maires demandent plus de moyens pour les communes rurales.",
    "La ligne de chemin de fer de la vallée ne fermera pas.",
]

print(f"Machine : {socket.gethostname()} | Python {platform.python_version()}")
print(f"Job Slurm : {os.environ.get('SLURM_JOB_ID', 'none')} | CPUs : {os.environ.get('SLURM_CPUS_PER_TASK', '?')}")
for s in SENTENCES:
    print(f"  {len(s.split())} mots -> {s}")
print("Terminé.")
