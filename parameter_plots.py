import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.colors import colorConverter
from adjustText import adjust_text


def scatter_angle(
    df, x, y, xlabel, ylabel, lower_lim, upper_lim, highlight_color, name, adjust=False
):
    fig, ax = plt.subplots(1, figsize=(6 * 1.2, 6))
    text = []

    labeled_df = pd.DataFrame()
    for i, j in zip(df[x], df[y]):
        # Find rows matching this value...
        i = np.round(i, 2)
        j = np.round(j, 2)

        tmp = df[(np.round(df[x], 2) == i) & (np.round(df[y], 2) == j)]
        atom1s = tmp.atom1
        atom2s = tmp.atom2
        atom3s = tmp.atom3
        names = [f"{i}-{j}-{k}" for i, j, k in zip(atom1s, atom2s, atom3s)]

        # I've added additional rounding because multiple angles are really quite close together.
        labeled_df = labeled_df.append(
            pd.DataFrame({"i": np.round(i, 1), "j": np.round(j, 1), "names": ",".join(names)}, index=[0]),
            ignore_index=True,
        )

    labeled_df.drop_duplicates(inplace=True)
    labeled_df.reset_index(inplace=True)

    for index, row in labeled_df.iterrows():
        all_names = row.names.split(",")
        elements = []
        for name in all_names:
            atoms = name.split("-")
            elemental_angle = "--".join(atom[0] for atom in atoms)
            elements.append(elemental_angle)

        element_angles = [i for i in set(elements)]
        element_names = ",".join(element_angles)
        labeled_df.iloc[index, labeled_df.columns.get_loc("names")] = element_names

    # return labeled_df, labeled_df.drop_duplicates(inplace=True)
    # Merge angles which are the same, but labeled in reverse

    for index, row in labeled_df.iterrows():
        names = row.names
        # seen = set ()
        # Something like this should be more general: https://stackoverflow.com/questions/17212208/removing-reverse-elements-in-a-python-list
        # reduced_names = [x for x in names if tuple(x[::-1]) not in seen and not seen.add(tuple(names))]
        print(f"Pruning {names.split(',')[1:]} from {names.split(',')[0]}.")
        # I am printing this out, because it is not the most general solution.
        # This doesn't truly detect if things are palindromes.
        labeled_df.iloc[index, labeled_df.columns.get_loc("names")] = names.split(",")[0]

    # Deduplicate names, again.
    labeled_df.drop_duplicates(subset = "names", inplace=True)
    labeled_df.reset_index(inplace=True)

    for index, row in labeled_df.iterrows():
        if abs(row.i - row.j) > 0.1 * row.i:
            ax.scatter(
                row.i, row.j, s=80, edgecolor="none", lw=0.2, color="r", zorder=2
            )
            text.append(plt.text(row.i, row.j, f"{row.names}", color="r", size=14))

        else:
            ax.scatter(row.i, row.j, s=80, edgecolor="none", lw=0.2, color="0.5")


    ax.plot([-500, 500], [-500, 500], ls="-", c="0.3", zorder=-1, lw="0.5")
    ax.set_ylim([lower_lim, upper_lim])
    ax.set_xlim([lower_lim, upper_lim])

    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)

    if adjust:
        adjust_text(
            text,
            expand_points=(1.5, 1.5),
            expand_text=(2, 2),
            arrowprops=dict(arrowstyle="-", color="k"),
        )

    fig.savefig(f"figures/{name}", bbox_inches="tight")
