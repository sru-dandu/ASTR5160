import numpy as np
import pandas as pd



### TASK 1 (RED) ###

data = pd.read_csv('result.csv')

ra = data['ra']
dec = data['dec']
mag_g = data['g']

print('TASK 1:')
print(f'There are {len(ra)} objects in the table, which is about the expected number (350).')
print('----------')




