import glob as glob
import numpy as np
import time
import subprocess as sp
import os as os

systems = glob.glob("systems/*")

for system in systems:
    attach_windows = glob.glob(os.path.join("..", system, "smirnoff") + "/a*")
    pull_windows = glob.glob(os.path.join("..", system, "smirnoff") + "/p*")
    windows = attach_windows + pull_windows
    
    counter = 0
    for window in windows:
        if os.path.isfile(os.path.join(window, "prod.009.nc")):
            counter += 1
        else:
            # print(f"{system} {window}")
            pass
    if counter < 60:
        print(f"{system}\t{counter:2}/60")
        pass
    else:
        print(f"{system}\tComplete")
        pass
