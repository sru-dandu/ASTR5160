import numpy as np
import os
from astropy.table import Table



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
print("The magnitudes for g and z bands obtained by converting from UBVRI colors generally match the same values from the SDSS Navigate Tool.")
print('----------')



### TASK 2 (RED) ###

#SD save the the the sweep file containing the star we are looking at
#SD PG1633+A has (ra, dec) = (248.858 deg, 9.798 deg)
sweepfile = '/d/scratch/ASTR5160/data/legacysurvey/dr9/south/sweep/9.0/sweep-240p005-250p010.fits'

#SD read in the file as an astropy table and extract the obj we are looking at
table = Table.read(sweepfile)
mask = (table['RA'] > 248.857) & (table['RA'] < 248.859) & (table['DEC'] > 9.797) & (table['DEC'] < 9.799)
obj = table[mask]

#SD extract the g,r,z fluxes for the object
sweep_flux_g = obj['FLUX_G'][0]
sweep_flux_r = obj['FLUX_R'][0]
sweep_flux_z = obj['FLUX_Z'][0]

#SD calculate mags from fluxes
#SD fluxes were given in nanomaggies so need to add 22.5 when finding mags
sweep_g = 22.5 - 2.5*np.log10(sweep_flux_g)
sweep_r = 22.5 - 2.5*np.log10(sweep_flux_r)
sweep_z = 22.5 - 2.5*np.log10(sweep_flux_z)

print("TASK 2:")
print(f"g mag: from conversion = {sweep_g} ; from SDSS Navigate Tool = 15.70")
print(f"r mag: from conversion = {sweep_r} ; from SDSS Navigate Tool = 15.19")
print(f"z mag: from conversion = {sweep_z} ; from SDSS Navigate Tool = 14.55")
print("The magnitudes in g, r, and z bands obtained from the fluxes in the sweep file generally match the same values from the SDSS Navigate Tool.")

#SD extract WISE fluxes for the object
sweep_flux_W1 = obj['FLUX_W1'][0]
sweep_flux_W2 = obj['FLUX_W2'][0]
sweep_flux_W3 = obj['FLUX_W3'][0]
sweep_flux_W4 = obj['FLUX_W4'][0]

#SD calculate mags from fluxes
#SD fluxes were given in nanomaggies so need to add 22.5 when finding mags
sweep_W1 = 22.5 - 2.5*np.log10(sweep_flux_W1)
sweep_W2 = 22.5 - 2.5*np.log10(sweep_flux_W2)
sweep_W3 = 22.5 - 2.5*np.log10(sweep_flux_W3)
#W4 flux is negative, so cannot calculate magnitude for it

print(f"The WISE magnitudes are W1={sweep_W1}, W2={sweep_W2}, and W3={sweep_W3}. It was not detected in the W4 band.")
print('----------')

