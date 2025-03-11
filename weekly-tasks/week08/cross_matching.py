from astropy.table import Table
import matplotlib.pyplot as plt
import os
#importing python file in directory
import sdssDR9query



### TASK 1 (BLACK) ###

#SD read in fits file
objs = Table.read('/d/scratch/ASTR5160/data/first/first_08jul16.fits')

#SD extract ra and dec from file
ra = objs['RA']
dec = objs['DEC']

#SD plot ra vs dec
plt.scatter(ra, dec, s=1)

#SD labeling the plot
plt.xlabel('ra [deg]')
plt.ylabel('dec [deg]')
plt.title('Task 1: ra vs dec')

plt.show()

print('Task 1:')
print('See plot.')
print('----------')



### TASK 2 (BLACK) ###

print('Task 2:')
print("Tried out the 'sdssDR9query.py' module.")
print('----------')



### TASK 3 (RED) ###

#SD extract first 100 coords
ra_small = ra[:100]
dec_small = dec[:100]

print('Task 3:')
print('Creating file...')

#SD query the coords and append results to file
for i in range(len(ra_small)):
	os.system(f"python sdssDR9query.py {ra_small[i]} {dec_small[i]} >> query-results.txt")

print('Created the query results file.')
print('----------')
