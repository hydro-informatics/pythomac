import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

try:
    from flux_analyst import extract_fluxes, calculate_convergence, get_convergence_time
except ModuleNotFoundError:
    print("Failed to initialize Pythomac - consider re-installation")
