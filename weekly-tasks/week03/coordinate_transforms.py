from astropy.coordinates import SkyCoord



### TASK 1 (RED)

#SD saving RA and DEC of Fomalhaut using SkyCoord
#SD coords obtained from Google
fomalhaut_coords = SkyCoord('22h57m39s', '-29d37m20s')

#SD saving RA and DEC (in degrees)
fomalhaut_ra = fomalhaut_coords.ra.deg
fomalhaut_dec = fomalhaut_coords.dec.deg

#SD convert RA and DEC to cartesian coords
fomalhaut_coords.representation_type = "cartesian"

#SD printing the resulting values
print(fomalhaut_ra)
print(fomalhaut_dec)
print(fomalhaut_coords)
