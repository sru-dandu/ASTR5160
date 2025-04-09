from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.table import Table



### TASK 1 (RED) ###

#SD save coords to search for
coords = SkyCoord(188.53667, 21.04572, unit=u.deg)

#SD read in relevant sweep file as astropy table
sweepfile = '/d/scratch/ASTR5160/data/legacysurvey/dr9/south/sweep/9.0/sweep-180p020-190p025.fits'
sweeptable = Table.read(sweepfile)
#SD extract coords of objs in sweep file
sweepcoords = SkyCoord(sweeptable['RA'], sweeptable['DEC'], unit=u.deg)

#SD find the object we want in the sweep file
n=2
match_rad = 1*u.arcsec
while n > 1:
    mask = sweepcoords.separation(coords) < match_rad
    sweepobj = sweeptable[mask]
    n = len(sweepobj)
    match_rad -= 0.05*u.arcsec

print('TASK 1:')
print(f"The object type is given as {sweepobj['TYPE'][0]}, aka an exponential galaxy.")
print('----------')



### TASK 2 (RED) ###

print('TASK 2:')

#SD print out the allmask bit values
print(f"ALLMASK_G = {sweepobj['ALLMASK_G']}")
print(f"ALLMASK_R = {sweepobj['ALLMASK_R']}")
print(f"ALLMASK_Z = {sweepobj['ALLMASK_Z']}")

print("None of the g,r,z bands are saturated in all exposures for this object.")

print("Looking at the Legacy Surveys Sky Viewer, the object seems saturated.")


