import glob
import os

directories = glob.glob("systems/*/smirnoff/a*")
directories += glob.glob("systems/*/smirnoff/p*")
directories = [i for i in directories if os.path.isdir(i)]

patterns = ["prod*"]


for directory in sorted(directories):
    for pattern in patterns:
        files = glob.glob(directory + "/" + pattern)
        for file in files:
            try:
                os.remove(file)
                print(f"Deleting {file}")
            except:
                print(f"Problem deleting {file}")
                pass
