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
#SD check number of objs in csv file
print(f'There are {len(ra)} objects in the table, which is about the expected number (350).')
print('----------')



### TASK 2 (RED) ###


