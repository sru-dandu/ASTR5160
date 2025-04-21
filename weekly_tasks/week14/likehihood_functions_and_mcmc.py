import numpy as np



def posterior_prob_func(x, ydata, var, m, b, mrange, brange):
    """Finds natural log of posterior probability for a linear fit to a dataset.
    
    INPUTS
    ------
    
    
    RETURNS
    -------
    
    
    """
    
    #SD find y values predicted by model
    ypred = m*x + b
    
    #SD find values that are in the summation part of the equation
    summand = ((ydata - ypred)**2 / var) + np.log(2 * np.pi * var)
    
    #SD solve likelihood function
    ln_L = -1 * (1/2) * np.sum(summand)
    
    #SD find m and b priors according to acceptable m and b ranges
    if mrange[0] < m < mrange[1]:
        mprior = 1
    else:
        mprior = 0
    if brange[0] < b < brange[1]:
        bprior = 1
    else:
        bprior = 0
    #SD calculate flat prior
    ln_prior = np.log(mprior * b_prior)
    
    #SD find posterior probability
    ln_posterior_prob = ln_L + ln_prior
    
    return ln_posterior_prob, ln_L



if __name__ == '__main__':


    ### TASK 1 (RED) ###

    #SD import datafile
    #SD unpack=True transposes the array
    data = np.loadtxt('/d/scratch/ASTR5160/week13/line.data', unpack=True)

    #SD find means and variances of each bin
    means = [np.mean(xbin) for xbin in data]
    variances = [np.var(xbin, ddof=1) for xbin in data]
    
    print('TASK 1:')
    print("bin means:", means)
    print("bin variances:", variances)
    print('----------')



    ### TASK 2 (RED) ###

    print('TASK 2:')
    print("Created a function to find ln(posterior probability) of a linear dataset.")
    print('----------')
    
    
    
    ### TASK 3 (RED) ###
    
    
    
    
    
    
    
    
    
