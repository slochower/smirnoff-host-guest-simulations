def read_energies(ff, system, state):
    file_mask = get_files(ff, system, state)
    print(file_mask)
    files = glob.glob(file_mask)
    files = [i for i in files if i[-2:] != "pl"]
    energies = []

    vdw, ele, bnd, ang, dih, v14, e14 = [], [], [], [], [], [], []

    for file in files:
        with open(file, "r") as f:
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

    print(len(bnd), len(ang), len(dih), len(v14), len(e14), len(vdw), len(ele))
    energies = {"Bond"    : bnd,
                "Angle"   : ang,
                "Dihedral": dih,
                "V14"     : v14,
                "E14"     : e14,
                "VDW"     : vdw,
                "Ele"     : ele,
                "Total"   : [sum(x) for x in zip(bnd, ang, dih, v14, e14, vdw, ele)]}

    return pd.DataFrame(energies)


def get_files(ff, system, state):
    base = {"SMIRNOFF99Frosst": f"../smirnoff-host-guest-simulations/systems/",
            "BGBG-TIP3P"      : f"/home/dslochower/niel/projects/cds/wat6/bgbg-tip3p/"
            }

    systems = {"SMIRNOFF99Frosst": "smirnoff/",
               "BGBG-TIP3P"      : f""
               }

    states = {"SMIRNOFF99Frosst": {"attach" : "a000",
                                   "release": "p045"},
              "BGBG-TIP3P"      : {"attach" : "a00",
                                   "release": "r00"}}

    mask = {"SMIRNOFF99Frosst": "prod*.mden",
            "BGBG-TIP3P"      : f"mden*"
            }

    if ff == "BGBG-TIP3P" and state == "release":
        system = f"{system[0]}-xxxx-s"

    return os.path.join(base[ff], system, systems[ff], states[ff][state], mask[ff])