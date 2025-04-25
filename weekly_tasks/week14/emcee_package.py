import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import emcee
import corner



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





### TASK 2 (RED) ###
###SD code adapted from https://emcee.readthedocs.io/en/stable/tutorials/line/


print('TASK 2:')




#SD adapted from posterior_prob_func() for use in this moduele
def likelihood_func(params, x, ydata, var):
    
    #SD extract m and b from params
    m, b = params
    
    #SD find y values predicted by model
    ypred = m*x + b
    
    #SD find values that are in the summation part of the equation
    summand = ((ydata - ypred)**2 / var) + np.log(2 * np.pi * var)
    
    #SD solve likelihood function
    ln_L = -1 * (1/2) * np.sum(summand)

    return ln_L



#SD adapted from posterior_prob_func() for use in this moduele
def post_prob_func(params, x, ydata, var):
    
    #SD extract m and b from params
    m, b = params
    
    #SD set the flat prior according to given acceptable m and b ranges
    if (1 <= m <= 5) and (2 <= b <= 8):
        #SD prior = 1, therefore ln(prior) = 0
        ln_prior = 0
    else:
        #SD prior = 0, therefore ln(prior) = -inf
        ln_prior = -1 * np.inf
    
    #SD find posterior probability
    ln_posterior_prob = likelihood_func(params, x, ydata, var) + ln_prior
    
    return ln_posterior_prob



###SD maximum likelihood estimation

#SD initial guesses for m and b
initial = np.array([3, 4])
#SD maximize the likelihood function to find best m and b
neg_likelihood_func = lambda *args: -1*likelihood_func(*args)
soln = minimize(neg_likelihood_func, initial, args=(x, means, variances))
m_ml, b_ml = soln.x

print("Maximum likelihood estimates:")
print(f"m = {m_ml:.3f}")
print(f"b = {b_ml:.3f}")



#SD marginalization and uncertainty estimation
#SD use emcee package to run mcmc algorithm
pos = soln.x + 1e-4 * np.random.randn(32, 2)
nwalkers, ndim = pos.shape
sampler = emcee.EnsembleSampler(
    nwalkers, ndim, post_prob_func, args=(x, means, variances)
    )
sampler.run_mcmc(pos, 5000, progress=True)


#SD plotting time series of mcmc chain
fig, axes = plt.subplots(2, figsize=(10, 7), sharex=True)
samples = sampler.get_chain()
labels = ["m", "b"]
for i in range(ndim):
    ax = axes[i]
    ax.plot(samples[:, :, i], "k", alpha=0.3)
    ax.set_xlim(0, len(samples))
    ax.set_ylabel(labels[i])
    ax.yaxis.set_label_coords(-0.1, 0.5)

axes[-1].set_xlabel("step number")

plt.show()


#SD discard some of the initial steps and flatten the chain
flat_samples = sampler.get_chain(discard=100, thin=15, flat=True)
print(flat_samples.shape)


#SD corner plot
corner.corner(flat_samples, labels=labels)
plt.show()


#SD plot datapoints with some of the walks from the chain
inds = np.random.randint(len(flat_samples), size=100)
for ind in inds:
    sample = flat_samples[ind]
    if ind==inds[0]:
        plt.plot(x, np.dot(np.vander(x, 2), sample[:2]), "C1", alpha=0.1, label='walk samples')
    else:    
        plt.plot(x, np.dot(np.vander(x, 2), sample[:2]), "C1", alpha=0.1)
plt.errorbar(x, means, yerr=np.sqrt(variances), fmt=".k", capsize=0, label='data')
plt.plot(x, m_ml*x+b_ml, label='best fit')
plt.legend(fontsize=14)
plt.xlabel("x")
plt.ylabel("average y")
plt.show()


#SD print the best fit m and b values with errors
for i in range(ndim):
    mcmc = np.percentile(flat_samples[:, i], [16, 50, 84])
    q = np.diff(mcmc)
    print(f"{labels[i]} = {mcmc[1]} ; errors: + {q[0]} , - {q[1]}")


print('----------')




