from astropy.table import Table, vstack
from astropy.coordinates import SkyCoord
from astropy import units as u
#SD import a function I previously wrote
from weekly_tasks.week08.cross_matching import sweep_func



def cross_match(file, coords_center, radius, sweepdir, match_radius=1*u.arcsec):
    
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
    #SD extract coords from chosen sweep files
    coords_sweeps = [SkyCoord(ts['RA'], ts['DEC'], unit=u.deg) for ts in table_sweeps]
    
    #SD find indices of dataset and sweeps that correspond with each other
    id1 = [sweep.search_around_sky(coords_selected, match_radius)[0] for sweep in coords_sweeps]
    id2 = [sweep.search_around_sky(coords_selected, match_radius)[1] for sweep in coords_sweeps]
    
    #SD cross-match betwen objects in datafile and the sweep files, using given matching radius
    table_selected_matched = [table_selected[id1[i]] for i in range(len(id1))]
    table_sweeps_matched = [table_sweeps[i][id2[i]] for i in range(len(id2))]
    
    return [len(c) for c in table_selected_matched]



if __name__=='__main__':
    
    #SD define variables
    filename = '/d/scratch/ASTR5160/data/first/first_08jul16.fits'
    sweepdir = '/d/scratch/ASTR5160/data/legacysurvey/dr9/north/sweep/9.0'
    c_center = SkyCoord(163, 50, unit=u.deg)
    
    #SD run the function to get objects within 3 deg of (163 deg, 50 deg)
    print(cross_match(filename, c_center, 3*u.deg, sweepdir))
    
    
