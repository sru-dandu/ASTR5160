import numpy as np
from numpy.random import random
import matplotlib.pyplot as plt



### TASK 1 (RED) ###

#SD creating arrays for ra and dec
ra = 2 * np.pi * (random(10000)-0.5)
dec = np.arcsin(1. - 2.*random(10000))

#SD plotting dec vs ra to create a cylindrical projection of a sphere
plt.scatter(ra, dec, s=2)
plt.xlabel('ra [rad]')
plt.ylabel('dec [rad]')
plt.show()

#SD There are more points near the equator than near the poles.
#SD This is in line with how the cylindrical projection works.
