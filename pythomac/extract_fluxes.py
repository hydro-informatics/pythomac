""" Extract data from a Telemac simulation that has already been running.
The codes are inspired by the following jupyter notebook:
    HOMETEL/notebooks/data_manip/extraction/output_file_extraction.ipynb
 which uses the following example case:
    /examples/telemac2d/bump/t2d_bump_FE.cas

@author: Sebastian Schwindt (July 2023)
"""

# retrieve file paths - this script must be stored in the directory where the simulation lives
import sys
import os
# data processing
import pandas as pd
import numpy as np
# plotting
import matplotlib
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
# Telemac stuff
from parser_output import get_latest_output_files
from parser_output import OutputFileData


def extract_fluxes(
        model_directory="",
        cas_name="steady2d.cas",
        plotting=True
):
    """This function writes a .csv file and an x-y plot of fluxes across the boundaries of a Telemac2d model. It auto-
        matically place the .csv and .png plot files into the simulation directory (i.e., where the .cas file is).

    Notes:
        * The Telemac simulation must have been running with the '-s' flag (``telemac2d.py my.cas -s``).
        * Make sure to activate the .cas keyword ``PRINTING CUMULATED FLOWRATES : YES``
        * This script skips volume errors (search tags are not implemented).
        * Read more about this script at
            https://hydro-informatics.com/numerics/telemac/telemac2d-steady.html#verify-steady-tm2d

    :param str model_directory: the file directory where the simulation lives
    :param str cas_name: name of the .cas steering file (without directory)
    :param bool plotting: default (True) will place a figure called flux-convergence.png in the simulation directory
    :return pandas.DataFrame: time series of fluxes across boundaries (if Error int: -1)
    """

    # assign cas file name in the folder
    file_name = get_latest_output_files(
        os.path.join(model_directory,  # os.path.dirname(os.path.realpath(__file__))
                     cas_name
                     )
        )

    # go to working directory
    try:
        os.chdir(model_directory)
    except Exception as problem:
        print("ERROR: the provided directory {0} does not exist:\n{1}".format(str(model_directory), str(problem)))
        return -1

    try:
        out_file = OutputFileData(file_name[0])
    except Exception as e:
        print("CAS name: " + str(os.path.join(os.path.dirname(os.path.realpath(__file__)), cas_name)))
        print("ERROR in file {0}:\n{1}".format(str(file_name), str(e)))
        print("Recall: the simulation must run with the -s flags")
        return -1

    print("Found study with name: {}".format(out_file.get_name_of_study()))
    print("The simulation took: {} seconds".format(out_file.get_exec_time()))

    # extract total volume, fluxes, and volume error
    out_fluxes = out_file.get_value_history_output("voltotal;volfluxes;volerror")
    out_fluxes_dict = {}
    for e in out_fluxes:
        try:
            # differentiate between Time and Flux series with nested lists
            if not isinstance(e[0], tuple):
                out_fluxes_dict.update({e[0]: np.array(e[1])})
            else:
                for sub_e in e:
                    try:
                        if "volume" in str(sub_e[0]).lower():
                            # go here if ('Volumes (m3/s)', [volume(t)])
                            out_fluxes_dict.update({sub_e[0]: np.array(sub_e[1])})
                        if "fluxes" in str(sub_e[0]).lower():
                            for bound_i, bound_e in enumerate(sub_e[1]):
                                out_fluxes_dict.update({
                                    "Fluxes {}".format(str(bound_e)): np.array(sub_e[2][bound_i])
                                })
                    except Exception as problem:
                        print("ERROR in intended VOLUME tuple " + str(sub_e[0]) + ":\n" + str(problem))
        except Exception as problem:
            print("ERROR in " + str(e[0]) + ":\n" + str(problem))
            print("WARNING: Flux series seem empty. Verify:")
            print("         - did you run telemac2d.py sim.cas with the -s flag?")
            print("         - did your define all required VARIABLES FOR GRAPHIC PRINTOUTS (U,V,S,B,Q,F,H)?")

    try:
        df = pd.DataFrame.from_dict(out_fluxes_dict)
        df.set_index(list(df)[0], inplace=True)
    except Exception as problem:
        print("ERROR: could not convert dict to DataFrame because:\n" + str(problem))
        return -1

    export_fn = "extracted_fluxes.csv"
    print("* Exporting to {}".format(str(os.path.join(model_directory, export_fn))))
    df.to_csv(os.path.join(model_directory, export_fn))

    if plotting:
        font = {'size': 9}
        matplotlib.rc('font', **font)
        fig = plt.figure(figsize=(6, 3), dpi=400)
        axes = fig.add_subplot()
        colors = plt.cm.Blues(np.linspace(0, 1, len(df.columns)))
        markers = ("x", "o", "s", "+", "1", "D", "*", "CARETDOWN", "3", "^", "p", "2")
        for i, y in enumerate(list(df)):
            if "flux" in str(y).lower():
                axes.plot(df.index.values, df[y].abs(), color=colors[i], markersize=2, marker=markers[i], markerfacecolor='none',
                          markeredgecolor=colors[i], linestyle='-', linewidth=1.0, alpha=0.6, label=y)
        axes.set_xlim((np.nanmin(df.index.values), np.nanmax(df.index.values)))
        axes.set_ylim(bottom=0)
        axes.set_xlabel("Time (s)")
        axes.set_ylabel("Fluxes (m$^3$/s)")
        axes.legend(loc="best", facecolor="white", edgecolor="gray", framealpha=0.5)
        fig.tight_layout()
        fig.savefig(os.path.join(model_directory, "flux-convergence.png"))
        print("* Saved plot as " + str(os.path.join(model_directory, "flux-convergence.png")))
    return df
