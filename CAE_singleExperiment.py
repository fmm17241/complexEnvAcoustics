# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 15:52:12 2025
Complex Acoustic Environment (CAE) modeling.
Frank McQuarrie, Skidaway Institute of Oceanography

Purpose of script: Runs a single experiment and saves the propagation modeling.

Scripts.
CAE_automate : current. Runs and saves outputs from propagation modeling.
****CAE_singleExperiment: Run and save a specific model.

CAE_createEnv: Creates an environment for Bellhop to model sound through.
CAE_ssp: Sets a soundspeed profile. Currently set to create one given stratification strength and depth.
CAE_surfaceLevels: defines surface waves for the environment.

CAE_rayTracing: Traces (and can plot) sound pathways through the environment.
CAE_arrivals: Measures signal strength and arrival timing for sound through the environment. Also adds initial power, and given a detection threshold, can define a ray as detectable or not.
@author: fmm17241
"""
import os
# Script location
os.chdir(r"C:\*")
import arlpy.uwapm as pm
import numpy as np
from importlib import reload
import matplotlib.pyplot as plt
import CAE_createEnv
import CAE_bathymetry 
import CAE_surfaceLevels
import CAE_ssp
import CAE_rayTracing
import CAE_arrivals
reload(CAE_createEnv)
reload(CAE_bathymetry)
reload(CAE_ssp)
reload(CAE_surfaceLevels)
reload(CAE_rayTracing)
reload(CAE_arrivals)
from CAE_createEnv import createEnv
from CAE_rayTracing import rayTracing
from CAE_arrivals import calculateArrivals

# Output Directory
output_dir = r"C:\Users\fmm17241\OneDrive - University of Georgia\data\Chapter5Scenarios\scenarioData"


# CREATING THE ENVIRONMENT TO WORK IN
# Creates the environment for ray tracing.
env, topDescrip, sspDescrip, botDescrip, bottom, soundspeed, signalRange, \
    SBL, tx_depth, rx_depth, detectionThreshold \
        = createEnv(
                surface_type = "flat_surface",  # Sets surface, defined in "CAE_surfaceLevels"
                scenario = "STSNew1toFS17Real", # Sets the scenario, defined below and in "CAE_bathymetry"
                ssp_type = "exampleStrat5",     # Sets soundspeed profile (m/s), defined in "CAE_ssp"
                SBL = 10,                       # Surface Bubble Loss (dB), set by UWAPL. See McQuarrie et al, 2025
                detectionThreshold = 50,        # Represents background noise, used in "CAE_arrivals" to test detectability.  
                nBeams = 100,                   # Number of beams modeled. 1000 was average to ensure coverage.
                bottom_density = 1600,          # g/cm^3, between 1500 for sandy, 2500 for structured.
                bottom_absorption= 5.0,         # dB/lambda, loss per wavelength.
                deltaSS = 4,                    # Strength of sound speed stratification (m/s). Used in "CAE_ssp"
                gradient_depth = 6              # Depth of sound speed stratification (m/s). Used in "CAE_ssp"
                )
#pm.plot_env(env) # Optional plotting of the environment.
pm.print_env(env)
##

# Define depth values (make sure this matches the number of rows in soundspeed), and is defined above sea surface (0 m).
plotDepth = np.arange(-2, 23, 2)  # Produces depths: -2, 0, 2, ... 22

# Use all columns so that the first SSP column ("0") is included
range_cols = soundspeed.columns[:]  
ranges = np.array([float(col) for col in range_cols])

# Extract the speed data from all columns
speed_data = soundspeed.values

###############################
# MODELING RAYS THROUGH THE ENVIRONMENT
# Range sets distance to trace and monitor.
# env is built using BDA_createEnv's "createEnv" function.
#sumBDA, bdaDataFrame,percentageRays,rays,rays_per_distance, filtered_rays = rayTracing(signalRange,
rayTracing(signalRange,
            topDescrip,
            botDescrip,
            sspDescrip,
            env=env)

# Plot each ray. Optional
#plt.figure(figsize=(10, 5))
#for ray in filtered_rays:
#    ray = np.array(ray)
#    plt.plot(ray[:, 0], ray[:, 1], 'k')  # range (x) vs depth (y)

# Flip Y axis for depth
#plt.gca().invert_yaxis()

#plt.title("Non-Bottom-Bounce Rays")
#plt.xlabel("Range (m)")
#plt.ylabel("Depth (m)")
#plt.grid(True)
#plt.tight_layout()
#plt.show()

###############################
# CALCULATING ARRIVAL TIMING AND AMPLITUDE
#env is built using CAE_createEnv's "createEnv" function.
arrivals, binned_countsLow, low_power_dB_hist, confidence_interval, \
    X_detectable, Y_undetectable,avg_low_dB, ci_lower_lp,\
        ci_upper_lp, nonBottom_Arrivals  = calculateArrivals(topDescrip,
                                                                            botDescrip,
                                                                            sspDescrip,
                                                                            env,
                                                                            detectionThreshold, 
                                                                            SBL)

##########

plt.scatter(arrivals['bottom_bounces'], arrivals['amplitude_db'])
plt.xlabel("Bottom Bounces")
plt.ylabel("Signal Strength (dB)")
plt.axhline(y=detectionThreshold, color='r', linestyle='--', label="Detection Threshold")
plt.title("Arrival Strength vs. Bottom Bounces")
plt.legend()
plt.show()



