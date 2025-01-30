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
