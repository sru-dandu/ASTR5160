import numpy as np
from astropy.coordinates import SkyCoord
from astropy import units as u
import matplotlib.pyplot as plt



### TASK 1 (RED) ###

#SD saving coordinates in SkyCoord
ra1 = 263.75 * u.deg
dec1 = -17.9 * u.deg

ra2 = '20h24m59.9s'
dec2 = '10d6m0s'

coord1 = SkyCoord(ra1, dec1)
coord2 = SkyCoord(ra2, dec2)

#SD need to have coords in Cartesian coords
coord1_cart = coord1.cartesian
coord2_cart = coord2.cartesian

#SD find angle using dot product:
#SD a_vector * b_vector = |a||b|cos(zenith angle), where
	#SD a_vector * b_vector = x1x2 + y1y2 + z1z2
	#SD |a| = (x1^2 + y1^2 + z1^2)^(1/2)
dot_prod = coord1_cart.x*coord2_cart.x + coord1_cart.y*coord2_cart.y + coord1_cart.z*coord2_cart.z
mag1 = (coord1_cart.x**2 + coord1_cart.y**2 + coord1_cart.z**2)**(1/2)
mag2 = (coord2_cart.x**2 + coord2_cart.y**2 + coord2_cart.z**2)**(1/2)

z_angle = np.arccos(dot_prod / (mag1 * mag2))

#SD check using SkyCoord's "separation" method
z_angle_check = coord1.separation(coord2).rad

print("TASK 1:")
print(f"The zenith angle (found manually) is {z_angle}")
print("check:")
print(f"The zenith angle (found using SkyCoord's 'separation' method) is {z_angle_check}")



### TASK 2 (RED) ###

#SD find 2 sets of 100 ra values between 2 hr and 3 hr
ra_array1 = (np.random.random(100) + 2) * u.hour
ra_array2 = (np.random.random(100) + 2) * u.hour

#SD find 2 sets of 100 dec values between -2 deg and 2 deg
dec_array1 = (4*np.random.random(100) - 2) * u.deg
dec_array2 = (4*np.random.random(100) - 2) * u.deg

#SD save ra and dec values into SkyCoord objects
coord_array1 = SkyCoord(ra_array1, dec_array1)
coord_array2 = SkyCoord(ra_array2, dec_array2)

#SD creating defined function for plotting
#SD in order to specify whether or not to highlight short separations
def plot_func(c1, c2, sep=None):
	"""Plots two sets of coordinates in a scatterplot.
	
	PARAMETERS
	----------
	c1 : :class:`astropy.coordinates.sky_coordinate.SkyCoord`
		SkyCoord object containing coordinates in (ra, dec)
	c2 : :class:`astropy.coordinates.sky_coordinate.SkyCoord`
		SkyCoord object containing coordinates in (ra, dec)
	sep : :class:`astropy.units.quantity.Quantity`, optional, defaults to None
		If given, also plots points that have the given separation value
	
	RETURNS
	-------
	matplotlib popup window
	"""
	
	#SD extract ra and dec from given coordinates
	ra1 = c1.ra.hour
	dec1 = c1.dec.deg
	ra2 = c2.ra.hour
	dec2 = c2.dec.deg
	
	#SD find coordinates that have the specified separation angle or less
	if sep is not None:
		id1, id2, d2, d3 = c2.search_around_sky(c1, sep)
		ra1_close = ra1[id1]
		dec1_close = dec1[id1]
		ra2_close = ra2[id2]
		dec2_close = dec2[id2]
	
	#SD plotting dec vs ra for both sets of coordinates
	plt.scatter(ra1, dec1, marker='o', c='steelblue', label='set 1')
	plt.scatter(ra2, dec2, marker='x', c='maroon', label='set 2')

	#SD plotting the points with specified separation angle or less
	if sep is not None:
		plt.scatter(ra1_close, dec1_close, marker='o', c='gold',
			label="set 1, with 10' separation from set 2")
		plt.scatter(ra2_close, dec2_close, marker='x', c='gold',
			label="set 2, with 10' separation from set 1")
	
	plt.xlabel("ra [hours]")
	plt.ylabel("dec [degrees]")
	plt.legend()
	plt.show()
	
	return



#SD use defined function to create plot
plot_func(coord_array1, coord_array2)

print("TASK 2:")
print("See plot")



### TASK 3 (RED) ###

#SD using defined function again
#SD but this time specifying separation of 10 arcmin
plot_func(coord_array1, coord_array2, sep=10*u.arcmin)

print("TASK 3:")
print("See plot")



### TASK 4 (BLACK) ###

#SD making defined function for plotting
#SD in order to specify whether or not to highlight certain point
def plot_func2(coord, plate_coord=None, plate_r=None):
	"""Plots a set of coordinates in a scatterplot.
	
	PARAMETERS
	----------
	coord : :class:`astropy.coordinates.sky_coordinate.SkyCoord`
		(RA, DEC) coordinates to be plotted
	plate_coord : :class:`astropy.coordinates.sky_coordinate.SkyCoord`, optional, defaults to None
		If given, highlights the points that will fall
		on a spectroscopic plate placed at the given coordinates
	plate_r : :class:`astropy.units.quantity.Quantity`, optional, defaults to None
		If given, highlights the points that will fall
		on a spectroscopic plate of given radius
	
	RETURNS
	-------
	matplotlib popup window
	"""
	
	#SD extracting RA (in hours) and DEC (in deg) from SkyCoord coorinates
	ra = coord.ra.hour
	dec = coord.dec.deg
	
	#SD plotting the new arrays
	plt.scatter(ra, dec, label='coordinates')
	
	if plate_coord and plate_r is not None:
		
		#SD find which points fall on plate
		mask = plate_coord.separation(coord) < plate_r
		coords_on_plate = coord[mask]
		
		#SD extract RA (in hours) and DEC (in deg) of coords on plate
		ras_plate = coords_on_plate.ra.hour
		decs_plate = coords_on_plate.dec.deg
		
		#SD plot the points on the plate in a different color
		plt.scatter(ras_plate, decs_plate, c='gold',
			label='coordinates falling on plate')
	
	#SD in case only one of the plate's parameters is given
	elif plate_coord or plate_r is not None:
		print("WARNING: Mising an input;",
			"resulting plot will not have highlighted points.")
	
	plt.xlabel('ra [hours]')
	plt.ylabel('dec [degrees]')
	plt.legend()
	plt.show()
	
	return



#SD combining ra and dec arrays, and saving in SkyCoord object
ra_tot = np.concatenate([ra_array1, ra_array2])
dec_tot = np.concatenate([dec_array1, dec_array2])
coord_tot = SkyCoord(ra_tot, dec_tot)

#SD plot DECs va RAs
plot_func2(coord_tot)

print("TASK 4:")
print("See plot")



### TASK 5 (BLACK) ###

#SD save radius and coordinates of plate
plate_radius = 1.8 * u.deg
plate_coord = SkyCoord('2h20m5s', '-0d6m12s')

#SD plot coordinates, and highlight ones falling on plate
plot_func2(coord_tot, plate_coord, plate_radius)

print("TASK 5:")
print("See plot")
