import glob
import os
import sys
import subprocess as sp
import shutil
import json
import argparse
import logging

from importlib import reload

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--name", required=True, help="System")
args = vars(ap.parse_args())
system = args["name"]

logging.basicConfig(
    filename=system + "-analyze.log",
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S %p",
    level=logging.DEBUG,
)
logging.info("Started logging...")


import parmed as pmd
import pytraj as pt

from setup.anchor_atoms import grep_anchor_atoms
from setup.restraints import (
    setup_static_restraints,
    setup_conformation_restraints,
    setup_guest_restraints,
    setup_guest_wall_restraints,
)
from paprika.analysis import fe_calc
from paprika.restraints import create_window_list


import base64
import json
import numpy as np


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        """If input object is an ndarray it will be converted into a dict 
        holding dtype, shape and the data, base64 encoded.
        """
        if isinstance(obj, np.ndarray):
            if obj.flags["C_CONTIGUOUS"]:
                obj_data = obj.data
            else:
                cont_obj = np.ascontiguousarray(obj)
                assert cont_obj.flags["C_CONTIGUOUS"]
                obj_data = cont_obj.data
            data_b64 = base64.b64encode(obj_data)
            # obj_data = obj.tolist()
            return dict(
                __ndarray__=data_b64.decode("utf-8"),
                dtype=str(obj.dtype),
                shape=obj.shape,
            )
            # return dict(__ndarray__=obj_data,
            #             dtype=str(obj.dtype),
            #             shape=obj.shape)
        elif isinstance(
            obj,
            (
                np.int_,
                np.intc,
                np.intp,
                np.int8,
                np.int16,
                np.int32,
                np.int64,
                np.uint8,
                np.uint16,
                np.uint32,
                np.uint64,
            ),
        ):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()

        # Let the base class default method raise the TypeError
        # return json.JSONEncoder(self, obj)
        return super(NumpyEncoder, self).default(obj)


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


if os.path.exists(f"results/enthalpy/{system}-results.json"):
    print(f"Skipping {system}")
    sys.exit()
else:
    print(f"Running {system}")


attach_string = (
    "0.00 0.40 0.80 1.60 2.40 4.00 5.50 8.65 11.80 18.10 24.40 37.00 49.60 74.80 100.00"
)
attach_fractions = [float(i) / 100 for i in attach_string.split()]

pull_string = (
    "0.00 0.40 0.80 1.20 1.60 2.00 2.40 2.80 3.20 3.60 4.00 4.40 4.80 5.20 5.60 6.00 6.40 6.80 7.20 7.60 8.00 8.40 8.80 9.20 9.60 10.00 10.40 10.80 11.20 11.60 12.00 12.40 12.80 13.20 13.60 14.00 14.40 14.80 15.20 15.60 16.00 16.40 16.80 17.20 17.60 18.00"
)
pull_distances = [float(i) + 6.00 for i in pull_string.split()]

release_fractions = attach_fractions[::-1]

windows = [len(attach_fractions), len(pull_distances), 0]


structure = pmd.load_file(
    os.path.join("systems", system, "smirnoff", "smirnoff.prmtop"),
    os.path.join("systems", system, "smirnoff", "smirnoff.inpcrd"),
    structure=True,
)

anchor_atoms = grep_anchor_atoms(system)
static_restraints = setup_static_restraints(
    anchor_atoms, windows, structure, distance_fc=5.0, angle_fc=100.0
)

guest_restraints = setup_guest_restraints(
    anchor_atoms,
    windows,
    structure,
    attach_fractions,
    distance_fc=5.0,
    angle_fc=100.0,
    pull_initial=6.0,
    pull_final=24.0,
)

host_conformational_template = [["O5", "C1", "O1", "C4"], ["C1", "O1", "C4", "C5"]]
host_conformational_targets = [104.30, -108.8]

conformational_restraints = setup_conformation_restraints(
    host_conformational_template,
    host_conformational_targets,
    windows,
    attach_fractions,
    structure,
    resname="MGO",
    fc=6.0,
)

guest_wall_template = [
    ["O2", anchor_atoms["G1"]],
    ["O6", anchor_atoms["G1"]],
    [anchor_atoms["D2"], anchor_atoms["G1"], anchor_atoms["G2"]],
]
guest_wall_targets = [11.3, 13.3, 80.0]

guest_wall_restraints = setup_guest_wall_restraints(
    guest_wall_template,
    guest_wall_targets,
    structure,
    windows,
    resname="MGO",
    angle_fc=500.0,
    distance_fc=50.0,
)

restraints = (
    static_restraints
    + conformational_restraints
    + guest_restraints
    + guest_wall_restraints
)

for restraint in restraints:
    restraint.phase["release"]["force_constants"] = None
    restraint.phase["release"]["targets"] = None

if not os.path.exists(
    os.path.join("systems", system, "smirnoff", "a000", "vac.prmtop")
):
    structure = pt.load(
        os.path.join("systems", system, "smirnoff", "a000", "smirnoff.inpcrd"),
        os.path.join("systems", system, "smirnoff", "a000", "smirnoff.prmtop"),
    )
    stripped = structure.strip(":WAT,:Na+,:Cl-")
    stripped.save(os.path.join("systems", system, "smirnoff", "a000", "vac.prmtop"))

if not os.path.exists(
    os.path.join("systems", system, "smirnoff", "a000", "vac.inpcrd")
):
    structure = pt.load(
        os.path.join("systems", system, "smirnoff", "a000", "smirnoff.inpcrd"),
        os.path.join("systems", system, "smirnoff", "a000", "smirnoff.prmtop"),
    )
    stripped = structure.strip(":WAT,:Na+,:Cl-")
    stripped.save(os.path.join("systems", system, "smirnoff", "a000", "vac.inpcrd"))




structure = pt.load(
    os.path.join("systems", system, 'smirnoff', 'a000', 'vac.inpcrd'),
    os.path.join("systems", system, 'smirnoff', 'a000', 'vac.prmtop'))
analyze = fe_calc()
analyze.prmtop = structure.topology
analyze.trajectory = "vac.*.nc"
analyze.path = os.path.join("systems", system, "smirnoff")

analyze.restraint_list = guest_restraints + conformational_restraints
analyze.collect_data()
analyze.methods = ["ti-block"]
analyze.quicker_ti_matrix = True
analyze.bootcycles = 1000
analyze.compute_free_energy(phases=["attach", "pull"])
analyze.compute_ref_state_work(
    [guest_restraints[0], guest_restraints[1], None, None, guest_restraints[2], None]
)

with open(f"results/enthalpy/{system}-results.json", "w") as f:
    dumped = json.dumps(analyze.results, cls=NumpyEncoder)
    f.write(dumped)
