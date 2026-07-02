"""pythomac test suite.

Covers the ``.sortie`` parser (both boundary-count formats TELEMAC emits), the
flux extraction into the CSV/plot artifacts, the convergence maths, and the
optimum-simulation-length detection. The end-to-end test runs on the shipped
``example-simulation`` listing (a real TELEMAC v8 steady2d run); the TELEMAC v9
format (``NUMBER OF LIQUID BOUNDARIES:`` with a colon) is exercised with a
synthetic listing.

Run via: pytest tests/
"""

import shutil
from pathlib import Path

import numpy as np
import pytest

from pythomac import (calculate_convergence, extract_fluxes,
                      get_convergence_time)
from pythomac.parser_output import OutputFileData

REPO = Path(__file__).resolve().parents[1]
EXAMPLE = REPO / "example-simulation"
EXAMPLE_SORTIE = "steady2d.cas_2024-12-06-12h52min49s.sortie"


@pytest.fixture()
def example_dir(tmp_path):
    """The example simulation copied to a scratch folder (extract_fluxes writes
    its CSV/plot next to the cas file)."""
    shutil.copy(EXAMPLE / "steady2d.cas", tmp_path / "steady2d.cas")
    shutil.copy(EXAMPLE / EXAMPLE_SORTIE, tmp_path / EXAMPLE_SORTIE)
    return tmp_path


def test_extract_fluxes_end_to_end(example_dir):
    df = extract_fluxes(model_directory=str(example_dir), cas_name="steady2d.cas",
                        plotting=True)
    assert not isinstance(df, int), "extract_fluxes returned an error code"
    flux_cols = [c for c in df.columns if "flux" in str(c).lower()]
    assert flux_cols == ["Fluxes Boundary 1", "Fluxes Boundary 2"]
    # the example run drives ~50 m3/s: both boundaries must carry non-zero fluxes
    assert np.abs(df[flux_cols].to_numpy(dtype=float)).max() > 10.0
    assert (example_dir / "extracted-fluxes.csv").exists()
    assert (example_dir / "flux-convergence.png").stat().st_size > 0
    # the caller's working directory is not changed by extract_fluxes
    assert Path.cwd() != example_dir


def test_extract_fluxes_missing_directory():
    assert extract_fluxes(model_directory="/nonexistent-dir", cas_name="x.cas") == -1


_V9_SORTIE = """\
 LISTING OF TELEMAC2D
 NUMBER OF LIQUID BOUNDARIES:           2

 ITERATION      100    TIME:     10.0000 S
                       BALANCE OF WATER VOLUME
     VOLUME IN THE DOMAIN :    100.0000     M3
     FLUX BOUNDARY    1:    -1.500000     M3/S  ( >0 : ENTERING  <0 : EXITING )
     FLUX BOUNDARY    2:     2.000000     M3/S  ( >0 : ENTERING  <0 : EXITING )
     RELATIVE ERROR IN VOLUME AT T =        10.00     S :    0.1000000E-14

 ITERATION      200    TIME:     20.0000 S
                       BALANCE OF WATER VOLUME
     VOLUME IN THE DOMAIN :    105.0000     M3
     FLUX BOUNDARY    1:    -1.999000     M3/S  ( >0 : ENTERING  <0 : EXITING )
     FLUX BOUNDARY    2:     2.000000     M3/S  ( >0 : ENTERING  <0 : EXITING )
     RELATIVE ERROR IN VOLUME AT T =        20.00     S :    0.1000000E-14

  INITIAL VOLUME :    90.00000     M3
"""


def test_parser_reads_v9_boundary_count(tmp_path):
    """TELEMAC v9 prints 'NUMBER OF LIQUID BOUNDARIES:' with a colon; the parser
    must detect the count (v2.0.0 found 0 boundaries and extracted no fluxes)."""
    sortie = tmp_path / "case.cas_2026-01-01-00h00min00s.sortie"
    sortie.write_text(_V9_SORTIE)
    _, fluxes, _ = OutputFileData(str(sortie)).get_volume_profile()
    _, bound_names, series = fluxes
    assert bound_names == ["Boundary 1", "Boundary 2"]
    # leading 0.0 is the assumed initial flux; then the two parsed printouts
    assert series[0] == [0.0, -1.5, -1.999]
    assert series[1] == [0.0, 2.0, 2.0]


def test_calculate_convergence_columns_and_index():
    q_in = np.full(6, 2.0)
    q_out = -q_in * (1.0 - 10.0 ** -np.arange(1.0, 7.0))   # imbalance decays 1e-1..1e-6
    df = calculate_convergence(q_in, q_out, cas_timestep=50)
    assert list(df.columns) == ["Relative imbalance", "Convergence rate"]
    assert df.index[1] - df.index[0] == 50                  # index in simulation seconds
    imbalance = df["Relative imbalance"].to_numpy(dtype=float)
    assert np.allclose(imbalance, 10.0 ** -np.arange(2.0, 7.0))


def test_get_convergence_time_permanent_crossing():
    # dips below the tolerance once (index 2) before converging for good at index 5
    imbalance = np.array([1e-1, 1e-2, 1e-5, 1e-3, 1e-2, 1e-5, 1e-6, 1e-7])
    assert get_convergence_time(imbalance, convergence_precision=1e-4) == 5


def test_get_convergence_time_never_reached():
    assert np.isnan(get_convergence_time(np.full(10, 1e-2),
                                         convergence_precision=1e-6))
