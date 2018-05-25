import os as os
import shutil as shutil
import re as re

import paprika as paprika
from paprika.amber import Simulation

import logging

logging.basicConfig(
    filename='tscc.log',
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %I:%M:%S %p',
    level=logging.DEBUG)
logging.info('Started logging...')
logging.info(paprika.__version__)

ntwprt = 146
nstlim = 1250000
dt = 0.004
initial_topology = 'full.hmr.topo'
initial_coordinates = 'full.crds'

sim = Simulation()

# Minimization
sim.executable = 'pmemd.cuda'
sim.topology = initial_topology
sim.prefix = 'minimize'
sim.inpcrd = initial_coordinates
sim.path = './'
sim.ref = initial_coordinates
sim.config_pbc_min()
sim.cntrl['maxcyc'] = 50000
sim.cntrl['ncyc'] = 5000
sim.cntrl['ntr'] = 1
sim.cntrl['restraint_wt'] = 50.0
sim.cntrl['restraintmask'] = "'@DUM | :10@C4 | :10@N1'"
sim.cntrl['cut'] = 9.0
sim.restraint_file = 'disang.rest'
sim.run(fail_ok=False)

# Equilibration
sim.config_pbc_md()
sim.executable = 'pmemd.cuda'
sim.topology = initial_topology
sim.path = './'
sim.restraint_file = 'disang.rest'

sim.cntrl['nstlim'] = nstlim
sim.cntrl['ntwx'] = 250
sim.cntrl['ntwprt'] = ntwprt
sim.cntrl['ntwr'] = 250
sim.cntrl['cut'] = 9.0

iteration = 0
sim.prefix = 'equil.{:03d}'.format(iteration)
sim.inpcrd = initial_coordinates
sim.ref = initial_coordinates

while not os.path.isfile('equil.rst7') and iteration < 10:
    sim.run(fail_ok=True)
    with open('equil.{:03d}.out'.format(iteration)) as f:
        for line in f.readlines():
            if re.search(' TIMINGS', line):
                shutil.copy(sim.restart, 'equil.rst7')
    iteration += 1
    sim.prefix = 'equil.{:03d}'.format(iteration)
    sim.inpcrd = 'equil.{:03d}.rst7'.format(iteration - 1)
    sim.ref = initial_coordinates

# Production -- first 5 ns
iteration = 0
sim.executable = 'pmemd.cuda'
sim.path = './'
sim.topology = initial_topology
sim.restraint_file = 'disang.rest'
sim.config_pbc_md()

sim.prefix = 'prod.{:03d}'.format(iteration)
if iteration == 0:
    sim.inpcrd = 'equil.rst7'
else:
    sim.inpcrd = 'prod.{:03d}.rst7'.format(iteration - 1)

sim.ref = 'solvate.rst7'
sim.cntrl['ntx'] = 5
sim.cntrl['irest'] = 1
sim.cntrl['nstlim'] = nstlim
sim.cntrl['ntwr'] = nstlim
sim.cntrl['ntwx'] = 250
sim.cntrl['ntwprt'] = ntwprt
sim.cntrl['ntxo'] = 2
sim.cntrl['cut'] = 9.0
sim.restraint_file = 'disang.rest'
sim.run(fail_ok=False)