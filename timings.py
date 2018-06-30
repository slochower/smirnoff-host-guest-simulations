def count_simulation_time(window):
    with open(os.path.join(window, "mdin"), "r") as f:
        read_data = f.read()
    dt = [float(i.split("=")[1][:-1]) for i in read_data.splitlines() if "dt" in i][0]
    nstlim = [
        int(i.split("=")[1][:-1]) for i in read_data.splitlines() if "nstlim" in i
    ][0]
    trajectories = glob.glob(os.path.join(window, "traj") + "*")
    trajectories = [i for i in trajectories if "rst" not in i]
    number_trajectories = len(trajectories)

    simulation_time = dt * nstlim * number_trajectories

    return nstlim, number_trajectories, simulation_time
