from astropy.table import Table
from astropy.coordinates import SkyCoord
from astropy import units as u


def main():
    #SD read in FIRST file and extract coords
    table = Table.read('/d/scratch/ASTR5160/data/first/first_08jul16.fits')
    coords = SkyCoord(table['RA'], table['DEC'], unit=u.deg)
    
    #SD find objects within 3 deg of (163 deg, 50 deg)
    coords_center = SkyCoord(163, 50, unit=u.deg)
    mask = coords.separation(coords_center) < 3*u.deg
    table_survey = table[mask]
    
    return table_survey

if __name__=='__main__':
	print(main())
