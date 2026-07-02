""" Extract data from a Telemac simulation that has already been running.

The codes are inspired by the following jupyter notebook::

    HOMETEL/notebooks/data_manip/extraction/output_file_extraction.ipynb

which uses the following example case::

    /examples/telemac2d/bump/t2d_bump_FE.cas

@author: Sebastian Schwindt (July 2023; updates: May and July 2026)
"""

import os

import numpy as np
import pandas as pd

from pythomac.parser_output import OutputFileData, get_latest_output_files
from pythomac.utils.plots import plot_df


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
            https://hydro-informatics.com/telemac2d-steady/#verify-steady-tm2d

    :param str model_directory: the file directory where the simulation lives
    :param str cas_name: name of the .cas steering file (without directory)
    :param bool plotting: default (True) will place a figure called flux-convergence.png in the simulation directory
    :return pandas.DataFrame: time series of fluxes across boundaries (if Error int: -1)
    """

    if not os.path.isdir(model_directory or "."):
        print(f"ERROR: the provided directory {model_directory} does not exist")
        return -1

    # locate the newest main .sortie listing next to the cas file (absolute paths;
    # the working directory of the calling process is never changed)
    file_name = get_latest_output_files(os.path.join(model_directory, cas_name))

    try:
        out_file = OutputFileData(file_name[0])
    except Exception as e:
        print(f"CAS name: {os.path.join(model_directory, cas_name)}")
        print(f"ERROR in file {file_name}:\n{e}")
        print("Recall: the simulation must run with the -s flag")
        return -1

    print(f"Found study with name: {out_file.get_name_of_study()}")
    print(f"The simulation took: {out_file.get_exec_time()} seconds")

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
                                    f"Fluxes {bound_e}": np.array(sub_e[2][bound_i])
                                })
                    except Exception as problem:
                        print(f"ERROR in intended VOLUME tuple {sub_e[0]}:\n{problem}")
        except Exception as problem:
            print(f"ERROR in {e[0]}:\n{problem}")
            print("WARNING: Flux series seem empty. Verify:")
            print("         - did you run telemac2d.py sim.cas with the -s flag?")
            print("         - did your define all required VARIABLES FOR GRAPHIC PRINTOUTS (U,V,S,B,Q,F,H)?")

    try:
        df = pd.DataFrame.from_dict(out_fluxes_dict)
        df.set_index(list(df)[0], inplace=True)
    except Exception as problem:
        print(f"ERROR: could not convert dict to DataFrame because:\n{problem}")
        return -1

    export_fn = "extracted-fluxes.csv"
    print(f"* Exporting to {os.path.join(model_directory, export_fn)}")
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
            https://hydro-informatics.com/convergence/#tm-calculate-convergence

    :param list or np.array series_1: inflow flux series Q_in; the relative imbalance is normalized by this series, which should converge toward series_2 (both must have the same length)
    :param list or np.array series_2: outflow flux series Q_out; should converge toward series_1 (both must have the same length)
    :param float conv_constant: a convergence constant to reach (default is 1.0)
    :param int cas_timestep: the timestep defined in the cas file
    :param str plot_dir: if a directory is provided, a convergence plot will be saved here
    :return pandas.DataFrame: columns "Relative imbalance" (Delta_{Q,t}) and "Convergence rate" (iota), indexed by timestep
    """
    # relative flux imbalance Delta_{Q,t} = ||Q_in| - |Q_out|| / |Q_in|, normalized by the
    #   inflow (series_1) so that the imbalance is dimensionless; cf. the mass-flux-error
    #   equation in the numerics script. Telemac reports boundary fluxes signed (inflow
    #   positive, outflow negative), so the discharge magnitudes |.| are differenced here:
    #   balance means |Q_in| == |Q_out|, hence Delta_{Q,t} -> 0 at steady state. Taking the
    #   magnitudes also keeps the metric robust to momentary reverse flow at a boundary.
    q_in = np.abs(np.array(series_1))
    q_out = np.abs(np.array(series_2))
    epsilon = np.abs(q_in - q_out) / q_in
    # derive epsilon at t and t+1
    epsilon_t0 = epsilon[:-1]  # cut off last element
    epsilon_t1 = epsilon[1:]  # cut off element zero
    # convergence rate iota = log with base Delta_{Q,t} of Delta_{Q,t+1}
    iota = np.emath.logn(epsilon_t0, epsilon_t1) / conv_constant

    # keep the relative imbalance alongside the rate: Delta_{Q,t+1} pairs with iota(t)
    iota_df = pd.DataFrame({
        "Relative imbalance": epsilon_t1,
        "Convergence rate": iota,
    })
    iota_df.set_index(iota_df.index.values * cas_timestep, inplace=True)

    if plot_dir:
        plot_df(
            df=iota_df,
            file_name=str(os.path.join(plot_dir, "convergence-rate.png")),
            x_label="Timesteps",
            y_label=r"Convergence rate $c_{\iota(t)}$",
            column_keyword="rate",
            legend=False,
            tight_ylim=True,
            hline=1.0
        )

    return iota_df


def get_convergence_time(relative_imbalance, convergence_precision=1.0E-4):
    """
    Identify the optimum simulation length as the smallest output interval index beyond
        which the relative flux imbalance Delta_{Q,t} (see calculate_convergence) remains
        permanently below the target tolerance. This implements the optimum-simulation-
        length criterion described at https://hydro-informatics.com/convergence.

    :param numpy.array relative_imbalance: the Delta_{Q,t} series, e.g. the
        "Relative imbalance" column returned by calculate_convergence
    :param float convergence_precision: target tolerance Delta_{Q,tar}; 1e-4 is typically
        acceptable for preliminary runs, while 1e-6 or smaller is warranted for validation
        and hotstart initialization runs
    :return numpy.int64: the time iteration number, or np.nan if the tolerance is never reached
    """

    imbalance = np.real(np.asarray(relative_imbalance, dtype=float))
    below = imbalance < convergence_precision

    if not below.any() or not below[-1]:
        print("WARNING: the desired convergence precision was never reached.")
        return np.nan

    # smallest index beyond which the imbalance stays permanently below the tolerance
    not_below = np.flatnonzero(~below)
    return int(not_below[-1] + 1) if not_below.size else 0
