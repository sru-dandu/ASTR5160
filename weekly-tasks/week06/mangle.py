from astropy.coordinates import SkyCoord
from astropy import units as u
import sys

#SD use sys to add week05 to system path
#SD this way, I can import from week 5's tasks while keeping week 6's tasks separate
sys.path.insert(0, '/d/users/srujan/ASTR5160/weekly-tasks/week05')

#SD importing from week05
from spherical_caps import cap_coords



### TASK 1 (BLACK) ###

#SD saving the coordinates of the caps
cap1_coords = SkyCoord(76, 36, unit=u.deg)
cap2_coords = SkyCoord(75, 35, unit=u.deg)

#SD finding 4-vectors of the caps
cap1_vector = cap_coords(cap1_coords, 5*u.deg)
cap2_vector = cap_coords(cap2_coords, 5*u.deg)

print('TASK 1:')
print(f"cap1: {cap1_vector}")
print(f"cap2: {cap2_vector}")
print('----------')



### TASK 2 (RED) ###

#SD extract values from vectors
x1, y1, z1, one_minus_h1 = cap1_vector
x2, y2, z2, one_minus_h2 = cap2_vector

#SD write the string to be saved to intersection.ply
intersection_contents = ["1 polygons\n",
		"polygon 1 ( 2 caps, 1 weight, 0 pixel, 0 str):\n",
		f"\t{x1:19.16f} {y1:19.16f} {z1:19.16f} {one_minus_h1:19.16f}\n",
		f"\t{x2:19.16f} {y2:19.16f} {z2:19.16f} {one_minus_h2:19.16f}"]
		
#SD write the string to be saved to bothcaps.ply
bothcaps_contents =  ["2 polygons\n",
		"polygon 1 ( 1 caps, 1 weight, 0 pixel, 0 str):\n",
		f"\t{x1:19.16f} {y1:19.16f} {z1:19.16f} {one_minus_h1:19.16f}\n",
		"polygon 2 ( 1 caps, 1 weight, 0 pixel, 0 str):\n",
		f"\t{x2:19.16f} {y2:19.16f} {z2:19.16f} {one_minus_h2:19.16f}"]

#SD create files and write to them
with open("intersection.ply", "w") as f:
	f.writelines(intersection_contents)
with open("bothcaps.ply", "w") as f:
	f.writelines(bothcaps_contents)

print('TASK 2:')
print("Written to files.")
print('----------')


