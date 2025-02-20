import numpy as np



### TASK 1 (BLACK) ###

#SD make ra and dec arrays with 1 million values
ra = 360 * np.random.random(10**6)
dec = (180/np.pi) * np.arcsin(1 - 2*np.random.random(10**6))

