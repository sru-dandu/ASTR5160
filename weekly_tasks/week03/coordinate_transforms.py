from astropy.coordinates import SkyCoord, get_constellation
import numpy as np
from astropy.table import Table
from astropy import units as u
import matplotlib.pyplot as plt



### TASK 1 (RED) ###

#SD saving RA and DEC of Fomalhaut using SkyCoord
#SD coords obtained from Google
fomalhaut_coords = SkyCoord('22h57m39s', '-29d37m20s')

#SD saving RA and DEC (in radians)
#SD need radians in order to be used with np.cos and np.sin
fomalhaut_ra = fomalhaut_coords.ra.rad
fomalhaut_dec = fomalhaut_coords.dec.rad

#SD convert RA and DEC to cartesian coords
fomalhaut_coords.representation_type = "cartesian"

#SD printing the RA and DEC values, in radians
print("--------------")
print("### TASK 1 ###")
print("--------------")
print(f"The right ascension of Fomalhaut is {fomalhaut_ra} radians")
print(f"The declination of Fomalhaut is {fomalhaut_dec} radians")

#SD check conversions using equations from slides
#SD converting radians to cartesian
fomalhaut_x = np.cos(fomalhaut_ra) * np.cos(fomalhaut_dec)
fomalhaut_y = np.sin(fomalhaut_ra) * np.cos(fomalhaut_dec)
fomalhaut_z = np.sin(fomalhaut_dec)

#SD creating columns to make a table below
names = ['astropy', 'manual']
x_values = np.array([fomalhaut_coords.x, fomalhaut_x])
y_values = np.array([fomalhaut_coords.y, fomalhaut_y])
z_values = np.array([fomalhaut_coords.z, fomalhaut_z])

#SD creating table for manual and astropy conversions of cartesian coords
table = Table([names, x_values, y_values, z_values],
		names=[' ', 'x', 'y', 'z'])

print("CHECK:")
print("Check that converting to cartesian with astropy gives same result as manually converting:")
print(table)

print()



### TASK 2 (RED) ###

#SD save l and b of galactic center
gal_coords = SkyCoord(0*u.deg, 0*u.deg, frame='galactic')

#SD convert galactic coordinates to RA and DEC
#SD want RA in hms so that I can use constellation chart later
gal_coords_radec = gal_coords.icrs.to_string('hmsdms')

print("--------------")
print("### TASK 2 ###")
print("--------------")
print(f"The (RA, DEC) of the Galactic center is ({gal_coords_radec})")

#SD find constellation corresponding to galactic center
constellation = get_constellation(gal_coords)
print(f"The Galactic center is in the constellation {constellation}.")
print("Using the constellation chart, I concluded that the Galactic center is near the edge of the constellation.")

print()



### TASK 3 (RED) ###

#SD generate RA values from 0 to 24
laramie_ra = np.arange(0, 24, 0.01) * u.h

#SD declination of Laramie
laramie_dec = 40 * u.deg

#SD save RA and DEC as SkyCoord variable
laramie_coords = SkyCoord(laramie_ra, laramie_dec)

#SD convert RA and DEC coords to Galactic frame
laramie_coords_gal = laramie_coords.galactic

#SD extract l and b values from Galactic coords
laramie_coords_l = laramie_coords_gal.l.degree
laramie_coords_b = laramie_coords_gal.b.degree

#SD plotting b in terms of l
plt.plot(laramie_coords_l, laramie_coords_b)
plt.xlabel("l")
plt.ylabel("b")
plt.show()

print("--------------")
print("### TASK 3 ###")
print("--------------")
print("See plot")
print()



### TASK 4 (BLACK)###

#SD save RA and DEC values for sun, moon, and planets (and pluto)
#SD obtained from links on Canvas page
ss_ra =	['21h10m25s', '1h42m2s', '20h57m3.2s', '23h54m11.7s', '7h26m1.0s', '4h37m41.3s', '23h16m42.5s', '3h22m20.2s', '23h53m37.0s', '20h19m25.8s']
ss_dec = ['-16d17m35s', '13d3m42s', '-19d23m58s', '1d59m19s', '26d13m2s', '21d36m10s', '-6d44m29s', '18d15m58s', '-2d4m28s', '-22d59m15s']

#SD also need distances to find ecliptic coords
dist = np.array([0.9858111 , 1, 1.410, 0.501, 0.698, 4.587, 10.439, 19.390, 30.612, 36.151]) * u.AU

#SD use RAs, DECs, and distacnes to find ecliptic coords
ss_coords= SkyCoord(ss_ra, ss_dec, distance=dist).heliocentrictrueecliptic

#SD extract longitudes and latitudes from ecliptic coords
ss_lon = ss_coords.lon.degree
ss_lat = ss_coords.lat.degree

#SD plot ecliptic coords
colors = ['black', 'gray', 'sandybrown', 'darkkhaki', 'firebrick', 'orange', 'gold', 'darkturquoise', 'steelblue', 'tan']
plt.scatter(ss_lon, ss_lat, c=colors)
plt.xlabel("latitude")
plt.ylabel("longitude")

#SD label each point with object name
names = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']
for idx in range(len(names)):
	plt.annotate(names[idx], (ss_lon[idx]+5, ss_lat[idx]+0.1))

plt.show()

print("--------------")
print("### TASK 4 ###")
print("--------------")
print("See plot")
print()
