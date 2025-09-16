# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 18:27:08 2024
Complex Acoustic Environment (CAE) modeling.
Frank McQuarrie, Skidaway Institute of Oceanography

Purpose of script: Define the surface waves for acoustic modeling.

Scripts.
CAE_automate : current. Runs and saves outputs from propagation modeling.
CAE_singleExperiment: Run and save a specific model.

CAE_createEnv: Creates an environment for Bellhop to model sound through.
CAE_ssp: Sets a soundspeed profile. Currently set to create one given stratification strength and depth.
******CAE_surfaceLevels: defines surface waves for the environment.

CAE_rayTracing: Traces (and can plot) sound pathways through the environment.
CAE_arrivals: Measures signal strength and arrival timing for sound through the environment. Also adds initial power, and given a detection threshold, can define a ray as detectable or not.
"""

import numpy as np

##########################

def flat_surface(signal_range, depth=0.0):
    range_max = signal_range + 5
    num_points = range_max + 1
    return np.array([[r, depth] for r in np.linspace(0, range_max, num_points)])

def mid_waves(signal_range, wave_amplitude=0.6, wave_frequency=0.01429):
    range_max = signal_range + 5
    num_points = range_max + 1
    return np.array([[r, -wave_amplitude * np.sin(2 * np.pi * wave_frequency * r)]
                     for r in np.linspace(0, range_max, num_points)])

def rough_waves(signal_range, wave_amplitude=1.0, wave_frequency=0.01):
    range_max = signal_range + 5
    num_points = range_max + 1
    return np.array([[r, -wave_amplitude * np.sin(2 * np.pi * wave_frequency * r)]
                     for r in np.linspace(0, range_max, num_points)])






