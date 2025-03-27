import numpy as np



### TASK 1 (RED) ###

#SD copying in the given mags and colors for PG1633+A
V, BminusV, UminusB, VminusR, RminusI = 15.256, 0.873, 0.320, 0.505, 0.511

#SD copying conversion equations from Jester et al. 2005
#SD https://classic.sdss.org/dr7/algorithms/sdssUBVRITransform.php
g = V + 0.74*(BminusV) - 0.07
g_minus_r = 0.93*(BminusV) - 0.06
r_minus_z = 1.20*(RminusI) - 0.20

#SD calculating z mag
r = g - g_minus_r
z = r - r_minus_z

print("TASK 1:")
print(f"g mag: from conversion = {g} ; from SDSS Navigate Tool = 15.70")
print(f"z mag: from conversion = {z} ; from SDSS Navigate Tool = 14.55")
print("The values for g and z obtained by converting from UBVRI match the same values from the SDSS Navigate Tool.")
print('----------')



