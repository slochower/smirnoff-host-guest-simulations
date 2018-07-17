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


host = load_mol2(filename="MGO-sybyl.mol2", name="MGO", add_tripos=True)

guest = load_mol2(filename="mo3-sybyl.mol2", name="MO3", add_tripos=False)

molecules = [host, guest]

topology = pmd.load_file("../p000/smirnoff.pruned.pdb")
components = topology.split()

hg_topology = pmd.Structure()
for component in components:
    if component[0].residues[0].name == "MGO" or component[0].residues[0].name == "MO3":
        hg_topology += component[0]

print(hg_topology)


topology = pmd.load_file("smirnoff.pruned.pdb")
components = topology.split()

hg_topology = pmd.Structure()
for component in components:
    if component[0].residues[0].name == "MGO" or component[0].residues[0].name == "MO3":
        hg_topology += component[0]

print(hg_topology)

for bond in hg_topology.bonds:
    if bond.atom1.residue.name == "MGO" and bond.atom2.residue.name == "MO3":
        bond.delete()
        print("Bad bond!")
    elif bond.atom1.residue.name == "MO3" and bond.atom2.residue.name == "MGO":
        bond.delete()
        print("Bad bond!")

print(hg_topology)

# ff = ForceField("forcefield/smirnoff99Frosst.offxml")
# openmm = ff.createSystem(
#     hg_topology.topology,
#     molecules,
#     nonbondedCutoff=1.1 * unit.nanometer,
#     ewaldErrorTolerance=1e-4,
# )
