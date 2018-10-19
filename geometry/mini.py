#!/usr/bin/env python

import subprocess as sp

for system in ["alpha_smirnoff", "beta_smirnoff", "alpha_gaff", "beta_gaff"]:
	
	command = f"sander -O -p {system}.prmtop -ref {system}.rst7 -c {system}.rst7 -i mini.in -o {system}_minimized.out -r {system}_minimized.rst7 -inf /dev/null"
	sp.call(command, shell=True)
