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
coords1 = SkyCoord(tab1['RA'], tab1['DEC'], unit=u.deg)
coords2 = SkyCoord(tab2['RA'], tab2['DEC'], unit=u.deg)
coords_all = [coords1, coords2]

#SD extract coords from sweep files
coords_sweep1 = SkyCoord(sweeptabs[0]['RA'], sweeptabs[0]['DEC'], unit=u.deg)
coords_sweep2 = SkyCoord(sweeptabs[1]['RA'], sweeptabs[1]['DEC'], unit=u.deg)
coords_sweep3 = SkyCoord(sweeptabs[2]['RA'], sweeptabs[2]['DEC'], unit=u.deg)
coords_sweep4 = SkyCoord(sweeptabs[3]['RA'], sweeptabs[3]['DEC'], unit=u.deg)
coords_sweep_all = [coords_sweep1, coords_sweep2, coords_sweep3, coords_sweep4]

#SD find objects in given files that match those in sweeps
id1_all = []
id2_all = []
for c in coords_all:
	for sweep in coords_sweep_all:
		#SD get matching indices
		id1, id2, d2, d3 = sweep.search_around_sky(c, 0.5*u.arcsec)
		id1_all.append(id1)
		id2_all.append(id2)

#SD mask the sweep files to get only the matched objects
#SD 'sweeptabs' is list of [sweep1, sweep2, sweep3, sweep4] astropy tables
sweep1_match_c1 = sweeptabs[0][id2_all[0]]
sweep2_match_c1 = sweeptabs[1][id2_all[1]]
sweep3_match_c1 = sweeptabs[2][id2_all[2]]
sweep4_match_c1 = sweeptabs[3][id2_all[3]]
sweep1_match_c2 = sweeptabs[0][id2_all[4]]
sweep2_match_c2 = sweeptabs[1][id2_all[5]]
sweep3_match_c2 = sweeptabs[2][id2_all[6]]
sweep4_match_c2 = sweeptabs[3][id2_all[7]]
sweep_match_c = [sweep1_match_c1, sweep2_match_c1,
		sweep3_match_c1, sweep4_match_c1,
		sweep1_match_c2, sweep2_match_c2,
		sweep3_match_c2, sweep4_match_c2]

#SD mask the object files to get only the matched objects
c1_match_sweep1 = tab1[id1_all[0]]
c1_match_sweep2 = tab1[id1_all[1]]
c1_match_sweep3 = tab1[id1_all[2]]
c1_match_sweep4 = tab1[id1_all[3]]
c2_match_sweep1 = tab2[id1_all[4]]
c2_match_sweep2 = tab2[id1_all[5]]
c2_match_sweep3 = tab2[id1_all[6]]
c2_match_sweep4 = tab2[id1_all[7]]
c_match_sweep = [c1_match_sweep1, c1_match_sweep2,
		c1_match_sweep3, c1_match_sweep4,
		c2_match_sweep1, c2_match_sweep2,
		c2_match_sweep3, c2_match_sweep4,]

#SD get relevant fluxes from sweep files
g_lists = [t['FLUX_G'] for t in sweep_match_c]
g_uncorrected = np.concatenate(g_lists)
r_lists = [t['FLUX_R'] for t in sweep_match_c]
r_uncorrected = np.concatenate(r_lists)
z_lists = [t['FLUX_Z'] for t in sweep_match_c]
z_uncorrected = np.concatenate(z_lists)
W1_lists = [t['FLUX_W1'] for t in sweep_match_c]
W1_uncorrected = np.concatenate(W1_lists)
W2_lists = [t['FLUX_W2'] for t in sweep_match_c]
W2_uncorrected = np.concatenate(W2_lists)

print("TASK 1:")
print(f"Extracted g, r, z, W1, and W2 fluxes of the {len(g)} objects.")
print('----------')



### TASK 2 (RED) ###

#SD extract Galactic dust corrections
g_dustcorr = np.concatenate([t['MW_TRANSMISSION_G'] for t in sweep_match_c])
r_dustcorr = np.concatenate([t['MW_TRANSMISSION_R'] for t in sweep_match_c])
z_dustcorr = np.concatenate([t['MW_TRANSMISSION_Z'] for t in sweep_match_c])
W1_dustcorr = np.concatenate([t['MW_TRANSMISSION_W1'] for t in sweep_match_c])
W2_dustcorr = np.concatenate([t['MW_TRANSMISSION_W2'] for t in sweep_match_c])

#SD correct fluxes for Galactic dust
g = g_uncorrected / g_dustcorr
r = r_uncorrected / r_dustcorr
z = z_uncorrected / z_dustcorr
W1 = W1_uncorrected / W1_dustcorr
W2 = W2_uncorrected / W2_dustcorr

#SD convert fluxes to mags
mag_g = 22.5 - 2.5*np.log10(g)
mag_r = 22.5 - 2.5*np.log10(r)
mag_z = 22.5 - 2.5*np.log10(z)
mag_W1 = 22.5 - 2.5*np.log10(W1)
mag_W2 = 22.5 - 2.5*np.log10(W2)

print("TASK 2:")
print("Fluxes for g, r, z, W1, and W2 bands were corrected for Galactic dust and converted to magnitudes.")



### TASK 3 (RED) ###
