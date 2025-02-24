from astropy import units as u
import numpy as np
import sys

#SD use sys to add week05 to system path
#SD this way, I can import from week 5's tasks while keeping week 6's tasks separate
sys.path.insert(0, '/d/users/srujan/ASTR5160/weekly-tasks/week05')

#SD importing from week05
from spherical_caps import cap_ra, cap_dec



### TASK 1 (RED) ###

#SD save ra and dec bounds
ra1 = 5*u.hr
ra2 = 6*u.hr
dec1 = 30*u.deg
dec2 = 40*u.deg

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
contents = ["1 polygons\n",
		f"polygon 1 ( 4 caps, 1 weight, 0 pixel, {area.value} str):\n",
		f"\t{x1:19.16f} {y1:19.16f} {z1:19.16f} {one_minus_h1:19.16f}\n",
		f"\t{x2:19.16f} {y2:19.16f} {z2:19.16f} {one_minus_h2:19.16f}\n",
		f"\t{x3:19.16f} {y3:19.16f} {z3:19.16f} {one_minus_h3:19.16f}\n",
		f"\t{x4:19.16f} {y4:19.16f} {z4:19.16f} {one_minus_h4:19.16f}"]

#SD create files and write to them
with open("masking-vectors.ply", "w") as f:
	f.writelines(contents)

print('TASK 1:')
print(f"The area of the lat-lon rectangle is {area.value} str.")
print("Vectors written to file.")
print('----------')
