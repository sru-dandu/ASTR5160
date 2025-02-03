from astropy.coordinates import SkyCoord
import numpy as np



### TASK 1 (RED)

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

#SD printing the cartesian coords obtained through both methods
print("Converting the RA and DEC into cartesian coordinates gives:")
print( "        |          x         |          y           |            z   ")
print(f"astropy | {fomalhaut_coords.x} | {fomalhaut_coords.y} | {fomalhaut_coords.z}")
print(f" manual | {fomalhaut_x} | {fomalhaut_y} | {fomalhaut_z}")

