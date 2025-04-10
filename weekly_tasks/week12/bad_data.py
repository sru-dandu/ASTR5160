from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.table import Table, vstack
import numpy as np
from weekly_tasks.week10.imaging_classification import classify_func



### TASK 1 (RED) ###

#SD save coords to search for
coords = SkyCoord(188.53667, 21.04572, unit=u.deg)

#SD read in relevant sweep file as astropy table
sweepdir = '/d/scratch/ASTR5160/data/legacysurvey/dr9/south/sweep/9.0/'
sweepfile = 'sweep-180p020-190p025.fits'
sweeptable = Table.read(sweepdir + sweepfile)
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
print(f"ALLMASK_G = {sweepobj['ALLMASK_G'][0]}")
print(f"ALLMASK_R = {sweepobj['ALLMASK_R'][0]}")
print(f"ALLMASK_Z = {sweepobj['ALLMASK_Z'][0]}")

print("None of the g,r,z bands are saturated in all exposures for this object.")

#SD check obj in Legacy Surveys Sky Viewer
#SD https://www.legacysurvey.org/viewer?ra=188.5367&dec=21.0458&layer=ls-dr9&zoom=16
print("Looking at the Legacy Surveys Sky Viewer, the object seems saturated. It also seems to be a blazar candidate.")
print('----------')



### TASK 3 (RED) ###

#SD obtain tables of relevant sweep files
sweepfiles_list = ['sweep-170p025-180p030.fits', 'sweep-170p030-180p035.fits',
                    'sweep-180p025-190p030.fits', 'sweep-180p030-190p035.fits']
sweeptables_list = [Table.read(sweepdir + f) for f in sweepfiles_list]
sweeptables_all = vstack([t for t in sweeptables_list])


#SD create a mask for objs that are point sources
psf_mask = (sweeptables_all['TYPE'] == 'PSF')

#SD create mask for objs within 3 deg of (180 deg, 30 deg)
center_coords = SkyCoord(180, 30, unit=u.deg)
sweeptables_all_coords = SkyCoord(sweeptables_all['RA'], sweeptables_all['DEC'], unit=u.deg)
separation_mask = (sweeptables_all_coords.separation(center_coords) < 3*u.deg)

#SD mask the sweepfile objects
psfobjs = sweeptables_all[psf_mask & separation_mask]


#SD create mask to only get objects for which r flux > 0
#SD flux <= 0 means it wasn't detected in that band
flux_mask = psfobjs['FLUX_R'] > 0
psfobjs = psfobjs[flux_mask]

#SD get magnitude from flux
#SD flux is in units of nanomaggies
r_flux = psfobjs['FLUX_R']
r_mag = 22.5 - 2.5*np.log10(r_flux)

#SD mask for sources with r < 20
psfobjs = psfobjs[r_mag < 20]

print('TASK 3:')
print(f"There are {len(psfobjs)} point-source objects within 3 degrees of (180 deg, 30 deg) with an r-band magnitude < 20")


#SD read in qsos file
qsos_file = '/d/scratch/ASTR5160/week10/qsos-ra180-dec30-rad3.fits'
qsos_table = Table.read(qsos_file)

#SD extract coords from psfobjs and qsos
psfobjs_coords = SkyCoord(psfobjs['RA'], psfobjs['DEC'], unit=u.deg)
qsos_coords = SkyCoord(qsos_table['RA'], qsos_table['DEC'], unit=u.deg)

#SD cross-match objects
id1, id2, d2, d3 = qsos_coords.search_around_sky(psfobjs_coords, 1*u.arcsec)
qsos = psfobjs[id1]

print(f"There are {len(qsos)} objects within 3 degrees of (180 deg, 30 deg) with an r-band magnitude < 20 that we know for sure are quasars.")
print('----------')



### TASK 4 (BLACK) ###

#SD extract fluxes of psfobjs
flux_mask = (psfobjs['FLUX_G'] > 0) & (psfobjs['FLUX_Z'] > 0) & (psfobjs['FLUX_R'] > 0) & (psfobjs['FLUX_W1'] > 0)
psfobjs_flux_detected = psfobjs[flux_mask]

#SD find magnitudes of psfobjs
g_mag = 22.5 - 2.5*np.log10(psfobjs_flux_detected['FLUX_G'])
z_mag = 22.5 - 2.5*np.log10(psfobjs_flux_detected['FLUX_Z'])
r_mag = 22.5 - 2.5*np.log10(psfobjs_flux_detected['FLUX_R'])
W1_mag = 22.5 - 2.5*np.log10(psfobjs_flux_detected['FLUX_W1'])

#SD run function from Week 10 tasks to classify psfobjs objs as stars or quasars using color cuts
class_list = [classify_func(g_mag[i], z_mag[i], r_mag[i], W1_mag[i]) for i in range(len(psfobjs_flux_detected))]


#SD print numbers of quasars and stars
num_quasars = len(class_list[class_list=='quasar'])
num_stars = len(class_list) - num_quasars
print(f"quasars: {num_quasars}")
print(f"stars: {num_stars}")








