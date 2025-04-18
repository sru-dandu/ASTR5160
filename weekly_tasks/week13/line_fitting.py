import numpy as np
from scipy.stats import chi2



### TASK 1 (RED) ###

#SD read in file
data = np.loadtxt('/d/scratch/ASTR5160/week13/line.data')

#SD find means and variances for each bin
means = [np.mean(data[:,i]) for i in range(len(data[0]))]
variances = [np.var(data[:,i]) for i in range(len(data[0]))]

print('----------')
print('TASK 1:')
print(f"Bin means: {means}")
print(f"Bin variances: {variances}")



### TASK 2 (RED) ###











