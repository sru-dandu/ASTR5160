import numpy as np
import matplotlib.pyplot as plt



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
    m0 = 3
    b0 = 4
    
    #SD set acceptable ranges for m and b
    m_range = [1, 5]
    b_range = [2, 8]
    
    #SD set step size for proposal function
    #SD (standard deviation of Gaussian centered around m and b)
    step = 0.33
    
    #SD find first iteration of posterior probability and likelihood
    P0, L0 = posterior_prob_func(x, means, variances, m0, b0, m_range, b_range)
    
    #SD start the MCMC chain with the initial values
    #SD each item in the chain corresponds to a single proposal (iteration in for loop)
    chain = [[m0, b0, L0, P0]]
    
    
    #SD counters for the for loop
    iterations = 10000
    filtered_count = 0
    
    for i in range(iterations):
        
        #SD find new m and b using proposal function
        m = np.random.normal(m0, step)
        b = np.random.normal(b0, step)

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
        #SD and turn current values into old values for next iteration
        if append_to_chain == True:
            chain.append([m, b, L, P])
            m0, b0, L0, P0 = m, b, L, P
        else:
            filtered_count += 1
    
    
    #SD convert completed chain from list to array
    chain = np.array(chain)


    #SD total number of proposals accepted to chain is the length of the chain minus 1
    #SD because initial guess was added to chain first
    accepted_count = len(chain) - 1
    
    print('TASK 3:')
    print("Created an MCMC chain using the Metropolis-Hastings algorithm.")
    print("total number of proposals:", iterations)
    print("step size:", step)
    print("proposals accepted:", accepted_count)
    print("proposals rejected:", filtered_count)
    print(f"acceptance rate: {100 * accepted_count/iterations}%")
    print('----------')
    
    
    
    ### TASK 4 (BLACK) ###
    
    print('TASK 4:')
    print("With step=0.1, I was getting an acceptance rate of ~67%, which is much greater than 30%.")
    print(f"After changing the step size to {step}, I'm getting an acceptance rate very close to 30%.")
    print('----------')
    
    
    
    ### TASK 5 (BLACK) ###
    
    #SD find best fit m and b
    idx_best = np.argsort(chain[:,3])[-1]
    m_best, b_best = chain[idx_best][0:2]
    
    #SD order the chain by m and by b
    idx_ordered_m = np.argsort(chain[:,0])
    idx_ordered_b = np.argsort(chain[:,1])
    m_ordered = chain[idx_ordered_m][:,0]
    b_ordered = chain[idx_ordered_b][:,1]
    
    #SD 68% of the data around the best fit m and b means 34% below and 34% above
    #SD 34% below the center is same as 16% away from lower edge of distribution (50-34=16)
    #SD 34% above the center is same as 84% away from lower edge of distribution (50+34=16)
    #SD therefore, need to find indices that are .16*len(data) and .84*len(data)
    idx_68conf_low = int(0.16*len(chain))
    idx_68conf_high = int(0.84*len(chain))
    
    #SD extract the m and b values at 68% confidence
    m_68conf_low = m_ordered[idx_68conf_low]
    m_68conf_high = m_ordered[idx_68conf_high]
    b_68conf_low = b_ordered[idx_68conf_low]
    b_68conf_high = b_ordered[idx_68conf_high]
    
    
    print('TASK 5:')
    print(f"m: best fit = {m_best} ; 68% confidence range = {m_68conf_low} to {m_68conf_high}")
    print(f"b: best fit = {b_best} ; 68% confidence range = {b_68conf_low} to {b_68conf_high}")
    print('----------')
    
    
    
    ###SD plot histograms to check confidence ranges
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12, 8))
    
    #SD histogram of m values in chain
    ax1.hist(m_ordered)
    ax1.plot([m_best, m_best], [0, 800], c='red', label='average')
    ax1.plot([m_68conf_low, m_68conf_low], [0, 800], c='orange', label='68% confidence')
    ax1.plot([m_68conf_high, m_68conf_high], [0, 800], c='orange')
    ax1.set_xlabel('m')
    ax1.set_ylabel('counts')
    ax1.legend()

    #SD histogram of b values in chain
    ax2.hist(b_ordered)
    ax2.plot([b_best, b_best], [0, 800], c='red', label='average')
    ax2.plot([b_68conf_low, b_68conf_low], [0, 800], c='orange', label='68% confidence')
    ax2.plot([b_68conf_high, b_68conf_high], [0, 800], c='orange')
    ax2.set_xlabel('b')
    ax2.set_ylabel('counts')
    ax2.legend()
    
    plt.show()
    
    
    
    
    
    
    
