import os
import shutil
from glob import glob

systems = glob("systems/*")
for system in systems[0:2]:
    windows = glob(system +  "/smirnoff/a*")
    windows += glob(system + "/smirnoff/p*")
    windows += glob(system + "/smirnoff/r*")
    for window in windows:
        shutil.rmtree(window)

    gaff_detritus = glob(system + "/bgbg-tip3p/*")
    for file in gaff_detritus:
        print(file)
