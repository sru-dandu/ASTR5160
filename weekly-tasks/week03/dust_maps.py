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



### TASK 2 (RED) ###

#SD create 100x100 grid centered around (236.6 deg, 2.4 deg) with 0.1 deg bins in RA and DEC
#SD 100 steps of 0.1 deg is 10 steps of 1 deg
#SD Therefore go 5 below and 5 above of RA and DEC for lower and upper bounds
ra1 = np.linspace(236.6-5, 236.6+5, 100)
dec1 = np.linspace(2.4-5, 2.4+5, 100)
ra1_grid, dec1_grid = np.meshgrid(ra1, dec1)

#SD create 100x100 grid centered around (246.9 deg, 40.8 deg) with 0.13 deg bins in RA and 0.1 deg bins in DEC
#SD 100 steps of 0.13 deg is 13 steps of 1 deg
#SD Therefore go 6.5 below and 6.5 above of RA value for lower and upper bounds
#SD for DEC do same thing as before
ra2 = np.linspace(246.9-6.5, 246.9+6.5, 100)
dec2 = np.linspace(40.8-5, 40.8+5, 100)
ra2_grid, dec2_grid = np.meshgrid(ra2, dec2)



### TASK 3 (BLACK) ###

#SD make SkyCoord items using meshgrid results
grid1 = SkyCoord(ra1_grid, dec1_grid, unit=u.deg)
grid2 = SkyCoord(ra2_grid, dec2_grid, unit=u.deg)

#SD find reddening for coords1 and coords2
grid1_reddening = sfd(grid1)
grid2_reddening = sfd(grid2)

#SD plot colormap of reddening at coordinates in grid1
plt.contourf(ra1, dec1, grid1_reddening)
plt.colorbar()
plt.show()

#SD plot colormap of reddening at coordinates in grid2
plt.contourf(ra2, dec2, grid2_reddening)
plt.colorbar()
plt.show()

