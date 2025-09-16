Complex Acoustic Environment Modeling
Created by Frank McQuarrie Jr., Spring 2025

Purpose: Modeling acoustic propagation in noisy environments. Can be manual or automatic.


Setup required:
CAE used Acoustic toolbox, you'll have to run a makefile to create the Bellhop executable ahead of time.
https://oalib-acoustics.org/models-and-software/acoustics-toolbox/


Scripts included:
-CAE_automate.py - automatically runs X iterations of the model, can pick semi-random values for env.
-CAE_singleExperiment.py - manually runs one model.
-CAE_createEnv.py - Creates the environment for acoustic propagation.
-CAE_ssp.py - Creates or selects a sound speed profile for modeling.
-CAE_rayTracing.py - Traces and can plot acoustic rays through the given acoustic environment.
-CAE_arrivals.py - Traces and describes sound that travels from transmitter to receiver, outputs strength and
		   also defines whether or not a ray is detectable by comparing it to the set detection threshold.


For outside users: this was created for a few scenarios in a 20 m water column. You will need to create new
scenarios in createEnv if you would like to adapt it, it should be very easy, manually defining instrument
depths and ranges.
