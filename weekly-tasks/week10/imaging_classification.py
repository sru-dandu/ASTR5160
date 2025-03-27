import numpy as np
from astropy.table import Table



### TASK 1 (RED) ###

#SD read in the files as astropy tables
tab1 = Table.read('/d/scratch/ASTR5160/week10/stars-ra180-dec30-rad3.fits')
tab2 = Table.read('/d/scratch/ASTR5160/week10/qsos-ra180-dec30-rad3.fits')

#SD read in sweep files that contain points within 3 deg of (180 deg, 30 deg)
sweepdir = '/d/scratch/ASTR5160/data/legacysurvey/dr9/south/sweep/9.0/'
sweepfiles = ['sweep-170p025-180p030.fits',
		'sweep-170p030-180p035.fits',
		'sweep-180p025-190p030.fits',
		'sweep-180p030-190p035.fits',]
sweepfiles_long = [sweepdir + f for f in sweepfiles]
sweeptabs = [Table.read(f) for f in sweepfiles_long]
	
