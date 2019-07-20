import itertools
import pandas as pd
import os

def table(thermodynamic_quantity="G", subset="overall", comparison="experimental_smirnoff"):
    if not thermodynamic_quantity == "-TdS":
        file_prefixes = [f"{comparison}_d{thermodynamic_quantity}_statistics_{subset}.csv"]
    else:
        file_prefixes = [f"{comparison}_{thermodynamic_quantity}_statistics_{subset}.csv"]

#         file_prefixes = [
#             f"experimental_smirnoff_d{thermodynamic_quantity}_statistics",
#             f"experimental_bgbg_d{thermodynamic_quantity}_statistics",
#             f"experimental_bg2bg2_d{thermodynamic_quantity}_statistics",
#         ]


        
#     suffixes = ["_overall.csv",
#                 "_aliphatic_ammoniums.csv",
#                 "_aliphatic_carboxylates.csv",
#                 "_cyclic_alcohols.csv"
#                ]
        
    files = [file for file in file_prefixes]
    mapping = {"smirnoff": "SMIRNOFF99Frosst",
               "bgbg": "GAFF v1.7",
               "bg2bg2": "GAFF v2.1"
              }
    
#     names = ["SMIRNOFF99Frosst", "SMIRNOFF99Frosst", "SMIRNOFF99Frosst", "SMIRNOFF99Frosst",
#              "GAFF v1.7", "GAFF v1.7", "GAFF v1.7", "GAFF v1.7", 
#              "GAFF v2.1", "GAFF v2.1", "GAFF v2.1", "GAFF v2.1"]
    simulation_name = comparison.split("_")[1]
    names = [mapping[simulation_name]]
    for name, file in zip(names, files):
        statistics = pd.read_csv(os.path.join("results", file))
        statistics.index = statistics["Unnamed: 0"]

        rmse = statistics["mean"]["RMSE"]
        rmse_ci_low, rmse_ci_high = statistics["ci_low"]["RMSE"], statistics["ci_high"]["RMSE"]
        mse = statistics["mean"]["MSE"]
        mse_ci_low, mse_ci_high = statistics["ci_low"]["MSE"], statistics["ci_high"]["MSE"]
        r_2 = statistics["mean"]["R**2"]
        r_2_ci_low, r_2_ci_high = statistics["ci_low"]["R**2"], statistics["ci_high"]["R**2"]
        slope = statistics["mean"]["slope"]
        slope_ci_low, slope_ci_high = statistics["ci_low"]["slope"], statistics["ci_high"]["slope"]
        intercept = statistics["mean"]["intercept"]
        intercept_ci_high, intercept_ci_low = statistics["ci_low"]["intercept"], statistics["ci_high"]["intercept"]
        tau = statistics["mean"]["Tau"]
        tau_ci_high, tau_ci_low = statistics["ci_low"]["Tau"], statistics["ci_high"]["Tau"]

        statistics = [
            rmse,
            [rmse_ci_low,
            rmse_ci_high],
            mse,
            [mse_ci_low,
            mse_ci_high],
            r_2,
            [r_2_ci_low,
            r_2_ci_high],
            slope,
            [slope_ci_low,
            slope_ci_high],
            intercept,
            [intercept_ci_low,
            intercept_ci_high],
            tau,
            [tau_ci_low,
             tau_ci_high]
        ]
#         print("| | RMSE |         |          |"
#               "    MSE  |         |          |"
#               "    R²   |         |          |"
#               "   Slope |         |          |"
#               "Intercept|         |          |")
#         print("| | Mean | 2.5% CI | 97.5% CI |",
#               "    Mean | 2.5% CI | 97.5% CI |",
#               "    Mean | 2.5% CI | 97.5% CI |",
#               "    Mean | 2.5% CI | 97.5% CI |",
#               "    Mean | 2.5% CI | 97.5% CI |",
#                 )

#         print("")
#         print(file)
#         print("")
    
        if thermodynamic_quantity == "G":
            print(f"| Δ{thermodynamic_quantity}°", end = " | ")
        elif thermodynamic_quantity == "H":
            print(f"| Δ{thermodynamic_quantity}", end = " | ")
        else:
            print(f"| −TΔS°", end = " | ")
        print(name, end=" | ")
        for value in statistics:
            if not isinstance(value, list):
                print(f"{value:0.2f}", end=" | ")
            else:
                print(f"[{value[0]:0.2f}, {value[1]:0.2f}]", end = " | ")
        print("")
        
