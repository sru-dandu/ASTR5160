import numpy as np
from numpy.random import random
import matplotlib.pyplot as plt
from astropy import units as u
import argparse



#SD defined function for finding area of lat-lon rectangle
def latlon_area(ra_min, ra_max, dec_min, dec_max):
	
	#SD make sure inputs are in radians
	#SD convert each separately in case there is a mix of deg and rad in inputs
	bounds = [ra_min, ra_max, dec_min, dec_max]
	ra_min, ra_max, dec_min, dec_max = [b.to(u.rad) for b in bounds]
	
	#SD area of lat-lon rectangle, in square degrees
	area = (180/np.pi)*(180/np.pi) * (ra_max - ra_min) * (np.sin(dec_max) - np.sin(dec_min))
	
	#SD return only value, without the unit
	return area.value



def latlon_sides_plotter(ra_min, ra_max, dec_min, dec_max, color, label):
	
	plt.plot([ra_min, ra_min], [dec_min, dec_max], c=color, label=label)
	plt.plot([ra_max, ra_max], [dec_min, dec_max], c=color)
	plt.plot([ra_min, ra_max], [dec_min, dec_min], c=color)
	plt.plot([ra_min, ra_max], [dec_max, dec_max], c=color)
	
	return
	


#SD make 4 lat-lon rectangles using given ra bounds
def latlon_plotter(ra_min, ra_max):
	
	#SD make sure inputs are in radians
	#SD need values in radians for plotting in Aitoff
	ra_min = ra_min.to(u.rad)
	ra_max = ra_max.to(u.rad)
	
	#SD save 4 pairs of dec_mins and dec_maxes to make 4 lat-lon rectangles
	dec_mins = [-90, -55, 0, 50] * u.deg
	dec_maxes = [-70, -35, 20, 70] * u.deg
	
	#SD convert decs to radians in order to plot in Aitoff
	dec_mins = dec_mins.to(u.rad)
	dec_maxes = dec_maxes.to(u.rad)
	
	#SD find area of each rectangle
	areas = [latlon_area(ra_min, ra_max, dec_mins[i], dec_maxes[i]) for i in range(4)]
	labels = [f"Area = {a:.3f} deg$^2$" for a in areas]
	
	#SD create lists for colors for plotting
	colors = ['blue', 'darkorange', 'green', 'red']
	
	#SD strip units from quantities in order to plot
	#SD because code is throwing error when plotting as quantities
	ra_min = ra_min.value
	ra_max = ra_max.value
	dec_mins = dec_mins.value
	dec_maxes = dec_maxes.value
	
	
	#SD create plot of lat-lon rectangle
	fig = plt.figure(figsize=(12,10))
	ax = fig.add_subplot(111, projection="aitoff")
	
	#SD plot one side of the rectangle at a time for each (dec_min, dec_max) pair
	#Sd using defined function that plots each line of a lat-lon rectangle
	[latlon_sides_plotter(ra_min, ra_max, dec_mins[i], dec_maxes[i], colors[i], labels[i]) for i in range(4)]
	
	ax.grid(color='gray', linestyle='dashed')
	plt.xlabel('ra [deg]')
	plt.ylabel('dec [deg]')
	plt.legend(loc='upper right')
	plt.show()
	
	return



#SD defined function for populating the area inside a lat-lon rectangle with points
def latlon_populator(ra_min, ra_max, dec_min, dec_max):
	
	#SD create 10,000 random values of ra and dec:
	ra = (2*random(10000) - 1) * np.pi * u.rad   #SD ranges from -pi to pi
	dec = (2*random(10000) - 1) * np.pi/2 * u.rad   #SD ranges from -pi/2 to pi/2
	
	#SD find the (ra,dec) coords that fall within given lat-lon rectangle bounds
	mask = (ra >= ra_min) & (ra <= ra_max) & (dec >= dec_min) & (dec <= dec_max)
	ra_inside = ra[mask]
	dec_inside = dec[mask]
	
	fig = plt.figure(figsize=(12,10))
	ax = fig.add_subplot(111, projection="aitoff")
	plt.scatter(ra_inside, dec_inside, s=5)
	plt.show()
	
	return ra_inside, dec_inside



if __name__ == "__main__":
	
	#SD description when passing -h
	parser = argparse.ArgumentParser(description="""Takes bounds of a lat-lon rectangle, and returns its area.
	Bounds are: (ra_min, ra_max, dec_min, dec_max).
	Inputs must be in either degrees or radians; must be specified.""")
	
	#SD inputs for bounds of lat-lon rectangle
	parser.add_argument("ra_min", type=float,
			help="['float'] Min ra bound of lat-lon rectangle. Must be between -180 and 180 deg.")
	parser.add_argument("ra_max", type=float,
			help="['float'] Max ra bound of lat-lon rectangle. Must be between -180 and 180 deg.")
	parser.add_argument("dec_min", type=float,
			help="['float'] Min dec bound of lat-lon rectangle. Must be between -90 and 90 deg.")
	parser.add_argument("dec_max", type=float,
			help="['float'] Max dec bound of lat-lon rectangle. Must be between -90 and 90 deg.")
	#SD let code know if inputs are radians or degrees
	parser.add_argument("unit", type=str,
			choices=['radians', 'rad', 'r', 'degrees', 'deg', 'd'],
			help="['str'] Units of inputted values. All inputs must be in same units.")
	args = parser.parse_args()
	
	
	#SD add astropy units to inputted values
	coords = [args.ra_min, args.ra_max, args.dec_min, args.dec_max]
	if args.unit in ['radians', 'rad', 'r']:
		ra_min, ra_max, dec_min, dec_max = coords * u.rad
	elif args.unit in ['degrees', 'deg', 'd']:
		ra_min, ra_max, dec_min, dec_max = coords * u.deg
	
	#SD make sure inputs are in correct ranges
	#SD Aitoff projection only takes ra from -pi to pi rad, dec from -pi/2 to pi/2 rad
	if ra_min < -180*u.deg or ra_min > 180*u.deg:
		raise argparse.ArgumentTypeError(f"ra_min={args.ra_min} {args.unit} outside range of 0 to 360 degrees.")
	if ra_max < -180*u.deg or ra_max > 180*u.deg:
		raise argparse.ArgumentTypeError(f"ra_max={args.ra_max} {args.unit} outside range of 0 to 360 degrees.")
	if dec_min < -90*u.deg or dec_min > 90*u.deg:
		raise argparse.ArgumentTypeError(f"dec_min={args.dec_min} {args.unit} outside range of -90 to 90 degrees.")
	if dec_max < -90*u.deg or dec_max > 90*u.deg:
		raise argparse.ArgumentTypeError(f"ra_max={args.dec_max} {args.unit} outside range of -90 to 90 degrees.")
	
	
	#SD run defined function to find lat-lon rectangles
	latlon_plotter(ra_min, ra_max)
	
	#SD run function to randomly populate points inside lat-lon rectangle with given bounds
	latlon_populator(ra_min, ra_max, dec_min, dec_max)
