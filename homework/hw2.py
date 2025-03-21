import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u
import argparse



#def lat_lon_area(ra_min, ra_max, dec_min, dec_max):
	
	
	
	
	

if __name__ == "__main__":
	
	#SD description when passing -h
	parser = argparse.ArgumentParser(description="""Takes bounds of a lat-lon rectangle, and returns its area.
	Bounds are: (ra_min, ra_max, dec_min, dec_max).
	Inputs must be in either degrees or radians; must be specified.""")
	
	#SD inputs for bounds of lat-lon rectangle
	parser.add_argument("ra_min", type=float,
			help="['float'] Min ra bound of lat-lon rectangle.")
	parser.add_argument("ra_max", type=float,
			help="['float'] Max ra bound of lat-lon rectangle.")
	parser.add_argument("dec_min", type=float,
			help="['float'] Min dec bound of lat-lon rectangle.")
	parser.add_argument("dec_max", type=float,
			help="['float'] Max dec bound of lat-lon rectangle.")
	#SD let code know if inputs are radians or degrees
	parser.add_argument("unit", type=str, choices=['radians', 'rad', 'r', 'degrees', 'deg', 'd'],
			help="['str'] Units of inputted values")
	args = parser.parse_args()
	
	
	#SD convert inputted bounds to radians, if needed
	coords = [args.ra_min, args.ra_max, args.dec_min, args.dec_max]
	if args.unit in ['radians', 'rad', 'r']:
		ra_min, ra_max, dec_min, dec_max = coords * u.rad
	elif args.unit in ['degrees', 'deg', 'd']:
		ra_min, ra_max, dec_min, dec_max = u.deg.to(u.rad, coords)
	
	#SD run defined function to find lat-lon rectangle
	#lat_lon_area(ra_min, ra_max, dec_min, dec_max)
	print(ra_min, ra_max, dec_min, dec_max)
