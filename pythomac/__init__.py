import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

try:
    from extract_fluxes import extract_fluxes
except ModuleNotFoundError:
    print("Failed to initialize Pythomac - consider re-installation")
