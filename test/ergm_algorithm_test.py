"""
  Processing time: 42 seconds
  dataset: TCS_C_WONSI_20151016.dat
  
"""

from study.algorithm.ERGM_algorithm import *

# Default value
filename = "../asset/TCS_C_WONSI_20151016.dat"
target = "TRAVEL_TIME"

ERGM(filename, target)

