# Complex Acoustic Environment Modeling

**Created by Frank McQuarrie Jr., Spring 2025**
contact@frankmcq.com

mcquarrie@marine.rutgers.edu
---

## Purpose

This project models acoustic propagation in noisy environments. It supports both manual and automatic simulation modes, enabling users to investigate sound transmission in complex underwater settings.

---

## Setup

- **Acoustic Toolbox Dependency:**  
  This project uses the [Acoustic Toolbox](https://oalib-acoustics.org/models-and-software/acoustics-toolbox/) (Bellhop).  
  **Before running any scripts, you must build the Bellhop executable:**
  1. Download the Acoustic Toolbox from the link above.
  2. Follow the provided instructions to compile it (usually running `make` in the toolbox directory).
  3. Ensure the Bellhop executable is accessible from your environment (add to your PATH or specify its location in scripts if necessary).

---

## Included Scripts

| Script                    | Purpose                                                                                                                      |
|---------------------------|------------------------------------------------------------------------------------------------------------------------------|
| `CAE_automate.py`         | Automatically runs X iterations of the model, using semi-randomized environment parameters.                                  |
| `CAE_singleExperiment.py` | Manually runs a single model simulation.                                                                                     |
| `CAE_createEnv.py`        | Creates and configures the environment for acoustic propagation.                                                             |
| `CAE_ssp.py`              | Generates or selects a sound speed profile (SSP) for modeling.                                                              |
| `CAE_rayTracing.py`       | Traces and optionally plots acoustic rays through the defined environment.                                                   |
| `CAE_arrivals.py`         | Analyzes acoustic arrivals at the receiver, outputs signal strengths, and checks detectability against a defined threshold.  |

---

## Usage Notes

- **Scenario Customization:**  
  The provided scripts are configured for example scenarios in a 20 m water column.  
  To adapt for new scenarios, edit `CAE_createEnv.py`:
  - Manually define instrument depths and ranges as needed.
  - The structure is designed for easy modification by the user.

- **Running Simulations:**  
  - Use `CAE_singleExperiment.py` for a single, manually defined run.
  - Use `CAE_automate.py` to batch-run multiple simulations with varied parameters.

---

## Citation

If you use or adapt this project, please credit:
> McQuarrie, F.: Complex Environmental Acoustic Modeling package. https://github.com/frankMcQuarrie/complexEnvAcoustics.git. Version 1.0 (2025)

---

## Contact

For questions or contributions, please contact Frank McQuarrie Jr. {contact@frankmcq.com}

