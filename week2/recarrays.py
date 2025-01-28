from astropy.table import Table
import matplotlib.pyplot as plt

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
