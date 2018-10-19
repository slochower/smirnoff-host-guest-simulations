import logging
from importlib import reload

reload(logging)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%Y-%m-%d %I:%M:%S %p")

import glob as glob
import os as os
import subprocess as sp
import shutil as shutil
from itertools import compress

import parmed as pmd
import paprika
from paprika.restraints import static_DAT_restraint
from paprika.restraints import DAT_restraint
from paprika.restraints import amber_restraint_line
from paprika.restraints import create_window_list
from paprika.utils import make_window_dirs

from smirnovert.convert import convert
from smirnovert.utils import create_pdb_with_conect
from smirnovert.utils import prune_conect
from smirnovert.utils import extract_water_and_ions
from smirnovert.utils import create_water_and_ions_parameters
from smirnovert.utils import load_mol2
from smirnovert.utils import split_topology
from smirnovert.utils import create_host_guest_topology

from openforcefield.typing.engines.smirnoff import ForceField, unit
from openforcefield.utils import mergeStructure

logging.info("Started logging...")
logging.info("pAPRika version: " + paprika.__version__)

systems = """./a-bam-p
./a-bam-s
./a-but-p
./a-but-s
./a-cbu-p
./a-chp-p
./a-cbu-s
./a-chp-s
./a-cpe-p
./a-coc-p
./a-coc-s
./a-cpe-s
./a-hep-p
./a-ham-s
./a-ham-p
./a-hep-s
./a-hp6-p
./a-hex-p
./a-hex-s
./a-hp6-s
./a-hx2-p
./a-hpa-s
./a-hpa-p
./a-hx2-s
./a-mba-p
./a-hx3-s
./a-hx3-p
./a-mba-s
./a-mhp-p
./a-mha-p
./a-mha-s
./a-mhp-s
./a-nmh-p
./a-nmb-p
./a-nmb-s
./a-nmh-s
./a-oct-p
./a-oam-p
./a-oam-s
./a-oct-s
./a-pnt-p
./a-pam-p
./a-pam-s
./a-pnt-s
./b-ben-s
./a-xxxx-s
./b-ben-p
./b-cbu-p
./b-cbu-s
./b-chp-s
./b-chp-p
./b-coc-s
./b-coc-p
./b-cpe-s
./b-cpe-p
./b-ham-s
./b-ham-p
./b-hep-s
./b-hep-p
./b-hex-p
./b-hex-s
./b-m4c-s
./b-m4c-p
./b-m4t-p
./b-m4t-s
./b-mch-s
./b-mha-s
./b-mha-p
./b-mch-p
./b-mo3-s
./b-mo4-p
./b-mo4-s
./b-mo3-p
./b-mp3-s
./b-mp4-s
./b-mp4-p
./b-mp3-p
./b-oam-s
./b-pb3-s
./b-pb3-p
./b-oam-p
./b-pb4-s
./b-pha-s
./b-pb4-p
./b-pha-p
./b-pnt-s
./b-pnt-p"""
systems = systems.split("\n")
systems = [i[2:] for i in systems]
systems = [i for i in systems if "xxxx" not in i]


def grep_anchor_atoms(system):
    pdb = os.path.join("systems", system, "bgbg-tip3p", system + ".pdb")
    with open(pdb, "r") as file:
        remark = file.readline()
    remark = remark.rstrip()
    remark = remark.split(" ")

    prmtop = pmd.load_file(
        os.path.join("systems", system, "smirnoff", "smirnoff.prmtop")
    )
    dummy_residues = prmtop[":DUM"].residues
    host_residue = prmtop[":MGO"].residues[0].number + 1
    guest_residue = prmtop[f":{system.split('-')[1].upper()}"].residues[0].number + 1

    anchor_atoms = {
        "D1": f":{dummy_residues[0].number + 1}",
        "D2": f":{dummy_residues[1].number + 1}",
        "D3": f":{dummy_residues[2].number + 1}",
        "H1": f":{host_residue}@{remark[2].split('@')[1]}",
        "H2": f":{host_residue + 2}@{remark[3].split('@')[1]}",
        "H3": f":{host_residue + 4}@{remark[4].split('@')[1]}",
        "G1": f":{guest_residue}@{remark[5].split('@')[1]}",
        "G2": f":{guest_residue}@{remark[6].split('@')[1]}",
    }
    return anchor_atoms


def setup_static_restraints(
    anchor_atoms, windows, structure, distance_fc=5.0, angle_fc=100.0
):
    static_restraints = []
    static_restraint_atoms = [
        [anchor_atoms["D1"], anchor_atoms["H1"]],
        [anchor_atoms["D2"], anchor_atoms["D1"], anchor_atoms["H1"]],
        [anchor_atoms["D1"], anchor_atoms["H1"], anchor_atoms["H2"]],
        [
            anchor_atoms["D3"],
            anchor_atoms["D2"],
            anchor_atoms["D1"],
            anchor_atoms["H1"],
        ],
        [
            anchor_atoms["D2"],
            anchor_atoms["D1"],
            anchor_atoms["H1"],
            anchor_atoms["H2"],
        ],
        [
            anchor_atoms["D1"],
            anchor_atoms["H1"],
            anchor_atoms["H2"],
            anchor_atoms["H3"],
        ],
    ]

    for _, atoms in enumerate(static_restraint_atoms):
        this = static_DAT_restraint(
            restraint_mask_list=atoms,
            num_window_list=windows,
            ref_structure=structure,
            force_constant=angle_fc if len(atoms) > 2 else distance_fc,
            amber_index=True,
        )

        static_restraints.append(this)
    print(f"There are {len(static_restraints)} static restraints")
    return static_restraints


def setup_guest_restraints(
    anchor_atoms,
    windows,
    structure,
    distance_fc=5.0,
    angle_fc=100.0,
    pull_initial=6.0,
    pull_final=24.0,
):
    guest_restraints = []

    guest_restraint_atoms = [
        [anchor_atoms["D1"], anchor_atoms["G1"]],
        [anchor_atoms["D2"], anchor_atoms["D1"], anchor_atoms["G1"]],
        [anchor_atoms["D1"], anchor_atoms["G1"], anchor_atoms["G2"]],
    ]
    guest_restraint_targets = {
        "initial": [pull_initial, 180.0, 180.0],
        "final": [pull_final, 180.0, 180.0],
    }

    for index, atoms in enumerate(guest_restraint_atoms):
        if len(atoms) > 2:
            angle = True
        else:
            angle = False
        this = DAT_restraint()
        this.auto_apr = True
        this.amber_index = True
        this.topology = structure
        this.mask1 = atoms[0]
        this.mask2 = atoms[1]
        if angle:
            this.mask3 = atoms[2]
            this.attach["fc_final"] = angle_fc
            this.release["fc_final"] = angle_fc
        else:
            this.attach["fc_final"] = distance_fc
            this.release["fc_final"] = angle_fc
        this.attach["target"] = guest_restraint_targets["initial"][index]
        this.attach["fraction_list"] = attach_fractions

        this.pull["target_final"] = guest_restraint_targets["final"][index]
        this.pull["num_windows"] = windows[1]

        this.release["target"] = guest_restraint_targets["final"][index]
        # Keep the guest restraints on during release.
        this.release["fraction_list"] = [1.0] * windows[2]

        this.initialize()

        guest_restraints.append(this)
    print(f"There are {len(guest_restraints)} guest restraints")
    return guest_restraints


def setup_conformation_restraints(
    template, targets, windows, attach_fractions, structure, resname, fc=6.0
):

    conformational_restraints = []
    host_residues = len(structure[":{}".format(resname.upper())].residues)
    first_host_residue = structure[":{}".format(resname.upper())].residues[0].number + 1

    for n in range(first_host_residue, host_residues + first_host_residue):
        if n + 1 < host_residues + first_host_residue:
            next_residue = n + 1
        else:
            next_residue = first_host_residue

        for (index, atoms), target in zip(enumerate(template), targets):

            conformational_restraint_atoms = []
            if index == 0:
                conformational_restraint_atoms.append(f":{n}@{atoms[0]}")
                conformational_restraint_atoms.append(f":{n}@{atoms[1]}")
                conformational_restraint_atoms.append(f":{n}@{atoms[2]}")
                conformational_restraint_atoms.append(f":{next_residue}@{atoms[3]}")
            else:
                conformational_restraint_atoms.append(f":{n}@{atoms[0]}")
                conformational_restraint_atoms.append(f":{n}@{atoms[1]}")
                conformational_restraint_atoms.append(f":{next_residue}@{atoms[2]}")
                conformational_restraint_atoms.append(f":{next_residue}@{atoms[3]}")

            this = DAT_restraint()
            this.auto_apr = True
            this.amber_index = True
            this.topology = structure
            this.mask1 = conformational_restraint_atoms[0]
            this.mask2 = conformational_restraint_atoms[1]
            this.mask3 = conformational_restraint_atoms[2]
            this.mask4 = conformational_restraint_atoms[3]

            this.attach["fraction_list"] = attach_fractions
            this.attach["target"] = target
            this.attach["fc_final"] = fc
            this.pull["target_final"] = target
            this.pull["num_windows"] = windows[1]

            this.release["fraction_list"] = attach_fractions[::-1]
            this.release["target"] = target
            this.release["fc_final"] = fc

            this.initialize()
            conformational_restraints.append(this)
    print(f"There are {len(conformational_restraints)} conformational restraints")
    return conformational_restraints


def setup_guest_wall_restraints(
    template, targets, structure, resname, angle_fc=500.0, distance_fc=50.0
):

    guest_wall_restraints = []
    host_residues = len(structure[":{}".format(resname.upper())].residues)
    first_host_residue = structure[":{}".format(resname.upper())].residues[0].number + 1

    for n in range(first_host_residue, host_residues + first_host_residue):
        for (index, atoms), target in zip(enumerate(template[0:2]), targets[0:2]):
            guest_wall_restraint_atoms = []
            guest_wall_restraint_atoms.append(f":{n}@{atoms[0]}")
            guest_wall_restraint_atoms.append(f"{atoms[1]}")

            this = DAT_restraint()
            this.auto_apr = True
            this.amber_index = True
            this.topology = structure
            this.mask1 = guest_wall_restraint_atoms[0]
            this.mask2 = guest_wall_restraint_atoms[1]
            this.attach["fc_initial"] = distance_fc
            this.attach["fc_final"] = distance_fc
            this.custom_restraint_values["rk2"] = 50.0
            this.custom_restraint_values["rk3"] = 50.0
            this.custom_restraint_values["r1"] = 0.0
            this.custom_restraint_values["r2"] = 0.0

            this.attach["target"] = target
            this.attach["num_windows"] = windows[1]

            this.initialize()
            guest_wall_restraints.append(this)
            print("Added guest wall distance restraint.")

    # Add a single angle restraint!
    guest_wall_restraint_atoms = []
    guest_wall_restraint_atoms.append(f"{template[2][0]}")
    guest_wall_restraint_atoms.append(f"{template[2][1]}")
    guest_wall_restraint_atoms.append(f"{template[2][2]}")
    target = targets[2]

    this = DAT_restraint()
    this.auto_apr = True
    this.amber_index = True
    this.topology = structure
    this.mask1 = guest_wall_restraint_atoms[0]
    this.mask2 = guest_wall_restraint_atoms[1]

    this.mask3 = guest_wall_restraint_atoms[2]
    this.attach["fc_initial"] = angle_fc
    this.attach["fc_final"] = angle_fc
    this.custom_restraint_values["rk2"] = 500.0
    this.custom_restraint_values["rk3"] = 0.0

    this.attach["target"] = target
    this.attach["num_windows"] = windows[1]

    this.initialize()
    guest_wall_restraints.append(this)
    print("Added guest wall angle restraint.")

    print(f"There are {len(guest_wall_restraints)} guest wall restraints")
    return guest_wall_restraints


attach_string = (
    "0.00 0.40 0.80 1.60 2.40 4.00 5.50 8.65 11.80 18.10 24.40 37.00 49.60 74.80 100.00"
)
attach_fractions = [float(i) / 100 for i in attach_string.split()]

pull_string = (
    "0.00 0.40 0.80 1.20 1.60 2.00 2.40 2.80 3.20 3.60 4.00 4.40 4.80 5.20 5.60 6.00 6.40 6.80 7.20 7.60 8.00 8.40 8.80 9.20 9.60 10.00 10.40 10.80 11.20 11.60 12.00 12.40 12.80 13.20 13.60 14.00 14.40 14.80 15.20 15.60 16.00 16.40 16.80 17.20 17.60 18.00"
)
pull_distances = [float(i) + 6.00 for i in pull_string.split()]

release_fractions = attach_fractions[::-1]

windows = [len(attach_fractions), len(pull_distances), len(release_fractions)]
print(f"There are {windows} windows in this attach-pull-release calculation.")

for system in systems:
    anchor_atoms = grep_anchor_atoms(system)
    structure = pmd.load_file(
        os.path.join("systems", system, "smirnoff", "smirnoff.prmtop"),
        os.path.join("systems", system, "smirnoff", "smirnoff.inpcrd"),
        structure=True,
    )
    static_restraints = setup_static_restraints(
        anchor_atoms, windows, structure, distance_fc=5.0, angle_fc=100.0
    )

    guest_restraints = setup_guest_restraints(
        anchor_atoms,
        windows,
        structure,
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
    if system[0] == "a":
        guest_wall_targets = [11.3, 13.3, 80.0]
    else:
        guest_wall_targets = [12.5, 14.5, 80.0]
    guest_wall_restraints = setup_guest_wall_restraints(
        guest_wall_template,
        guest_wall_targets,
        structure,
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

    window_list = create_window_list(guest_restraints)

    print("Writing restratint file in each window...")
    for window in window_list:
        with open(
            os.path.join("systems", system, "smirnoff", window, "disang.rest"), "w"
        ) as file:
            if window[0] == "a":
                phase = "attach"
                restraints = (
                    static_restraints
                    + guest_restraints
                    + conformational_restraints
                    + guest_wall_restraints
                )
            if window[0] == "p":
                phase = "pull"
                restraints = (
                    static_restraints + conformational_restraints + guest_restraints
                )
            if window[0] == "r":
                phase = "release"
                restraints = (
                    static_restraints + conformational_restraints + guest_restraints
                )

            for restraint in restraints:
                string = amber_restraint_line(restraint, phase, int(window[1:]))
                if string is not None:
                    file.write(string)
