import numpy as np



### TASK 1 (RED) ###

#SD read in file
data = np.loadtxt('/d/scratch/ASTR5160/week13/line.data')


#SD find covarianve of dataset
cov_matrix = np.cov(data, rowvar=False)

print('----------')
print('TASK 1:')
print(f"The covariance matrix has the shape {np.shape(cov_matrix)}.")
print("This makes sense because there should be one variance value for each bin, resulting in 10 variances values. This makes up the diagonal of the covariance matrix, hence the covariance matrix has to be 10x10.")

#SD extract diagonal of covariance matrix
cov_diagonal = [cov_matrix[i][i] for i in range(len(cov_matrix))]
#SD find variance of each bin
variances = [np.var(data[:,i], ddof=1) for i in range(len(data[0]))]


print("Covariance matrix diagonal , Bin variances:")
print(np.vstack((cov_diagonal, variances)).T)
print("The covariance matrix's diagonal values matches the variances of the bins.")



### TASK 2 (RED) ###

#SD create matrix of std*std values
std_list = [np.std(data[:,i], ddof=1) for i in range(len(data[0]))]
stdxstd_matrix = np.array([std_list]*10) * np.array([std_list]*10).T

#SD find correlation matrix
corr_matrix = cov_matrix / stdxstd_matrix

#SD find highest correlation value that isn't a diagonal
corr_unique, unique_idx = np.unique(corr_matrix, return_index=True)
highest_corr_idx = np.max(unique_idx[corr_unique < 1])

print('TASK 2:')
print('I found the correlation matrix.')
print("Ignoring the diagonals, the highest correlation seems to be between bin indices",
        str(highest_corr_idx)[0], 'and', str(highest_corr_idx)[1])
print('----------')

