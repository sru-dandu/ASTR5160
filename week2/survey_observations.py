from astropy.coordinates import SkyCoord
from astropy.time import Time
import numpy as np

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
