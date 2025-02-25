from astropy import units as u
import numpy as np
from numpy.random import random
import pymangle
import matplotlib.pyplot as plt
import sys

#SD use sys to add week05 to system path
#SD this way, I can import from week 5's tasks while keeping week 6's tasks separate
sys.path.insert(0, '/d/users/srujan/ASTR5160/weekly-tasks/week05')

#SD importing from week05
from spherical_caps import cap_ra, cap_dec



### TASK 1 (RED) ###

#SD defined function that takes two ra and two dec values and gives contents of Mangle file
def Mangle_contents(ra1, ra2, dec1, dec2):
	"""Takes 2 ra and 2 dec values, and writes the contents of a Mangle file.
	File consists of the vectors of 4 caps, each one bounded by a given value.
	Also gives the area of the resulting lat-lon rectangle.
	
	INPUTS
	------
	ra1 : class: 'astropy.units.quantity.Quantity'
		The ra bound of the first spherical cap.
		Must be in units of hours.
	ra2 : class: 'astropy.units.quantity.Quantity'
		The ra bound of the second spherical cap.
		Must be in units of hours.
	dec1 : class: 'astropy.units.quantity.Quantity'
		The dec bound of the third spherical cap.
		Must be in angular units.
	dec2 : class: 'astropy.units.quantity.Quantity'
		The dec bound of the fourth spherical cap.
		Must be in angular units.
	
	RETURNS
	-------
	class: 'str'
		The contents of a Mangle file.
		Has one polygon made up of 4 caps.
		Each cap is constrained by one of the given bounds.
	class: 'numpy.float64'
		The area (in str) of the lat-lon rectangle resulting from the 4 caps.
	"""
	
	#SD find area of lat-lon rectangle, in units of str
	ra1_rad = ra1 * (2*np.pi*u.rad) / (24*u.hr)
	ra2_rad = ra2 * (2*np.pi*u.rad) / (24*u.hr)
	area = (ra2_rad - ra1_rad) * (np.sin(dec2) - np.sin(dec1))
	
	#SD use week05 code to find 4-vectors of the caps
	vector_ra1 = cap_ra(ra1)
	vector_ra2 = cap_ra(ra2)
	vector_dec1 = cap_dec(dec1)
	vector_dec2 = cap_dec(dec2)
	
	#SD extract values from vectors
	x1, y1, z1, one_minus_h1 = vector_ra1
	x2, y2, z2, one_minus_h2 = vector_ra2
	x3, y3, z3, one_minus_h3 = vector_dec1
	x4, y4, z4, one_minus_h4 = vector_dec2

	#SD write the string to be saved to intersection.ply
	filestring = [f"\t{x1:19.16f} {y1:19.16f} {z1:19.16f} {one_minus_h1:19.16f}\n",
			f"\t{x2:19.16f} {y2:19.16f} {z2:19.16f} {one_minus_h2:19.16f}\n",
			f"\t{x3:19.16f} {y3:19.16f} {z3:19.16f} {one_minus_h3:19.16f}\n",
			f"\t{x4:19.16f} {y4:19.16f} {z4:19.16f} {one_minus_h4:19.16f}"]
	
	return filestring, area.value


#SD run the defined function with given ra and dec bounds
contents1, area1 = Mangle_contents(5*u.hr, 6*u.hr, 30*u.deg, 40*u.deg)

#SD create files and write to them
with open("masking-vectors.ply", "w") as f:
	f.write("1 polygons\n")
	f.write(f"polygon 1 ( 4 caps, 1 weight, 0 pixel, {area1} str):\n")
	f.writelines(contents1)

print('TASK 1:')
print(f"The area of the lat-lon rectangle is {area1} str.")
print("Vectors written to file.")
print('----------')



### TASK 2 (RED) ###

#SD run the defined function with given ra and dec bounds
contents2, area2 = Mangle_contents(11*u.hr, 12*u.hr, 60*u.deg, 70*u.deg)

#SD rewrite existing file to have 2 polygons
with open("masking-vectors.ply", "w") as f:
	f.write("2 polygons\n")
	f.write(f"polygon 1 ( 4 caps, 1 weight, 0 pixel, {area1} str):\n")
	f.writelines(contents1)
	f.write('\n')
	f.write(f"polygon 2 ( 4 caps, 1 weight, 0 pixel, {area2} str):\n")
	f.writelines(contents2)

print('TASK 2:')
print(f"The area of the lat-lon rectangle is {area2} str.")
print("Vectors written to file.")
print('----------')



### TASK 3 (BLACK) ###

#SD generate 1e6 random coordinates that equally populate sphere surface
ra_rand = 360.*(random(1*10**6))
dec_rand = (180/np.pi) * np.arcsin(1 - 2*random(1*10**6))

print('TASK 3:')
print("1e6 random coordinates created.")
print('----------')



### TASK 4 (BLACK) ###

#SD read in Mangle file
m = pymangle.Mangle("masking-vectors.ply")

#SD find which of the random coordinates fall within the lat-lon rectangles
good = m.contains(ra_rand, dec_rand)

#SD plotting the coordinates that fall within the lat-lon rectangles
plt.scatter(ra_rand, dec_rand, c='gray', s=1)
plt.scatter(ra_rand[good], dec_rand[good], c='green', s=1, label='lat-lon rectangles')

plt.xlabel('ra [deg]')
plt.ylabel('dec [deg]')
plt.legend(loc='lower right')

plt.show()

print('TASK 4:')
print("See plot.")
print('----------')
