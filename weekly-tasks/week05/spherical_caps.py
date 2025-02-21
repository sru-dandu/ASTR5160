import numpy as np
from astropy.coordinates import SkyCoord
from astropy import units as u



### TASK 1 (RED) ###

def cap_ra(ra_bound):
	"""Find the (x, y, z, 1-h) vector of the spherical cap bounded by a given ra."
	
	INPUTS
	------
	ra : class: 'str' or 'astropy.units.quantity.Quantity'
		The right ascension that is the bound of the spherical cap.
		Must be in format acceptable by astropy.coordinates.SkyCoord().
	
	RETURNS
	-------
	class: 'numpy.ndarray'
		The 4-vector of the spherical cap bound by the given RA.
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
	
	#SD make SkyCoord object with given dec bound
	coords_bound = SkyCoord(0*u.deg ,dec_bound)
	
	#SD find 1-h from given dec
	one_minus_h = 1 - np.sin(coords_bound.dec)
	
	#SD convert center of cap = (0 deg, 90 deg) to cartesian
	coords = SkyCoord(0, 90, unit=u.deg).cartesian
	
	#SD create vector 4-array for cap
	vector = np.array([coords.x, coords.y, coords.z, one_minus_h])
	
	return vector




if __name__ == '__main__':
	
	#SD answer for Task 1
	print("Task 1:", cap_ra('5h'))
	print('----------')
	
	#SD answer for Task 1
	print("Task 2:", cap_dec(36*u.deg))
	print("(The x coordinate is very small so we can approximate it to 0. This would give us the correct answer.)")
	print('----------')
