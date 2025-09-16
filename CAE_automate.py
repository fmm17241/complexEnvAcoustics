# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 14:13:18 2025
Complex Acoustic Environment (CAE) modeling.
Frank McQuarrie, Skidaway Institute of Oceanography

Purpose of script: automatically run and save the propagation modeling for a set range of variables. Currently this is set up to grab values semi-randomly using LHS, but can easily change to static values for experiments.

Scripts.
***CAE_automate : current. Runs and saves outputs from propagation modeling.
CAE_singleExperiment: Run and save a specific model.

CAE_createEnv: Creates an environment for Bellhop to model sound through.
CAE_ssp: Sets a soundspeed profile. Currently set to create one given stratification strength and depth.
CAE_surfaceLevels: defines surface waves for the environment.

CAE_rayTracing: Traces (and can plot) sound pathways through the environment.
CAE_arrivals: Measures signal strength and arrival timing for sound through the environment. Also adds initial power, and given a detection threshold, can define a ray as detectable or not.

@author: fmm17241
"""

##
# Load in packages, install if necessary.
import os
#Code Repository
os.chdir()
import csv
import datetime
import pandas as pd
# Import simulation routines.
from CAE_createEnv import createEnv
#from BDA_Rays2 import rayTracing
from CAE_arrivals import calculateArrivals
import numpy as np
import random
from pyDOE2 import lhs  # For Latin Hypercube Sampling


# Logistics of the model. How many times, where to put the outputs, etc.
n_iterations = 9  # Number of simulations

# File paths
output_file = r"C:\...*\modelOutputs.csv"
output_file2 = r"C:\...*\binnedAmplitudesNew.csv"
output_dir = os.path.dirname(output_file)
output_dir2 = os.path.dirname(output_file2)

# File creation if it doesnt exist. Each model run will be saved as a new line.
#
# Output Columns:
# Timestamp            - time the model was run. Can remove if not needed.
# Scenario             - User defined bathymetry in "CAE_createEnv" and "CAE_bathymetry"
# topDescrip           - User defined surface in "CAE_surfaceLevels"
# SBL                  - Surface Bubble Loss defined in UW-Applied Physics handbook, 0-15 dB. See McQuarrie et al 2025 for calculation description.
# deltaSS              - Set by "CAE_ssp". Strength of stratification. Can be static or set as semi-random range.
# gradient_depth       - Set by "CAE_ssp". Depth of stratifiation. Can be static or set as semi-random range.
# Detection_Threshold  - Represents background noise. Currently set as a range to represent seasonal/diurnal changes but can be adapted in static environments.
# Bottom_Absorption    - Bottom absorption in (dB/lambda), decibels per wavelength.
# Detectable           - Output, detectable pathways between transmitter and receiver; pathways that arrive above the detection threshold.
# Undetectable         - Output, undetectable pathways between transmitter and receiver; pathways that arrive at or below the detection threshold.
# Avg_Signal_dB        - Output, signal strength of the arriving rays in dB re 1 µPa. Note: this is calculated using the power set in "CAE_arrivals". Please ensure you set the transmitting strength as needed.
# 

# Ensures your path exists, and if not, creates the files with the headers below.
if not os.path.exists(output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = [
            "Timestamp", "Scenario", "topDescrip", "SBL", "deltaSS", "gradient_depth", "Detection_Threshold",
            "Bottom_Absorption", "Detectable", "Undetectable", "Avg_Signal_dB"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

if not os.path.exists(output_file2):
    bin_centers = list(range(0, 100, 10))
    meta_fields = ["Scenario", "deltaSS", "gradient_depth", "Surface_Type", "Detection_Threshold", "Bottom_Absorption"]
    bin_fields = [f"Bin_{center}" for center in bin_centers]
    with open(output_file2, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(meta_fields + bin_fields)

########################################################
# DATA FOR THE MODEL.
# Each model will semi-randomly grab one of these categories or a number in a continuous range.

# These options are fixed, categorical. This gives us bathymetry, range, and instrument depths, set in "CAE_createEnv".
scenarios = ["STSNew1toSURT20Flat", "STSNew1toSURT20Linear", "STSNew1toSURT20Real",
             "SURT20toSTSNew1Flat", "SURT20toSTSNew1Linear", "SURT20toSTSNew1Real",
             "STSNew1toFS17Flat", "STSNew1toFS17Linear", "STSNew1toFS17Real",
             "FS17toSTSNew1Flat", "FS17toSTSNew1Linear", "FS17toSTSNew1Real"]

#Picks surface type for this transceiver pairing. Appends them to the range set by scenario.
surface_types = ["flat_surface", "mid_waves", "rough_waves"]

# Define continuous variable ranges. These are realistic ranges set by literature for testing purposes, but can be changed to narrow/widen the range or change to static values.
param_bounds = {
    "bottom_absorption": (0, 5),    # dB/lambda, absorption per wavelength. This one has been odd, keep investigating.
    "SBL": (0, 15),                 # Surface bubble loss (dB), represents wind from calm to stormy. Capped at 15 dB by UWAPL.
    "detectionThreshold": (30, 75), # (dB) Threshold representing background noise, very quiet to deafening.
    "deltaSS": (0, 10),             # (m/s), Strength of stratification layer 
    "gradient_depth": (5, 12)       # (m) Depth of stratification layer
}

# Latin Hypercube Sampling
# LHS limits the clustering and gaps that occur when fully random.
# So LHS is NOT fully random, but instead tries to more efficiently explore variables. This helps test the model in a wide variety of environments.

# Run LHS to generate values in [0, 1]
lhs_samples = lhs(len(param_bounds), samples=n_iterations)

# Scale samples to real-world parameter ranges set above
param_names = list(param_bounds.keys())
scaled_samples = np.zeros_like(lhs_samples)
for i, param in enumerate(param_names):
    low, high = param_bounds[param]
    scaled_samples[:, i] = lhs_samples[:, i] * (high - low) + low

# LOOP: This goes through as many iterations as I request.
for i in range(n_iterations):

# Select my variables from the ranges of possibles.
    bottom_absorption = round(scaled_samples[i, 0], 2)
    SBL = round(scaled_samples[i, 1], 2)
    detectionThreshold = round(scaled_samples[i, 2], 1)
    deltaSS = round(scaled_samples[i, 3], 2)
    gradient_depth = round(scaled_samples[i, 4], 1)
    scenario = random.choice(scenarios)
    surface = random.choice(surface_types)

# Create the environment using the variables above.    
    try:
        print(">>> Creating environment...")
        env, topDescrip, sspDescrip, botDescrip, bottom, soundspeed, signalRange, \
           _, tx_depth, rx_depth, _ = createEnv(
               surface_type=surface,
               scenario=scenario,
               bottom_absorption=bottom_absorption,
               SBL=SBL,
               detectionThreshold=detectionThreshold,
               deltaSS=deltaSS,
               gradient_depth=gradient_depth
       )
    except Exception as e:
           print(f" SKIPPING simulation {i+1} (createEnv error): {e}")
           continue

#Plotting is helpful for testing but too much for 1000+ iterations. Enable this if you'd like.  
#    try:
#        print(">>> Computing rays...")
#        filtered_rays = rayTracing(signalRange, topDescrip, botDescrip, sspDescrip, env)
#    except Exception as e:
#        print(f" SKIPPING simulation {i+1} (rayTracing error): {e}")
#        continue

# Calculates arrivals. This will output how many arrivals there are between transmitter and receiver, how strong those arriving sounds are, and how many are detectable. 
    try:
        print(">>> Calculating arrivals...")
        arrivals, binned_countsLow, low_power_dB_hist, confidence_interval, \
        X_detectable, Y_undetectable, avg_low_dB, ci_lower_lp, ci_upper_lp, \
        nonBottomArrivals = calculateArrivals(
            topDescrip, botDescrip, sspDescrip, env,
            detectionThreshold, SBL
        )
    except Exception as e:
        print(f" SKIPPING simulation {i+1} (calculateArrivals error): {e}")
        continue

# Writing output files.    
    if isinstance(binned_countsLow, pd.Series):
        bin_centers = [(interval.left + interval.right) / 2 for interval in binned_countsLow.index]
        bin_labels = [f"Bin_{int(center)}" for center in bin_centers]
        row_data = {
            "Scenario": scenario,
            "deltaSS": deltaSS,
            "gradient_depth": gradient_depth,
            "Surface_Type": surface,
            "Detection_Threshold": detectionThreshold,
            "Bottom_Absorption": bottom_absorption
        }
        for label, count in zip(bin_labels, binned_countsLow.values):
            row_data[label] = int(count)
        with open(output_file2, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=row_data.keys())
            writer.writerow(row_data)

#    nonBottomRays = len(filtered_rays)
    metrics_dict = {
        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Scenario": scenario,
        "topDescrip": topDescrip,
        "SBL": SBL,
        "deltaSS": deltaSS,
        "gradient_depth": gradient_depth,
        "Detection_Threshold": detectionThreshold,
        "Bottom_Absorption": bottom_absorption,
        "Detectable": X_detectable,
        "Undetectable": Y_undetectable,
        "Avg_Signal_dB": f"{avg_low_dB:.1f}"
    }

    with open(output_file, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=metrics_dict.keys())
        writer.writerow(metrics_dict)

    print(f" COMPLETED simulation {i+1}/{n_iterations}")
.