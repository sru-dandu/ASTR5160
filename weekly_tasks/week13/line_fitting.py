import numpy as np
from scipy.stats import chi2
import matplotlib.pyplot as plt



### TASK 1 (RED) ###

#SD read in file
data = np.loadtxt('/d/scratch/ASTR5160/week13/line.data')

#SD find means and variances for each bin
means = [np.mean(data[:,i]) for i in range(len(data[0]))]
variances = [np.var(data[:,i], ddof=1) for i in range(len(data[0]))]

print('----------')
print('TASK 1:')
print(f"Bin means: {means}")
print(f"Bin variances: {variances}")
print('----------')



### TASK 2 (RED) ###

#SD create x values
#SD average of each bin range (0-1, 1-2, 2-3, ... , 9-10)
x = np.linspace(0.5, 9.5, 10)

#SD plot datapoints
plt.scatter(x, means)
plt.xlabel('x')
plt.ylabel('bin means')
plt.show()

#SD find possible b values for the data
#b = np.linspace(4, 6, 10)
b = np.linspace(0, 5, 100)

#SD find possible m values for the data
#m = np.linspace(2, 4, 10)
m = np.linspace(0, 5, 100)

'''
for i in range(len(m)):
    plt.plot(x, m[i]*x+b[i], label=f'm={m[i]}, b={b[i]}')
plt.show()
'''


print('TASK 2:')
print('Found some possible values for m and b.')
print('----------')



### TASK 3 (RED) ###

#SD create grid of chi square values
#SD each row corresponds to a value of m
#SD each column corresponds to a value of b
chisquared = []
for bb in b:
    cs = []
    for mm in m:
        ypred = mm*x + bb
        chi = (np.sum((means - ypred)**2)) / np.var(means, ddof=1)
        cs.append(chi)
    chisquared.append(cs)

chisquared = np.array(chisquared)


print('TASK 3:')
print('Founds chi square values for every combination of m and b values I chose in Task 2.')
print('----------')



### TASK 4 (BLACK) ###

#SD plot chi squared for each m and each b
#[plt.plot(m, arr, label=f'b = {b[idx]:.2f}') for idx, arr in enumerate(chisquared)]
[plt.plot(m, arr, label=f'b = {b[idx]:.3f}') for idx, arr in enumerate(chisquared) if np.min(chisquared) in arr]

plt.xlabel('m')
plt.ylabel(f'$\chi^2$')
plt.legend()
plt.show()


print('TASK 4:')
print('The minimum chi squared seems to correspond to')
print('around m = 3 and b = 4.646.')
print('----------')



### TASK 5 (BLACK) ###

#SD find delta chi squared
delta_chisquared = chisquared - np.min(chisquared)

#SD find confidence limits
#SD 10 bins, 2 parameters: ddof = 10-2-1 = 7
conf_lvl = chi2.sf(delta_chisquared, 7)
conf_lvl_flat = conf_lvl.flatten()

#SD find indices where alpha=0.32 and alpha=0.05
conf_1sigma_idx = np.argmin(np.abs(conf_lvl_flat - 0.32))
conf_2sigma_idx = np.argmin(np.abs(conf_lvl_flat - 0.05))

#SD extract the chi squared values and alpha values at those indices
chi_1sigma = chisquared.flatten()[conf_1sigma_idx]
chi_2sigma = chisquared.flatten()[conf_2sigma_idx]
conf_1sigma = conf_lvl_flat[conf_1sigma_idx]
conf_2sigma = conf_lvl_flat[conf_2sigma_idx]

#SD extract corresponding m and b values
M, B = np.meshgrid(m, b)
m_1sigma = M.flatten()[conf_1sigma_idx]
b_1sigma = B.flatten()[conf_1sigma_idx]
m_2sigma = M.flatten()[conf_2sigma_idx]
b_2sigma = B.flatten()[conf_2sigma_idx]


print('TASK 5:')

print("The closest we get to a 1 sigma confidence interval in this dataset is " +
        f"at chisquared={chi_1sigma:.5f}, alpha={conf_1sigma:.5f}.")
print(f"This corresponds to m={m_1sigma:.3f} and b={b_1sigma:.3f}.")

print("The closest we get to a 2 sigma confidence interval in this dataset is " +
        f"at chisquared={chi_2sigma:.5f}, alpha={conf_2sigma:.5f}.")
print(f"This corresponds to m={m_2sigma:.3f} and b={b_2sigma:.3f}.")



### TASK 6 (BLACK) ###

#SD plot datapoints with errorbars
plt.errorbar(x, means, yerr=np.std(means, ddof=1), elinewidth=1, barsabove=False, fmt='none')
plt.scatter(x, means, edgecolor='black', label='data')

#SD plot best fit lines and confidence levels
plt.plot(x, 3*x+4.646, c='red', label='best fit')


plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()






