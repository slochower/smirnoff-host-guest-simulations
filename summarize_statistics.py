import os
import pandas as pd
from bootstrap import bootstrap


def write_statistics(
    df_one, df_two, thermodynamic_quantity, file_prefix, cycles=100000,
    overwrite=True,
):

    try:
        df = df_one.merge(df_two, on=["System", "Type"], suffixes=("_i", "_j"))
    except KeyError:
        # Experimental doesn't have a Type column, so won't merge cleanly.
        df = df_one.merge(df_two, on=["System"], suffixes=("_i", "_j"))
    overall_file = (
        f"results/{file_prefix}_d{thermodynamic_quantity}_statistics_overall.csv"
    )

    if not os.path.exists(overall_file) or overwrite:
        print(f"Bootstrapping {overall_file}")
        results = bootstrap(
            x=df[f"Delta {thermodynamic_quantity}_i"],
            x_sem=df[f"{thermodynamic_quantity}_SEM_i"],
            y=df[f"Delta {thermodynamic_quantity}_j"],
            y_sem=df[f"{thermodynamic_quantity}_SEM_j"],
            cycles=cycles,
        )
        overall = pd.DataFrame(results)
        overall.to_csv(overall_file)
    else:
        print(f"Skipping {overall_file}...")

    aliphatic_ammoniums_file = f"results/{file_prefix}_d{thermodynamic_quantity}_statistics_aliphatic_ammoniums.csv"
    if not os.path.exists(aliphatic_ammoniums_file) or overwrite:
        print(f"Bootstrapping {aliphatic_ammoniums_file}")
        tmp = df[df["Type"] == "aliphatic_ammoniums"]
        results = bootstrap(
            tmp[f"Delta {thermodynamic_quantity}_i"].values,
            tmp[f"{thermodynamic_quantity}_SEM_i"].values,
            tmp[f"Delta {thermodynamic_quantity}_j"].values,
            tmp[f"{thermodynamic_quantity}_SEM_j"].values,
            cycles=cycles,
        )
        aliphatic_ammoniums = pd.DataFrame(results)
        aliphatic_ammoniums.to_csv(aliphatic_ammoniums_file)
    else:
        print(f"Skipping {aliphatic_ammoniums_file}...")

    cyclic_alcohols_file = f"results/{file_prefix}_d{thermodynamic_quantity}_statistics_cyclic_alcohols.csv"
    if not os.path.exists(cyclic_alcohols_file) or overwrite:
        print(f"Bootstrapping {cyclic_alcohols_file}")
        tmp = df[df["Type"] == "cyclic_alcohols"]
        results = bootstrap(
            tmp[f"Delta {thermodynamic_quantity}_i"].values,
            tmp[f"{thermodynamic_quantity}_SEM_i"].values,
            tmp[f"Delta {thermodynamic_quantity}_j"].values,
            tmp[f"{thermodynamic_quantity}_SEM_j"].values,
            cycles=cycles,
        )

        cyclic_alcohols = pd.DataFrame(results)
        cyclic_alcohols.to_csv(cyclic_alcohols_file)
    else:
        print(f"Skipping {cyclic_alcohols_file}...")

    aliphatic_carboxylates_file = f"results/{file_prefix}_d{thermodynamic_quantity}_statistics_aliphatic_carboxylates.csv"
    if not os.path.exists(aliphatic_carboxylates_file) or overwrite:
        print(f"Bootstrapping {aliphatic_carboxylates_file}")
        tmp = df[df["Type"] == "aliphatic_carboxylates"]
        results = bootstrap(
            tmp[f"Delta {thermodynamic_quantity}_i"].values,
            tmp[f"{thermodynamic_quantity}_SEM_i"].values,
            tmp[f"Delta {thermodynamic_quantity}_j"].values,
            tmp[f"{thermodynamic_quantity}_SEM_j"].values,
            cycles=cycles,
        )

        aliphatic_carboxylates = pd.DataFrame(results)
        aliphatic_carboxylates.to_csv(aliphatic_carboxylates_file)
    else:
        print(f"Skipping {aliphatic_carboxylates_file}...")


def write_entropy_statistics(
    df_one, df_two, thermodynamic_quantity, file_prefix, cycles=100000,
    overwrite=True
):

    try:
        df = df_one.merge(df_two, on=["System", "Type"], suffixes=("_i", "_j"))
    except KeyError:
        # Experimental doesn't have a Type column, so won't merge cleanly.
        df = df_one.merge(df_two, on=["System"], suffixes=("_i", "_j"))
    overall_file = (
        f"results/{file_prefix}_{thermodynamic_quantity}_statistics_overall.csv"
    )

    if not os.path.exists(overall_file) or overwrite:
        print(f"Bootstrapping {overall_file}")
        results = bootstrap(
            x=df[f"{thermodynamic_quantity}_i"],
            x_sem=df[f"{thermodynamic_quantity}_SEM_i"],
            y=df[f"{thermodynamic_quantity}_j"],
            y_sem=df[f"{thermodynamic_quantity}_SEM_j"],
            cycles=cycles,
        )
        overall = pd.DataFrame(results)
        overall.to_csv(overall_file)
    else:
        print(f"Skipping {overall_file}...")

    aliphatic_ammoniums_file = f"results/{file_prefix}_{thermodynamic_quantity}_statistics_aliphatic_ammoniums.csv"
    if not os.path.exists(aliphatic_ammoniums_file) or overwrite:
        print(f"Bootstrapping {aliphatic_ammoniums_file}")
        tmp = df[df["Type"] == "aliphatic_ammoniums"]
        results = bootstrap(
            tmp[f"{thermodynamic_quantity}_i"].values,
            tmp[f"{thermodynamic_quantity}_SEM_i"].values,
            tmp[f"{thermodynamic_quantity}_j"].values,
            tmp[f"{thermodynamic_quantity}_SEM_j"].values,
            cycles=cycles,
        )
        aliphatic_ammoniums = pd.DataFrame(results)
        aliphatic_ammoniums.to_csv(aliphatic_ammoniums_file)
    else:
        print(f"Skipping {aliphatic_ammoniums_file}...")

    cyclic_alcohols_file = f"results/{file_prefix}_{thermodynamic_quantity}_statistics_cyclic_alcohols.csv"
    if not os.path.exists(cyclic_alcohols_file) or overwrite:
        print(f"Bootstrapping {cyclic_alcohols_file}")
        tmp = df[df["Type"] == "cyclic_alcohols"]
        results = bootstrap(
            tmp[f"{thermodynamic_quantity}_i"].values,
            tmp[f"{thermodynamic_quantity}_SEM_i"].values,
            tmp[f"{thermodynamic_quantity}_j"].values,
            tmp[f"{thermodynamic_quantity}_SEM_j"].values,
            cycles=cycles,
        )

        cyclic_alcohols = pd.DataFrame(results)
        cyclic_alcohols.to_csv(cyclic_alcohols_file)
    else:
        print(f"Skipping {cyclic_alcohols_file}...")

    aliphatic_carboxylates_file = f"results/{file_prefix}_{thermodynamic_quantity}_statistics_aliphatic_carboxylates.csv"
    if not os.path.exists(aliphatic_carboxylates_file) or overwrite:
        print(f"Bootstrapping {aliphatic_ammoniums_file}")
        tmp = df[df["Type"] == "aliphatic_carboxylates"]
        results = bootstrap(
            tmp[f"{thermodynamic_quantity}_i"].values,
            tmp[f"{thermodynamic_quantity}_SEM_i"].values,
            tmp[f"{thermodynamic_quantity}_j"].values,
            tmp[f"{thermodynamic_quantity}_SEM_j"].values,
            cycles=cycles,
        )

        aliphatic_carboxylates = pd.DataFrame(results)
        aliphatic_carboxylates.to_csv(aliphatic_carboxylates_file)
    else:
        print(f"Skipping {aliphatic_carboxylates_file}...")
