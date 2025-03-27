import numpy as np



### TASK 1 (RED) ###

#SD copying in the given mags and colors for PG1633+A
V, BminusV, UminusB, VminusR, RminusI = 15.256, 0.873, 0.320, 0.505, 0.511

#SD finding the mags from the given information
B = BminusV + V
U = UminusB + B
R = V - VminusR
I = R - RminusI


