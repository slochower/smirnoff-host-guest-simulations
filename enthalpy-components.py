import glob
import os
import numpy as np
import sys
import json
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--name", required=True, help="System")
ap.add_argument("-ff", "--forcefield", required=True, help="Force field")

args = vars(ap.parse_args())
system = args["name"]
ff = args["forcefield"]


# https://stackoverflow.com/questions/6800193/what-is-the-most-efficient-way-of-finding-all-the-factors-of-a-number-in-python
# THis is good.
from functools import reduce


def fctors(n):
    return sorted(
        list(
            set(
                reduce(
                    list.__add__,
                    ([i, n // i] for i in range(1, int(n ** 0.5) + 1) if n % i == 0),
                )
            )
        )
    )


def get_nearest_max(n):
    """
    Return the number with the largest number of factors between n-100 and n.
    """
    num_factors = []
    max_factors = 0
    if n % 2 == 0:
        beg = n - 100
        end = n
    else:
        beg = n - 101
        end = n - 1
    if beg < 0:
        beg = 0
    for i in range(beg, end + 2, 2):
        num_factors = len(fctors(i))
        if num_factors >= max_factors:
            max_factors = num_factors
            most_factors = i
    return most_factors


def get_block_sem(data_array):
    """
    Compute the standard error of the mean (SEM) for a data_array using the blocking method."
    """
    # Get the integer factors for the number of data points. These
    # are equivalent to the block sizes we will check.
    block_sizes = fctors(len(data_array))

    # An array to store means for each block ... make it bigger than we need.
    block_means = np.zeros([block_sizes[-1]], np.float64)

    # Store the SEM for each block size, except the last two size for which
    # there will only be two or one blocks total and thus very noisy.
    sems = np.zeros([len(block_sizes) - 2], np.float64)
    sems_error = np.zeros([len(block_sizes) - 2], np.float64)

    # Check each block size except the last two.
    for size_idx in range(len(block_sizes) - 2):
        # Check each block, the number of which is conveniently found as
        # the other number of the factor pair in block_sizes
        num_blocks = block_sizes[-size_idx - 1]
        for blk_idx in range(num_blocks):
            # Find the index for beg and end of data points for each block
            data_beg_idx = blk_idx * block_sizes[size_idx]
            data_end_idx = (blk_idx + 1) * block_sizes[size_idx]
            # Compute the mean of this block and store in array
            block_means[blk_idx] = np.mean(data_array[data_beg_idx:data_end_idx])
        # Compute the standard deviation across all blocks, devide by num_blocks-1 for SEM
        sems[size_idx] = np.std(block_means[0:num_blocks], ddof=0) / np.sqrt(
            num_blocks - 1
        )
        # Hmm or should ddof=1? I think 0, see Flyvbjerg -----^
        sems_error[size_idx] = sems[size_idx] / np.sqrt(2 * (num_blocks - 1))

    # Return the max SEM found ... this is a conservative approach.

    return np.max(sems)


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


if os.path.exists(f"{system}-{ff}-enthalpy-full.json"):
    print(f"Skipping {system}-{ff}-enthalpy-full.json")
    sys.exit(1)

if ff == "smirnoff":
    windows = ["a000", "p045"]
elif ff == "bgbg_tip3p":
    windows = ["a00", "r00"]

end_point_energies = {}
end_point_energies[system] = {}
for window in windows:
    end_point_energies[system][window] = {}
    if ff == "smirnoff":
        mden_files = glob.glob(
            os.path.join("systems", system, "smirnoff", window) + "/prod*.mden"
        )
    elif ff == "bgbg_tip3p":
        mden_files = glob.glob(
            os.path.join("/data/nhenriksen/projects/cds/wat6/bgbg-tip3p/", system, window) + "/mden*"
        )
        mden_files = [i for i in mden_files if "pl" not in i]
    else:
        sys.exit(1)

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

    end_point_energies[system][window]["total"] = [np.mean(e_total), get_block_sem(e_total)]
    end_point_energies[system][window]["bond"] = [np.mean(e_bond), get_block_sem(e_bond)]
    end_point_energies[system][window]["ang"]  = [np.mean(e_ang), get_block_sem(e_ang)]
    end_point_energies[system][window]["dih"] = [np.mean(e_dih), get_block_sem(e_dih)]
    end_point_energies[system][window]["v14"] = [np.mean(e_v14), get_block_sem(e_v14)]
    end_point_energies[system][window]["e14"] = [np.mean(e_e14), get_block_sem(e_e14)]
    end_point_energies[system][window]["ele"] = [np.mean(e_ele), get_block_sem(e_ele)]
    end_point_energies[system][window]["vdw"] = [np.mean(e_vdw), get_block_sem(e_vdw)]
with open(f"{system}-{ff}-enthalpy-full.json", "w") as f:
    json.dump(end_point_energies[system], f)
