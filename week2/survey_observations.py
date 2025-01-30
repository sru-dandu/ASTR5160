from astropy.coordinates import SkyCoord

### TASK 2 (RED) ###

# SD saving RA and DEC of the object Fomalhaut
   # SD coords obtained from Google
fomalhaut_ra = '22h57m39s'
fomalhaut_dec = '-29d37m20s'

# SD saving fomalhaut's coordinates to single variable using SkyCoord
fomalhaut_coords = SkyCoord(fomalhaut_ra, fomalhaut_dec)

# SD printing the RA and DEC, in both their original units and in degrees
print(f"Fomalhaut's declination is {fomalhaut_dec}, or {fomalhaut_coords.dec.deg} degrees.")
print(f"Fomalhaut's right ascension is {fomalhaut_ra}, or {fomalhaut_coords.ra.deg} degrees.")

# SD converting the coords to degrees using the equations from the notes
fomalhaut_ra_check = 15 * (22 + 57/60 + 39/3600)
fomalhaut_dec_check = -1 * (29 + 37/60 + 20/3600)

# SD comparing manual coord conversion to SkyCoord's conversion
print('CHECK:')
print(f"Declination: SkyCoord = {fomalhaut_coords.dec.deg} ; Manual conversion = {fomalhaut_dec_check}.")
print(f"Right Ascension: SkyCoord = {fomalhaut_coords.ra.deg} ; Manual conversion = {fomalhaut_ra_check}.")
