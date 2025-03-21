import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u
import argparse


#SD defined function for finding area of lat-lon rectangle
def lat_lon_area(ra_min, ra_max, dec_min, dec_max):
	
	#SD area of lat-lon rectangle, in steradians
	area = (ra_max - ra_min) * (np.sin(dec_max) - np.sin(dec_min))
	
	#SD create plots of lat-lon rectangles
	
	
	return area
	
	
	
	
	
	
	
	

if __name__ == "__main__":
	
	#SD description when passing -h
	parser = argparse.ArgumentParser(description="""Takes bounds of a lat-lon rectangle, and returns its area.
	Bounds are: (ra_min, ra_max, dec_min, dec_max).
	Inputs must be in either degrees or radians; must be specified.""")
	
	#SD inputs for bounds of lat-lon rectangle
	parser.add_argument("ra_min", type=float,
			help="['float'] Min ra bound of lat-lon rectangle. Must be between 0 and 2pi rad.")
	parser.add_argument("ra_max", type=float,
			help="['float'] Max ra bound of lat-lon rectangle. Must be between 0 and 2pi rad.")
	parser.add_argument("dec_min", type=float,
			help="['float'] Min dec bound of lat-lon rectangle. Must be between -pi and pi rad.")
	parser.add_argument("dec_max", type=float,
			help="['float'] Max dec bound of lat-lon rectangle. Must be between -pi and pi rad.")
	#SD let code know if inputs are radians or degrees
	parser.add_argument("unit", type=str,
			choices=['radians', 'rad', 'r', 'degrees', 'deg', 'd'],
			help="['str'] Units of inputted values")
	args = parser.parse_args()
	
	
	#SD convert inputted bounds to radians, if needed
	coords = [args.ra_min, args.ra_max, args.dec_min, args.dec_max]
	if args.unit in ['radians', 'rad', 'r']:
		ra_min, ra_max, dec_min, dec_max = coords * u.rad
	elif args.unit in ['degrees', 'deg', 'd']:
		ra_min, ra_max, dec_min, dec_max = u.deg.to(u.rad, coords)
	
	#SD make sure inputs are in correct ranges
	#SD ranges: ra from 0 to 2pi, dec from -pi to pi
	if ra_min < 0 or ra_min > 2*np.pi:
		raise argparse.ArgumentTypeError(f"ra_min={args.ra_min} {args.unit} outside range of 0 to 2pi radians.")
	if ra_max < 0 or ra_max > 2*np.pi:
		raise argparse.ArgumentTypeError(f"ra_max={args.ra_max} {args.unit} outside range of 0 to 2pi radians.")
	if dec_min < -np.pi or dec_min > np.pi:
		raise argparse.ArgumentTypeError(f"dec_min={args.dec_min} {args.unit} outside range of -pi to pi radians.")
	if dec_max < -np.pi or dec_max > np.pi:
		raise argparse.ArgumentTypeError(f"ra_max={args.dec_max} {args.unit} outside range of -pi to pi radians.")
	
	
	#SD run defined function to find lat-lon rectangle
	area = lat_lon_area(ra_min, ra_max, dec_min, dec_max)
	print(area)
	
