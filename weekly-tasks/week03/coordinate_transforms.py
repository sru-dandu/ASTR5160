from astropy.coordinates import SkyCoord, get_constellation
import numpy as np
from astropy.table import Table
from astropy import units as u



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
print("--------------")
print("### TASK 1 ###")
print("--------------")
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

print("CHECK:")
print("Check that converting to cartesian with astropy gives same result as manually converting:")
print(table)

print()



### TASK 2 (RED) ###

#SD save l and b of galactic center
gal_coords = SkyCoord(0*u.deg, 0*u.deg, frame='galactic')

#SD convert galactic coordinates to RA and DEC
#SD want RA in hms so that I can use constellation chart later
gal_coords_radec = gal_coords.icrs.to_string('hmsdms')

print("--------------")
print("### TASK 2 ###")
print("--------------")
print(f"The (RA, DEC) of the Galactic center is ({gal_coords_radec})")

#SD find constellation corresponding to galactic center
constellation = get_constellation(gal_coords)
print(f"The Galactic center is in the constellation {constellation}.")
print("Using the constellation chart, I concluded that the Galactic center is near the edge of the constellation.")

print()
