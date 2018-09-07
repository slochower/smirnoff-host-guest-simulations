import os

import parmed as pmd

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
