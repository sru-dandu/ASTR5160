from astropy.table import Table, vstack
from astropy.coordinates import SkyCoord
from astropy import units as u
import numpy as np
#SD import a function I previously wrote
from weekly_tasks.week08.cross_matching import sweep_func



def cross_match(file, coords_center, radius, sweepdir, match_radius=1*u.arcsec):
    """Finds objects in a data file within some circular area, and
    cross-matches them with objects from sweep files.
    
    INPUTS
    ------
    file : :class:'str'
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
    - The second outputted table, which contains objects from the sweep files, combines
      cros-matched objects from all relevant sweep files in the directory.
    - The function used here for finding relevant sweep files comes from
      a function in ASTR5160/weekly_tasks/week08/cross_matching.
    """
    
    #SD read in FIRST file and extract coords
    table = Table.read(file)
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
    
    #SD cross-match betwen objects in datafile and the sweep files, using given matching radius
    table_selected_matched = table_selected[id1]
    table_sweeps_matched = table_sweeps_all[id2]
    
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
        This table should have the r, W1, and W2 fluxes of the objects.
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



if __name__=='__main__':
    
    #SD define variables
    filename = '/d/scratch/ASTR5160/data/first/first_08jul16.fits'
    sweepdir = '/d/scratch/ASTR5160/data/legacysurvey/dr9/north/sweep/9.0'
    c_center = SkyCoord(163, 50, unit=u.deg)
    
    #SD run the function to get objects within 3 deg of (163 deg, 50 deg)
    table_survey, table_sweeps = cross_match(filename, c_center, 3*u.deg, sweepdir)
    
    #SD run the function to get objects with r mag < 22 and W1-W2 color > 0.5
    table_survey, table_sweeps = r_W1minusW2_bounds(table_survey, table_sweeps,
                                                    r_low=-100, r_high=22,
                                                    W1minusW2_low=0.5, W1minusW2_high=100)
    
    
    
    
    
