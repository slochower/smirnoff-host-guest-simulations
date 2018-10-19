import os
import subprocess as sp
from constants import systems

for system in systems:
    source = os.path.join("/data/nhenriksen/projects/cds/wat6/bgbg-tip3p", system, "fe")
    destination = os.path.join("systems", system, "bgbg-tip3p")
    if not os.path.isdir(destination):
        print(f"Creating {destination}...")
        os.makedirs(destination)

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
    p = sp.Popen([" ".join(rsync_list)], cwd=destination, shell=True)
    output, error = p.communicate()
    if p.returncode == 0:
        pass
    elif p.returncode == 1:
        print("Output: {}".format(output))
        print("Error: {}".format(error))

for niel, dave in zip(["a-xxxx-s", "b-xxxx-s"], ["a-release", "b-release"]):
    source = os.path.join("/data/nhenriksen/projects/cds/wat6/bgbg-tip3p", niel, "fe")
    destination = os.path.join("systems", dave, "bgbg-tip3p")

    if not os.path.isdir(destination):
        print(f"Creating {destination}...")
        os.makedirs(destination)

    rsync_list = [
        "rsync",
        "-armv",
        '-e "ssh"',
        '--include="ti-r.dat"',
        '--exclude="*"',
        "{}".format("davids4@kirkwood:" + source + "/"),
        "{}".format("."),
    ]
    p = sp.Popen([" ".join(rsync_list)], cwd=destination, shell=True)
    output, error = p.communicate()
    if p.returncode == 0:
        pass
    elif p.returncode == 1:
        print("Output: {}".format(output))
        print("Error: {}".format(error))
