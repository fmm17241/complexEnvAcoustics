# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 14:51:49 2024
Complex Acoustic Environment (CAE) modeling.
Frank McQuarrie, Skidaway Institute of Oceanography

Purpose of script: Create and format an environment for Bellhop acoustic modeling.

Scripts.
CAE_automate : current. Runs and saves outputs from propagation modeling.
CAE_singleExperiment: Run and save a specific model.

******CAE_createEnv: Creates an environment for Bellhop to model sound through.
CAE_ssp: Sets a soundspeed profile. Currently set to create one given stratification strength and depth.
CAE_surfaceLevels: defines surface waves for the environment.

CAE_rayTracing: Traces (and can plot) sound pathways through the environment.
CAE_arrivals: Measures signal strength and arrival timing for sound through the environment. Also adds initial power, and given a detection threshold, can define a ray as detectable or not.
"""

import arlpy.uwapm as pm
import os
import CAE_surfaceLevels
import CAE_bathymetry
from CAE_ssp import build_stratified_ssp

# Script Directory
os.chdir(r"C:\Users\fmm17241\Documents\GitHub\franksCardroom\pythonWork")

#################################################

def createEnv(
    surface_type = "F",         # Categorical, set in "CAE_surfaceLevels"
    scenario = "F",             # Categorical, set here and in "CAE_bathymetry"
    ssp_type = "exampleMar",    # Sound speed profile (m/s), set in "CAE_ssp" 
    signalRange    = 2000,      # Range (m) to cutoff propagation
    frequency=69000,            # Frequency (Hz) of sound to model. 69 kHz for telemetry.
    nBeams = 1000,              # Number of beams to model. 1000 for basic models.
    bottom_soundspeed=1800,     # Sound speed (m/s) at the bottom
    bottom_density=1600,        # Density (g/m^3) at the bottom
    bottom_absorption=0,        # Bottom Absorption (dB/lambda) at the bottom, loss per wavelength
    tx_depth = None,            # Depth (m) of transmitter
    rx_depth = None,            # Depth (m) of receiver
    SBL = 0,                    # Surface bubble loss (SBL), capped at 15 dB. Calculated in UWAPL Handbook and McQuarrie et al 2025.
    detectionThreshold = 50,    # Det. threshold (dB) representing background noise. Range from 30 (very quiet) to 75 (extremely loud)
    deltaSS = 4,                # Strength of sound speed (m/s) stratification.
    gradient_depth = 6          # Depth (m) of sound speed stratification.
):
 
#    Create an underwater environment with the given parameters.
#    
#    Args:
#        surface_type: Preset surface conditions to represent changes in air-sea interface.
#        scenario: Defines bathymetry, range, and instrument depths.
#        ssp_type: Sound speed profiles from glider data. Must be monotonic.
#        frequency: Transmission frequency in Hz.
#        bottom_soundspeed: Sound speed of the bottom.
#        bottom_density: Density of the bottom.
#        bottom_absorption: Absorption of the bottom.
#
#    Returns:
#        Configured environment object.
###############
# 
# Generate dynamic SSP from deltaSS
    soundspeed = build_stratified_ssp(deltaSS=deltaSS, gradient_depth=gradient_depth)
    sspDescrip = f"Stratified (Δc = {deltaSS:.1f} m/s, z={gradient_depth}m)"
###########
# Modeled scenarios,  given instrument depths, range, and bathymetry.
# This is designed for McQuarrie's 6/2025 dissertation, but format should be intuitive.

    if scenario == "FS17toSTSNew1Flat":
        depth = 20
        bottom = CAE_bathymetry.FS17toSTSNew1Flat(depth=depth)
        botDescrip  = "FS17toSTSNew1Flat"
        signalRange = 668
        rx_range = signalRange
        rx_depth = rx_depth if rx_depth is not None else 13.7
        tx_depth = tx_depth if tx_depth is not None else 17.8              
        
    elif scenario == "FS17toSTSNew1Real":
        depth = 20
        bottom = CAE_bathymetry.FS17toSTSNew1Real(depth=depth)
        botDescrip  = "FS17toSTSNew1Real"
        signalRange = 668
        rx_range = signalRange   
        rx_depth = rx_depth if rx_depth is not None else 13.7
        tx_depth = tx_depth if tx_depth is not None else 17.8          

    
    elif scenario == "STSNew1toFS17Flat":
        depth = 20
        bottom = CAE_bathymetry.STSNew1toFS17Flat(depth=depth)
        botDescrip  = "STSNew1toFS17Flat"
        signalRange = 668
        rx_range = signalRange         
        rx_depth = rx_depth if rx_depth is not None else 17.8
        tx_depth = tx_depth if tx_depth is not None else 13.7


    elif scenario == "STSNew1toFS17Real":
        depth = 20
        bottom = CAE_bathymetry.STSNew1toFS17Real(depth=depth)
        botDescrip  = "STSNew1toFS17Real"
        signalRange = 668
        rx_range = signalRange              
        rx_depth = rx_depth if rx_depth is not None else 17.8
        tx_depth = tx_depth if tx_depth is not None else 13.7
        
    elif scenario == "STSNew1toFS17Linear":
        depth = 20
        bottom = CAE_bathymetry.STSNew1toFS17Linear(depth=depth)
        botDescrip  = "STSNew1toFS17Linear"
        signalRange = 668
        rx_range = signalRange              
        rx_depth = rx_depth if rx_depth is not None else 17.8
        tx_depth = tx_depth if tx_depth is not None else 13.7

    elif scenario == "FS17toSTSNew1Linear":
        depth = 20
        bottom = CAE_bathymetry.FS17toSTSNew1Linear(depth=depth)
        botDescrip  = "FS17toSTSNew1Linear" 
        signalRange = 668
        rx_range = signalRange 
        rx_depth = rx_depth if rx_depth is not None else 13.7
        tx_depth = tx_depth if tx_depth is not None else 17.8             
        
       
    elif scenario == "STSNew1toSURT20Flat":
        depth = 20
        bottom = CAE_bathymetry.STSNew1toSURT20Flat(depth=depth)
        botDescrip  = "STSNew1toSURT20Flat" 
        signalRange = 530
        rx_range = signalRange  
        rx_depth = rx_depth if rx_depth is not None else 16.8
        tx_depth = tx_depth if tx_depth is not None else 13.7                  

    elif scenario == "STSNew1toSURT20Linear":
        depth = 20
        bottom = CAE_bathymetry.STSNew1toSURT20Linear(depth=depth)
        botDescrip  = "STSNew1toSURT20Linear" 
        signalRange = 530
        rx_range = signalRange    
        rx_depth = rx_depth if rx_depth is not None else 16.8
        tx_depth = tx_depth if tx_depth is not None else 13.7                      

    elif scenario == "STSNew1toSURT20Real":
        depth = 20
        bottom = CAE_bathymetry.STSNew1toSURT20Real(depth=depth)
        botDescrip  = "STSNew1toSURT20Real" 
        signalRange = 530
        rx_range = signalRange 
        rx_depth = rx_depth if rx_depth is not None else 16.8
        tx_depth = tx_depth if tx_depth is not None else 13.7                    

    elif scenario == "SURT20toSTSNew1Flat":
        depth = 20
        bottom = CAE_bathymetry.SURT20toSTSNew1Flat(depth=depth)
        botDescrip  = "SURT20toSTSNew1Flat" 
        signalRange = 530
        rx_range = signalRange 
        rx_depth = rx_depth if rx_depth is not None else 13.7
        tx_depth = tx_depth if tx_depth is not None else 16.8               

    elif scenario == "SURT20toSTSNew1Linear":
        depth = 20
        bottom = CAE_bathymetry.SURT20toSTSNew1Linear(depth=depth)
        botDescrip  = "SURT20toSTSNew1Linear" 
        signalRange = 530
        rx_range = signalRange  
        rx_depth = rx_depth if rx_depth is not None else 13.7
        tx_depth = tx_depth if tx_depth is not None else 16.8                

    elif scenario == "SURT20toSTSNew1Real":
        depth = 20
        bottom = CAE_bathymetry.SURT20toSTSNew1Real(depth=depth)
        botDescrip  = "SURT20toSTSNew1Real" 
        signalRange = 530
        rx_range = signalRange 
        rx_depth = rx_depth if rx_depth is not None else 13.7
        tx_depth = tx_depth if tx_depth is not None else 16.8               

    elif scenario == "simple2k":
        depth = 20
        bottom = CAE_bathymetry.simple2k(depth=depth)
        botDescrip = "Simplified"
        signalRange = 1999
        rx_range = signalRange
        rx_depth = rx_depth if rx_depth is not None else 15
        tx_depth = tx_depth if tx_depth is not None else 15  
        
    elif scenario == "simple1800":
        depth = 20
        bottom = CAE_bathymetry.simple1800(depth=depth)
        botDescrip = "Simplified"
        signalRange = 1800
        rx_range = signalRange
        rx_depth = rx_depth if rx_depth is not None else 15
        tx_depth = tx_depth if tx_depth is not None else 15  
        
    else:
        raise ValueError(f"Invalid scenario '{scenario}'. Must be a given scenarios. Check CAE_createEnv.")
 
###########
# Setting the surface types for the model. Builds a flat environment, little waves or big waves.
# Done in CAE_surfaceLevels

## Used for examples, 2 kilometers.        
    if surface_type == "flat_surface":
        surface = CAE_surfaceLevels.flat_surface(signalRange)
        topDescrip = "Flat"
    elif surface_type == "mid_waves":
        surface = CAE_surfaceLevels.mid_waves(signalRange)
        topDescrip = "Mid"
    elif surface_type == "rough_waves":
        surface = CAE_surfaceLevels.rough_waves(signalRange)
        topDescrip = "Rough"

    else:
       raise ValueError(f"Invalid surface_type '{surface_type}'. Must be a preset condition.")

###########   
# Surface bubble loss (SBL), used in CAE_Arrivals to estimate attenuation.
# Some examples below, please see UWAPL Acoustics Handbook or McQuarrie et al 2025 for more explanation of calculation.
#        SBL = 0 #dB Represents calm seas at 10deg angle
#        SBL = 4.42 #dB Represents 6 m/s wind at 10deg angle
#        SBL = 13.12 #dB Represents 12 m/s wind at 10deg angle
    SBL = SBL,
    detectionThreshold = detectionThreshold
      
###########    
    # Create the environment
    env = pm.create_env2d(
        frequency=frequency,
        rx_range=rx_range,
        rx_depth=rx_depth,
        depth=bottom,
        soundspeed=soundspeed,
        soundspeed_interp = "linear",        #Interpolates SSP linearly for the sound environment; highly advise this especially in shallow waters and using something like glider data. You don't want random curves introduced through spline fit.
        bottom_soundspeed=bottom_soundspeed,
        bottom_density=bottom_density,
        bottom_absorption=bottom_absorption,
        tx_depth=tx_depth,
        surface=surface,
        surface_interp='curvilinear',
        nbeams=nBeams,
        max_angle = 60,                     # Fan of the beam angles. Can be changed, -60 and 60 were chosen to balance coverage and efficiency.
        min_angle = -60
    )

    return env, topDescrip, sspDescrip, botDescrip, bottom, soundspeed, signalRange, SBL, tx_depth, rx_depth, detectionThreshold

