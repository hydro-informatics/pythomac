"""
Usage example for a Telemac simulation that lives in a neighbor directory of where this python scripts lives:

+ Simulation: HOME/hytelemac/steady2d-tutorial/steady2d.cas
+ This script: HOME/postpro/example.py

The simulation ran with ``telemac2d.py steady2d.cas -s`` and the .cas file contained the keyword
    ``PRINTING CUMULATED FLOWRATES : YES``.
"""
import os
from pathlib import Path
from pythomac import extract_fluxes
import numpy as np

# set directories and define steering (cas) file name
simulation_dir = str(Path(__file__).parents[1]) + "{0}hytelemac{0}steady2d-tutorial".format(os.sep)
telemac_cas = "steady2d.cas"
print(simulation_dir)

# extract fluxes across boundaries
fluxes_df = extract_fluxes(
    model_directory=simulation_dir,
    cas_name=telemac_cas,
    plotting=True
)


# estimate convergence
def approx_convergence(series_1, series_2):
    """ Approximate convergence according to
            https://hydro-informatics.com/numerics/telemac/telemac2d-steady.html#verify-steady-tm2d

    :param list or np.array series_1: series_1 should converge toward series_2 (both must have the same length)
    :param list or np.array series_2: series_2 should converge toward series_1 (both must have the same length)
    :return: (convergence_rate i, convergence constant c)
    """
    epsilon = np.array(abs(series_1 - series_2))

    i_series = 1

    x = np.arange(len(epsilon) - 1)
    y = np.log(np.abs(np.diff(np.log(epsilon))))
    line = np.polyfit(x, y, 1)  # fit degree 1 polynomial
    iota = np.exp(line[0])  # find q
    c_eps = epsilon[-1] / epsilon[-2] ^ iota

    return iota, c_eps

