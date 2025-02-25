from astropy.coordinates import SkyCoord
from astropy.coordinates import EarthLocation
from astropy.table import Table
from astropy import units as u
import pandas
import numpy as np



#SD read in file and extract ra and dec
coords = pandas.read_csv('/d/scratch/ASTR5160/week4/HW1quasarfile.txt', header=None)[0]

#SD add spaces in order to get in format hh mm ss +dd mm ss
#SD this allows it to be read by SkyCoord
coords_parsed = [(i[0:2] + ' ' + i[2:4] + ' ' + i[4:9] + ' '
		+ i[9:12] + ' ' + i[12:14] + ' ' + i[14:]) for i in coords]

#SD pass coordinates through SkyCoord
coords_radec = SkyCoord(coords_parsed, unit=(u.hr, u.deg))

#SD convert ra and dec to deg
ra_deg = coords_radec.ra.deg
dec_deg = coords_radec.dec.deg
