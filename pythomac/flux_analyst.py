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

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
# Telemac stuff
from parser_output import get_latest_output_files
from parser_output import OutputFileData
# plot utils
from utils.plots import plot_df


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
                            if not(len(np.array(sub_e[1])) < 2):
                                out_fluxes_dict.update({sub_e[0]: np.array(sub_e[1])})
                            else:
                                print("WARNING: there is an issue with the simulation: volumes cannot be read.")
                        if "flux" in str(sub_e[0]).lower():
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
        plot_df(
            df=df,
            file_name=str(os.path.join(model_directory, "flux-convergence.png")),
            x_label="Timesteps",
            y_label="Fluxes (m$^3$/s)",
            column_keyword="flux"
        )
    return df


def calculate_convergence(series_1, series_2, conv_constant=1., cas_timestep=1, plot_dir=None):
    """ Approximate convergence according to
            https://hydro-informatics.com/numerics/telemac/convergence.html#tm-calculate-convergence

    :param list or np.array series_1: series_1 should converge toward series_2 (both must have the same length)
    :param list or np.array series_2: series_2 should converge toward series_1 (both must have the same length)
    :param float conv_constant: a convergence constant to reach (default is 1.0)
    :param int cas_timestep: the timestep defined in the cas file
    :param str plot_dir: if a directory is provided, a convergence plot will be saved here
    :return pandas.DataFrame: with one column, notably the convergence_rate iota as np.array
    """
    # calculate the error epsilon between two series
    epsilon = np.array(abs(series_1 - series_2))
    # derive epsilon at t and t+1
    epsilon_t0 = epsilon[:-1]  # cut off last element
    epsilon_t1 = epsilon[1:]  # cut off element zero
    # calculate convergence
    iota = np.emath.logn(epsilon_t0, epsilon_t1) / conv_constant

    iota_df = pd.DataFrame({"Convergence rate": iota})
    iota_df.set_index(iota_df.index.values * cas_timestep, inplace=True)

    if plot_dir:
        plot_df(
            df=iota_df,
            file_name=str(os.path.join(plot_dir, "convergence-rate.png")),
            x_label="Timesteps",
            y_label="Convergence rate $\iota$ (-)",
            column_keyword="rate",
            legend=False
        )

    return iota_df


def get_convergence_time(convergence_rate, convergence_precision=1.0E-4):
    """
    Calculate at which simulation time the simulation converged at a desired level of
        convergence precision

    :param numpy.array convergence_rate: iota calculated with calculate_convergence
    :param float convergence_precision: define the desired level of convergence precision
    :return numpy.int64: the time iteration number
    """

    convergence_diff = np.diff(convergence_rate)
    idx = np.flatnonzero(abs(convergence_diff) > convergence_precision)[-1] + 1

    if idx < len(convergence_rate) - 1:
        return idx
    else:
        print("WARNING: the desired convergence precision was never reached.")
        return np.nan



