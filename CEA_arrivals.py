# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 12:12:24 2025
Complex Environmental Acoustics (CEA) modeling.
Frank McQuarrie, Skidaway Institute of Oceanography

Purpose of script: Calculates and plots the strength of arrivals that get to the receiver.

Scripts.
CEA_automate : current. Runs and saves outputs from propagation modeling.
CEA_singleExperiment: Run and save a specific model.

CEA_createEnv: Creates an environment for Bellhop to model sound through.
CEA_ssp: Sets a soundspeed profile. Currently set to create one given stratification strength and depth.
CEA_surfaceLevels: defines surface waves for the environment.

CEA_rayTracing: Traces (and can plot) sound pathways through the environment.
******CEA_arrivals: Measures signal strength and arrival timing for sound through the environment. Also adds initial power, and given a detection threshold, can define a ray as detectable or not.
@author: fmm17241
"""
import arlpy.uwapm as pm
import numpy as np
import pandas as pd
import scipy.stats as st
import os

# Calculates the number of arrivals, sets their strength, and defines them as detectable or undetectable.
def calculateArrivals(topDescrip, botDescrip, sspDescrip, env, detectionThreshold, SBL):
# Set output directory
    base_dir = r"path"

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
     #Bellhop's location. You need to have previously run the AT makefile to create executables.
    os.chdir(r"path\executables")   

    # Computes the arrival time of rays between instruments.
    arrivals = pm.compute_arrivals(env)
    #Optional: plot the arrivals
#    pm.plot_arrivals(arrivals, width=500, dB=True, title=f"Arrivals: 69 kHz,{topDescrip}, {botDescrip}, {sspDescrip}")

# Table of arrivals, and converts complex number to decibels.
    arrivals[['time_of_arrival', 'angle_of_arrival', 'surface_bounces', 'bottom_bounces']]
    arrivals['amplitude_magnitude'] = arrivals['arrival_amplitude'].apply(lambda x: abs(complex(x)))
    arrivals['arrival_dB'] = 20 * np.log10(arrivals['amplitude_magnitude'])
# Compute mean arrival amplitude
#    arrivalAmplitude = np.mean(arrivals['arrival_amplitude'])

# VR2Tx powers. These scripts currently set to only use and save the low_power transmissions, but number can be easily edited to fit needs.
    low_power_SL = 142  # Weaker source
#    high_power_SL = 160  # Stronger source
    arrivals["low_power_dB"] = arrivals["arrival_dB"] + low_power_SL
#    arrivals["high_power_dB"] = arrivals["arrival_dB"] + high_power_SL


# Implementing SBL: uses the number of surface bounces to correct for the surface layer.
    counts4SBL = arrivals.surface_bounces
    SBLattenuation = counts4SBL * SBL 
    arrivals["low_power_dB"] = arrivals["low_power_dB"] - SBLattenuation
#    arrivals["high_power_dB"] = arrivals["high_power_dB"] - SBLattenuation
    arrivals["SBLattenuation"] = SBLattenuation

# High powered arrivals
#    bins = np.arange(0, 111, 10)
#    arrivals['dB_binHigh'] = pd.cut(arrivals['high_power_dB'], bins=bins, include_lowest=True)
#    binned_countsHigh = arrivals['dB_binHigh'].value_counts().sort_index()


# Low powered arrivals, and clipping them so that negative values become 0
# This is done to make a more accurate average; a ray that's -80 dB at the end is not actually arriving at the receiver, it is being lost well before.
    bins = np.arange(0, 100, 10)
    low_power_dB_hist = arrivals["low_power_dB"].clip(lower=0)
    arrivals['dB_binLow'] = pd.cut(low_power_dB_hist, bins=bins, include_lowest=True)
    binned_countsLow = arrivals['dB_binLow'].value_counts().sort_index()
    avg_low_dB = np.mean(arrivals["low_power_dB"])


# 95% confidence interval
    low_power_values = arrivals["low_power_dB"]
    n_lp = len(low_power_values)
    std_lp = np.std(low_power_values, ddof=1)
    sem_lp = std_lp / np.sqrt(n_lp)
    t_value_lp = st.t.ppf(1 - 0.05/2, n_lp - 1)
    margin_of_error_lp = t_value_lp * sem_lp
    ci_lower_lp = avg_low_dB - margin_of_error_lp
    ci_upper_lp = avg_low_dB + margin_of_error_lp
    confidence_interval = (ci_lower_lp, ci_upper_lp)

    # Detectability classification using raw arrival values
    low_power_dB_vals = arrivals["low_power_dB"].clip(lower=0)  # Ensure valid values
    X_detectable = (low_power_dB_vals >= detectionThreshold).sum()
    Y_undetectable = (low_power_dB_vals < detectionThreshold).sum()
    # arrivals that don't touch the bottom.
    nonbottom_arrivals = len(arrivals[arrivals["bottom_bounces"] == 0])
    
# Create a summary DataFrame for console output
    summary_df = pd.DataFrame({
        "Metric": ["Detectable", "Undetectable", "Avg Signal (dB)", "95% CI (dB)"],
        "Value": [X_detectable, Y_undetectable, f"{avg_low_dB:.1f}", f"({ci_lower_lp:.1f}, {ci_upper_lp:.1f})"]
    })
    print(summary_df)



    return arrivals, binned_countsLow, low_power_dB_hist, confidence_interval, X_detectable, Y_undetectable, avg_low_dB, ci_lower_lp, ci_upper_lp, nonbottom_arrivals
