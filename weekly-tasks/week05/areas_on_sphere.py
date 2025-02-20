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
print('----------')



### TASK 3 (RED) ###

#SD find the number of points in each of the HEALpixels
_, counts = np.unique(pix, return_counts=True)

#SD find the fraction of points in each pixel, for easier comparision
counts_frac = counts / np.sum(counts)

print("TASK 3:")

#SD print the percent of points for each pixel
for i in range(len(counts_frac)):
	print(f"In pixel {i+1}, there are {100*counts_frac[i]}% of the points.")
print("The results are consistent with the fact that the pixels are equal-area.")
print('----------')



### TASK 4 (BLACK) ###
