from astropy.coordinates import SkyCoord
from astropy import units as u
import numpy as np
import matplotlib.pyplot as plt



### TASK 1 (RED) ###

obj1 = SkyCoord(246.933, 40.795, unit=u.deg)
obj2 = SkyCoord(236.562, 2.440, unit=u.deg)

print(obj1)
print(obj2)

#SD mags obtained from SDSS Navigator Tool
#SD array is [u, g, r, i, z]
obj1_mags = np.array([18.82, 18.81, 18.73, 18.82, 18.90])
obj2_mags = np.array([19.37, 19.10, 18.79, 18.73, 18.63])

#SD finding r-i aand g-r for both objs
obj1_r_minus_i = obj1_mags[2] - obj1_mags[3]
obj1_g_minus_r = obj1_mags[1] - obj1_mags[2]
obj2_r_minus_i = obj2_mags[2] - obj2_mags[3]
obj2_g_minus_r = obj2_mags[1] - obj2_mags[2]

#SD plotting g-r vs r-i for both objs
plt.scatter(obj1_r_minus_i, obj1_g_minus_r, label='object 1')
plt.scatter(obj2_r_minus_i, obj2_g_minus_r, label='object 2')
plt.xlabel('r - i')
plt.ylabel('g - r')
plt.legend()
plt.show()

#SD In the resulting plot, the two quasars do not have the same colors.
#SD However, I think they should have similar colors.


