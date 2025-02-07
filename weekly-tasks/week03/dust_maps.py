from astropy.coordinates import SkyCoord
from astropy import units as u
import numpy as np
import matplotlib.pyplot as plt



### TASK 1 (RED) ###

#SD save the ra, dec of the given objects in Galactic coords
obj1 = SkyCoord(246.933, 40.795, unit=u.deg).galactic
obj2 = SkyCoord(236.562, 2.440, unit=u.deg).galactic

#SD ugriz mags obtained from SDSS Navigator Tool
#SD array is [u, g, r, i, z]
obj1_mags = np.array([18.82, 18.81, 18.73, 18.82, 18.90])
obj2_mags = np.array([19.37, 19.10, 18.79, 18.73, 18.63])

#SD finding r-i aand g-r for both objs
obj1_r_minus_i = obj1_mags[2] - obj1_mags[3]
obj1_g_minus_r = obj1_mags[1] - obj1_mags[2]
obj2_r_minus_i = obj2_mags[2] - obj2_mags[3]
obj2_g_minus_r = obj2_mags[1] - obj2_mags[2]

#SD plotting g-r vs r-i for both objs
plt.scatter(obj1_r_minus_i, obj1_g_minus_r, c='blue', label='object 1')
plt.scatter(obj2_r_minus_i, obj2_g_minus_r, c='red', label='object 2')
plt.xlabel('r - i')
plt.ylabel('g - r')
plt.legend()
plt.show()

#SD In the resulting plot, the two quasars do not have the same colors.
#SD However, I think they should have similar colors.

#SD configure dustmaps
from dustmaps.config import config
dustdir = "/d/scratch/ASTR5160/data/dust/v0_1/maps"
config["data_dir"] = dustdir
from dustmaps.sfd import SFDQuery
sfd = SFDQuery()

#SD find reddening for obj1 and obj2
obj1_reddening = sfd(obj1)
obj2_reddening = sfd(obj2)

#SD find Galactic extinction for obj1 and obj2
ugriz = np.array([4.239 ,3.303 , 2.285 , 1.698 , 1.263])   #SD from Schlafly & Finkbeiner
obj1_A = obj1_reddening * ugriz
obj2_A = obj2_reddening * ugriz

#SD correct the mags to account for extiction
obj1_mags_corrected = obj1_mags - obj1_A
obj2_mags_corrected = obj2_mags - obj2_A

#SD finding corrected r-i aand g-r for both objs
obj1_r_minus_i_corrected = obj1_mags_corrected[2] - obj1_mags_corrected[3]
obj1_g_minus_r_corrected = obj1_mags_corrected[1] - obj1_mags_corrected[2]
obj2_r_minus_i_corrected = obj2_mags_corrected[2] - obj2_mags_corrected[3]
obj2_g_minus_r_corrected = obj2_mags_corrected[1] - obj2_mags_corrected[2]

#SD plot original and corrected g-r vs r-i
#SD original colors
plt.scatter(obj1_r_minus_i, obj1_g_minus_r, c='blue', label='object 1')
plt.scatter(obj2_r_minus_i, obj2_g_minus_r, c='red', label='object 2')
#SD corrected colors
plt.scatter(obj1_r_minus_i_corrected, obj1_g_minus_r_corrected, c='blue', marker='x', label='object 1 (corrected for extinction)')
plt.scatter(obj2_r_minus_i_corrected, obj2_g_minus_r_corrected, c='red', marker='x', label='object 2 (corrected for extinction)')
plt.xlabel('r - i')
plt.ylabel('g - r')
plt.legend()
plt.show()

#SD The colors agree better after correcting for extinction.

