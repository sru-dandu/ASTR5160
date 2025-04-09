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

print(sweepobj)
