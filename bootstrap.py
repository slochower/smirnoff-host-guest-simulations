import numpy as np
import scipy as sc


def summarize(x, y):

    summary_statistics = np.empty(8)
    # Slope, intercept, R
    summary_statistics[0], summary_statistics[1], summary_statistics[
        2
    ], pval, stderr = sc.stats.linregress(x, y)
    # R**2
    summary_statistics[3] = summary_statistics[2] ** 2
    # RMSE
    summary_statistics[4] = np.sqrt(np.mean((y - x) ** 2))
    # MSE
    summary_statistics[5] = np.mean(y - x)
    # MUE
    summary_statistics[6] = np.mean(np.absolute(y - x))
    # Tau
    summary_statistics[7], prob = sc.stats.kendalltau(x, y)

    return summary_statistics


def bootstrap(
    x, x_sem, y, y_sem, cycles=1000, with_replacement=True, with_uncertainty=True
):
    summary_statistics = np.empty((cycles, 8))
    for cycle in range(cycles):
        new_x = np.empty_like(x)
        new_y = np.empty_like(y)
        for index in range(len(x)):
            if with_replacement:
                j = np.random.randint(len(x))
            else:
                j = index
            if with_uncertainty and x_sem is not None:
                new_x[index] = np.random.normal(x[j], x_sem[j])
            elif with_uncertainty and x_sem is None:
                new_x[index] = x[j]
            if with_uncertainty and y_sem is not None:
                new_y[index] = np.random.normal(y[j], y_sem[j])
            elif with_uncertainty and y_sem is None:
                new_y[index] = y[j]
        summary_statistics[cycle] = summarize(new_x, new_y)

    results = {
        "mean": {
            "slope": np.mean(summary_statistics[:, 0]),
            "intercept": np.mean(summary_statistics[:, 1]),
            "R": np.mean(summary_statistics[:, 2]),
            "R**2": np.mean(summary_statistics[:, 3]),
            "RMSE": np.mean(summary_statistics[:, 4]),
        },
        "sem": {
            "slope": np.std(summary_statistics[:, 0]),
            "intercept": np.std(summary_statistics[:, 1]),
            "R": np.std(summary_statistics[:, 2]),
            "R**2": np.std(summary_statistics[:, 3]),
            "RMSE": np.std(summary_statistics[:, 4]),
        },
    }
    return results


def thermodynamic_bootstrap(
        x, x_sem, y, y_sem, cycles=1000, with_replacement=True, with_uncertainty=True
):
    summary_statistics = np.empty((cycles))
    R = 1.987204118e-3  # kcal/mol-K
    temperature = 300  # K
    beta = 1.0 / (R * temperature)

    for cycle in range(cycles):
        new_x = np.empty_like(x)
        new_y = np.empty_like(y)

        if with_uncertainty and x_sem is not None:
            new_x = np.random.normal(x, x_sem)
        elif with_uncertainty and x_sem is None:
            new_x = x
        if with_uncertainty and y_sem is not None:
            new_y = np.random.normal(y, y_sem)
        elif with_uncertainty and y_sem is None:
            new_y = y
        summary_statistics[cycle] = -R * temperature * np.log(
            np.exp(-beta * new_x) + np.exp(-beta * new_y))

    results = {
        "mean": np.mean(summary_statistics),
        "sem" : np.std(summary_statistics)
    }
    return results