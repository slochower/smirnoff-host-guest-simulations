import pandas as pd
import os


def table(thermodynamic_quantity="G"):
    file_prefixes = [
        f"experimental_smirnoff_d{thermodynamic_quantity}_statistics",
        f"experimental_bgbg_d{thermodynamic_quantity}_statistics",
        f"experimental_bg2bg2_d{thermodynamic_quantity}_statistics",
    ]
    files = [file + "_overall.csv" for file in file_prefixes]
    names = ["SMIRNOFF99Frosst", "GAFF v1.7", "GAFF v2.1"]
    for name, file in zip(names, files):
        statistics = pd.read_csv(os.path.join("results", file))
        statistics.index = statistics["Unnamed: 0"]

        rmse = statistics["mean"]["RMSE"]
        rmse_sem = statistics["sem"]["RMSE"]
        mse = statistics["mean"]["MSE"]
        mse_sem = statistics["sem"]["MSE"]
        r_2 = statistics["mean"]["R**2"]
        r_2_sem = statistics["sem"]["R**2"]
        slope = statistics["mean"]["slope"]
        slope_sem = statistics["sem"]["slope"]
        intercept = statistics["mean"]["intercept"]
        intercept_sem = statistics["sem"]["intercept"]

        statistics = [
            rmse,
            rmse_sem,
            mse,
            mse_sem,
            r_2,
            r_2_sem,
            slope,
            slope_sem,
            intercept,
            intercept_sem,
        ]
        print(name, end="\t")
        for value in statistics:
            print(f"{value:0.2f}", end="\t")
        print("\n")


def entropy_table(thermodynamic_quantity="-TdS"):
    file_prefixes = [
        f"experimental_smirnoff_{thermodynamic_quantity}_statistics",
        f"experimental_bgbg_{thermodynamic_quantity}_statistics",
        f"experimental_bg2bg2_{thermodynamic_quantity}_statistics",
    ]
    files = [file + "_overall.csv" for file in file_prefixes]
    names = ["SMIRNOFF99Frosst", "GAFF v1.7", "GAFF v2.1"]
    for name, file in zip(names, files):
        statistics = pd.read_csv(os.path.join("results", file))
        statistics.index = statistics["Unnamed: 0"]

        rmse = statistics["mean"]["RMSE"]
        rmse_sem = statistics["sem"]["RMSE"]
        mse = statistics["mean"]["MSE"]
        mse_sem = statistics["sem"]["MSE"]
        r_2 = statistics["mean"]["R**2"]
        r_2_sem = statistics["sem"]["R**2"]
        slope = statistics["mean"]["slope"]
        slope_sem = statistics["sem"]["slope"]
        intercept = statistics["mean"]["intercept"]
        intercept_sem = statistics["sem"]["intercept"]

        statistics = [
            rmse,
            rmse_sem,
            mse,
            mse_sem,
            r_2,
            r_2_sem,
            slope,
            slope_sem,
            intercept,
            intercept_sem,
        ]
        print(name, end="\t")
        for value in statistics:
            print(f"{value:0.2f}", end="\t")
        print("\n")

def big_table():
    pass
