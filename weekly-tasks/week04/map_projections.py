import numpy as np
from numpy.random import random
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy import wcs



### TASK 1 (RED) ###

#SD creating arrays for ra and dec
ra = 2 * np.pi * (random(10000)-0.5)
dec = np.arcsin(1. - 2.*random(10000))

#SD plotting dec vs ra to create a cylindrical projection of a sphere
plt.scatter(ra, dec, s=2)
plt.xlabel('ra [rad]')
plt.ylabel('dec [rad]')
plt.show()

#SD There are more points near the equator than near the poles.
#SD This is in line with how the cylindrical projection works.



### TASK 2 (RED) ###

#SD create figure environment
fig = plt.figure(figsize=(16,20))
#SD x-tick labels for both subplots
xlab = ['14h','16h','18h','20h','22h','0h','2h','4h','6h','8h','10h']

#SD subplot with aitoff projection
ax1 = fig.add_subplot(121, projection='aitoff')
ax1.scatter(ra, dec, c='gray', alpha=0.5, s=2)
ax1.grid(color='blue', linestyle='dashed', linewidth=2)
ax1.set_xticklabels(xlab, weight=800)
ax1.set_xlabel("ra [hours]", weight=800)
ax1.set_ylabel("dec [deg]", weight=800)

#SD subplot with lambert projection
ax2 = fig.add_subplot(122, projection='lambert')
ax2.scatter(ra, dec, c='gray', alpha=0.5, s=2)
ax2.set_xticklabels(xlab, weight=800)
ax2.grid(color='blue', linestyle='dashed', linewidth=2)
ax2.set_xlabel("ra [hours]", weight=800)
ax2.set_ylabel("dec [deg]", weight=800)

plt.show()



### TASK 3 (BLACK) ###

#SD create a grid of ra and dec
ra_task3 = np.arange(0.5, 359.5, 1)
dec_task3 = np.arange(-89.5, 89.5, 1)
ra_grid, dec_grid = np.meshgrid(ra_task3, dec_task3)

#SD saving grid as SkyCoord obect
grid = SkyCoord(ra_grid, dec_grid, unit=u.deg)

#SD configure dustmaps
from dustmaps.config import config
dustdir = "/d/scratch/ASTR5160/data/dust/v0_1/maps"
config["data_dir"] = dustdir
from dustmaps.sfd import SFDQuery
sfd = SFDQuery()

#SD find reddening for grid
grid_reddening = sfd(grid)

#SD convert (ra, dec) to (x, y)
w = wcs.WCS(naxis=2)
w.wcs.ctype = ["RA---AIT", "DEC--AIT"]
x_grid, y_grid = w.wcs_world2pix(ra_grid, dec_grid, 1)

#SD plotting both coordinate systems
fig = plt.figure(figsize=(16,20))

#SD subplot with aitoff projection
ax1 = fig.add_subplot(121, projection='aitoff')
ax1.scatter(ra_grid, dec_grid, c='gray', alpha=0.5, s=2)
ax1.grid(color='blue', linestyle='dashed', linewidth=2)
ax1.set_xlabel("ra [deg]", weight=800)
ax1.set_ylabel("dec [deg]", weight=800)

#SD subplot with lambert projection
ax2 = fig.add_subplot(122, projection='aitoff')
ax2.scatter(ra, dec, c='gray', alpha=0.5, s=2)
ax2.grid(color='blue', linestyle='dashed', linewidth=2)
ax2.set_xlabel("x", weight=800)
ax2.set_ylabel("y", weight=800)

plt.show()
