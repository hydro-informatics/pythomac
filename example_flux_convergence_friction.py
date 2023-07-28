"""
This script is a copy of *example_flux_convergence.py*, but for the analysis of unsteady
   flux evolution through inflow and outflow boundaries

@author: Sebastian Schwindt
@year: 2023

Example:
    Visit https://hydro-informatics.com/numerics/telemac/convergence.html

"""
import os
from pathlib import Path
from pythomac import extract_fluxes, calculate_convergence, get_convergence_time

# set directories and define steering (cas) file name
simulation_dir = str(Path(__file__).parents[1]) + "{0}hytelemac{0}friction".format(os.sep)
telemac_cas = "steady2d-zonal-ks.cas"
print(simulation_dir)

# extract fluxes across boundaries
fluxes_df = extract_fluxes(
    model_directory=simulation_dir,
    cas_name=telemac_cas,
    plotting=True
)

# back-calculate Telemac timestep size
timestep_in_cas = int(max(fluxes_df.index.values) / (len(fluxes_df.index.values) - 1))


# plot convergence
iota_t = calculate_convergence(
    series_1=fluxes_df["Fluxes Boundary 1"][1:],  # remove first zero-entry
    series_2=fluxes_df["Fluxes Boundary 2"][1:],  # remove first zero-entry
    cas_timestep=timestep_in_cas,
    plot_dir=simulation_dir
)

# write the result to a CSV file
iota_t.to_csv(os.path.join(simulation_dir, "convergence-rate.csv"))

# identify the timestep at which convergence was reached at a desired precision
convergence_time_iteration = get_convergence_time(
    convergence_rate=iota_t["Convergence rate"],
    convergence_precision=1.0E-6
)

if not("nan" in str(convergence_time_iteration).lower()):
    print("The simulation converged after {0} simulation seconds ({1}th printout).".format(
        str(timestep_in_cas * convergence_time_iteration), str(convergence_time_iteration)))
