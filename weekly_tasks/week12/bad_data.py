from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.table import Table, vstack
import numpy as np
from weekly_tasks.week10.imaging_classification import classify_func



def task3(r_max, PSF=True):
    """Code for Task 3 of this module.
        Get objs from sweep files within 3 deg of (180 deg, 30 deg) and with r-band mag < given upper limit for r.
        Then, cross-match with objs from qsos file to find which of those objs are for sure quasars.
    
    INPUTS
    ------
    r_max : :class:'int' or 'float'
        Upper limit of r band magnitude that survey is being limited to.
    PSF : :class:'bool' ; Optional, default is True
        If set to False, then uses all object types in sweep files.
        Else, uses only objects of type PSF (as asked for in this lecture's tasks).
    
    RETURNS
    -------
    :class:'astropy.table.table.Table'
        Table of objects from sweep files that are within 3 deg of (180 deg, 30 deg) and have r-band mag < r_max.
    :class:'astropy.table.table.Table'
        Table of objects from first output that cross-matched with objects in qsos file.
        These are the objects from first output that are for sure quasars.
    :class:'numpy.ndarray'
        Indices of first outputted table that corresponds to objects in second outputted table.
    
    NOTES
    -----
    - I made this its own function to avoid rewriting the code in Lecture 22's task 2.
    """

    #SD obtain tables of relevant sweep files
    sweepdir = '/d/scratch/ASTR5160/data/legacysurvey/dr9/south/sweep/9.0/'
    sweepfiles_list = ['sweep-170p025-180p030.fits', 'sweep-170p030-180p035.fits',
                        'sweep-180p025-190p030.fits', 'sweep-180p030-190p035.fits']
    sweeptables_list = [Table.read(sweepdir + f) for f in sweepfiles_list]
    sweeptables_all = vstack([t for t in sweeptables_list])


    #SD create mask for objs within 3 deg of (180 deg, 30 deg)
    center_coords = SkyCoord(180, 30, unit=u.deg)
    sweeptables_all_coords = SkyCoord(sweeptables_all['RA'], sweeptables_all['DEC'], unit=u.deg)
    separation_mask = (sweeptables_all_coords.separation(center_coords) < 3*u.deg)

    #SD mask the sweepfile objects
    #SD mask depends on whether PSF is True or False
    if PSF==True:
        #SD create a mask for objs that are point sources
        psf_mask = (sweeptables_all['TYPE'] == 'PSF')
        psfobjs = sweeptables_all[psf_mask & separation_mask]
    
    elif PSF==False:
        psfobjs = sweeptables_all[separation_mask]


    #SD create mask to only get objects for which r flux > 0
    #SD flux <= 0 means it wasn't detected in that band
    flux_mask = psfobjs['FLUX_R'] > 0
    psfobjs = psfobjs[flux_mask]

    #SD get magnitude from flux
    #SD flux is in units of nanomaggies
    r_flux = psfobjs['FLUX_R']
    r_mag = 22.5 - 2.5*np.log10(r_flux)

    #SD mask for sources with r < given r_max
    psfobjs = psfobjs[r_mag < r_max]


    #SD call function to cross-match psfobjs with known quasars
    qsos, id1 = qsos_cross_matcher(psfobjs)


    return psfobjs, qsos, id1



def qsos_cross_matcher(psfobjs):
    """Cross-matches given objects with known quasars.
    
    INPUTS
    ------
    psfobjs : :class:'astropy.table.table.Table'
        The objects to be cross-matched with the known quasars.
    
    RETURNS
    -------
    :class:'astropy.table.table.Table'
        The objects from the inputted table that are known quasars.
    :class:'numpy.ndarray'
        The indices of the inputted table where there are known quasars.
    """

    #SD read in qsos file
    qsos_file = '/d/scratch/ASTR5160/week10/qsos-ra180-dec30-rad3.fits'
    qsos_table = Table.read(qsos_file)

    #SD extract coords from psfobjs and qsos
    psfobjs_coords = SkyCoord(psfobjs['RA'], psfobjs['DEC'], unit=u.deg)
    qsos_coords = SkyCoord(qsos_table['RA'], qsos_table['DEC'], unit=u.deg)

    #SD cross-match objects
    id1, id2, d2, d3 = qsos_coords.search_around_sky(psfobjs_coords, 1*u.arcsec)
    qsos = psfobjs[id1]
    
    return qsos, id1



if __name__ == '__main__':

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

    print('----------')
    print('TASK 1:')
    print(f"The object type is given as {sweepobj['TYPE'][0]}, aka an exponential galaxy.")
    print('----------')



    ### TASK 2 (RED) ###

    print('TASK 2:')

    #SD print out the allmask values
    #SD if saturated, bit = 1, therefore output should be 2^1 = 2
    print(f"ALLMASK_G = {sweepobj['ALLMASK_G'][0]}")
    print(f"ALLMASK_R = {sweepobj['ALLMASK_R'][0]}")
    print(f"ALLMASK_Z = {sweepobj['ALLMASK_Z'][0]}")

    print("Each of the g,r,z bands are saturated in all exposures for this object.")

    #SD check obj in Legacy Surveys Sky Viewer
    #SD https://www.legacysurvey.org/viewer?ra=188.5367&dec=21.0458&layer=ls-dr9&zoom=16
    print("Looking at the Legacy Surveys Sky Viewer, the object seems saturated. It also seems to be a blazar candidate.")
    print('----------')



    ### TASK 3 (RED) ###

    #SD call function to run task 3 code
    psfobjs, qsos, id1 = task3(r_max=20)
    
    print('TASK 3:')
    print(f"There are {len(psfobjs)} point-source objects within 3 degrees of (180 deg, 30 deg) with an r-band magnitude < 20.")
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
    quasar_mask = classify_func(g_mag, r_mag, z_mag, W1_mag)

    #SD print numbers of quasars and stars
    num_quasars = len(quasar_mask[quasar_mask==True])
    num_stars = len(quasar_mask) - num_quasars
    
    print("TASK 4:")
    print("Using my function from the previous week: " +
            f"There are {num_quasars} quasars and {num_stars} stars.")
    
    #SD area of a spherical cap is 2*pi*(1-cos(theta))
    area = 2 * np.pi * (1 - np.cos(3*u.deg))
    area_str = area.value
    area_deg2 = area_str * 180/np.pi * 180/np.pi
    print(f"The area of the circle we are considering is {area_str} str, or {area_deg2} square degrees.")
    print(f"Since there are {num_quasars} potential quasars within an area of {area_deg2} square degrees, " +
            f"we would need at least {np.ceil(num_quasars/area_deg2)} spectra per square degree to determine " +
            "the true number of quasars per square degree.")
    print('-')
    

    #SD create mask to remove some bad data
    flag = 2**2 + 2**3 + 2**4 + 2**5 + 2**6 + 2**7 + 2**8
    bitmask = (psfobjs_flux_detected['MASKBITS'] & flag) == 0
    
    #SD mask the datasets to get only the good objects
    psfobjs_flux_detected_goodobjs = psfobjs_flux_detected[bitmask]
    g_mag_goodobjs = g_mag[bitmask]
    z_mag_goodobjs = z_mag[bitmask]
    r_mag_goodobjs = r_mag[bitmask]
    W1_mag_goodobjs = W1_mag[bitmask]
    
    #SD find number of qsos objs after bitmasking
    qsos_goodobjs, idx_goodobjs = qsos_cross_matcher(psfobjs_flux_detected_goodobjs)
    print(f"After masking for good data using bitmasks, there are now {len(qsos_goodobjs)} objects " +
            "within 3 degrees of (180 deg, 30 deg) with an r-band magnitude < 20 " +
            "that we know for sure are quasars.")
    print('(This meets the criteria of retaining at least 250 of the 275 qsos objects.)')
    print('-')
    
    #SD this time, run function from Week 10 tasks
    #SD to classify the selected good psfobjs objects as stars or quasars using color cuts
    quasar_mask_goodobjs = classify_func(g_mag_goodobjs, r_mag_goodobjs, z_mag_goodobjs, W1_mag_goodobjs)
    num_quasars_goodobjs = len(quasar_mask_goodobjs[quasar_mask_goodobjs==True])
    num_stars_goodobjs = len(quasar_mask_goodobjs) - num_quasars_goodobjs
    
    print("Using my function from the previous week, but masking for good data using bitmasks:")
    print(f"There are now {num_quasars_goodobjs} quasars and {num_stars_goodobjs} stars.")
    print(f"This means we now only need {np.ceil(num_quasars_goodobjs/area_deg2)} spectra " +
            "per square degree to determine the true number of quasars per square degree.")
    print('----------')















