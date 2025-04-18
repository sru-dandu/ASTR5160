import numpy as np



### TASK 1 (RED) ###

#SD read in file
data = np.loadtxt('/d/scratch/ASTR5160/week13/line.data')


#SD find covarianve of dataset
data_cov = np.cov(data, rowvar=False)

print('----------')
print('TASK 1:')
print(f"The covariance matrix has the shape {np.shape(data_cov)}.")
print("This makes sense because there should be one variance value for each bin, resulting in 10 variances values. This makes up the diagonal of the covariance matrix, hence the covariance matrix has to be 10x10.")

#SD extract diagonal of covariance matrix
cov_diagonal = [data_cov[i][i] for i in range(len(data_cov))]
#SD find variance of each bin
variances = [np.var(data[:,i], ddof=1) for i in range(len(data[0]))]


print("Covariance matrix diagonal , Bin variances:")
print(np.vstack((cov_diagonal, variances)).T)
print("The covariance matrix's diagonal values matches the variances of the bins."



### TASk 2 (RED) ###





