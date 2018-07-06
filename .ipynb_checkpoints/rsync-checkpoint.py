import glob as glob
import os as os
import subprocess as sp


def rsync(system):

    source = os.path.join(
        "/data/nhenriksen/projects/cds/wat6/bgbg-tip3p", system, "a00"
    )
    destination = os.path.join("systems", system, "bgbg-tip3p")

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
