# Code for analyzing host-guest calculations with SMIRNOFF99Frosst using the attach-pull-release method

This repository contains the results from attach-pull-release calculations on host-guest systems and notebooks to generate figures.

## Introduction
For the most direct comparison between force fields, we wanted to reuse existing files -- including exact coordinates -- that were previously used for GAFF v1.7 host-guest binding free energy calculations with APR in [Henriksen, et al. (2017)](https://pubs.acs.org/doi/abs/10.1021/acs.jctc.7b00359). This entailed writing a module to convert the parameters by separating the host and guest, dummy atoms, and solvent plus ions, parameterizing the host and guest using SMIRNOFF99Frosst, and then combining the structures. This task is accomplished in `setup/process.py`. Finally, we prepare and analyze the binding free energy simulations using our open source toolbox, `paprika`.

## Testing and caveats
Not shown in this repository, I used this pipeline to re-run the GAFF v1.7 calculations on a sample of systems to determine that preparing the calculations using `paprika` (in place of the old system of scripts), writing the input files using `simulate.py` and analyzing the calculations using `analyze.py` are able to reproduce the published results within the statistical uncertainty.

## Manifest
- `analysis`/: Contains files to compute the free energy of binding and enthalpy of binding after the simulations are completed. Some of the functions written into these files have been incorporated into pAPRika v0.0.4. *N.B.* I moved some of these into the `analysis` subdirectory after running them, and therefore, some paths will need to be updated for re-analysis. Several of the functions in the analysis scripts can be performed in a much more straight-forward way now (for example: by saving system restraints as JSON).
    - `analyze*.py`: Compute binding free energies
    - `enthalpy*.py`: Compute binding enthalpies
    - `parse_mden.py`: Helper function to read energies from AMBER `mden` files
    - `vac.py`: Create trajectories containing only the host and guest for faster postprocessing
- `build/`: Contains a `conda` environment file used for the setup and analysis of these simulations. Because it is not clear from the commits listed in the environment file, these simulations were performed with:
    - `paprika` version 0.0.3
    - Open Force Field Toolkit version 0.0.3
    - SMIRNOFF99Frosst version 1.0.5 using SMIRNOFF specification 1.0
    - AMBER16 and AMBER18 `pmemd.cuda` modules
    - ParmEd 2.7.3
- `geometry/`: Contains structures of alpha- and beta-cyclodextrin minimized with SMIRNOFF99Frosst and GAFF v1.7 and input files, in the `trimer` subdirectory, to run an MM energy scan along dihedral coordinates using three glucose units.
- `setup/`: Python files used to prepare the simulations.
    - `anchor_atoms.py`: Defines a helper function to determine the anchor atoms used to setup the APR calculation, based on the scheme in [Henriksen, et al. (2017)](https://pubs.acs.org/doi/abs/10.1021/acs.jctc.7b00359).
    - `process.py`: An example file converting the system `a-bam-p` from GAFF v1.7 parameters to SMIRNOFF99Frosst parameters. This relies on a local copy of `smirnovert.utils`, which is not currently in this directory -- and so it will not run -- but it is useful for me to keep it here as a historical artifact.
    - `release.py`: Setup a single release calculation for each cyclodextrin. This step computes the work of releasing the conformational restraints on the host, in the absence of guest, and therefore only needs to be computed once for each unique host.
    - `restraints.py`: Defines helper functions to setup APR restraints on cyclodextrins.
    - `setup_restraints.py`: Uses `smirnovert` to convert systems from GAFF v1.7 to SMIRNOFF99Frosst, sets up the restraint scheme using `paprika`, and then writes the AMBER restraint file (`disang.rest`) in each window for each system.
- `simulation/`: Python files used to run and check the completion status of the simulations.
    - `simulate.py`: Main simulation file, intended to be run in each window of each system.
    - `simulate-enthalpy.py`: Adaptation of `simulate.py` to run the end points to 1 us for enthalpy calculations.
    - `link*.py`/`check*.py`/`clean.py`/`run.py`: Utility files to create links and check of the status of the simulations.
- `systems/`: The host-guest complexes considered in this study. To put this on GitHub, I have not included any files from individual APR windows. There are `prmtop` files for GAFF v1.7 and GAFF v2.1 simulations. For SMIRNOFF99Frosst, there are individual `mol2` files for the host and guest (in GAFF format and Tripos/SYBYL format) along with initial coordinates and `prmtop` files.

### Note
The analysis scripts in this repository write files into a subdirectory `results/` which is not present on GitHub. In the interest in simplicity, speed, and due to limitations with Git repository sizes, the actual analysis notebooks are in [this separate](https://github.com/slochower/smirnoff-host-guest-simulations) notebook, where the `results/` directory lives.

Also, in case it is not clear, the analysis scripts will not work out-of-the-box to reproduce the results because the raw simulation data (500 GB--1 TB per force field) is not stored on GitHub.

## Assumptions
Please see [this repository](https://github.com/slochower/smirnoff-host-guest) for assumptions that go into the conversion of parameters from GAFF to SMIRNOFF99Frosst.