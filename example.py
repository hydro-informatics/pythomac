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

simulation_dir = str(Path(__file__).parents[1]) + "{0}hytelemac{0}steady2d-tutorial".format(os.sep)
telemac_cas = "steady2d.cas"

print(simulation_dir)

extract_fluxes(
    model_directory=simulation_dir,
    cas_name=telemac_cas,
    plotting=True
)
