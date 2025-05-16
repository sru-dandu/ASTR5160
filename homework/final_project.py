from astropy.table import Table
import numpy as np
import matplotlib.pyplot as plt
import emcee
import corner
import argparse
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
        The y values of the dataset.
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
    if (-5 <= m <= 0) and (0 <= b <= 5):
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
        The y values of the dataset.
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
        The y values of the dataset.
    var : :class:'list' or 'numpy.ndarray'
        The variances of each datapoint.
    
    RETURNS
    -------
    :class:'float'
        The natural log of the posterior probability function.
    """
    
    #SD extract a2, a1, a0 from params
    a2, a1, a0 = params
    
    #SD set the flat prior according to given acceptable a2, a1, a0 ranges
    if (0 <= a2 <= 5) and (-10 <= a1 <= 10) and (0 <= a0 <= 20):
        #SD prior = 1, therefore ln(prior) = 0
        ln_prior = 0
    else:
        #SD prior = 0, therefore ln(prior) = -inf
        ln_prior = -1 * np.inf
    
    #SD find posterior probability
    ln_posterior_prob = likelihood_func_quadratic(params, x, ydata, var) + ln_prior
    
    return ln_posterior_prob



###SD code adapted from https://emcee.readthedocs.io/en/stable/tutorials/line/
def finalproject_linearfit(x, y, yerr):
    """Contains code for finding a linear best-fit line to the data given for the final project.
    
    INPUTS
    ------
    x : :class:'list' or 'numpy.ndarray'
        The x values of the dataset.
    y : :class:'list' or 'numpy.ndarray'
        The y values of the dataset.
    yerr : :class:'list' or 'numpy.ndarray'
        The errors on each y.
    
    RETURNS
    -------
    None
    
    NOTES
    -----
    - Best-fit parameters for the model will be printed to screen with their errors.
    - Two plots will be printed to screen:
        - A corner plot with the posterior probability distributions of the fitted parameters.
        - A plot of the datapoints and the model made using the best-fit parameters.
    """
    
    #SD initial guesses for m and b
    initial = np.array([-1, 4])


    #SD marginalization and uncertainty estimation
    #SD use emcee package to run mcmc algorithm
    pos = initial + 1e-4 * np.random.randn(32, 2)
    nwalkers, ndim = pos.shape
    sampler = emcee.EnsembleSampler(
        nwalkers, ndim, post_prob_func_linear, args=(x, y, yerr**2)
        )
    sampler.run_mcmc(pos, 5000, progress=True)


    #SD discard some of the initial steps and flatten the chain
    flat_samples = sampler.get_chain(discard=100, thin=15, flat=True)
    print(flat_samples.shape)


    #SD corner plot
    labels=['m', 'b']
    corner.corner(flat_samples, labels=labels)
    plt.show()


    #SD print the best fit m and b values with errors
    print('----------')
    print('linear best-fit parameters:')
    bestfit_params = []
    for i in range(ndim):
        mcmc = np.percentile(flat_samples[:, i], [16, 50, 84])
        q = np.diff(mcmc)
        bestfit_params.append(mcmc[1])
        print(f"{labels[i]} = {mcmc[1]} ; errors: + {q[0]} , - {q[1]}")
    print('----------')


    #SD plot datapoints with the best-fit line from
    plt.errorbar(x, y, yerr=yerr, fmt=".k", capsize=0, label='data')
    plt.plot(x, bestfit_params[0]*x+bestfit_params[1], label='linear best-fit model')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.show()

    return



###SD code adapted from https://emcee.readthedocs.io/en/stable/tutorials/line/
def finalproject_quadfit(x, y, yerr):
    """Contains code for finding a quadratic best-fit line to the data given for the final project.
    
    INPUTS
    ------
    x : :class:'list' or 'numpy.ndarray'
        The x values of the dataset.
    y : :class:'list' or 'numpy.ndarray'
        The y values of the dataset.
    yerr : :class:'list' or 'numpy.ndarray'
        The errors on each y.
    
    RETURNS
    -------
    None
    
    NOTES
    -----
    - Best-fit parameters for the model will be printed to screen with their errors.
    - Two plots will be printed to screen:
        - A corner plot with the posterior probability distributions of the fitted parameters.
        - A plot of the datapoints and the model made using the best-fit parameters.
    """
    
    #SD initial guesses for a2, a1, a0
    initial = np.array([3, 0, 0])


    #SD marginalization and uncertainty estimation
    #SD use emcee package to run mcmc algorithm
    pos = initial + 1e-4 * np.random.randn(32, 3)
    nwalkers, ndim = pos.shape
    sampler = emcee.EnsembleSampler(
        nwalkers, ndim, post_prob_func_quadratic, args=(x, y, yerr**2)
        )
    sampler.run_mcmc(pos, 5000, progress=True)


    #SD discard some of the initial steps and flatten the chain
    flat_samples = sampler.get_chain(discard=100, thin=15, flat=True)
    print(flat_samples.shape)


    #SD corner plot
    labels=['a2', 'a1', 'a0']
    corner.corner(flat_samples, labels=labels)
    plt.show()


    #SD print the best fit a2, a1, a0 values with errors
    print('----------')
    print('quadratic best-fit parameters:')
    bestfit_params = []
    for i in range(ndim):
        mcmc = np.percentile(flat_samples[:, i], [16, 50, 84])
        q = np.diff(mcmc)
        bestfit_params.append(mcmc[1])
        print(f"{labels[i]} = {mcmc[1]} ; errors: + {q[0]} , - {q[1]}")
    print('----------')


    #SD plot datapoints with the best-fit line from
    plt.errorbar(x, y, yerr=yerr, fmt=".k", capsize=0, label='data')
    plt.plot(x,
        bestfit_params[0]*(x**2) + bestfit_params[1]*x + bestfit_params[2],
        label='quadratic best-fit model')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.show()

    return





if __name__ == '__main__':

    #SD description when passing -h
    parser = argparse.ArgumentParser(
        description="Takes a file containing data of x and y coordinates with errors on y. \n" +
        "Computes both a linear and quadratic fit to the data using the emcee package. \n" +
        "Returns the following for each fit: \n" +
        "    - a corner plot with the posterior probability distributions of the fitted parameters, \n" +
        "    - a plot of the datapoints and the model made using the best-fit parameters, \n" +
        "    - the best-fit paramters, with uncertainties based on " +
        "the 16th, 50th, and 84th percentiles of the MCMC samples.",
        formatter_class=argparse.RawTextHelpFormatter)

    args = parser.parse_args()


    #SD read in data
    data = Table.read('/d/scratch/ASTR5160/final/dataxy.fits')
    x = data['x']
    y = data['y']
    yerr = data['yerr']


    #SD fit a linear model to the data
    finalproject_linearfit(x, y, yerr)

    #SD fit a quadratic model to the data
    finalproject_quadfit(x, y, yerr)


    print("Looking at the corner plot for the quadratic parameters, I can see that a2's histogram is tightly" +
    " constrained around its best-fit value of ~0.06, and is shaped like a Gaussian. I can also see that a2 is" +
    " correlated with a0 and strongly negatively correlated with a1. This all tells me that a" +
    " quadratic model is justified to represent this dataset.")




