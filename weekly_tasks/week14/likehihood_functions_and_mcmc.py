import numpy as np



def posterior_prob_func(x, ydata, var, m, b, mrange, brange):
    """Finds natural log of posterior probability for a linear fit to a dataset.
    
    INPUTS
    ------
    x : :class:'numpy.ndarray'
        A 1d array containing the x values of the dataset.
        
    ydata : :class:'numpy.ndarray'
        A 1d array containing the y values of the dataset.
        
    var : :class:'numpy.ndarray'
        A 1d array containing the variances in the dataset.
        
    m : :class:'int' or 'float'
        The estimated slope of the linear fit.
        
    b : :class:'int' or 'float'
        The estimated y-intercept of the linear fit.
        
    mrange : :class:'list' or 'numpy.ndarray'
        The lower and upper limits of the acceptable range of slopes.
        
    brange : :class:'list' or 'numpy.ndarray'
        The lower and upper limits of the acceptable range of y-intercepts.
    
    
    RETURNS
    -------
    :class:'numpy.float64'
        The natural log of the posterior probability.
        
    :class:'numpy.float64'
        The natural log of the likelihood function.
    
    
    NOTES
    -----
    - x, ydata, var should be the same length.
    - mrange and brange should be of length 2.
    
    """
    
    #SD find y values predicted by model
    ypred = m*x + b
    
    #SD find values that are in the summation part of the equation
    summand = ((ydata - ypred)**2 / var) + np.log(2 * np.pi * var)
    
    #SD solve likelihood function
    ln_L = -1 * (1/2) * np.sum(summand)
    
    
    #SD make sure mrange and brange are in ascending order
    #SD and extract lower and upper values
    m_low, m_high = np.unique(mrange)
    b_low, b_high = np.unique(brange)
    
    #SD set the flat prior according to given acceptable m and b ranges
    if (m_low < m < m_high) and (b_low < b < b_high):
        #SD prior = 1, therefore ln(prior) = 0
        ln_prior = 0
    
    else:
        #SD prior = 0, therefore ln(prior) = -inf
        ln_prior = -1 * np.inf
    
    
    #SD find posterior probability
    ln_posterior_prob = ln_L + ln_prior
    
    
    return ln_posterior_prob, ln_L



if __name__ == '__main__':


    ### TASK 1 (RED) ###

    #SD import datafile
    #SD unpack=True transposes the array
    data = np.loadtxt('/d/scratch/ASTR5160/week13/line.data', unpack=True)
    
    #SD create array of x values
    #SD correspond to means of bin ranges (0-1, 1-2, 2-3, ... , 9-10)
    x = np.arange(0.5, 10, 1)

    #SD find means of each bin
    means = [np.mean(xbin) for xbin in data]
    means = np.array(means)
    
    #SD find variances of each bin
    variances = [np.var(xbin, ddof=1) for xbin in data]
    variances = np.array(variances)
    
    print('TASK 1:')
    print("bin means:", means)
    print("bin variances:", variances)
    print('----------')



    ### TASK 2 (RED) ###

    print('TASK 2:')
    print("Created a function to find ln(posterior probability) of a linear dataset.")
    print('----------')
    
    
    
    ### TASK 3 (RED) ###
    
        
    aaa = posterior_prob_func(x, means, variances, 3, 5, [1,5], [2,6])
    
    print(aaa)
    
    
    
    
    
    
