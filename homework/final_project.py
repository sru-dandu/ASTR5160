from astropy.table import Table
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import emcee
import corner
from weekly_tasks.week14.emcee_package import likelihood_func as likelihood_func_linear



#SD adapted from post_prob_func() in weekly_tasks/week14/emcee_package.py for use in this moduele
def post_prob_func_linear(params, x, ydata, var):
    """Finds the natural log of the posterior probability function for a linear fit to the data.
    
    INPUTS
    ------
    params : :class:'list' or 'numpy.ndarray'
        Contains the m and b values of the linear fit, in that order.
    x : :class:'list' or 'numpy.ndarray'
        The x values of the dataset.
    ydata : :class:'list' or 'numpy.ndarray'
        The y values in the dataset.
    var : :class:'list' or 'numpy.ndarray'
        The variances of each datapoint.
    
    RETURNS
    -------
    :class:'float'
        The natural log of the posterior probability function.
    """
    
    #SD extract m and b from params
    m, b = params
    
    #SD set the flat prior according to given acceptable m and b ranges
    if (0 <= m <= -5) and (0 <= b <= 5):
        #SD prior = 1, therefore ln(prior) = 0
        ln_prior = 0
    else:
        #SD prior = 0, therefore ln(prior) = -inf
        ln_prior = -1 * np.inf
    
    #SD find posterior probability
    ln_posterior_prob = likelihood_func_linear(params, x, ydata, var) + ln_prior
    
    return ln_posterior_prob



#SD adapted from likelihood_func() in weekly_tasks/week14/emcee_package.py for use in this moduele
def likelihood_func_quadratic(params, x, ydata, var):
    """Finds the natural log of the likelihood function for a quadratic fit to the data.
    
    INPUTS
    ------
    params : :class:'list' or 'numpy.ndarray'
        For a quadratic function of equation y = a2*x^2 + a1*x + a0,
        contains the a2, a1, and a0 values of the quadratic fit, in that order.
    x : :class:'list' or 'numpy.ndarray'
        The x values of the dataset.
    ydata : :class:'list' or 'numpy.ndarray'
        The y values in the dataset.
    var : :class:'list' or 'numpy.ndarray'
        The variances of each datapoint.
    
    RETURNS
    -------
    :class:'float'
        The natural log of the likelihood function.
    """
    
    #SD extract a2, a1, a0 from params
    a2, a1, a0 = params
    
    #SD find y values predicted by model
    ypred = a2*(x**2) + a1*x + a0
    
    #SD find values that are in the summation part of the equation
    summand = ((ydata - ypred)**2 / var) + np.log(2 * np.pi * var)
    
    #SD solve likelihood function
    ln_L = -1 * (1/2) * np.sum(summand)

    return ln_L



#SD adapted from post_prob_func() in weekly_tasks/week14/emcee_package.py for use in this moduele
def post_prob_func_quadratic(params, x, ydata, var):
    """Finds the natural log of the posterior probability function for a quadratic fit to the data.
    
    INPUTS
    ------
    params : :class:'list' or 'numpy.ndarray'
        For a quadratic function of equation y = a2*x^2 + a1*x + a0,
        contains the a2, a1, and a0 values of the quadratic fit, in that order.
    x : :class:'list' or 'numpy.ndarray'
        The x values of the dataset.
    ydata : :class:'list' or 'numpy.ndarray'
        The y values in the dataset.
    var : :class:'list' or 'numpy.ndarray'
        The variances of each datapoint.
    
    RETURNS
    -------
    :class:'float'
        The natural log of the posterior probability function.
    """
    
    #SD extract a2, a1, a0 from params
    a2, a1, a0 = params
    
    #SD set the flat prior according to given acceptable m and b ranges
    if (1 <= a2 <= 5) and (1 <= a1 <= 5) and (1 <= a0 <= 5):
        #SD prior = 1, therefore ln(prior) = 0
        ln_prior = 0
    else:
        #SD prior = 0, therefore ln(prior) = -inf
        ln_prior = -1 * np.inf
    
    #SD find posterior probability
    ln_posterior_prob = likelihood_func_quadratic(params, x, ydata, var) + ln_prior
    
    return ln_posterior_prob





if __name__ == '__main__':

    #SD read in data
    data = Table.read('/d/scratch/ASTR5160/final/dataxy.fits')
    x = data['x']
    y = data['y']
    yerr = data['yerr']
    variances = yerr**2
    
    """
    ###SD maximum likelihood estimation

    #SD initial guesses for m and b
    initial = np.array([-7/9, 3])
    #SD maximize the likelihood function to find best m and b
    neg_likelihood_func = lambda *args: -1*likelihood_func_linear(*args)
    soln = minimize(neg_likelihood_func, initial, args=(x, y, variances))
    m_ml, b_ml = soln.x

    print("Maximum likelihood estimates:")
    print(f"m = {m_ml:.3f}")
    print(f"b = {b_ml:.3f}")



    #SD marginalization and uncertainty estimation
    #SD use emcee package to run mcmc algorithm
    pos = soln.x + 1e-4 * np.random.randn(32, 2)
    nwalkers, ndim = pos.shape
    sampler = emcee.EnsembleSampler(
        nwalkers, ndim, post_prob_func_linear, args=(x, y, variances)
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
    plt.errorbar(x, y, yerr=yerr, fmt=".k", capsize=0, label='data')
    plt.plot(x, m_ml*x+b_ml, label='best fit')
    plt.legend(fontsize=14)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()


    #SD print the best fit m and b values with errors
    for i in range(ndim):
        mcmc = np.percentile(flat_samples[:, i], [16, 50, 84])
        q = np.diff(mcmc)
        print(f"{labels[i]} = {mcmc[1]} ; errors: + {q[0]} , - {q[1]}")


    print('----------')
    """
    
    
