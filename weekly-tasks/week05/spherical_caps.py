import numpy as np
from astropy.coordinates import SkyCoord
from astropy import units as u



### TASK 1 (RED) ###

def cap_ra(ra_bound):
	
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




if __name__ == '__main__':
	
	#SD answer for Task 1
	print("Task 1:", cap_ra('5h'))
