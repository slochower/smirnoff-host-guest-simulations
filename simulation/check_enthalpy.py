import glob as glob
import numpy as np
import time
import subprocess as sp
import os as os

systems = [os.path.basename(i) for i in glob.glob("../systems/*")]
print(systems)

for system in systems:
    end_points = [os.path.join("..", "systems", system, "smirnoff", "a000")]
    end_points.append(os.path.join("..", "systems", system, "smirnoff", "p045"))
    counter = 0
    for window in end_points:
        if os.path.isfile(os.path.join(window, "prod.999.nc")):
            counter += 1
        else:
            # print(f"{system} {window}")
            pass
    if counter < 2:
        print(f"{system}\t{counter:2}/2")
        pass
    else:
        print(f"{system}\tComplete")
        pass
