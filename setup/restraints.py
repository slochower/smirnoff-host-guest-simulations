import glob as glob
import os as os
import subprocess as sp
import shutil as shutil
from itertools import compress

import parmed as pmd
import pytraj as pt

from paprika.restraints import static_DAT_restraint
from paprika.restraints import DAT_restraint
from paprika.restraints import amber_restraint_line
from paprika.restraints import create_window_list
from paprika.utils import make_window_dirs


def setup_static_restraints(
    anchor_atoms, windows, structure, distance_fc=5.0, angle_fc=100.0,
        release=True
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

    for index, atoms in enumerate(static_restraint_atoms):
        this = static_DAT_restraint(
            restraint_mask_list=atoms,
            num_window_list=windows,
            ref_structure=structure,
            force_constant=angle_fc if len(atoms) > 2 else distance_fc,
            amber_index=True,
        )

        static_restraints.append(this)
    return static_restraints


def setup_guest_restraints(
    anchor_atoms,
    windows,
    structure,
    attach_fractions,
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
    return conformational_restraints


def setup_guest_wall_restraints(
    template, targets, structure, windows, resname, angle_fc=500.0, distance_fc=50.0
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
            this.attach["num_windows"] = windows[0]

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
    this.attach["num_windows"] = windows[0]

    this.initialize()
    guest_wall_restraints.append(this)
    print("Added guest wall angle restraint.")

    print(f"There are {len(guest_wall_restraints)} guest wall restraints")
    return guest_wall_restraints
