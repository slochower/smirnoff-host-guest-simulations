import pandas as pd
from constants import *
import os
import json
import numpy as np
from summarize import combine_data
from tqdm import tqdm

bg2bg2_tip3p = pd.DataFrame()

for system in tqdm(systems):

    # Delta G

    prefix = os.path.join("/home/davids4/gpfs-niel/bg2bg2-tip3p", system, "fe")
    bg2bg2_tip3p_attach = np.genfromtxt(os.path.join(prefix, "ti-a.dat"))
    bg2bg2_tip3p_pull = np.genfromtxt(os.path.join(prefix, "ti-u.dat"))

    if system[0] == "a":
        bg2bg2_tip3p_release = np.genfromtxt(
            os.path.join("systems", "a-release", "bg2bg2-tip3p", "ti-r.dat")
        )
    else:
        bg2bg2_tip3p_release = np.genfromtxt(
            os.path.join("systems", "b-release", "bg2bg2-tip3p", "ti-r.dat")
        )
    bg2bg2_tip3p_analytic = 7.14

    delta_g = -1 * (
        bg2bg2_tip3p_attach[-1, 1]
        + bg2bg2_tip3p_pull[-1, 1]
        - bg2bg2_tip3p_release[-1, 1]
        - bg2bg2_tip3p_analytic
    )
    delta_g_sem = np.sqrt(
        bg2bg2_tip3p_attach[-1, 2] ** 2
        + bg2bg2_tip3p_pull[-1, 2] ** 2
        + bg2bg2_tip3p_release[-1, 2] ** 2
    )

    # Delta H

    with open(f"results/{system}-bg2bg2_tip3p-enthalpy-full.json", "r") as f:
        json_data = f.read()
    loaded = json.loads(json_data)
    delta_h = loaded["a00"]["total"][0] - loaded["r00"]["total"][0]
    delta_h_sem = np.sqrt(
        loaded["a00"]["total"][1] ** 2 + loaded["r00"]["total"][1] ** 2
    )

    bg2bg2_tip3p = bg2bg2_tip3p.append(
        {
            "System": system,
            "Delta G": delta_g,
            "G_SEM": delta_g_sem,
            "Delta H": delta_h,
            "H_SEM": delta_h_sem,
            "Type": guest_types[system[0:-2]],
        },
        ignore_index=True,
    )

bg2bg2_tip3p.to_csv("results/bg2bg2_tip3p_by_orientation.csv")
bg2bg2_tip3p_combined = combine_data(bg2bg2_tip3p)
bg2bg2_tip3p_combined.to_csv("results/bg2bg2_tip3p_combined.csv")
