import numpy as np



### TASK 1 (RED) ###

#SD import datafile
#SD unpack=True transposes the array
data = np.loadtxt('/d/scratch/ASTR5160/week13/line.data', unpack=True)

#SD find means and variances of each bin
means = [np.mean(xbin) for xbin in data]
variances = [np.var(xbin, ddof=1) for xbin in data]



### TASK 2 (RED) ###




