from astropy.table import Table
import matplotlib.pyplot as plt

# SD calling in fits file
objs = Table.read("/d/scratch/ASTR5160/week2/struc.fits")

# SD plotting dec vs ra
plt.scatter(objs['RA'], objs['DEC'], s=10, edgecolor='black')
plt.xlabel(r'$\alpha$')
plt.ylabel(r'$\delta$')
plt.show()
