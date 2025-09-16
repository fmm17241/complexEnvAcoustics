# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 19:52:10 2024
Complex Acoustic Environment (CAE) modeling.
Frank McQuarrie, Skidaway Institute of Oceanography

Purpose of script: Create (or define) a sound speed profile for acoustic modeling.

Scripts.
CAE_automate : current. Runs and saves outputs from propagation modeling.
CAE_singleExperiment: Run and save a specific model.

CAE_createEnv: Creates an environment for Bellhop to model sound through.
******CAE_ssp: Sets a soundspeed profile. Currently set to create one given stratification strength and depth.
CAE_surfaceLevels: defines surface waves for the environment.

CAE_rayTracing: Traces (and can plot) sound pathways through the environment.
CAE_arrivals: Measures signal strength and arrival timing for sound through the environment. Also adds initial power, and given a detection threshold, can define a ray as detectable or not.
"""


###########################################################
import numpy as np
import pandas as pd

def build_stratified_ssp(deltaSS, gradient_depth=6, base_speed=1513.5, depth_range=(0, 22), range_steps=[-10, 0, 2100]):
    """
    Build a stratified sound speed profile including a -5 m surface value and below the bottom for Bellhop.
    """
    top_speed = base_speed + deltaSS  # Surface sound speed

    # Add -5 m explicitly and concatenate with desired profile depths
    profile_depths = np.arange(depth_range[0], depth_range[1] + 2, 2)
    depths = np.insert(profile_depths, 0, -5)

    ssp_profile = []

    for d in depths:
        if d <= gradient_depth:
            ssp_profile.append(top_speed)
        else:
            ssp_profile.append(base_speed)  # Constant below gradient_depth


    ssp_df = pd.DataFrame({r: ssp_profile for r in range_steps}, index=depths)
    return ssp_df


##########
# Below are some working examples for a set sound speed profile. CAE can be changed to set a specific and range-dependent sound speed profile, below.
# Feel free to edit to make them range dependent. Bellhop does not require the SSP be constant with distance.

#Modeling difference across the coastal frontal zone. Estimated 4degC diff, so ~16 m/s difference, huge.
#def CFZStrongOnShore300(depth=20):
#    # Define depths (index)
#    depth_values = [-5, 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20,22]  
#    # Define sound speed 
#    ssp_df = pd.DataFrame({
#        0: [1521.3, 1521.2, 1521.2, 1521.2, 1520.7, 1520.48, 1520.68, 1520.95, 1521.04, 1521.1, 1521.1, 1521.15, 1521.2],  # Profile at 0 m range
#      200: [1521.3, 1521.2, 1521.2, 1521.2, 1520.7, 1520.48, 1520.68, 1520.95, 1521.04, 1521.1, 1521.1, 1521.15, 1521.2],  # Profile at 200 m range
#      300: [1505.3, 1505.2, 1505.2, 1505.2, 1504.7, 1504.48, 1504.68, 1504.95, 1505.04, 1505.1, 1505.1, 1505.15, 1505.2],  # Profile at 400 m range
#      400: [1505.3, 1505.2, 1505.2, 1505.2, 1504.7, 1504.48, 1504.68, 1504.95, 1505.04, 1505.1, 1505.1, 1505.15, 1505.2],  # Profile at 400 m range
#      600: [1505.3, 1505.2, 1505.2, 1505.2, 1504.7, 1504.48, 1504.68, 1504.95, 1505.04, 1505.1, 1505.1, 1505.15, 1505.2],  # Profile at 600 m range
#      800: [1505.3, 1505.2, 1505.2, 1505.2, 1504.7, 1504.48, 1504.68, 1504.95, 1505.04, 1505.1, 1505.1, 1505.15, 1505.2],  # Profile at 800 m range
#     1000: [1505.3, 1505.2, 1505.2, 1505.2, 1504.7, 1504.48, 1504.68, 1504.95, 1505.04, 1505.1, 1505.1, 1505.15, 1505.2],  # Profile at 1000 m range
#     1200: [1505.3, 1505.2, 1505.2, 1505.2, 1504.7, 1504.48, 1504.68, 1504.95, 1505.04, 1505.1, 1505.1, 1505.15, 1505.2],  # Profile at 1200 m range
#    }, index=depth_values)
#
#    return ssp_df  # Return a Pandas DataFrame


#def exampleStrat18(depth=20):
#    # Define depths (index)
#    depth_values = [-5, 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]
#    # Define sound speed
#    ssp_df = pd.DataFrame({
#      -10: [1514, 1514, 1514, 1514, 1514, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5],   # Profile at 0 m range
#        0: [1514, 1514, 1514, 1514, 1514, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5],   # Profile at 0 m range
#     2100: [1514, 1514, 1514, 1514, 1514, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5],    # Profile at 1300 m range
#    }, index=depth_values)
#
#    return ssp_df  # Return a Pandas DataFrame

#def exampleStrat19(depth=20):
#   # Define depths (index)
#   depth_values = [-5, 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]
#   # Define sound speed
#   ssp_df = pd.DataFrame({
#      -10: [1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5],   # Profile at 0 m range
#        0: [1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5],   # Profile at 0 m range
#     2100: [1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5, 1513.5],    # Profile at 1300 m range
#    }, index=depth_values)
#
#    return ssp_df  # Return a Pandas DataFrame



