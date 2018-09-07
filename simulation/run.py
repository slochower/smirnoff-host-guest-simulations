import glob as glob
import numpy as np
import time
import subprocess as sp
import os as os

# directories = glob.glob("systems/*/smirnoff/a*")
# directories += glob.glob("systems/*/smirnoff/p*")
# directories = glob.glob("../systems/a-release/smirnoff/*")
# directories += glob.glob("../systems/b-release/smirnoff/*")
directories = glob.glob("../systems/*/smirnoff/a000")
directories += glob.glob("../systems/*/smirnoff/p045")
directories = [i for i in directories if "release" not in i]
directories = [i for i in directories if os.path.isdir(i)]

jobs = sp.Popen(("qstat"), stdout=sp.PIPE)
try:
    my_jobs = sp.check_output(("grep", "davids4"), stdin=jobs.stdout)
    my_jobs_split = my_jobs.decode("utf-8").split()
    my_jobs_scheduled = my_jobs_split[1::6]
except:
    my_jobs_scheduled = []


full_multiples = int(np.floor(len(directories) / 100))
chunks = [[i * 100, i * 100 + 100] for i in range(full_multiples)] + [
    [full_multiples * 100, len(directories)]
]

wall_time = 60 * 60
counter = 0
for chunk in chunks:
    for directory in sorted(directories)[chunk[0] : chunk[1]]:
        job_name = directory[8:15] + "-" + directory[25:29]
        if job_name in my_jobs_scheduled:
            print(f"{directory} already in the scheduler.")
            continue
        if not os.path.isfile(os.path.join(directory, "prod.999.nc")):
            print(f"Running qsub tscc-driver.sh in {directory}")
            sp.call("qsub tscc-driver.sh", cwd=directory, shell=True)
            counter += 1
        if counter == 1400:
            print("Sleeping for 60 seconds.")
            time.sleep(wall_time)
            counter = 0
