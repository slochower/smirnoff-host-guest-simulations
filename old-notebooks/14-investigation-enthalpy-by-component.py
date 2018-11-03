# ---
# jupyter:
#   jupytext_format_version: '1.2'
#   kernelspec:
#     display_name: Python [default]
#     language: python
#     name: python3
#   language_info:
#     codemirror_mode:
#       name: ipython
#       version: 3
#     file_extension: .py
#     mimetype: text/x-python
#     name: python
#     nbconvert_exporter: python
#     pygments_lexer: ipython3
#     version: 3.6.4
# ---

# + {"ExecuteTime": {"start_time": "2018-09-20T22:52:31.988665Z", "end_time": "2018-09-20T22:52:32.783247Z"}}
import pandas as pd
import scipy as sc
import glob
import os
import numpy as np
from tqdm import tqdm

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.colors import colorConverter
import seaborn as sns

# %load_ext autoreload
# %autoreload 2
# %load_ext blackcellmagic
# %matplotlib inline

# + {"ExecuteTime": {"start_time": "2018-09-20T22:52:12.036830Z", "end_time": "2018-09-20T22:52:12.062277Z"}}
import plotting

# +
def read_energies(ff, system, state):

    file_mask = get_files(ff, system, state)
    print(file_mask)
    files = glob.glob(file_mask)
    files = [i for i in files if i[-2:] != "pl"]
    energies = []

    vdw, ele, bnd, ang, dih, v14, e14 = [], [], [], [], [], [], []

    for file in files:
        with open(file, "r") as f:
            for line in f.readlines()[10:]:
                words = line.rstrip().split()
                if words[0] == "L6":
                    vdw.append(float(words[3]))
                    ele.append(float(words[4]))
                elif words[0] == "L7":
                    bnd.append(float(words[2]))
                    ang.append(float(words[3]))
                    dih.append(float(words[4]))
                elif words[0] == "L8":
                    v14.append(float(words[1]))
                    e14.append(float(words[2]))

    print(len(bnd), len(ang), len(dih), len(v14), len(e14), len(vdw), len(ele))
    energies = {
        "Bond": bnd,
        "Angle": ang,
        "Dihedral": dih,
        "V14": v14,
        "E14": e14,
        "VDW": vdw,
        "Ele": ele,
        "Total": [sum(x) for x in zip(bnd, ang, dih, v14, e14, vdw, ele)],
    }

    return pd.DataFrame(energies)


def get_files(ff, system, state):

    base = {
        "SMIRNOFF99Frosst": f"../smirnoff-host-guest-simulations/systems/",
        "BGBG-TIP3P": f"/home/dslochower/niel/projects/cds/wat6/bgbg-tip3p/",
    }

    systems = {"SMIRNOFF99Frosst": "smirnoff/", "BGBG-TIP3P": f""}

    states = {
        "SMIRNOFF99Frosst": {"attach": "a000", "release": "p045"},
        "BGBG-TIP3P": {"attach": "a00", "release": "r00"},
    }

    mask = {"SMIRNOFF99Frosst": "prod*.mden", "BGBG-TIP3P": f"mden*"}

    if ff == "BGBG-TIP3P" and state == "release":
        system = f"{system[0]}-xxxx-s"

    return os.path.join(base[ff], system, systems[ff], states[ff][state], mask[ff])


# -

smirnoff_initial = read_energies("SMIRNOFF99Frosst", "b-mch-p", "attach")
smirnoff_final = read_energies("SMIRNOFF99Frosst", "b-mch-p", "release")

gaff_initial = read_energies("BGBG-TIP3P", "b-mch-p", "attach")
gaff_final = read_energies("BGBG-TIP3P", "b-mch-p", "release")

# +
for component in ["Bond", "Angle", "Dihedral", "V14", "E14", "VDW", "Ele", "Total"]:
    fig = plt.figure(figsize=(6 * 1.2, 6))

    sns.distplot(smirnoff_initial[component], label="Bound")
    sns.distplot(smirnoff_final[component], label="Unbound")
    plt.title(f"SMIRNOFF99Frosst -- {component}")
    plt.xlabel("Energy (kcal/mol)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.show()

for component in ["Bond", "Angle", "Dihedral", "V14", "E14", "VDW", "Ele", "Total"]:
    fig = plt.figure(figsize=(6 * 1.2, 6))

    sns.distplot(gaff_initial[component], label="Bound")
    sns.distplot(gaff_final[component], label="Unbound")
    plt.title(f"GAFF v1.7 -- {component}")
    plt.xlabel("Energy (kcal/mol)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.show()
# -

sns.distplot(smirnoff_final["Dihedral"])

sns.distplot(smirnoff_initial["Dihedral"] - smirnoff_final["Dihedral"])

sns.distplot(gaff_initial["Dihedral"] - gaff_final["Dihedral"])

sns.distplot(gaff_initial["Dihedral"])

sns.distplot(smirnoff_initial["Total"] - smirnoff_final["Total"])

sns.distplot(gaff_initial["Total"] - gaff_final["Total"])
