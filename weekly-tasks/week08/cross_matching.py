from astropy.table import Table
import matplotlib.pyplot as plt



### TASK 1 (BLACK) ###

#SD read in fits file
objs = Table.read('/d/scratch/ASTR5160/data/first/first_08jul16.fits')

#SD plot ra vs dec
plt.scatter(objs['RA'], objs['DEC'], s=1)

#SD labeling the plot
plt.xlabel('ra [deg]')
plt.ylabel('dec [deg]')
plt.title('Task 1: ra vs dec')

plt.show()

print('Task 1:')
print('See plot.')
print('----------')



