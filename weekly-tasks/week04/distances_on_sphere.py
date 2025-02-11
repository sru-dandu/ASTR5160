import numpy as np
from astropy.coordinates import SkyCoord
from astropy import units as u
import matplotlib.pyplot as plt



### TASK 1 (RED) ###

#SD saving coordinates in SkyCoord
ra1 = 263.75 * u.deg
dec1 = -17.9 * u.deg

ra2 = '20h24m59.9s'
dec2 = '10d6m0s'

coord1 = SkyCoord(ra1, dec1)
coord2 = SkyCoord(ra2, dec2)

#SD need to have coords in Cartesian coords
coord1_cart = coord1.cartesian
coord2_cart = coord2.cartesian

#SD find angle using dot product:
#SD a_vector * b_vector = |a||b|cos(zenith angle), where
	#SD a_vector * b_vector = x1x2 + y1y2 + z1z2
	#SD |a| = (x1^2 + y1^2 + z1^2)^(1/2)
dot_prod = coord1_cart.x*coord2_cart.x + coord1_cart.y*coord2_cart.y + coord1_cart.z*coord2_cart.z
mag1 = (coord1_cart.x**2 + coord1_cart.y**2 + coord1_cart.z**2)**(1/2)
mag2 = (coord2_cart.x**2 + coord2_cart.y**2 + coord2_cart.z**2)**(1/2)

z_angle = np.arccos(dot_prod / (mag1 * mag2))

#SD check using SkyCoord's "separation" method
z_angle_check = coord1.separation(coord2).rad

print("TASK 1:")
print(f"The zenith angle (found manually) is {z_angle}")
print("check:")
print(f"The zenith angle (found using SkyCoord's 'separation' method) is {z_angle_check}")



### TASK 2 (RED) ###

#SD find 2 sets of 100 ra values between 2 hr and 3 hr
ra_range1 = (np.random.random(100) + 2) * u.hour
ra_range2 = (np.random.random(100) + 2) * u.hour

#SD find 2 sets of 100 dec values between -2 deg and 2 deg
dec_range1 = (4*np.random.random(100) - 2) * u.deg
dec_range2 = (4*np.random.random(100) - 2) * u.deg

#SD plotting dec vs ra for both sets
plt.scatter(ra_range1, dec_range1, marker='o', c='steelblue', label='set 1')
plt.scatter(ra_range2, dec_range2, marker='x', c='maroon', label='set 2')
plt.xlabel("ra [hours]")
plt.ylabel("dec [degrees]")
plt.legend()
plt.show()
