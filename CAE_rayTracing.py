# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 11:39:25 2025
Complex Acoustic Environment (CAE) modeling.
Frank McQuarrie, Skidaway Institute of Oceanography

Purpose of script: Trace sound pathways through the given environment.

Scripts.
CAE_automate : current. Runs and saves outputs from propagation modeling.
CAE_singleExperiment: Run and save a specific model.

CAE_createEnv: Creates an environment for Bellhop to model sound through.
CAE_ssp: Sets a soundspeed profile. Currently set to create one given stratification strength and depth.
CAE_surfaceLevels: defines surface waves for the environment.

*******CAE_rayTracing: Traces (and can plot) sound pathways through the environment.
CAE_arrivals: Measures signal strength and arrival timing for sound through the environment. Also adds initial power, and given a detection threshold, can define a ray as detectable or not.
"""
import os
import arlpy.uwapm as pm
#import arlpy.plot as plt
#import numpy as np
#import pandas as pd

def rayTracing(signalRange,topDescrip,botDescrip,sspDescrip,env):
    
    #Bellhop's location.
    os.chdir(r"C:\Users\fmm17241\OneDrive - University of Georgia\data\toolbox\AT\executables")
    # ALL RAYS
    rays = pm.compute_rays(env)
    # ONLY RAYS BETWEEN TRANSMITTER AND RECEIVER.
#    #rays = pm.compute_eigenrays(env)


    pm.plot_rays(rays, env=env,
                width=900,
                 title= f"Ray Tracing: 69 kHz,{topDescrip}, {botDescrip}, {sspDescrip} Environment") 
    
###############################
# BDA, QUANTIFYING RAY DISTANCE TRAVELED
# This was a simplified metric created in 2021. Leaving here for completeness but BDA as a metric is outdated. See Francis McQuarrie's 2025 dissertation for more on this.
    
#    rayMax = []
#    beamDistances = []
#    distances_to_check = list(range(0, signalRange, 25))
    
#    for ray_array in rays.ray:
        # Ensure ray_array is a NumPy array
#        ray_array = np.array(ray_array)
        
        # Get the maximum value from the first column (distance)
#        max_value = max(ray_array[:, 0])
#        rayMax.append(max_value)
        
        # Create the binary list
#        binary_values = []
#        for distance in distances_to_check:
#            if max_value > distance:
#                binary_values.append(1)
#            else:
#                binary_values.append(0)
        
#        beamDistances.append(binary_values)
    
#    print("Maximum distances for each ray:", rayMax)
#    print("Binary distance checks:", beamDistances[:5])  # First 5 for brevity
    
    
    # Convert beamDistances to a NumPy array
#    beamDistancesArray = np.array(beamDistances)
    
#    # Sum along the rows (axis=0) to get the count for each distance
#    rays_per_distance = np.sum(beamDistancesArray, axis=0)
    
    # Print the results
#    for distance, count in zip(distances_to_check, rays_per_distance):
#        print(f"Distance: {distance} m, Rays: {count}")
#        
#    rays['rayDistance'] = rayMax
    
#    
#    ###############################
#    # PLOT BEAM DENSITY ANALYSIS RESULTS
#    # This was my go-to metric in 2021, fixing it now.
#    sumBDA = np.sum(beamDistances, axis=0)
#    bdaDataFrame = pd.DataFrame({'Distance': distances_to_check, 'Rays': sumBDA})
#    plt.plot(bdaDataFrame['Distance'], bdaDataFrame['Rays'], 'o-', xlabel='Distances', ylabel='Beams Traveled', title= f"BDA: 69 kHz,{topDescrip}, {botDescrip}, {sspDescrip}") 
#    
#    percentageRays = rays_per_distance/1000#

#    return sumBDA, bdaDataFrame,percentageRays,rays,rays_per_distance

