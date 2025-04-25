import numpy as np
import emcee



### TASK 1 (RED) ###
###SD code copied from Task 1 of previous lecture (likelihood_functions_and_mcmc.py)

#SD import datafile
#SD unpack=True transposes the array, such that 10 rows of x bins with 20 y datapoints each
data = np.loadtxt('/d/scratch/ASTR5160/week13/line.data', unpack=True)

#SD create array of x values
#SD correspond to means of bin ranges (0-1, 1-2, 2-3, ... , 9-10)
x = np.arange(0.5, 10, 1)

#SD find means and variances of each bin
means = np.mean(data, axis=1)
variances = np.var(data, axis=1, ddof=1)


print('TASK 1:')
print("bin means:", means)
print("bin variances:", variances)
print('----------')
print(np.shape(data))



### TASK 2 (RED) ###



