# MOL2 → SMILES

from openforcefield.topology import Molecule, Topology
from constants import systems
import json

def mol2_to_smiles(file_path):
    """Loads a receptor from a mol2 file.

    Parameters
    ----------
    file_path: str
        The file path to the mol2 file.

    Returns
    -------
    str
        The smiles descriptor of the loaded receptor molecule
    """

    receptor_molecule = Molecule.from_file(file_path, 'MOL2')
    return receptor_molecule.to_smiles()


smiles_dictionary = {}

for system in systems:
    guest = system.split("-")[1]
    file_path = f"../smirnoff-host-guest-simulations-data/systems/{system}/smirnoff/{guest}-sybyl.mol2"
    smiles = mol2_to_smiles(file_path)
    smiles_dictionary[guest] = smiles
print(json.dumps(smiles_dictionary, indent=2))