# Setup steps

The overall process is to take the solvated systems, use the existing force field to setup an APR calculation along the lines of what we used for SAMPLing, then convert each structure (in each window) to SMIRNOFF with `smirnovert`.

I'm having difficult opening the first `jupyter` notebook locally (but it is on GitHub).

The second notebook sets up the restraints.

## Technical
I'm working with `paprika` v0.0.3 for this setup, because the reorganization coming in v0.0.4 is not yet complete.


## pAPRika check list

- [ ] Make sure dummy atoms and guest anchor atoms lie roughly along the *z* axis.

# Analysis

It appears that simulations have been run for some amount (on `warthog`) of time in each window.

1. Confirm Niel's results for `a-bam-p`.
2. Look up my re-confirmation results.
3. Calculate the results, with the current trajectories in each window.

  This is BGBG-TIP3P.
