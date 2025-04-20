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

#SD find possible m and b values for the data
b = np.linspace(4, 6, 10)

m = np.linspace(2, 4, 10)
m = np.linspace(m[3], m[6], 10)
m = np.linspace(m[2], m[7], 10)

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

#print(chisquared)

print('TASK 3:')
print('Founds chi square values for every combination of m and b values I chose in Task 2.')
print('----------')



### TASK 4 (BLACK) ###

#SD plot chi squared for each m and each b
[plt.plot(m, arr, label=f'b = {b[idx]:.2f}') for idx, arr in enumerate(chisquared)]
#SD plot where best m is
chi_min = np.min(chisquared)
best_m_idx = np.where(chisquared == chi_min)[1][0]
plt.plot([m[0], m[best_m_idx]], [chi_min, chi_min], c='black', label=f'best m, lowest $\chi^2$')
plt.plot([m[best_m_idx], m[best_m_idx]], [chi_min-0.5, chi_min], c='black')

plt.xlabel('m')
plt.ylabel(f'$\chi^2$')
plt.xlim(m[0], m[-1])
plt.ylim(chi_min-0.025, chi_min+0.2)   #SD zoom in on relevant region
plt.legend()
plt.show()

print('TASK 4:')
print('The minimum chi squared seems to correspond to')
print('around m = 3 and b = 4.67.')
print('----------')



### TASK 5 (BLACK) ###

#SD find delta chi squared
delta_chisquared = chisquared - chi_min

#SD find confidence limits
#SD 10 bins, 2 parameters: ddof = 10-2-1 = 7
conf_lim = chi2.sf(delta_chisquared, 7)
conf1sigma = conf_lim > 0.32
conf2sigma = conf_lim > 0.05
print(conf1sigma)
print(conf2sigma)



### TASK 6 (BLACK) ###

plt.figure(figsize=(10,10))

#SD plot datapoints with errorbars
plt.errorbar(x, means, yerr=np.std(means, ddof=1), elinewidth=1, barsabove=False, fmt='none')
plt.scatter(x, means, edgecolor='black', label='data')

#SD plot best fit lines and confidence levels
plt.plot(x, 3*x+4.67, c='red', label='best fit')


plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()






