# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 14:13:18 2025

Complex Acoustic Environment (CAE) modeling.
Frank McQuarrie, Skidaway Institute of Oceanography

Purpose:
    Automate the running and saving of propagation modeling for a set of variables.
    Uses Latin Hypercube Sampling (LHS) to randomly sample parameter space,
    but can be adapted to use static variables.

Scripts:
    CAE_automate:     This script. Performs multiple simulation runs and saves outputs.
    CAE_singleExperiment: Run and save a single specific model.
    CAE_createEnv:    Builds an environment for Bellhop acoustic modeling.
    CAE_ssp:          Sets a sound speed profile (SSP).
    CAE_surfaceLevels:Defines surface wave conditions.
    CAE_rayTracing:   Traces/plots acoustic ray paths.
    CAE_arrivals:     Calculates signal strength, arrival times, and detectability.

@author: fmm17241
"""

import os
import csv
import datetime
import pandas as pd
import numpy as np
import random
from pyDOE2 import lhs  # For Latin Hypercube Sampling

# Import simulation routines.
from CAE_createEnv import createEnv
from CAE_arrivals import calculateArrivals
# from CAE_rayTracing import rayTracing  # Optional

# -------------- MODEL LOGISTICS -----------------
n_iterations = 9  # Number of model iterations (simulations) to run

# File paths for output CSVs (edit these to your own desired paths)
output_file = r"C:\...*\modelOutputs.csv"
output_file2 = r"C:\...*\binnedAmplitudesNew.csv"
output_dir = os.path.dirname(output_file)
output_dir2 = os.path.dirname(output_file2)

# Ensure output directories exist
os.makedirs(output_dir, exist_ok=True)
os.makedirs(output_dir2, exist_ok=True)

# Output file column headers:
# Timestamp            - Time simulation was run.
# Scenario             - Bathymetry scenario, see CAE_bathymetry.
# topDescrip           - Surface condition, see CAE_surfaceLevels.
# SBL                  - Surface Bubble Loss (dB).
# deltaSS              - Sound speed stratification strength.
# gradient_depth       - Depth of stratification change.
# Detection_Threshold  - Background noise (dB).
# Bottom_Absorption    - Absorption at the seafloor (dB/lambda).
# Detectable           - # of pathways arriving above threshold.
# Undetectable         - # below threshold.
# Avg_Signal_dB        - Mean arriving signal strength.
#
# For more info, see README.md

# ----------------- MODEL AUTOMATION -----------------
# Example structure for batch simulation
for run in range(n_iterations):
    # Example: Set up random parameters using LHS or another approach
    # Replace this block as desired for your experiment
    # Example static: scenario = "STSNew1toFS17Real"
    # Example random: scenario = random.choice(["STSNew1toFS17Real", ...])
    scenario = "STSNew1toFS17Real"  # Placeholder

    # Build environment for this run
    # (Pass parameters as needed for your experiment)
    env, topDescrip, sspDescrip, botDescrip, bottom, soundspeed, signalRange, 
        SBL, tx_depth, rx_depth, detectionThreshold = createEnv(
            surface_type = "flat_surface",
            scenario = scenario,
            ssp_type = "exampleStrat5",
            SBL = 10,
            detectionThreshold = 50,
            nBeams = 1000,
            bottom_density = 1600,
            bottom_absorption= 5.0,
            deltaSS = 4,
            gradient_depth = 6
        )
    
    # Optional: Trace rays (visualization)
    # rayTracing(signalRange, topDescrip, botDescrip, sspDescrip, env)

    # Calculate arrivals and analyze detectability
    calculateArrivals(topDescrip, botDescrip, sspDescrip, env, detectionThreshold, SBL)
    # Save outputs as needed (handled in calculateArrivals or here)

# See EXAMPLE_USAGE.md for batch processing tips.
