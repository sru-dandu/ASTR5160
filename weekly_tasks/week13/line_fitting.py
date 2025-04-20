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
x0 = np.random.random(20)
x1 = x0 + 1
x2 = x0 + 2
x3 = x0 + 3
x4 = x0 + 4
x5 = x0 + 5
x6 = x0 + 6
x7 = x0 + 7
x8 = x0 + 8
x9 = x0 + 9

#SD plot datapoints
x = np.array((x0,x1,x2,x3,x4,x5,x6,x7,x8,x9)).flatten()
y = data.T.flatten()

plt.scatter(x, y)
plt.xlabel('x')
plt.ylabel('y')
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
for mm in m:
    cs = []
    for bb in b:
        ypred = mm*x + bb
        chi = (np.sum((y - ypred)**2)) / np.var(y, ddof=1)
        cs.append(chi)
    chisquared.append(cs)

chisquared = np.array(chisquared)

#print(chisquared)

print('TASK 3:')
print('Founds chi square values for every combination of m and b values I chose in Task 2.')
print('----------')



### TASK 4 (BLACK) ###

#SD plot chi squared for each m and each b
[plt.plot(m, arr, label=f'b = {b[idx]:.2f}') for idx, arr in enumerate(chisquared.T)]
#SD plot where best m is
chi_min = np.min(chisquared)
best_m_idx = np.where(chisquared == chi_min)[0][0]
plt.plot([m[0], m[best_m_idx]], [chi_min, chi_min], c='black', label=f'best m, lowest $\chi^2$')
plt.plot([m[best_m_idx], m[best_m_idx]], [0, chi_min], c='black')

plt.xlabel('m')
plt.ylabel(r'$\chi^2$')
plt.xlim(m[0], m[-1])
plt.ylim(chi_min-1, chi_min+3)   #SD zoom in on relevant region
plt.legend()
plt.show()

print('TASK 4:')
print('The minimum chi squared seems to correspond to')
print('around m = 3 and b = 4.67-4.89.')
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
plt.errorbar(x, y, yerr=np.std(y, ddof=1), elinewidth=1, barsabove=False, fmt='none')
plt.scatter(x, y, s=20, edgecolor='black', label='data')

#SD plot best fit lines and confidence levels
plt.plot(x, 3*x+4.89, c='red', label='best fit')


plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()






