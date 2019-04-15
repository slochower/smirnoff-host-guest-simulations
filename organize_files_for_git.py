import os
import shutil
from glob import glob

systems = glob("systems/*")
for system in systems[0:2]:

    gaff_detritus = glob(system + "/bgbg-tip3p/*")
    for file in gaff_detritus:

        print(file)

        if "full" in file:
