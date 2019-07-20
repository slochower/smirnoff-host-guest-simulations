import pandas as pd
import numpy as np
import json
import os
import base64

from constants import experimental_deltaG
from constants import experimental_deltaH
from constants import systems
from constants import guest_types

from bootstrap import dG_bootstrap
from bootstrap import dH_bootstrap

def json_numpy_obj_hook(dct):
    """Decodes a previously encoded numpy ndarray with proper shape and dtype.
    :param dct: (dict) json encoded ndarray
    :return: (ndarray) if input was an encoded ndarray
    """
    if isinstance(dct, dict) and "__ndarray__" in dct:
        data = base64.b64decode(dct["__ndarray__"])
        return np.frombuffer(data, dct["dtype"]).reshape(dct["shape"])
        # return dct['__ndarray__']
    return dct
    

experimental_deltaG_list = experimental_deltaG.split("\n")
experimental_deltaH_list = experimental_deltaH.split("\n")

experimental = pd.DataFrame(
    [
        i.split("\t") + j.split("\t")[1:]
        for i, j in zip(experimental_deltaG_list, experimental_deltaH_list)
    ],
    columns=["System", "Delta G", "G_SEM", "Delta H", "H_SEM"],
)



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


# SMIRNOFF99Frosst

smirnoff = pd.DataFrame()

for system in systems:
    print(system)
    with open(f"results/{system}-mbar-results.json", "r") as f:
        json_data = f.read()
    results = json.loads(json_data, object_hook=json_numpy_obj_hook)

    with open(f"results/{system[0]}-release.json", "r") as f:
        json_data = f.read()
    results_release = json.loads(json_data, object_hook=json_numpy_obj_hook)

    smirnoff_attach = results["attach"]["mbar-block"]["fe"]
    smirnoff_pull = results["pull"]["mbar-block"]["fe"]
    smirnoff_release = results_release["release"]["ti-block"]["fe"]

    smirnoff_attach_sem = results["attach"]["mbar-block"]["sem"]
    smirnoff_pull_sem = results["pull"]["mbar-block"]["sem"]
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

smirnoff.to_csv("results/smirnoff_mbar_by_orientation.csv")
smirnoff_combined = combine_data(smirnoff)
smirnoff_combined.to_csv("results/smirnoff_mbar_combined.csv")
