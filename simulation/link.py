import os as os
import glob as glob

# directories = glob.glob("../systems/*/smirnoff/a*")
# directories += glob.glob("../systems/*/smirnoff/p*")
# directories += glob.glob("../systems/*/smirnoff/r*")
directories = glob.glob("../systems/a-release/smirnoff/*")
directories += glob.glob("../systems/b-release/smirnoff/*")
directories = [i for i in directories if os.path.isdir(i)]

for directory in sorted(directories):
    print(directory)
    try:
        os.symlink("../../../../simulation/simulate.py", os.path.join(directory,
                                                               "simulate.py"))
    except:
        os.remove(os.path.join(directory, "simulate.py"))
        os.symlink("../../../../simulation/simulate.py", os.path.join(directory,
                                                               "simulate.py"))

    tscc = f"""
#!/bin/bash
#PBS -l walltime=1:00:00,nodes=1:ppn=2 -q home-gibbs
#PBS -j oe -r n
#PBS -N {directory.split('/')[-3]}-{directory.split('/')[-1]}

source /home/davids4/amber18_gnu.sh

SCRDIR=/oasis/tscc/scratch/davids4/smirnoff-host-guest-simulations/{directory.split('/')[-3]}-{directory.split('/')[-1]}
mkdir -p $SCRDIR

# Need the `-L` to resolve any links.
rsync -avL $PBS_O_WORKDIR/ $SCRDIR/

cd $SCRDIR
source activate paprika
python simulate.py

rsync -avL $SCRDIR/ $PBS_O_WORKDIR/
"""
    with open(os.path.join(directory, "tscc-driver.sh"), "w") as f:
        f.write(tscc)
