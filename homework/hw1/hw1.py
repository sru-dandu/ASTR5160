from astropy.coordinates import SkyCoord, AltAz, EarthLocation
from astropy.table import Table
from astropy.time import Time
from astropy import units as u
import pandas
import numpy as np



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

###TESTING###
m = 3

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

#SD transform ra,dec coordinates to AltAz
ref_frame = AltAz(location=KPNO, obstime=time)
coords_altaz = coords.transform_to(ref_frame)

#SD convert alt,az to airmass
airmasses = coords_altaz.secz

print(airmasses)

