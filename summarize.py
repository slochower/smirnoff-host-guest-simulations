import pandas as pd
import numpy as np
import json
import os

from constants import experimental_deltaG
from constants import experimental_deltaH
from constants import systems
from constants import guest_types

from bootstrap import dG_bootstrap
from bootstrap import dH_bootstrap

from paprika.restraints_json import json_numpy_obj_hook

experimental_deltaG_list = experimental_deltaG.split("\n")
experimental_deltaH_list = experimental_deltaH.split("\n")

experimental = pd.DataFrame(
    [
        i.split("\t") + j.split("\t")[1:]
        for i, j in zip(experimental_deltaG_list, experimental_deltaH_list)
    ],
    columns=["System", "Delta G", "G_SEM", "Delta H", "H_SEM"],
)

experimental.to_csv("results/experimental.csv")


def combine_data(df):
    """
    Combine data for individual orientations into a single thermodynamic value.
    """

    combined = pd.DataFrame()
    df["Short"] = [i[0:-2] for i in df["System"].values]

    for hg in df["Short"].unique():
        tmp = df[df["Short"] == hg]
        for _, row in tmp.iterrows():
            if "p" in row["System"].split("-")[2]:
                # Reducing generality for speed.
                primary_fe = row[f"Delta G"]
                primary_fe_sem = row[f"G_SEM"]

                primary_enthalpy = row[f"Delta H"]
                primary_enthalpy_sem = row[f"H_SEM"]
            else:
                secondary_fe = row[f"Delta G"]
                secondary_fe_sem = row[f"G_SEM"]

                secondary_enthalpy = row[f"Delta H"]
                secondary_enthalpy_sem = row[f"H_SEM"]
                combined_fe = dG_bootstrap(
                    primary_fe,
                    primary_fe_sem,
                    secondary_fe,
                    secondary_fe_sem,
                    cycles=100000,
                )
        combined_enthalpy = dH_bootstrap(
            primary_enthalpy,
            primary_enthalpy_sem,
            secondary_enthalpy,
            secondary_enthalpy_sem,
            primary_fe,
            primary_fe_sem,
            secondary_fe,
            secondary_fe_sem,
            cycles=100000,
        )

        combined = combined.append(
            {
                "System": hg,
                "Delta G": combined_fe["mean"],
                "G_SEM": combined_fe["sem"],
                "G_CI": combined_fe["ci"],
                "Delta H": combined_enthalpy["mean"],
                "H_SEM": combined_enthalpy["sem"],
                "H_CI": combined_enthalpy["ci"],
                "Type": guest_types[hg],
            },
            ignore_index=True,
        )
    return combined


# BGBG-TIP3P / GAFF v1.7

bgbg_tip3p = pd.DataFrame()

for system in systems:

    # Delta G

    prefix = os.path.join("systems", system, "bgbg-tip3p")
    bgbg_tip3p_attach = np.genfromtxt(os.path.join(prefix, "ti-a.dat"))
    bgbg_tip3p_pull = np.genfromtxt(os.path.join(prefix, "ti-u.dat"))

    if system[0] == "a":
        bgbg_tip3p_release = np.genfromtxt(
            os.path.join("systems", "a-release", "bgbg-tip3p", "ti-r.dat")
        )
    else:
        bgbg_tip3p_release = np.genfromtxt(
            os.path.join("systems", "b-release", "bgbg-tip3p", "ti-r.dat")
        )
    bgbg_tip3p_analytic = 7.14

    delta_g = -1 * (
        bgbg_tip3p_attach[-1, 1]
        + bgbg_tip3p_pull[-1, 1]
        - bgbg_tip3p_release[-1, 1]
        - bgbg_tip3p_analytic
    )
    delta_g_sem = np.sqrt(
        bgbg_tip3p_attach[-1, 2] ** 2
        + bgbg_tip3p_pull[-1, 2] ** 2
        + bgbg_tip3p_release[-1, 2] ** 2
    )

    # Delta H

    with open(f"results/{system}-bgbg_tip3p-enthalpy-full.json", "r") as f:
        json_data = f.read()
    loaded = json.loads(json_data)
    delta_h = loaded["a00"]["total"][0] - loaded["r00"]["total"][0]
    delta_h_sem = np.sqrt(
        loaded["a00"]["total"][1] ** 2 + loaded["r00"]["total"][1] ** 2
    )

    bgbg_tip3p = bgbg_tip3p.append(
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

bgbg_tip3p.to_csv("results/bgbg_tip3p_by_orientation.csv")
bgbg_tip3p_combined = combine_data(bgbg_tip3p)
bgbg_tip3p_combined.to_csv("results/bgbg_tip3p_combined.csv")

# BG2BG2-TIP3P / GAFF v2.1

bg2bg2_tip3p = pd.DataFrame()

for system in systems:

    # Delta G

    prefix = os.path.join("systems", system, "bg2bg2-tip3p")
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

# SMIRNOFF99Frosst

smirnoff = pd.DataFrame()

for system in systems:

    with open(f"results/{system}-results.json", "r") as f:
        json_data = f.read()
    results = json.loads(json_data, object_hook=json_numpy_obj_hook)

    with open(f"results/{system[0]}-release.json", "r") as f:
        json_data = f.read()
    results_release = json.loads(json_data, object_hook=json_numpy_obj_hook)

    smirnoff_attach = results["attach"]["ti-block"]["fe"]
    smirnoff_pull = results["pull"]["ti-block"]["fe"]
    smirnoff_release = results_release["release"]["ti-block"]["fe"]

    smirnoff_attach_sem = results["attach"]["ti-block"]["sem"]
    smirnoff_pull_sem = results["pull"]["ti-block"]["sem"]
    smirnoff_release_sem = results_release["release"]["ti-block"]["sem"]

    smirnoff_analytic = 7.14

    delta_g = -1 * (
        smirnoff_attach + smirnoff_pull - smirnoff_release - smirnoff_analytic
    )
    delta_g_sem = np.sqrt(
        smirnoff_attach_sem ** 2 + smirnoff_pull_sem ** 2 + smirnoff_release_sem ** 2
    )

    with open(f"results/{system}-smirnoff-enthalpy-full.json", "r") as f:
        json_data = f.read()
    loaded = json.loads(json_data)
    delta_h = loaded["a000"]["total"][0] - loaded["r014"]["total"][0]
    delta_h_sem = np.sqrt(
        loaded["a000"]["total"][1] ** 2 + loaded["r014"]["total"][1] ** 2
    )

    smirnoff = smirnoff.append(
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

smirnoff.to_csv("results/smirnoff_by_orientation.csv")
smirnoff_combined = combine_data(smirnoff)
smirnoff_combined.to_csv("results/smirnoff_combined.csv")
