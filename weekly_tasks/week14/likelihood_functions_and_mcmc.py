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
    if (m_low <= m <= m_high) and (b_low <= b <= b_high):
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
    print("Created a function to find ln(posterior probability) for a linear dataset.")
    print('----------')
    
    
    
    ### TASK 3 (RED) ###
    
    #SD set initial guesses for parameters
    m = 3
    b = 4
    
    #SD set acceptable ranges for m and b
    m_range = [1, 5]
    b_range = [2, 6]
    
    #SD set step size for proposal function
    #SD (standard deviation of Gaussian centered around m and b)
    step = 0.02
    
    #SD find first iteration of posterior probability and likelihood
    P, L = posterior_prob_func(x, means, variances, m, b, m_range, b_range)
    
    #SD start the MCMC chain with the initial values
    #SD each item in the chain corresponds to a single proposal (iteration in for loop)
    chain = [[m, b, L, P]]
    
    
    #SD counters for the for loop
    iterations = 10000
    filtered_count = 0
    
    for i in range(iterations):
        
        #SD find new m and b using proposal function
        m = np.random.normal(m, step)
        b = np.random.normal(b, step)

        #SD find new posterior probability and likelihood
        P, L = posterior_prob_func(x, means, variances, m, b, m_range, b_range)
        
        #SD find R
        #SD R = P_new / P_old, or ln(R) = ln(P_new) - ln(P_old)
        #SD P and P0 here are their natural logs
        P0 = chain[-1][3]
        ln_R = P - P0
        R = np.exp(ln_R)
        
        #SD check to see if able to accept new parameters to chain
        if R >= 1:
            append_to_chain = True
        
        elif R < 1:
            #SD can only accept new parameters to chain with probability R
            R_test = np.random.random()
            if R_test <= R:
                append_to_chain = True
            else:
                append_to_chain = False
        
        #SD append new values to MCMC chain
        if append_to_chain == True:
            chain.append([m, b, L, P])
        else:
            filtered_count += 1
    
    
    #SD convert completed chain from list to array
    chain = np.array(chain)
    
    
    print('TASK 3:')
    print("Created an MCMC chain using the Metropolis-Hastings algorithm.")
    print('----------')
    
    
    
    ### TASK 4 (BLACK) ###
    
    #SD total number of proposals accepted to chain is the length of the chain minus 1
    #SD because initial guess was added to chain first
    accepted_count = len(chain) - 1
    
    '''
    print('TASK 4:')
    print("With step=0.1, I was getting an acceptance rate much less than 30%.")
    print(f"After changing the step size to {step}, I'm getting an acceptance rate around 30%.")
    '''
    
    print('~~~TEST~~~')
    print("total number of proposals:", iterations)
    print("amount accepted:", accepted_count)
    print("amount rejected:", filtered_count)
    print(f"acceptance rate: {100 * accepted_count/iterations}%")
    
    #print(chain)
    
    
    
