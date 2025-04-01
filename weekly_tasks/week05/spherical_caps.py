import numpy as np
from astropy.coordinates import SkyCoord
from astropy import units as u



### TASK 1 (RED) ###

def cap_ra(ra_bound):
	"""Find the (x, y, z, 1-h) vector of the spherical cap bounded by a given right ascension.
	
	INPUTS
	------
	ra_bound : class: 'str' or 'astropy.units.quantity.Quantity'
		The right ascension that is the bound of the spherical cap.
		Must be in format acceptable by astropy.coordinates.SkyCoord().
	
	RETURNS
	-------
	class: 'numpy.ndarray'
		The 4-vector of the spherical cap bound by the given right ascension.
		In format (x, y, z, 1-h).
	"""
	#SD make SkyCoord object with given ra bound
	coords_bound = SkyCoord(ra_bound, 0*u.deg)
	
	#SD find ra corresponding to center of cap
	ra = coords_bound.ra + 90*u.deg
	
	#SD create SkyCoord object
	coords = SkyCoord(ra, 0*u.deg)
	
	#SD convert given coords to cartesian
	coords = coords.cartesian
	
	#SD create vector 4-array for cap
	#SD if cap is bound by ra, then 1-h=1
	vector = np.array([coords.x, coords.y, coords.z, 1])
	
	return vector



### TASK 2 (RED) ###

def cap_dec(dec_bound):
	"""Find the (x, y, z, 1-h) vector of the spherical cap bounded by a given declination.
	
	INPUTS
	------
	dec_bound : class: 'str' or 'astropy.units.quantity.Quantity'
		The declination that is the bound of the spherical cap.
		Must be in format acceptable by astropy.coordinates.SkyCoord().
	
	RETURNS
	-------
	class: 'numpy.ndarray'
		The 4-vector of the spherical cap bound by the given declination.
		In format (x, y, z, 1-h).
	"""
	#SD make SkyCoord object with given dec bound
	coords_bound = SkyCoord(0*u.deg ,dec_bound)
	
	#SD find 1-h from given dec
	one_minus_h = 1 - np.sin(coords_bound.dec)
	
	#SD convert center of cap = (0 deg, 90 deg) to cartesian
	coords = SkyCoord(0, 90, unit=u.deg).cartesian
	
	#SD create vector 4-array for cap
	vector = np.array([coords.x, coords.y, coords.z, one_minus_h])
	
	return vector



### TASK 3 (RED) ###

def cap_coords(coords, r):
	"""Find the (x, y, z, 1-h) vector of the spherical cap of given radius centered on given coordinates.
	
	INPUTS
	------
	coords : class: 'astropy.coordinates.sky_coordinate.SkyCoord'
		The coordinates at the center of the spherical cap.
		Must be a astropy.coordinates.SkyCoord() object.
	r : class: 'int', 'float', 'astropy.units.quantity.Quantity'
		The angular radius of the spherical cap
		If not passed as astropy Quantity object, must be in units of radians
	
	RETURNS
	-------
	class: 'numpy.ndarray'
		The 4-vector of the spherical cap of given radius centered on given coordinates.
		In format (x, y, z, 1-h).
	"""
	#SD convert coordinates to cartesian
	coords = coords.cartesian
	
	#SD find 1-h from radius
	one_minus_h = 1 - np.cos(r)
	
	#SD create vector 4-array for cap
	vector = np.array([coords.x, coords.y, coords.z, one_minus_h])
	
	return vector



### TASK 4 (BLACK) ###

def caps_to_file(cap1, cap2, cap3):
	"""Saves the given spherical cap vectors to a file.
	
	INPUTS
	------
	cap1 : class: 'np.ndarray'
		The vector of a spherical cap.
		Must be in format [(x, y, z, 1-h)].
	cap2 : class: 'np.ndarray'
		The vector of a spherical cap.
		Must be in format [(x, y, z, 1-h)].
	cap3 : class: 'np.ndarray'
		The vector of a spherical cap.
		Must be in format [(x, y, z, 1-h)].
	
	RETURNS
	-------
	file
		A file with the given spherical cap vectors saved to it.
	"""
	#SD extract values from vectors
	x1, y1, z1, one_minus_h1 = cap1
	x2, y2, z2, one_minus_h2 = cap2
	x3, y3, z3, one_minus_h3 = cap3
	
	#SD write the strings to be saved to file
	#SD :19.16f forces number to be printed as a float with
		#SD 16 decimal places
		#SD total length of 19 (including spaces)
	contents = ["1 polygons\n",
			"polygon 1 ( 3 caps, 1 weight, 0 pixel, 0 str):\n",
			f"\t{x1:19.16f} {y1:19.16f} {z1:19.16f} {one_minus_h1:19.16f}\n",
			f"\t{x2:19.16f} {y2:19.16f} {z2:19.16f} {one_minus_h2:19.16f}\n",
			f"\t{x3:19.16f} {y3:19.16f} {z3:19.16f} {one_minus_h3:19.16f}"]
	
	#SD create file and write to it
	with open("cap-vectors-file.txt", "w") as f:
		f.writelines(contents)
	
	return




if __name__ == '__main__':
	
	#SD define the values used for this lecture's tasks
	ra = '5h'
	dec = 36 * u.deg
	coords = SkyCoord(ra, dec)
	radius = 1 * u.deg
	
	#SD force values to print as decimals instead of in scientific notation
	#SD this only affects print statements ; actual values in code are unchanged
	np.set_printoptions(suppress=True)
	
	#SD answer for Task 1
	c1 = cap_ra(ra)
	print("Task 1:", c1)
	print('----------')
	
	#SD answer for Task 2
	c2 = cap_dec(dec)
	print("Task 2:", c2)
	print('----------')
	
	#SD answer for Task 3
	c3 = cap_coords(coords, radius)
	print("Task 3:", c3)
	print('----------')
	
	#SD answer for Task 4
	caps_to_file(c1, c2, c3)
	print("Task 4: written to file")
	print('----------')
