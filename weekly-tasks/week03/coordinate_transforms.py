from astropy.coordinates import SkyCoord
import numpy as np
from astropy.table import Table



### TASK 1 (RED) ###

#SD saving RA and DEC of Fomalhaut using SkyCoord
#SD coords obtained from Google
fomalhaut_coords = SkyCoord('22h57m39s', '-29d37m20s')

#SD saving RA and DEC (in radians)
#SD need radians in order to be used with np.cos and np.sin
fomalhaut_ra = fomalhaut_coords.ra.rad
fomalhaut_dec = fomalhaut_coords.dec.rad

#SD convert RA and DEC to cartesian coords
fomalhaut_coords.representation_type = "cartesian"

#SD printing the RA and DEC values, in radians
print("TASK 1")
print("------")
print(f"The right ascension of Fomalhaut is {fomalhaut_ra} radians")
print(f"The declination of Fomalhaut is {fomalhaut_dec} radians")

#SD check conversions using equations from slides
#SD converting radians to cartesian
fomalhaut_x = np.cos(fomalhaut_ra) * np.cos(fomalhaut_dec)
fomalhaut_y = np.sin(fomalhaut_ra) * np.cos(fomalhaut_dec)
fomalhaut_z = np.sin(fomalhaut_dec)

#SD creating columns to make a table below
names = ['astropy', 'manual']
x_values = np.array([fomalhaut_coords.x, fomalhaut_x])
y_values = np.array([fomalhaut_coords.y, fomalhaut_y])
z_values = np.array([fomalhaut_coords.z, fomalhaut_z])

#SD creating table for manual and astropy conversions of cartesian coords
table = Table([names, x_values, y_values, z_values],
		names=[' ', 'x', 'y', 'z'])

print(table)


