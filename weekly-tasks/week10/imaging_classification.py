import numpy as np
from astropy.table import Table
from astropy.coordinates import SkyCoord
from astropy import units as u



### TASK 1 (RED) ###

#SD read in the files as astropy tables
tab1 = Table.read('/d/scratch/ASTR5160/week10/stars-ra180-dec30-rad3.fits')
tab2 = Table.read('/d/scratch/ASTR5160/week10/qsos-ra180-dec30-rad3.fits')

#SD read in sweep files that contain points within 3 deg of (180 deg, 30 deg)
sweepdir = '/d/scratch/ASTR5160/data/legacysurvey/dr9/south/sweep/9.0/'
sweepfiles = ['sweep-170p025-180p030.fits',
		'sweep-170p030-180p035.fits',
		'sweep-180p025-190p030.fits',
		'sweep-180p030-190p035.fits']
sweepfiles_long = [sweepdir + f for f in sweepfiles]
sweeptabs = [Table.read(f) for f in sweepfiles_long]

#SD extract coords from given files
ra = np.append(tab1['RA'], tab2['RA'])
dec = np.append(tab1['DEC'], tab2['DEC'])
coords = SkyCoord(ra, dec, unit=u.deg)

#SD extract ra and dec from sweep files
ra_sweep = np.concatenate((sweepfiles[0]['RA'],
			sweepfiles[1]['RA'],
			sweepfiles[2]['RA'],
			sweepfiles[3]['RA']))
dec_sweep = np.concatenate((sweepfiles[0]['DEC'],
			sweepfiles[1]['DEC'],
			sweepfiles[2]['DEC'],
			sweepfiles[3]['DEC']))
coords_sweep = SkyCoord(ra_sweep, dec_sweep)


	
