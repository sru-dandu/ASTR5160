import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



### TASK 1 (RED) ###

#SD read in csv file
data = pd.read_csv('result.csv')

#SD extract data columns from csv file
ra = data['ra']
dec = data['dec']
mag_g = data['g']

print('TASK 1:')
print('Saved csv file to current directory.')
#SD check number of objs in csv file
print(f'There are {len(ra)} objects in the table, which is about the expected number (350).')
print('----------')



### TASK 2 (RED) ###

#SD create scatterplot of ra vs dec
plt.scatter(ra, dec)

#SD labeling the plot
plt.xlabel('ra [deg]')
plt.ylabel('dec [deg]')
plt.title('Task 2: ra vs dec')

plt.show()

print('TASK 2:')
print('See plot.')
print('----------')



### TASK 3 (RED) ###

#SD finding integer values of each mag_g
#SD int(num) effectively truncates decimal values from num
#SD this effectively bins mag_g values by integer ranges (11-12, 12-13, etc)
g_int = np.array([int(g) for g in mag_g])

#SD creating sizes for each integer range of mag_g values
#SD range is from 1 to len(np.unique(g_int))
sizes_flipped = g_int - np.min(g_int) + 1

#SD need to have larger sizes correspond to smaller mag_g values (brighter objs)
#SD subtract original values by max value + 1
#SD this makes small int values become large int values, and vice versa
#SD but now all values are negative, so take absolute value
sizes = np.abs(sizes_flipped - (np.max(sizes_flipped)+1))

#SD size input in matplotlib is for area of marker
#SD therefore, squaring the sizes so that each bin size is an increase in radius
sizes = sizes**2

#SD plot ra vs dec, with new size values
plt.scatter(ra, dec, s=sizes, edgecolor='black')

#SD labeling the plot
plt.xlabel('ra [deg]')
plt.ylabel('dec [deg]')
plt.title('Task 3: ra vs dec')

plt.show()

print('TASK 3:')
print('See plot.')
print('----------')



