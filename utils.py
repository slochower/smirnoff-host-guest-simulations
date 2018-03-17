import numpy as np
import parmed as pmd
from openforcefield.typing.engines.smirnoff import ForceField, unit
from openforcefield.utils import mergeStructure
from smirnovert.utils import (
    create_pdb_with_conect, prune_conect, split_topology,
    create_host_guest_topology, create_host_mol2,
    convert_mol2_to_sybyl_antechamber, load_mol2, check_unique_atom_names,
    check_bond_lengths, extract_water_and_ions,
    create_water_and_ions_parameters)

CHARS = "0 1 2 3 4 5 6 7 8 9 a b c d e f g h i j k l m n o p q r\
            s t u v w x y z A B C D E F G H I J K L M N O P Q R S T\
            U V W X Y Z * & $ # % [ ] { } < > ? + = : ; ' . , ! ~ `\
            @ ^ ( ) _ | / \\ \"".split()


def create_element_type_lists(first_chars, second_chars):
    """ Create all possible two character atom types """
    return [first_char + second_char for first_char in first_chars for second_char in second_chars]


def create_mapping(structure, host_resname, guest_resname):
    hydrogen_list = create_element_type_lists(['H', 'h', '1'], CHARS)
    carbon_list = create_element_type_lists(['C', 'c', '6'], CHARS)
    oxygen_list = create_element_type_lists(['O', 'o', '8'], CHARS)
    nitrogen_list = create_element_type_lists(['N', 'n', '7'], CHARS)

    host_mapping = dict()
    guest_mapping = dict()
    hydrogen_index = 0
    carbon_index = 0
    nitrogen_index = 0
    oxygen_index = 0

    for residue in structure.residues:
        if residue.name == host_resname and not host_mapping:
            for atom_index, atom in enumerate(residue):
                # Assumption: each host has atoms numbered in the same order!
                # This is going to greatly simplify assigning unique atom types *only* within a residue.
                # To be completely thorough, we could add a check here that the parameters associated with each
                # atom type in each residue are identical.
                if atom.element == 1:
                    host_mapping[atom_index] = hydrogen_list[hydrogen_index]
                    hydrogen_index += 1
                elif atom.element == 6:
                    host_mapping[atom_index] = carbon_list[carbon_index]
                    carbon_index += 1
                elif atom.element == 7:
                    host_mapping[atom_index] = nitrogen_list[nitrogen_index]
                    nitrogen_index += 1
                elif atom.element == 8:
                    host_mapping[atom_index] = oxygen_list[oxygen_index]
                    oxygen_index += 1
                else:
                    print(f'Whoops, missing atom type lists for element {atom.element}.')
        elif residue.name == guest_resname and not guest_mapping:
            for atom_index, atom in enumerate(residue):
                if atom.element == 1:
                    guest_mapping[atom_index] = hydrogen_list[hydrogen_index]
                    hydrogen_index += 1
                elif atom.element == 6:
                    guest_mapping[atom_index] = carbon_list[carbon_index]
                    carbon_index += 1
                elif atom.element == 7:
                    guest_mapping[atom_index] = nitrogen_list[nitrogen_index]
                    nitrogen_index += 1
                elif atom.element == 8:
                    guest_mapping[atom_index] = oxygen_list[oxygen_index]
                    oxygen_index += 1
                else:
                    print(f'Whoops, missing atom type lists for this element {atom.element}')
    return host_mapping, guest_mapping


def remap_atom_types(AmberParm, host_resname, host_mapping, guest_resname, guest_mapping, destination):
    for residue in AmberParm.residues:
        if residue.name == host_resname:
            for index, atom in enumerate(residue):
                print(f'Assigning {residue.number} {atom.name} {atom.type} → {host_mapping[index]}')
                AmberParm.parm_data['AMBER_ATOM_TYPE'][int(atom.type) - 1] = host_mapping[index]
                atom.type = host_mapping[index]
        if residue.name == guest_resname:
            for index, atom in enumerate(residue):
                print(f'Assigning {residue.number} {atom.name} {atom.type} → {guest_mapping[index]}')

                # This is not working correctly!
                AmberParm.parm_data['AMBER_ATOM_TYPE'][int(atom.type) - 1] = guest_mapping[index]
                atom.type = guest_mapping[index]

    AmberParm.load_atom_info()
    AmberParm.fill_LJ()
    AmberParm.save(destination + 'smirnoff-unique.mol2', overwrite=True)
    AmberParm.save(destination + 'smirnoff-unique.prmtop', overwrite=True)

    parameter_set = pmd.amber.AmberParameterSet.from_structure(AmberParm)
    parameter_set.write(destination + 'smirnoff-unique.frcmod')

    # Read back in the `prmtop`...
    structure = pmd.load_file(destination + 'smirnoff-unique.prmtop', structure=True)

    # Write out a `mol2` file for the guest -- expecting all atom types to begin with `G`...
    single_guest = structure[':' + guest_resname]
    single_guest.save(destination + 'smirnoff-' + guest_resname + '-unique.mol2', overwrite=True)

    single_host = structure[
        ':' + str(structure[':' + host_resname].residues[0].number + 1)]
    single_host.save(destination + 'smirnoff-' + host_resname + '-unique.mol2', overwrite=True)


def unique_two_char_atom_types(reference_prmtop, reference_inpcrd,
                               host_resname, guest_resname, prefix):
    structure = pmd.load_file(
        reference_prmtop, reference_inpcrd, structure=True)
    print(f'{len(structure.bonds)} bonds in structure.')
    # Is O4 bonded to C1?
    for bond in structure.bonds:
        atom1, atom2 = bond.atom1, bond.atom2
        if atom1.residue != atom2.residue:
            print(f'({atom1.type}) {atom1.residue.number + 1}.{atom1.name} '
                  f'({atom2.type}) {atom2.residue.number + 1}.{atom2.name}')

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
            print(
                f'Mapping {atom.name} {atom.type} → {mapping[atom.type]} in {host_resname}'
            )
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
                  f'({atom2.type}) {atom2.residue.number + 1}.{atom2.name}')

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

    multi_host = structure[':' + host_resname]
    multi_host.save(prefix + '-' + host_resname + '-multi-unique.mol2')

    return mapping


def convert(destination, prefix, reference_prmtop, reference_inpcrd,
            host_resname, guest_resname):
    reference = pmd.load_file(
        destination + reference_prmtop, xyz=destination + reference_inpcrd)
    box = reference.box

    create_pdb_with_conect(
        solvated_pdb=destination + reference_inpcrd,
        amber_prmtop=destination + reference_prmtop,
        output_pdb=destination + prefix + '.pdb')

    prune_conect(
        input_pdb=prefix + '.pdb',
        output_pdb=prefix + '.pruned.pdb',
        path=destination)

    components = split_topology(file_name=destination + prefix + '.pruned.pdb')
    hg_topology = create_host_guest_topology(
        components, host_resname=host_resname, guest_resname=guest_resname)

    create_host_mol2(
        solvated_pdb=destination + prefix + '.pruned.pdb',
        amber_prmtop=destination + reference_prmtop,
        mask=host_resname,
        output_mol2=destination + host_resname + '.mol2')

    create_host_mol2(
        solvated_pdb=destination + prefix + '.pdb',
        amber_prmtop=destination + reference_prmtop,
        mask=guest_resname,
        output_mol2=destination + guest_resname + '.mol2')

    convert_mol2_to_sybyl_antechamber(
        input_mol2=destination + host_resname + '.mol2',
        output_mol2=destination + host_resname + '-sybyl.mol2',
        ac_doctor=False)

    convert_mol2_to_sybyl_antechamber(
        input_mol2=destination + guest_resname + '.mol2',
        output_mol2=destination + guest_resname + '-sybyl.mol2',
        ac_doctor=False)

    extract_water_and_ions(
        amber_prmtop=reference_prmtop,
        amber_inpcrd=reference_inpcrd,
        host_residue=':' + host_resname,
        guest_residue=':' + guest_resname,
        dummy_atoms=True,
        output_pdb='water_ions.pdb',
        path=destination)

    create_water_and_ions_parameters(
        input_pdb='water_ions.pdb',
        output_prmtop='water_ions.prmtop',
        output_inpcrd='water_ions.inpcrd',
        dummy_atoms=False,
        path=destination)

    host = load_mol2(
        filename=destination + host_resname + '-sybyl.mol2',
        name=host_resname,
        add_tripos=True)

    guest = load_mol2(
        filename=destination + guest_resname + '-sybyl.mol2',
        name=guest_resname,
        add_tripos=False)

    check_unique_atom_names(host)
    check_unique_atom_names(guest)
    molecules = [host, guest]

    ff = ForceField('forcefield/smirnoff99Frosst.ffxml')
    system = ff.createSystem(
        hg_topology.topology,
        molecules,
        nonbondedCutoff=1.1 * unit.nanometer,
        ewaldErrorTolerance=1e-4)

    hg_structure = pmd.openmm.topsystem.load_topology(
        hg_topology.topology, system, hg_topology.positions)

    check_bond_lengths(hg_structure, threshold=4)

    try:
        hg_structure.save(destination + 'hg.prmtop')
    except OSError:
        print('Check if the host-guest parameter file already exists...')

    try:
        hg_structure.save(destination + 'hg.inpcrd')
    except OSError:
        print('Check if the host-guest coordinate file already exists...')

    water_and_ions = pmd.amber.AmberParm(
        destination + 'water_ions.prmtop',
        xyz=destination + 'water_ions.inpcrd')

    merged = mergeStructure(hg_structure, water_and_ions)
    merged.box = reference.box
    try:
        merged.save(destination + 'smirnoff.prmtop')
    except:
        print('Check if solvated parameter file already exists...')
    try:
        merged.save(destination + 'smirnoff.inpcrd')
    except:
        print('Check if solvated coordinate file already exists...')

    # Run either with rewrite

    # Run with/without debug, to clean up trash files...

    return merged
