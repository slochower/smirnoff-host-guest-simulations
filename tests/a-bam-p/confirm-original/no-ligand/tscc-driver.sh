#!/bin/bash
#PBS -l walltime=1:00:00,nodes=1:ppn=2 -q home-gibbs
#PBS -j oe -r n
#PBS -N SHG-confirm

source /home/davids4/amber18_gnu.sh

SCRDIR=/oasis/tscc/scratch/davids4/SHG-confirm/$PBS_JOBID
mkdir -p $SCRDIR

# Need the `-L` to resolve any links.
rsync -avL $PBS_O_WORKDIR/ $SCRDIR/

cd $SCRDIR
source activate paprika
python simulate.py

rsync -avL $SCRDIR/ $PBS_O_WORKDIR/