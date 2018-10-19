import numpy as np
import json
import glob
import os
from tqdm import tqdm

from systems import systems
from blocking import get_block_sem

def get_energies_for_enthalpy(mden):
    """
    Modeled after Niel's version.
    """

    vdw = []
    ele = []
    bnd = []
    ang = []
    dih = []
    v14 = []
    e14 = []

    with open(mden, "r") as f:
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
    return bnd, ang, dih, v14, e14, vdw, ele


# This was previously (incorrectly) p045.
# Guest restraints "on" but conformational restraints "off."
windows = ["r014"]

for system in tqdm(systems):
    end_point_energies = dict()
    end_point_energies[system] = dict()

    for window in windows:
        end_point_energies[system][window] = dict()
        mden_files = glob.glob(
            os.path.join(
                "../smirnoff-host-guest-simulations/systems/",
                system,
                "smirnoff",
                window,
            )
            + "/prod*.mden"
        )
        e_bond = []
        e_ang = []
        e_dih = []
        e_v14 = []
        e_e14 = []
        e_vdw = []
        e_ele = []

        for index, file in enumerate(mden_files):
            bnd, ang, dih, v14, e14, vdw, ele = get_energies_for_enthalpy(file)
            e_bond.append(bnd)
            e_ang.append(ang)
            e_dih.append(dih)
            e_v14.append(v14)
            e_e14.append(e14)
            e_vdw.append(vdw)
            e_ele.append(ele)

        e_bond = [item for sublist in e_bond for item in sublist]
        e_ang = [item for sublist in e_ang for item in sublist]
        e_dih = [item for sublist in e_dih for item in sublist]
        e_v14 = [item for sublist in e_v14 for item in sublist]
        e_e14 = [item for sublist in e_e14 for item in sublist]
        e_vdw = [item for sublist in e_vdw for item in sublist]
        e_ele = [item for sublist in e_ele for item in sublist]

        lists = [e_bond, e_ang, e_dih, e_v14, e_e14, e_vdw, e_ele]
        e_total = [sum(x) for x in zip(*lists)]

        end_point_energies[system][window]["total"] = [
            np.mean(e_total),
            get_block_sem(e_total),
        ]
        end_point_energies[system][window]["bond"] = [
            np.mean(e_bond),
            get_block_sem(e_bond),
        ]
        end_point_energies[system][window]["ang"] = [
            np.mean(e_ang),
            get_block_sem(e_ang),
        ]
        end_point_energies[system][window]["dih"] = [
            np.mean(e_dih),
            get_block_sem(e_dih),
        ]
        end_point_energies[system][window]["v14"] = [
            np.mean(e_v14),
            get_block_sem(e_v14),
        ]
        end_point_energies[system][window]["e14"] = [
            np.mean(e_e14),
            get_block_sem(e_e14),
        ]
        end_point_energies[system][window]["ele"] = [
            np.mean(e_ele),
            get_block_sem(e_ele),
        ]
        end_point_energies[system][window]["vdw"] = [
            np.mean(e_vdw),
            get_block_sem(e_vdw),
        ]

    with open(f"results/enthalpy/{system}-smirnoff-enthalpy-full.json", "a") as f:
        json.dump(end_point_energies[system], f)
