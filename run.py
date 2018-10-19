import glob as glob
import numpy as np
import time
import subprocess as sp
import os as os

directories = glob.glob("systems/*/smirnoff/a*")
directories += glob.glob("systems/*/smirnoff/p*")
directories = [i for i in directories if os.path.isdir(i)]

full_multiples = int(np.floor(len(directories) / 100))
chunks = [[i * 100, i * 100 + 100] for i in range(full_multiples)] + [
    [full_multiples * 100, len(directories)]
]

for chunk in chunks:
    for directory in sorted(directories)[chunk[0] : chunk[1]]:
        if not os.path.isfile(os.path.join(directory, "prod.009.nc")):
            print(f"Running qsub tscc-driver.sh in {directory}")
            sp.call("qsub tscc-driver.sh", cwd=directory, shell=True)
        else:
            print(f"{directory} complete")
    print("Sleeping for 60 seconds.")
    time.sleep(60)
