#!/bin/bash
#SBATCH -A SNIC2017-11-7
#SBATCH -J run_iupred
#SBATCH -t 02:30:00
#SBATCH -n 1
#SBATCH -c 8 # Or 14, or any other number of cores to use for tblastn
# -c can also be specified as arg to "sbatch" and overrides the value
# specified here.

source ../../venv-work/bin/activate
python ./run_iupred.py