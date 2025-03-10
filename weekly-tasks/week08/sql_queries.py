import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



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
