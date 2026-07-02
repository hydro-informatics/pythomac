"""pythomac - lightweight post-processing for TELEMAC simulations.

Extracts the volume/flux printouts from a TELEMAC ``.sortie`` listing, quantifies
boundary-flux convergence of steady runs, and identifies the optimum simulation
length. Runs outside the TELEMAC Python environment (numpy/pandas/matplotlib only).

Public API::

    from pythomac import extract_fluxes, calculate_convergence, get_convergence_time
"""

from pythomac.flux_analyst import (calculate_convergence, extract_fluxes,
                                   get_convergence_time)
from pythomac.parser_output import OutputFileData, get_latest_output_files

__version__ = "3.0.0"

__all__ = [
    "extract_fluxes",
    "calculate_convergence",
    "get_convergence_time",
    "OutputFileData",
    "get_latest_output_files",
    "__version__",
]
