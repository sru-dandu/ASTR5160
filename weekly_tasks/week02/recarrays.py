from astropy.table import Table
import matplotlib.pyplot as plt
import numpy as np

### TASK 1 (RED) ###

# SD calling in fits file
objs = Table.read("/d/scratch/ASTR5160/week2/struc.fits")

# SD plotting dec vs ra
plt.scatter(objs['RA'], objs['DEC'], s=10, edgecolor='black')
plt.xlabel(r'$\alpha$')
plt.ylabel(r'$\delta$')
plt.show()



### TASK 2 (RED) ###

# SD printing first column of 'extinction' 5-array (100 rows, 5 columns)
print(objs['EXTINCTION'][:,0])



### TASK 3 (RED) ###

# SD creating Boolean mask for extinction values > 0.22
ext_mask = objs['EXTINCTION'][:,0] > 0.22

# SD plotting the plot from above, but using the new Boolean mask
plt.scatter(objs['RA'][ext_mask], objs['DEC'][ext_mask], s=10, edgecolor='black')
plt.xlabel(r'$\alpha$')
plt.ylabel(r'$\delta$')
plt.show()



### TASK 4 (BLACK) ###

# SD creating three different sets of 100 random integers
   # SD chose random ranges for the three arrays
x = np.array(np.random.uniform(0, 100, 100), dtype='int16')
y = np.array(np.random.uniform(0, 500, 100), dtype='int16')
z = np.array(np.random.uniform(0, 1000, 100), dtype='int16')

# SD combining the arrays to create an array of 3 rows and 100 columns
   # SD and then transposing (using .T) to get an array of 100 rows and 3 columns
randomnum = np.vstack((x, y, z)).T

# SD created a recarray as a table containing RA and DEC from struc.fits, and the newly created 3-array
table = Table([objs['RA'], objs['DEC'], randomnum],
	names=('RA', 'DEC', 'randomnum'))

# SD saving table as .fits file
table.write('recarrays-table.fits')
