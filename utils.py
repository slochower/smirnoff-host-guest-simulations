import parmed as pmd
import numpy as np


def unique_two_char_atom_types(reference_prmtop, reference_inpcrd, host_resname, guest_resname, prefix):
 
    structure = pmd.load_file(reference_prmtop, reference_inpcrd, structure=True)
    print(f'{len(structure.bonds)} bonds in structure.')
    # Is O4 bonded to C1?
    for bond in structure.bonds:
        atom1, atom2 = bond.atom1, bond.atom2
        if atom1.residue != atom2.residue:
            print(f'({atom1.type}) {atom1.residue.number + 1}.{atom1.name} '
                  f'({atom2.type}) {atom2.residue.number + 1}.{atom2.name}'
                )
        
    char_list = "0 1 2 3 4 5 6 7 8 9 a b c d e f g h i j k l m n o p q r\
                s t u v w x y z A B C D E F G H I J K L M N O P Q R S T\
                U V W X Y Z * & $ # % [ ] { } < > ? + = : ; ' . , ! ~ `\
                @ ^ ( ) _ | / \\ \"".split()

    guest_list = ['G' + char for char in char_list]
    # Apparently 'H' is bad because it is like hydrogen. Let's do 'Z'...
    host_list = ['Z' + char
                 for char in char_list] + ['z' + char for char in char_list]

    mapping = dict()
    guest_index = 0
    host_index = 0
    for index, atom in enumerate(structure.atoms):
        if atom.residue.name == host_resname:
            mapping[atom.type] = host_list[host_index]
            host_index += 1
            print(f'Mapping {atom.name} {atom.type} → {mapping[atom.type]} in {host_resname}')
        elif atom.residue.name == guest_resname:
            mapping[atom.type] = guest_list[guest_index]
            guest_index += 1
            # print(f'Mapping {atom.type} → {mapping[atom.type]} in {guest_resname}')
        else:
            mapping[atom.type] = atom.type

    # Use the mapping to write out a new `prmtop`
    for index, atom in enumerate(structure.atoms):
        if atom.type != mapping[atom.type]:
            # print(f'Assigning {atom.type} → {mapping[atom.type]}')
            structure.parm_data['AMBER_ATOM_TYPE'][index] = mapping[atom.type]
            atom.type = mapping[atom.type]

    structure.load_atom_info()
    structure.fill_LJ()
    
    # Is O4 bonded to C1?
    for bond in structure.bonds:
        atom1, atom2 = bond.atom1, bond.atom2
        if atom1.residue != atom2.residue:
            print(f'({atom1.type}) {atom1.residue.number + 1}.{atom1.name} '
                  f'({atom2.type}) {atom2.residue.number + 1}.{atom2.name}'
                )
        
    structure.save(prefix + '-unique.prmtop')

    new_parameters = pmd.amber.AmberParameterSet.from_structure(structure)
    
    
    # Is O4 bonded to C1?
#     for bond in new_parameters.bonds:
#         atom1, atom2 = bond.atom1, bond.atom2
#         if atom1.residue != atom2.residue:
#             print(f'bond model.{atom1.residue.number + 1}.{atom1.name} '
#                   f'model.{atom2.residue.number + 1}.{atom2.name}'
#                 )
    for bond in new_parameters.bond_types:
        if 'Z2' in bond[0:2] and 'Zb' in bond[0:2]:
            print(bond)

    
    new_parameters.write(prefix + '-unique.frcmod')

    # Read back in the `prmtop`...
    structure = pmd.load_file(prefix + '-unique.prmtop', structure=True)

    # Write out a `mol2` file for the guest -- expecting all atom types to begin with `G`...
    single_guest = structure[':' + guest_resname]
    single_guest.save(prefix + '-' + guest_resname + '-unique.mol2')

    single_host = structure[
        ':' + str(structure[':' + host_resname].residues[0].number + 1)]
    single_host.save(prefix + '-' + host_resname + '-unique.mol2')
    
    return mapping