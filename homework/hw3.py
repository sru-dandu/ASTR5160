from astropy.table import Table
from astropy.coordinates import SkyCoord
from astropy import units as u

#SD import a function I previously wrote
from weekly_tasks.week08.cross_matching import sweep_func



def object_extractor(file, coords_center, radius):
    
    #SD read in FIRST file and extract coords
    table = Table.read(file)
    coords = SkyCoord(table['RA'], table['DEC'], unit=u.deg)
    
    #SD find objects within circle centered at given center coords and with given radius
    mask = coords.separation(coords_center) < radius
    table_survey = table[mask]
    
    #SD find which sweep files are necessary for cross-matching
    sweeps_dir = '/d/scratch/ASTR5160/data/legacysurvey/dr9/north/sweep/9.0'
    sweepfiles = sweep_func(table_survey['RA'], table_survey['DEC'], directory=sweeps_dir)
    
    #SD read in sweep files as astropy tables
    sweepfiles_long = [sweeps_dir + '/' + sf for sf in sweepfiles]
    table_sweeps = [Table.read(sfl) for sfl in sweepfiles_long]
    
    return sweepfiles



if __name__=='__main__':
    
    #SD run the function to get objects within 3 deg of (163 deg, 50 deg)
    filename = '/d/scratch/ASTR5160/data/first/first_08jul16.fits'
    c_center = SkyCoord(163, 50, unit=u.deg)
    print(object_extractor(filename, c_center, 3*u.deg))
    
    
