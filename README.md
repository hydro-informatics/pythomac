# pythomac

[![PyPI](https://img.shields.io/pypi/v/pythomac)](https://pypi.org/project/pythomac/)
[![Docs](https://readthedocs.org/projects/pythomac/badge/?version=latest)](https://pythomac.readthedocs.io)

Lightweight post-processing for [TELEMAC](http://www.opentelemac.org/) simulations:
extract the volume and boundary-flux printouts from a `.sortie` listing, quantify
the boundary-flux convergence of steady runs, and identify the optimum simulation
length - all outside the TELEMAC Python environment (only `numpy`, `pandas`, and
`matplotlib` are required).

## Installation

```bash
pip install pythomac
```

Requires Python >= 3.9. The analyzed simulation must have run with the `-s` flag
(`telemac2d.py steady2d.cas -s`) and the steering file must contain
`PRINTING CUMULATED FLOWRATES : YES`.

## Quickstart

```python
from pythomac import extract_fluxes, calculate_convergence, get_convergence_time

fluxes_df = extract_fluxes(model_directory="/path/to/simulation",
                           cas_name="steady2d.cas", plotting=True)
iota_t = calculate_convergence(fluxes_df["Fluxes Boundary 1"][1:],
                               fluxes_df["Fluxes Boundary 2"][1:],
                               cas_timestep=50, plot_dir="/path/to/simulation")
idx = get_convergence_time(iota_t["Relative imbalance"], convergence_precision=1e-4)
```

This writes `extracted-fluxes.csv` + `flux-convergence.png` (the per-boundary
fluxes) and `convergence-rate.png` (the relative flux imbalance and its
convergence rate) into the simulation directory, and returns the printout index
from which the imbalance stays permanently below the tolerance. A worked example
lives in `example_flux_convergence.py` (with `example-simulation/`).

Read the full tutorial at <https://hydro-informatics.com/numerics/telemac/convergence.html>
and the API documentation at <https://pythomac.readthedocs.io>.

## Changelog

**3.0.0**
- Proper package structure: absolute in-package imports; the `sys.path`
  manipulation at import time and the `os.chdir` side effect in
  `extract_fluxes()` are gone (the caller's working directory is never touched).
- Parses the TELEMAC v9 listing format (`NUMBER OF LIQUID BOUNDARIES:` with a
  colon), which previously yielded an empty flux table.
- Runtime dependencies are declared in `pyproject.toml` with modern floors
  (`numpy>=1.24`, `pandas>=2.0`, `matplotlib>=3.7`); Python >= 3.9.
- Test suite (`pytest`) and GitHub workflows for CI and PyPI publishing
  (Trusted Publishing).
- Breaking: `from parser_output import ...` / `from utils... import ...` no
  longer work from copied folders - use the package imports
  (`from pythomac import ...`); Python 3.7/3.8 are no longer supported.

**2.0.0** - convergence-formula correction; `calculate_convergence` returns the
relative imbalance alongside the rate; convergence plot improvements.

## License

GPL-3.0 - see `LICENSE`. Parts of `pythomac/parser_output.py` and
`pythomac/utils/` are adapted from the TELEMAC-MASCARET scripts (GPL v3).
