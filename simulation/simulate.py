import os as os
import subprocess as sp
import shutil as shutil
import re as re

import paprika as paprika
from paprika.amber import Simulation

import logging


def recenter(prmtop, inpcrd, mask):
    trajout = inpcrd.split(".")[0] + "-centered.inpcrd"
    cpptraj = f"""
    parm {prmtop}
    trajin {inpcrd}
    center {mask} origin
    trajout {trajout} restart
    """
    with open("center.in", "w") as f:
        f.write(cpptraj)
    sp.call("cpptraj -i center.in > center.out", shell=True)


logging.basicConfig(
    filename="tscc.log",
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S %p",
    level=logging.DEBUG,
)
logging.info("Started logging...")
logging.info(paprika.__version__)
hostname = sp.check_output(["hostname"])
nvidia_smi = sp.check_output(["nvidia-smi"])
logging.info(hostname.decode("utf-8"))
logging.info(nvidia_smi.decode("utf-8"))

nstlim = 500000

sim = Simulation()

# Minimization
sim.executable = "pmemd.cuda"
sim.topology = "smirnoff.prmtop"
sim.prefix = "minimize"
sim.inpcrd = "smirnoff.inpcrd"
sim.path = "./"
sim.ref = "smirnoff.inpcrd"
sim.config_pbc_min()
sim.cntrl["maxcyc"] = 500
sim.cntrl["ncyc"] = 400
sim.cntrl["ntr"] = 1
sim.cntrl["restraint_wt"] = 50.0
sim.cntrl["restraintmask"] = "'@Pb'"
sim.cntrl["cut"] = 9.0
sim.restraint_file = "disang.rest"
sim.run(fail_ok=False)

# Equilibration
sim.config_pbc_md()
sim.executable = "pmemd.cuda"
sim.topology = "smirnoff.prmtop"
sim.path = "./"
sim.restraint_file = "disang.rest"

sim.cntrl["nstlim"] = nstlim
sim.cntrl["ntwx"] = 250
sim.cntrl["ntwr"] = 250
sim.cntrl["cut"] = 9.0

iteration = 0
sim.prefix = "equil.{:03d}".format(iteration)
sim.inpcrd = "minimize.rst7"
sim.ref = "smirnoff.inpcrd"

while not os.path.isfile("equil.rst7") and iteration < 10:
    sim.run(fail_ok=True)
    with open("equil.{:03d}.out".format(iteration)) as f:
        for line in f.readlines():
            if re.search(" TIMINGS", line):
                shutil.copy(sim.restart, "equil.rst7")

    recenter("smirnoff.prmtop", "equil.{:03d}.rst7", mask="@Pb")
    iteration += 1
    sim.prefix = "equil.{:03d}".format(iteration)
    sim.inpcrd = "equil.{:03d}.rst7".format(iteration - 1)
    sim.ref = "smirnoff.inpcrd"


recenter("smirnoff.prmtop", "equil.rst7", mask="@Pb")
recenter("smirnoff.prmtop", "smirnoff.inpcrd", mask="@Pb")

# Production
for iteration in range(0, 10):
    sim.executable = "pmemd.cuda"
    sim.path = "./"
    sim.topology = "smirnoff.prmtop"
    sim.restraint_file = "disang.rest"
    sim.config_pbc_md()

    sim.prefix = "prod.{:03d}".format(iteration)
    if iteration == 0:
        sim.inpcrd = "equil-centered.inpcrd"
    else:
        sim.inpcrd = "prod.{:03d}.rst7".format(iteration - 1)

    sim.ref = "smirnoff-centered.inpcrd"
    sim.cntrl["ntx"] = 5
    sim.cntrl["irest"] = 1
    sim.cntrl["nstlim"] = nstlim
    sim.cntrl["ntwr"] = nstlim
    sim.cntrl["ntwx"] = 250
    sim.cntrl["ntxo"] = 2
    sim.cntrl["cut"] = 9.0
    sim.cntrl["iwrap"] = 0

    sim.restraint_file = "disang.rest"
    sim.run(fail_ok=False)
