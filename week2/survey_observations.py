from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time
import numpy as np
import astropy.units as u

### TASK 2 (RED) ###

# SD saving RA and DEC of the object Fomalhaut
   # SD coords obtained from Google
fomalhaut_ra = '22h57m39s'
fomalhaut_dec = '-29d37m20s'

# SD saving fomalhaut's coordinates to single variable using SkyCoord
fomalhaut_coords = SkyCoord(fomalhaut_ra, fomalhaut_dec)

# SD printing the RA and DEC, in both their original units and in degrees
print("---TASK 2---")
print(f"Fomalhaut's declination is {fomalhaut_dec}, or {fomalhaut_coords.dec.deg} degrees.")
print(f"Fomalhaut's right ascension is {fomalhaut_ra}, or {fomalhaut_coords.ra.deg} degrees.")

# SD converting the original coords to degrees using the equations from the notes
fomalhaut_ra_check = 15 * (22 + 57/60 + 39/3600)
fomalhaut_dec_check = -1 * (29 + 37/60 + 20/3600)

# SD comparing manual coord conversion to SkyCoord's conversion
print('CHECK:')
print(f"Declination: SkyCoord = {fomalhaut_coords.dec.deg} ; Manual conversion = {fomalhaut_dec_check}.")
print(f"Right Ascension: SkyCoord = {fomalhaut_coords.ra.deg} ; Manual conversion = {fomalhaut_ra_check}.")



### TASK 3 (RED) ###

# SD obtained today's JD and MJD
jd_now = Time.now().jd
mjd_now = Time.now().mjd

# SD printed the JD and MJD
print("---TASK 3---")
print(f"Current time in JD = {jd_now}")
print(f"Current time in MJD = {mjd_now}")

# SD check that JD - MJD = 2400000.5 (from notes)
print("CHECK:")
print(f"From Time.now(): JD - MJD = {jd_now - mjd_now}")
print("From notes: JD - MJD = 2400000.5")



### TASK 4 (RED) ###

# SD finding MJDs 4 days before and after today's MJD
MJD_array = np.arange(mjd_now-4, mjd_now+5, 1)

# SD printing the MJDs
print("---TASK 4---")
print("Range of MJDs from 4 days before today to 4 days after today:")
print(MJD_array)



### TASK 5 (BLACK) ###

# SD saved location of WIRO using EarthLocation
WIRO_lon = '-105d58m33s'   # SD EarthLocation treats eastward as positive, hence westward longitudes need negative
WIRO_lat = '41d5m49s'
WIRO_alt = 2943 * u.m   # SD seems like u.m is not needed (answer is same regardless of its inclusion)
WIRO_loc = EarthLocation(lat=WIRO_lat, lon=WIRO_lon, height=WIRO_alt)

# SD printing EarthLocation for WIRO
print("---TASK 5---")
print(f"The geodetic location of WIRO is {WIRO_loc}")   # SD geodetic is for input of lon, lat, height (from EarthLocation documentation)



### TASK 6 (BLACK) ###

# SD saving coords of object
obj_ra = 12 * u.h
obj_dec = 30 * u.deg
obj_coords = SkyCoord(ra=obj_ra, dec=obj_dec)

# SD finding time of observation
utcoffset = -7 * u.h   # SD MST is 7 hours behind UTC
time_today = Time("2025-1-30 23:00:00") - utcoffset   # SD if observing tonight at 11 PM
time_1month = Time("2025-3-1 23:00:00") - utcoffset   # SD if observing 1 month (30 days) from today, at 11 PM

# SD find Alt,Az coordinates of object as observed from WIRO at the mentioned times
obj_altaz_today = obj_coords.transform_to(AltAz(obstime=time_today, location=WIRO_loc))
obj_altaz_1month = obj_coords.transform_to(AltAz(obstime=time_1month, location=WIRO_loc))

# SD convert alt,az to airmass
obj_airmass_today = obj_altaz_today.secz
obj_airmass_1month = obj_altaz_1month.secz

# SD printing the airmasses
print("---TASK 6---")
print(f"The airmass of the object tonight at 11 PM is {obj_airmass_today}")
print(f"The airmass of the object 1 month from now at 11 PM is {obj_airmass_1month}")
