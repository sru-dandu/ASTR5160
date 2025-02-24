from astropy.coordinates import SkyCoord
from astropy import units as u
import sys

#SD use sys to add week05 to system path
#SD this way, I can import from week 5's tasks while keeping week 6's tasks separate
sys.path.insert(0, '/d/users/srujan/ASTR5160/weekly-tasks/week05')

#SD importing from week05
from spherical_caps import cap_coords



### TASK 1 (BLACK) ###

#SD saving the coordinates of the caps
cap1_coords = SkyCoord(76, 36, unit=u.deg)
cap2_coords = SkyCoord(75, 35, unit=u.deg)

#SD finding 4-vectors of the caps
cap1_vector = cap_coords(cap1_coords, 5*u.deg)
cap2_vector = cap_coords(cap2_coords, 5*u.deg)

print('TASK 1:')
print(f"cap1: {cap1_vector}")
print(f"cap2: {cap2_vector}")
print('----------')
