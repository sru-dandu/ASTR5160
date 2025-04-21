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



### TASK 3 (BLACK) ###

###SD below code is adapted from my line_fitting.py code (previous lecture)

#SD find means for each bin
means = [np.mean(data[:,i]) for i in range(len(data[0]))]

#SD create x values
#SD average of each bin range (0-1, 1-2, 2-3, ... , 9-10)
x = np.linspace(0.5, 9.5, 10)

#SD find possible m and b values for the data
m = np.linspace(0, 5, 100)
b = np.linspace(0, 5, 100)


#SD find inverse covariance matrix
inv_cov_matrix = np.matrix(cov_matrix).I

#SD create grid of chi square values
#SD each row corresponds to a value of m
#SD each column corresponds to a value of b
#SD I know this is really messy, I just couldn't figure out a better way with the time I had
chisquared = []
for bb in b:
    cs = []
    for mm in m:
        ypred = mm*x + bb
        summand_list = []
        for i in range(len(inv_cov_matrix)):
            summand = [(means[i] - ypred[i]) * np.sum(inv_cov_matrix[i,j] * (means[j] - ypred[j]))
                        for j in range(len(inv_cov_matrix))]
            summand_list.append(summand)
        chi = np.sum(summand_list)
        cs.append(chi)
    chisquared.append(cs)

chisquared = np.array(chisquared)


#SD find index of minimum chi squared
chi_min = np.min(chisquared)
chi_min_idx = np.where(chisquared == chi_min)

#SD find m and b values corresponding to minimum chi squared
m_best = m[chi_min_idx[1][0]]
b_best = b[chi_min_idx[0][0]]


print('TASK 3:')
print("The minimum chi squared value is", chi_min)
print(f"The best fit parameters are m={m_best:.3f} and b={b_best:.3f}")

print("The values are practically the same as the results from the previous class.")
print("This makes sense. Since we are dealing with a linear dataset, there shouldn't be any ")
print("correlation between the different bins. Therefore, adding the covariance factor to the ")
print("chi squared values wouldn't make a difference.")
print('----------')




