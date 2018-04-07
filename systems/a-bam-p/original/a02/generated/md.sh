#!/usr/bin/env bash

$AMBERHOME/bin/pmemd.cuda -O -p smirnoff.prmtop -ref smirnoff.inpcrd -c md.000.rst -i mdin -o mdout.001 -r md.001.rst -x traj.001.nc -inf mdinfo.001 -e mden.001 

