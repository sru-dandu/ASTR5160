import numpy as np
import healpy as hp



### TASK 1 (BLACK) ###

#SD make ra and dec arrays with 1 million values
ra = 360 * np.random.random(10**6)
dec = (180/np.pi) * np.arcsin(1 - 2*np.random.random(10**6))



### TASK 2 (RED) ###

#SD find where each point lies in the HEALpix hierarchy with Nside = 1
pix = hp.ang2pix(1, ra, dec, lonlat=True)

#SD find the area of a HEALpixel when Nside = 1
nside_area = hp.nside2pixarea(1, degrees=True)

print("TASK 2:")
print(f"The area of a HEALpixel when Nside = 1 is {nside_area} square degrees.")

