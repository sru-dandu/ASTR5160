from astropy.coordinates import SkyCoord
from astropy import units as u
import pymangle
import matplotlib.pyplot as plt
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



### TASK 3 (RED) ###

#SD reading in the mask files
minter = pymangle.Mangle("intersection.ply")
mboth = pymangle.Mangle("bothcaps.ply")

#SD generate 10,000 random points to fill each mask
ra_inter, dec_inter = minter.genrand(10000)
ra_both, dec_both = mboth.genrand(10000)

#SD plot the randomly generated points
plt.scatter(ra_inter, dec_inter, s=1, label='intersection')
plt.scatter(ra_both, dec_both, s=1, label='both')

plt.xlabel('ra [deg]')
plt.ylabel('dec [deg]')
plt.title("Task 3")
plt.legend()

plt.show()

print("TASK 3:")
print('See plot.')
print("When the mask file specified two different polygons, each one being one cap vector, the points populated the areas of both caps. However, when the mask specified one polygon with two cap vectors, the points populated the intersection of the two caps. It works like a venn diagram.")
print('----------')



### TASK 4 (RED) ###

#SD flip the constraint on cap 1
one_minus_h1_flipped = -1 * one_minus_h1

#SD write the string to be saved to inter_flipped1.ply
inter_flipped1_contents = ["1 polygons\n",
			"polygon 1 ( 2 caps, 1 weight, 0 pixel, 0 str):\n",
			f"\t{x1:19.16f} {y1:19.16f} {z1:19.16f} {one_minus_h1_flipped:19.16f}\n",
			f"\t{x2:19.16f} {y2:19.16f} {z2:19.16f} {one_minus_h2:19.16f}"]

#SD create file and write to it
with open("inter_flipped1.ply", "w") as f:
	f.writelines(inter_flipped1_contents)

#SD read in mask file
mflip1 = pymangle.Mangle("inter_flipped1.ply")

#SD generate 2000 random points to fill mask
ra_flip1, dec_flip1 = mflip1.genrand(2000)

#SD plotting the generated points
plt.scatter(ra_inter, dec_inter, s=1, label='original')
plt.scatter(ra_flip1, dec_flip1, s=1, label='cap 1 flipped')

plt.xlabel('ra [deg]')
plt.ylabel('dec [deg]')
plt.title("Task 4")
plt.legend()

plt.show()

print("TASK 4:")
print('See plot.')
print('----------')



### TASK 5 (BLACK) ###

#SD flip the constraint on cap 2
one_minus_h2_flipped = -1 * one_minus_h2

#SD write the string to be saved to inter_flipped2.ply
inter_flipped2_contents = ["1 polygons\n",
			"polygon 1 ( 2 caps, 1 weight, 0 pixel, 0 str):\n",
			f"\t{x1:19.16f} {y1:19.16f} {z1:19.16f} {one_minus_h1:19.16f}\n",
			f"\t{x2:19.16f} {y2:19.16f} {z2:19.16f} {one_minus_h2_flipped:19.16f}"]

#SD create file and write to it
with open("inter_flipped2.ply", "w") as f:
	f.writelines(inter_flipped2_contents)

#SD read in mask file
mflip2 = pymangle.Mangle("inter_flipped2.ply")

#SD generate 2000 random points to fill mask
ra_flip2, dec_flip2 = mflip2.genrand(2000)

#SD plotting the generated points
plt.scatter(ra_inter, dec_inter, s=1, label='original')
plt.scatter(ra_flip1, dec_flip1, s=1, label='cap 1 flipped')
plt.scatter(ra_flip2, dec_flip2, s=1, label='cap 2 flipped')

plt.xlabel('ra [deg]')
plt.ylabel('dec [deg]')
plt.title("Task 5")
plt.legend()

plt.show()

print("TASK 5:")
print('See plot.')
print("When the caps' constraints became negative, the points were generated in the area of the non-flipped cap that is NOT within the cap whose constraint we flipped.")
print("Combining mflip1, mflip2, and intersection.ply's masks would result in the mask of bothcaps.ply. It is like a venn diagram: if cap1 and cap2 are the two circles, then intersection.ply's mask is the center of the venn diagram, and mflip1 and mflip2 are the areas of the circles outside of that center intersection.")
print('----------')



### TASK 6 (BLACK) ###

#SD write the string to be saved to inter_flipped12.ply
#SD use both flipped constraints
inter_flipped12_contents = ["1 polygons\n",
			"polygon 1 ( 2 caps, 1 weight, 0 pixel, 0 str):\n",
			f"\t{x1:19.16f} {y1:19.16f} {z1:19.16f} {one_minus_h1_flipped:19.16f}\n",
			f"\t{x2:19.16f} {y2:19.16f} {z2:19.16f} {one_minus_h2_flipped:19.16f}"]

#SD create file and write to it
with open("inter_flipped12.ply", "w") as f:
	f.writelines(inter_flipped12_contents)

#SD read in mask file
mflip12 = pymangle.Mangle("inter_flipped12.ply")

#SD generate 1,000,000 random points to fill mask
ra_flip12, dec_flip12 = mflip12.genrand(1000000)

#SD plotting the generated points
plt.scatter(ra_flip12, dec_flip12, s=1)

plt.xlabel('ra [deg]')
plt.ylabel('dec [deg]')
plt.title("Task 6")

plt.show()

print("TASK 6:")
print('See plot.')
print("This makes sense. Since we flipped the constraints of both caps and looked for the intersection, the points populated the area outside of both caps, or in other words, the entire area of the sphere minus the two caps.")
print('----------')
