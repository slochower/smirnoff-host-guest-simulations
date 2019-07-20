# Code for analyzing host-guest calculations with SMIRNOFF99Frosst using the attach-pull-release method

This repository contains the results from attach-pull-release calculations on host-guest systems and notebooks to generate figures.

## Introduction
This repository contains most of the analysis scripts used to generate the figures and the tables in our [manuscript](https://slochower.github.io/smirnoff-host-guest-manuscript/). For further information on how the simulations were setup, run, or parameterized, please see:

- [GitHub repository](https://github.com/slochower/smirnoff-host-guest) used to convert AMBER input files from GAFF force field to SMIRNOFF99Frosst.
- [GitHub repository](https://github.com/slochower/smirnoff-host-guest-simulations-data) for setting up the attach-pull-release calculations using `paprika` version 0.0.3.
- [GitHub repository](https://github.com/openforcefield/openforcefield) for the Open Force Field group containing the toolkit and force field XML file.

## Testing and caveats
The scripts in this repository were *mostly* generated using the `conda` environment in the `build` subdirectory. For a few analyses on the parameters, I used a later version of the open force field toolkit to parse `mol2` files into SMILES and more easily look at the applied parameters.

## Manifest
- `build/`: Contains a `conda` environment file used for the setup and analysis of these simulations. Because it is not clear from the commits listed in the environment file, this analysis was performed with:
    - `paprika` version 0.0.4

- `exploratory-notebooks/`: Contains notebooks used to probe and prod at the data without producing figures that made it into the manuscript. These notebooks include things like checking for data consistency, poking at the applied parameters, parsing energies from simulation output files, looking at the restraints, and other stuff. In general, this probably won't work out of the box and may contain absolute paths or links to files that don't exist in the repository.

- `figures/`: Figures automatically generated in PNG and PDF form.
- `images/`: (Mostly) visualizations manually created to look at specific systems.
- `results/`: Processed results from `paprika` in JSON format and summary statistics in CSV format. Reading the `np.array`s in the `json` will depend on the `json_numpy_hook` in `paprika`.
- `systems/`: The host-guest complexes considered in this study. To put this on GitHub, I have not included any files from individual APR windows. There are `prmtop` files for GAFF v1.7 and GAFF v2.1 simulations. For SMIRNOFF99Frosst, there are individual `mol2` files for the host and guest (in GAFF format and Tripos/SYBYL format) along with initial coordinates and `prmtop` files.
- `utilities/`: Miscellaneous scripts to help in data processing.

