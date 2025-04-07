from astropy.table import Table, vstack
from astropy.coordinates import SkyCoord
from astropy import units as u
import numpy as np
from time import sleep
import matplotlib.pyplot as plt
#SD import a function I previously wrote
from weekly_tasks.week08.cross_matching import sweep_func
#SD import Dr. Adam Myer's querying module (saved within my ASTR5160/weekly_tasks/week08 directory)
from weekly_tasks.week08.sdssDR9query import sdssQuery



#SD I made a more specific version of this function for use in hw 3, but I already wrote this version
#SD and I wanted to leave this function as a general use case as well
def cross_match(datafile, coords_center, radius, sweepdir, match_radius=1*u.arcsec):
    """Finds objects in a data file within some circular area, and
    cross-matches them with objects from sweep files.
    
    INPUTS
    ------
    datafile : :class:'str'
        The data file containing the objects being cross-matched.
    coords_center : :class:'astropy.coordinates.sky_coordinate.SkyCoord'
        The coordinates of the center of the area of the sky being cross-matched.
    radius : :class:'astropy.units.quantity.Quantity'
        The radius of the area of the sky being cross-matched.
    sweepdir : :class:'str'
        The directory in which the sweep files are saved.
    match_radius : :class:'astropy.units.quantity.Quantity' ; Optional, default is 1 arcsecond
        The radius to be used when cross-matching.
    
    RETURNS
    -------
    :class:'astropy.table.table.Table'
        An astropy table containing the objects from the data file that matched with objects in the sweep files.
    :class:'astropy.table.table.Table'
        An astropy table containing all objects from the sweep files that matched with objects in the data file.
    
    NOTES
    -----
    - Each index in the two outputted tables correspond to the same object.
        - Ex: table1[0] and table2[0] correspond to one object,
          table1[1] and table2[1] correspond another object, etc.
    - The second outputted table, which contains data from the sweep files, combines
      cross-matched objects from all relevant sweep files in the directory.
    - The function used here for finding relevant sweep files comes from
      a function in ASTR5160/weekly_tasks/week08/cross_matching.
    """
    
    #SD read in FIRST file and extract coords
    table = Table.read(datafile)
    coords = SkyCoord(table['RA'], table['DEC'], unit=u.deg)
    
    #SD find objects within circle centered at given center coords and with given radius
    mask = coords.separation(coords_center) < radius
    table_selected = table[mask]
    #SD extract coordinates of these objects
    coords_selected = coords[mask]
    
    #SD find which sweep files are necessary for cross-matching
    #SD running function from weekly_tasks/week08/cross_matching.py
    sweepfiles = sweep_func(table_selected['RA'], table_selected['DEC'], directory=sweepdir)
    
    #SD read in sweep files as astropy tables
    sweepfiles_long = [sweepdir + '/' + sf for sf in sweepfiles]
    table_sweeps = [Table.read(sfl) for sfl in sweepfiles_long]
    table_sweeps_all = vstack(table_sweeps)
    
    #SD extract coords from chosen sweep files
    coords_sweeps = SkyCoord(table_sweeps_all['RA'], table_sweeps_all['DEC'], unit=u.deg)
    #SD find indices of dataset and sweeps that correspond with each other
    id1, id2, d2, d3 = coords_sweeps.search_around_sky(coords_selected, match_radius)
    
    #SD remove duplicates in case cross-matching returns multiple objects that are within the matching radius
    id1_sorted, unique_idx = np.unique(id1, return_index=True)
    id2_sorted = id2[unique_idx]
    #SD again, but other way around
    id2_sorted, unique_idx = np.unique(id2_sorted, return_index=True)
    id1_sorted = id1_sorted[unique_idx]
    
    #SD cross-match betwen objects in datafile and the sweep files, using given matching radius
    table_selected_matched = table_selected[id1_sorted]
    table_sweeps_matched = table_sweeps_all[id2_sorted]
    
    return table_selected_matched, table_sweeps_matched



#SD this is the more specific version of the function above
#SD for use in hw 3
def cross_match_mags(datafile, coords_center, radius, sweepdir, match_radius=1*u.arcsec):
    """Finds objects in a data file within some circular area, and
    cross-matches them with objects from sweep files.
    
    INPUTS
    ------
    datafile : :class:'str'
        The data file containing the objects being cross-matched.
    coords_center : :class:'astropy.coordinates.sky_coordinate.SkyCoord'
        The coordinates of the center of the area of the sky being cross-matched.
    radius : :class:'astropy.units.quantity.Quantity'
        The radius of the area of the sky being cross-matched.
    sweepdir : :class:'str'
        The directory in which the sweep files are saved.
    match_radius : :class:'astropy.units.quantity.Quantity' ; Optional, default is 1 arcsecond
        The radius to be used when cross-matching.
    
    RETURNS
    -------
    :class:'astropy.table.table.Table'
        An astropy table containing all objects from the sweep files that matched with objects in the data file.
    
    NOTES
    -----
    - The outputted table, which contains data from the sweep files, combines
      cross-matched objects from all relevant sweep files in the directory.
    - The function used here for finding relevant sweep files comes from
      a function in ASTR5160/weekly_tasks/week08/cross_matching.
    """
    
    #SD read in FIRST file and extract coords
    table = Table.read(datafile)
    coords = SkyCoord(table['RA'], table['DEC'], unit=u.deg)
    
    #SD find objects within circle centered at given center coords and with given radius
    mask = coords.separation(coords_center) < radius
    table_selected = table[mask]
    #SD extract coordinates of these objects
    coords_selected = coords[mask]
    
    #SD find which sweep files are necessary for cross-matching
    #SD running function from weekly_tasks/week08/cross_matching.py
    sweepfiles = sweep_func(table_selected['RA'], table_selected['DEC'], directory=sweepdir)
    
    #SD read in sweep files as astropy tables
    sweepfiles_long = [sweepdir + '/' + sf for sf in sweepfiles]
    table_sweeps = [Table.read(sfl) for sfl in sweepfiles_long]
    #SD only extract the necessary columns
    colnames = ['RA', 'DEC', 'FLUX_G', 'FLUX_R', 'FLUX_Z',
                'FLUX_W1', 'FLUX_W2', 'FLUX_W3', 'FLUX_W4']
    table_sweeps_shortened = [ts[colnames] for ts in table_sweeps]
    table_sweeps_all = vstack(table_sweeps_shortened)
    
    #SD extract coords from chosen sweep files
    coords_sweeps = SkyCoord(table_sweeps_all['RA'], table_sweeps_all['DEC'], unit=u.deg)
    #SD find indices of dataset and sweeps that correspond with each other
    id1, id2, d2, d3 = coords_sweeps.search_around_sky(coords_selected, match_radius)
    
    #SD remove duplicates in case cross-matching returns multiple objects that are within the matching radius
    id1_sorted, unique_idx = np.unique(id1, return_index=True)
    id2_sorted = id2[unique_idx]
    #SD again, but other way around
    id2_sorted, unique_idx = np.unique(id2_sorted, return_index=True)
    id1_sorted = id1_sorted[unique_idx]
    
    #SD cross-match betwen objects in datafile and the sweep files, using given matching radius
    table_selected_matched = table_selected[id1_sorted]
    table_sweeps_matched = table_sweeps_all[id2_sorted]
    
    return table_selected_matched, table_sweeps_matched



def r_W1minusW2_bounds(table_data, table_sweep, r_low, r_high, W1minusW2_low, W1minusW2_high):
    """Find objects that have r-band magnitudes and W1-W2 colors that are within the specified bounds.
    
    INPUTS
    ------
    table_data : :class:'astropy.table.table.Table'
        An astropy table of objects from which the relevant objects will be extracted.
    table_sweep : :class:'astropy.table.table.Table'
        An astropy table of objects from which the relevant objects will be extracted.
        This table corresponds to the first one, but has data from sweep files.
        This table should contain the r, W1, and W2 fluxes of the objects.
    r_low : :class:'int' or 'float'
        The lower bound of the desired range of r-band magnitudes.
    r_high : :class:'int' or 'float'
        The upper bound of the desired range of r-band magnitudes.
    W1minusW2_low : :class:'int' or 'float'
        The lower bound of the desired range of W1-W2 colors.
    W1minusW2_high : :class:'int' or 'float'
        The upper bound of the desired range of W1-W2 colors.
    
    RETURNS
    -------
    :class:'astropy.table.table.Table'
        Same as the first inputted table, but with only
        the objects whose r-band magnitudes and W1-W2 colors fall within the specified bounds.
    :class:'astropy.table.table.Table'
        Same as the second inputted table, but with only
        the objects whose r-band magnitudes and W1-W2 colors fall within the specified bounds.
    
    NOTES
    -----
    - The two inputted tables should have the same objects in them.
        - Ex: table1[0] and table2[0] correspond to one object,
          table1[1] and table2[1] correspond another object, etc.
    - If a specific bound is not required, set it to an unobtainable value like -100 or 100.
    """
    
    #SD extract fluxes from sweep files
    r_flux = table_sweep['FLUX_R']
    W1_flux = table_sweep['FLUX_W1']
    W2_flux = table_sweep['FLUX_W2']
    
    #SD create mask to only get objects for which all fluxes > 0
    #SD flux <= 0 means it wasn't detected in that band
    flux_mask = (r_flux > 0) & (W1_flux > 0) & (W2_flux > 0)
    
    #SD mask the tables and fluxes to remove values <= 0
    table_data = table_data[flux_mask]
    table_sweep = table_sweep[flux_mask]
    r_flux = r_flux[flux_mask]
    W1_flux = W1_flux[flux_mask]
    W2_flux = W2_flux[flux_mask]
    
    #SD get magnitudes from fluxes
    #SD fluxes are in units of nanomaggies
    r_mag = 22.5 - 2.5*np.log10(r_flux)
    W1_mag = 22.5 - 2.5*np.log10(W1_flux)
    W2_mag = 22.5 - 2.5*np.log10(W2_flux)
    #SD get W1-W2 color
    W1minusW2 = W1_mag - W2_mag
    
    #SD find objects that fall within given bounds for r mag and W1-W2 color
    obj_mask = (r_mag > r_low) & (r_mag < r_high) & (W1minusW2 > W1minusW2_low) & (W1minusW2 < W1minusW2_high)
    table_data_bounded = table_data[obj_mask]
    table_sweep_bounded = table_sweep[obj_mask]
    
    return table_data_bounded, table_sweep_bounded



def sdss_query_mags_single(ra, dec):
    """Sends an SQL command to the SDSS database and returns ugriz mags for the single specified object.
       Adapted from Dr. Adam Myers' sdssDR9query.py module.
    
    INPUTS
    ------
    ra : :class:'int' or 'float'
        The right ascension, in degrees, of the object for which the query is being run.
    dec : :class:'int' or 'float'
        The declination, in degrees, of the object for which the query is being run.
    
    RETURNS
    -------
    :class:'list'
        A list of values obtained from the query.
        Contains the following data: [ra (deg), dec (deg), u, g, r, i, z]
    
    NOTES
    -----
    - Most of the code was copied from Dr. Adam Myers' code,
      but I commented wherever I made my own changes/additions.
    - If the object is not found in the SDSS database, then the list is populated with -100 for each magnitude.
    """
    
    # ADM initialize the query.
    qry = sdssQuery()
    
    # ADM the query to be executed. You can substitute any query, here!
    #SD removed distance from query
    #SD need to convert inputs to str
    query = """SELECT top 1 ra,dec,u,g,r,i,z FROM PhotoObj as PT
    JOIN dbo.fGetNearbyObjEq(""" + str(ra) + """,""" + str(dec) + """,0.02) as GNOE
    on PT.objID = GNOE.objID ORDER BY GNOE.distance"""
    
    # ADM execute the query.
    qry.query = query
    for line in qry.executeQuery():
        result = line.strip()
    
    # ADM NEVER remove this line! It won't speed up your code, it will
    # ADM merely overwhelm the SDSS server (a denial-of-service attack)!
    sleep(1)

    # ADM the server returns a byte-type string. Convert it to a string.
    #SD used to be a print statement. now saving to varable
    output_str = result.decode()
    
    #SD convert str to a list
    #SD then convert each str in the list to a float
    #SD if output is 'No objects have been found', return list with unobtainably low values
    output_list = output_str.split(',')
    try:
        output_list_nums = [float(n) for n in output_list]
    except ValueError:
        output_list_nums = [ra, dec, -100, -100, -100, -100, -100]
    
    return output_list_nums



def sdss_query_mags_multiple(ras, decs):
    """Queries the SDSS database for an array of coordinates
       by running the function sdss_query_mags_single() for each set of coordinates passed.
    
    INPUTS
    ------
    ras : :class:'list' or 'numpy.ndarray' or 'astropy.table.column.Column'
        Right ascensions of objects to be queried.
    decs : :class:'list' or 'numpy.ndarray' or 'astropy.table.column.Column'
        Declinations of objects to be queried.
    
    OUTPUTS
    -------
    :class:'astropy.table.table.Table
        Astropy table containing the results of the query.
        Contains the following data: [ra (deg), dec (deg), u, g, r, i, z]
    
    NOTES
    -----
    - If an object is not found in the SDSS database, then that object's row in the table
      is populated with -100 for each magnitude.
    """
    
    #SD run sdss_query_single for each ra,dec that was passed
    #SD creates list of lists; each list is for an object
    output = [sdss_query_mags_single(ras[i], decs[i]) for i in range(len(ras))]
    
    #SD combine into a single array of arrays
    #SD this also makes the array the correct shape to turn into a table
    output_formatted = np.vstack(output)
    
    #SD convert list of lists to astropy table
    table = Table(output_formatted,
                    names=('RA', 'DEC', 'MAG_U', 'MAG_G', 'MAG_R', 'MAG_I', 'MAG_Z'))
    
    return table



if __name__=='__main__':
    
    #SD define variables
    filename = '/d/scratch/ASTR5160/data/first/first_08jul16.fits'
    sweepdir = '/d/scratch/ASTR5160/data/legacysurvey/dr9/north/sweep/9.0'
    c_center = SkyCoord(163, 50, unit=u.deg)
    
    #SD run the function to get objects within 3 deg of (163 deg, 50 deg)
    survey_table, sweeps_table = cross_match_mags(filename, c_center, 3*u.deg, sweepdir)
    
    #SD run the function to get objects with r mag < 22 and W1-W2 color > 0.5
    survey_table, sweeps_table = r_W1minusW2_bounds(survey_table, sweeps_table, r_low=-100, r_high=22,
                                        W1minusW2_low=0.5, W1minusW2_high=100)
    
    #SD print the number of objects (Problem 3)
    print(f"There are {len(sweeps_table)} objects in the survey with r < 22 and W1-W2 > 0.5.")
    
    #SD run the function to SQL query the SDSS database for u and i mags of the objects
    ugriz_table = sdss_query_mags_multiple(sweeps_table['RA'], sweeps_table['DEC'])
    
    #SD print number of objects that had a match in the SDSS database (Problem 5)
    num_matched = len(ugriz_table[ugriz_table['MAG_U'] > -100])
    percent_num_matched = 100 * num_matched/len(ugriz_table)
    print(f"{num_matched} of the {len(ugriz_table)} objects ({percent_num_matched:5.2f}%)",
            "had a match in the SDSS database")
    
    #SD mask all tables to remove object not found in the SDSS database
    sdss_mask = ugriz_table['MAG_U'] > -100
    survey_table = survey_table[sdss_mask]
    sweeps_table = sweeps_table[sdss_mask]
    ugriz_table = ugriz_table[sdss_mask]
    
    #SD find brightest object in u-band (Problem 6)
    u_mag = ugriz_table['MAG_U']
    ubrite1_mask = u_mag == np.min(u_mag)
    ubrite_survey_table = survey_table[ubrite1_mask]
    ubrite_sweeps_table = sweeps_table[ubrite1_mask]
    ubrite_ugriz_table = ugriz_table[ubrite1_mask]
    
    #SD find SDSS u and i mags of ubrite1
    u_mag_ubrite1 = ubrite_ugriz_table['MAG_U'][0]
    i_mag_ubrite1 = ubrite_ugriz_table['MAG_I'][0]
    
    #SD convert ubrite1 mags to fluxes (Problem 7)
    #SD fluxes are in units of nanomaggies
    u_flux_ubrite1 = 10 ** ((22.5 - u_mag_ubrite1) / 2.5)
    i_flux_ubrite1 = 10 ** ((22.5 - i_mag_ubrite1) / 2.5)
    
    #SD plot fluxes as a function of wavelength
    
    
    
    
    
    
    
