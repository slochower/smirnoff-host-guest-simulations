import glob as glob
import os as os
import subprocess as sp


def rsync(system):

    source = os.path.join(
        "/data/nhenriksen/projects/cds/wat6/bgbg-tip3p", system, "a00"
    )
    destination = os.path.join("../systems", system, "bgbg-tip3p")

    if not os.path.isdir(destination):
        print(f"Creating {destination}...")
        os.makedirs(destination)

    log_file = os.path.join(destination, "rsync.log")
    rsync_list = [
        "rsync",
        "-armv",
        '-e "ssh"',
        '--include="mdin"',
        '--include="full.crds"',
        '--include="full.hmr.topo"',
        '--include="fe/ti-a.dat"',
        '--include="fe/ti-u.dat"',
        '--include="*.mol2"',
        '--exclude="*"',
        "{}".format("davids4@kirkwood:" + source + "/"),
        "{}".format("."),
    ]
    with open(log_file, "a") as file:
        file.write(" ".join(rsync_list))
        file.write("\n")
        p = sp.Popen(
            [" ".join(rsync_list)],
            cwd=destination,
            stdout=file,
            stderr=file,
            shell=True,
        )
        output, error = p.communicate()
        if p.returncode == 0:
            pass
        elif p.returncode == 1:
            print("Output: {}".format(output))
            print("Error: {}".format(error))

    source = os.path.join("/data/nhenriksen/projects/cds/wat6/bgbg-tip3p", system, "fe")
    destination = os.path.join("../systems", system, "bgbg-tip3p")

    rsync_list = [
        "rsync",
        "-armv",
        '-e "ssh"',
        '--include="ti-a.dat"',
        '--include="ti-u.dat"',
        '--exclude="*"',
        "{}".format("davids4@kirkwood:" + source + "/"),
        "{}".format("."),
    ]
    with open(log_file, "a") as file:
        file.write(" ".join(rsync_list))
        file.write("\n")
        p = sp.Popen(
            [" ".join(rsync_list)],
            cwd=destination,
            stdout=file,
            stderr=file,
            shell=True,
        )
        output, error = p.communicate()

    if system[0] == "a":
        source = os.path.join("/data/nhenriksen/projects/cds/wat6/bgbg-tip3p", "a-xxxx-s", "fe")
    elif system[0] == "b":
        source = os.path.join("/data/nhenriksen/projects/cds/wat6/bgbg-tip3p", "b-xxxx-s", "fe")
    rsync_list = [
        "rsync",
        "-armv",
        '-e "ssh"',
        '--include="ti-r.dat"',
        '--exclude="*"',
        "{}".format("davids4@kirkwood:" + source + "/"),
        "{}".format("."),
    ]
    with open(log_file, "a") as file:
        file.write(" ".join(rsync_list))
        file.write("\n")
        p = sp.Popen(
            [" ".join(rsync_list)],
            cwd=destination,
            stdout=file,
            stderr=file,
            shell=True,
        )
        output, error = p.communicate()

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
for system in systems:
    rsync(system)
