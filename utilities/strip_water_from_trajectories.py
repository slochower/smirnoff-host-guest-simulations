import subprocess as sp
import glob
import os
import re
import tqdm

windows = """
a000
a001
a002
a003
a004
a005
a006
a007
a008
a009
a010
a011
a012
a013
p000
p001
p002
p003
p004
p005
p006
p007
p008
p009
p010
p011
p012
p013
p014
p015
p016
p017
p018
p019
p020
p021
p022
p023
p024
p025
p026
p027
p028
p029
p030
p031
p032
p033
p034
p035
p036
p037
p038
p039
p040
p041
p042
p043
p044
p045"""

window_list = windows.split("\n")
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

for system in tqdm.tqdm(systems):
    for window in window_list:
        if os.path.exists(
            os.path.join("systems", system, "smrinoff", window, "vac.999.nc")
        ):
            # If we've already done the end points, skip.
            continue
        full_trajectories = []
        vacuum_trajectories = []
        files = glob.glob(
            os.path.join("systems", system, "smirnoff", window) + "/prod.*.nc"
        )
        for file in files:
            output = sp.check_output(f"ncdump -h {file} | grep 'atom ='", shell=True)
            m = re.search("atom = [0-9]*", output.decode("utf-8"))
            atoms = int(m.group(0).split("=")[1])
            if atoms > 200:
                full_trajectories.append(file)
            else:
                vacuum_trajectories.append(file)

        for trajectory in full_trajectories:
            traj = os.path.basename(trajectory)
            number = traj.split(".")[1]
            if os.path.exists(
                os.path.join("systems", system, "smirnoff", window, f"vac.{number}.nc")
            ):
                continue
            cpptraj = f"""
            parm smirnoff.prmtop 
            trajin {traj}
            strip :WAT
            strip :Na+
            strip :Cl-
            trajout vac.{number}.nc
            """

            with open(
                os.path.join(
                    "systems", system, "smirnoff", window, f"cpptraj.{number}.in"
                ),
                "w",
            ) as f:
                f.write(cpptraj)
            sp.call(
                f"cpptraj -i cpptraj.{number}.in > cpptraj.{number}.out",
                cwd=os.path.join("systems", system, "smirnoff", window),
                shell=True,
            )

        for trajectory in vacuum_trajectories:
            traj = os.path.basename(trajectory)
            number = os.path.basename(traj).split(".")[1]
            if os.path.exists(
                os.path.join("systems", system, "smirnoff", window, f"vac.{number}.nc")
            ):
                continue
            sp.call(
                f"cp {traj} vac.{number}.nc",
                cwd=os.path.join("systems", system, "smirnoff", window),
                shell=True,
            )

