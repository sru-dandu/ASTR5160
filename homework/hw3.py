from astropy.table import Table
from astropy.coordinates import SkyCoord
from astropy import units as u



def object_extractor(file, coords_center, radius):
    
    #SD read in FIRST file and extract coords
    table = Table.read('/d/scratch/ASTR5160/data/first/first_08jul16.fits')
    coords = SkyCoord(table['RA'], table['DEC'], unit=u.deg)
    
    #SD find objects within 3 deg of (163 deg, 50 deg)
    mask = coords.separation(coords_center) < radius
    table_survey = table[mask]
    
    return table_survey



if __name__=='__main__':
    
    filename = '/d/scratch/ASTR5160/data/first/first_08jul16.fits'
    c_center = SkyCoord(163, 50, unit=u.deg)
    print(object_extractor(filename, c_center, 3*u.deg))
