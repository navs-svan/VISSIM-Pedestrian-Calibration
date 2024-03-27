# Vissim Pedestrian Calibration

This repository contains the python scripts of my undergraduate research study. They involve the use of the Vissim COM interface.
* [Calibration.py](./Calibration.py) - script to calibrate the significant pedestrian walking behavior parameters under the adapted Social Force Model in Vissim. Calibration was done using Genetic Algorithm.
* [Validation.py](./Validation.py) - script to validate the potential calibrated parameters. Validation was done through Theil's Indicator U and Root Mean Square Percentage Error (RMSPE).
* [Analysis_GreenTiming.py](./Analysis_GreenTiming.py) - script used to establish an empirical relationship between pedestrian volume and minimum pedestrian green cycle time. Analysis was done by using the calibrated parameters in Vissim.
* [Analysis_SpeedDensity](./Analysis_SpeedDensity.py) - script used to establish an empirical relationship between pedestrian density and walking speed. Analysis was done by using the calibrated parameters in Vissim.

DISCLAIMER: Data collection is not included in this repository.

## Prerequisites

1. Python 3

2. Vissim License (Trial version does not have access to COM Interface)
 

## Configuration
* Python
```
pip install -r requirements.txt
```
