from astropy.coordinates import SkyCoord, AltAz, EarthLocation
from astropy.table import Table
from astropy.time import Time
from astropy import units as u
import pandas
import numpy as np
import argparse



def hw1_func(m):
	"""Creates an astropy table for a given month.
	Each entry in the table is a day of the given month at 11pm MST,
	and shows the quasar with the best airmass at that day/time.
	
	PARAMETERS
	----------
	m : :class:'int'
		The value corresponding to a month of this year.
	
	RETURNS
	-------
	:class:'astropy.table.table.Table'
		A table with the following columns:
		Date, Quasar Coordinates (hms.ss deg'"),
		RA (deg), DEC (deg), Airmass
	
	NOTES
	-----
	- Quasar data from '/d/scratch/ASTR5160/week4/HW1quasarfile.txt'
	"""
	
	#SD read in file and extract ra and dec
	coords_data = pandas.read_csv('/d/scratch/ASTR5160/week4/HW1quasarfile.txt', header=None)[0]
	
	#SD add spaces in order to get in format hh mm ss +dd mm ss
	#SD this allows it to be read by SkyCoord
	coords_parsed = [(i[0:2] + ' ' + i[2:4] + ' ' + i[4:9] + ' '
			+ i[9:12] + ' ' + i[12:14] + ' ' + i[14:]) for i in coords_data]
	
	#SD pass coordinates through SkyCoord
	coords = SkyCoord(coords_parsed, unit=(u.hr, u.deg))
		
	#SD convert ra and dec to deg
	ra_deg = coords.ra.deg
	dec_deg = coords.dec.deg
	
	
	
	#SD make range of dates for the months
	days28 = np.arange(1, 29)
	days30 = np.arange(1, 31)
	days31 = np.arange(1, 32)

	#SD save strings of date and time, in MST
	if m==2:
		time_mst = [f"2025-{m}-{d} 23:00:00" for d in days28]
	elif m in [1,3,5,7,8,10,12]:
		time_mst = [f"2025-{m}-{d} 23:00:00" for d in days31]
	elif m in [4,6,9,11]:
		time_mst = [f"2025-{m}-{d} 23:00:00" for d in days30]
		
	#SD finding time of observation
	#SD MST is 7 hrs behind UTC, so add 7 to MST time to get UTC time
	time = Time(time_mst) + 7*u.hr
	
	
	
	#SD get coordinates of Kitt Peak
	KPNO = EarthLocation.of_site('kpno')
	
	#SD find best airmass for each date
	airmass_best = []
	airmass_idx = []
	for i in time:
		#SD transform ra,dec coordinates to AltAz
		ref_frame = AltAz(location=KPNO, obstime=i)
		coords_altaz = coords.transform_to(ref_frame)
		
		#SD find best airmass for each day
		airmass = coords_altaz.secz
		best = np.min(airmass[airmass >= 0])
		airmass_best.append(best)
		
		#SD save the indexes of these airmasses
		idx = np.where(airmass == best)[0][0]
		airmass_idx.append(idx)
	
	#SD find corresponding obj coordinates, ra, and dec for each airmass
	coords_data_best = [coords_data[idx] for idx in airmass_idx]
	ra_best = [ra_deg[idx] for idx in airmass_idx]
	dec_best = [dec_deg[idx] for idx in airmass_idx]
	
	#SD create astropy table
	#SD \u00B0 is unicode for degree symbol
	table = Table([time_mst, coords_data_best, ra_best, dec_best, airmass_best],
		names=("Date", "Quasar Coordinates (hms.ss \u00B0'\")", "RA (\u00B0)", "DEC (\u00B0)", "Airmass"))
	
	
	return table



if __name__ == '__main__':
	
	#SD description when passing -h
	parser = argparse.ArgumentParser(description="""Takes input of a given month, and
	creates an astropy table for that month.
	Each entry in the table is a day of the given month at 11pm MST,
	and shows the quasar with the best airmass at that day/time.""")
	
	#SD args that have to be passed
	parser.add_argument("month", type=int,
			help="['int'] integer value corresponding to a month of this year")
	args = parser.parse_args()
	
	#SD call the function
	table = hw1_func(args.month)
	print(table)
