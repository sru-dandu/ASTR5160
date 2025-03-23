import numpy as np
from numpy.random import random
import matplotlib.pyplot as plt
from astropy import units as u
import argparse



#SD defined function for finding area of lat-lon rectangle
def latlon_area(ra_min, ra_max, dec_min, dec_max):
	"""Finds the area of a lat-lon rectangle.
	
	INPUTS
	------
	ra_min : :class:'astropy.units.quantity.Quantity'
		The lower right ascension bound of the lat-lon rectangle.
		Must be in angular units (deg, rad, etc).
	ra_max: :class:'astropy.units.quantity.Quantity'
		The upper right ascension bound of the lat-lon rectangle.
		Must be in angular units (deg, rad, etc).
	dec_min : :class:'astropy.units.quantity.Quantity'
		The lower declination bound of the lat-lon rectangle.
		Must be in angular units (deg, rad, etc).
	dec_max: :class:'astropy.units.quantity.Quantity'
		The upper declination bound of the lat-lon rectangle.
		Must be in angular units (deg, rad, etc).
	
	RETURNS
	-------
	:class:'numpy.float64'
		The area of the lat-lon rectangle, in units of deg^2.
	
	NOTES
	-----
	- All inputted bounds must be astropy quantities in angular units (deg, rad, etc).
	- The output will have no astropy unit attached to it;
	  however, the value itself will be in units of deg^2.
	"""
	
	#SD make sure inputs are in radians
	#SD convert each separately in case there is a mix of deg and rad in inputs
	bounds = [ra_min, ra_max, dec_min, dec_max]
	ra_min, ra_max, dec_min, dec_max = [b.to(u.rad) for b in bounds]
	
	#SD area of lat-lon rectangle, in deg^2
	area = (180/np.pi)*(180/np.pi) * (ra_max - ra_min) * (np.sin(dec_max) - np.sin(dec_min))
	
	#SD attached astropy unit is wrong; return only value, without the unit
	return area.value



#SD function to make sure inputs are in correct format when plotting in aitoff projections
def aitoff_input_formatter(x):
	"""Matplotlib throws an error if the given inputs are singular astropy quantities.
	Therefore, this function correctly formats inputs to work for plotting in Aitoff projections
	by converting to radians and stripping the unit off, if either is needed.
	For use in latlon_sides_plotter().
	
	INPUTS
	------
	x : :class:'int', 'float', or 'astropy.units.quantity.Quantity'
		Value for which formatting needs to be checked/changed.
	
	RETURNS
	-------
	:class:'int', 'float', or 'numpy.float64'
		Value returned after being formatted correctly.
		Will have no astropy units attached, but will be in units of radians.
	
	NOTES
	-----
	- If input class is 'int' or 'float', output will be identical to input.
	- If input class is 'astropy.units.quantity.Quantity', output class will be 'numpy.float64'.
	  Will also be converted to radians if input's units was not already in radians.
	"""
	
	#SD check if input is an astropy quantity or not
	try:
		#SD if input is not in radians, convert to radians
		if x.unit != 'rad':
			x = x.to(u.rad)
			
		#SD strip unit from quantity to get value
		x = x.value
	
	except AttributeError:
		pass
	
	return x



#SD function to write the main part of the code that plots a lat-lon rectangle
def latlon_sides_plotter(ra_min, ra_max, dec_min, dec_max, color='blue', label=None):
	"""Plots every side of a lat-lon rectangle.
	Enables you to write only a single line, instead of four lines, to plot a lat-lon rectangle.
	
	INPUTS
	------
	ra_min : :class:'int', 'float', or 'astropy.units.quantity.Quantity'
		The lower right ascension bound of the lat-lon rectangle.
		See NOTES for acceptable units.
	ra_max: :class:'int', 'float', or 'astropy.units.quantity.Quantity'
		The upper right ascension bound of the lat-lon rectangle.
		See NOTES for acceptable units.
	dec_min : :class:'int', 'float', or 'astropy.units.quantity.Quantity'
		The lower declination bound of the lat-lon rectangle.
		See NOTES for acceptable units.
	dec_max: :class:'int', 'float', or 'astropy.units.quantity.Quantity'
		The upper declination bound of the lat-lon rectangle.
		See NOTES for acceptable units.
	color : :class:'str' , Optional, default is 'blue'
		The color that the lat-lon rectangle will be plotted as.
	label : :class:'str' , Optional, default is None
		The label of the lat-lon rectangle to go in the legend.
	
	RETURNS
	-------
	None
	
	NOTES
	-----
	- Each of the inputted bounds can be of different classes and in different units.
	- If an inputted bound is of class 'astropy.units.quantity.Quantity',
	  then can be in any angular units (deg, rad, etc). Otherwise, value must be in radians.
	- If input for 'color' is manually given as None, matplotlib's default colors will be used,
	  and each line of the rectangle will have a different color.
	- If input for 'label' is not given, the resulting plot will have no label.
	  If a legend if printed along with said plot, it will have no entry for the rectangle.
	"""
	
	#SD if needed, get inputs in correct format (matplotlib does not take astropy quantities)
	#SD format each input separately in case not all inputs are in same format
	bounds = [ra_min, ra_max, dec_min, dec_max]
	ra_min, ra_max, dec_min, dec_max = [aitoff_input_formatter(b) for b in bounds]
	
	
	#SD plot each side of the lat-lon rectangle
	#SD first line also labels the rectangle
	plt.plot([ra_min, ra_min], [dec_min, dec_max], c=color, label=label)
	plt.plot([ra_max, ra_max], [dec_min, dec_max], c=color)
	plt.plot([ra_min, ra_max], [dec_min, dec_min], c=color)
	plt.plot([ra_min, ra_max], [dec_max, dec_max], c=color)
	
	return



#SD make 4 lat-lon rectangles using given ra bounds
def latlon_plotter(ra_min, ra_max):
	"""Outputs a plot of 4 lat-lon rectangles in an Aitoff projection map.
	Each rectangle will have the same bounds in ra, but differing bounds in dec.
	
	INPUTS
	------
	ra_min : :class:'astropy.units.quantity.Quantity'
		The lower right ascension bound of the lat-lon rectangles.
		See NOTES for acceptable units and range of values.
	ra_max: :class:'astropy.units.quantity.Quantity'
		The upper right ascension bound of the lat-lon rectangles.
		See NOTES for acceptable units and range of values.
	
	RETURNS
	-------
	None
	
	NOTES
	-----
	- The inputted bounds must be astropy quantities in angular units (deg, rad, etc).
	- The inputted bounds must be within the range -pi to pi rad (or equivalent for unit of choice).
	- The resulting plot will show up in a pop-up window.
	"""
	
	#SD save 4 pairs of dec_mins and dec_maxes to make 4 lat-lon rectangles
	dec_mins = [-90, -55, 0, 50] * u.deg
	dec_maxes = [-70, -35, 20, 70] * u.deg
	
	#SD find area of each rectangle
	areas = [latlon_area(ra_min, ra_max, dec_mins[i], dec_maxes[i]) for i in range(4)]
	
	#SD find fraction of the sphere's area that is within the rectangles
	area_sphere = (180/np.pi)*(180/np.pi) * 4*np.pi   #SD area of sphere is 4pi steradians
	area_percents = [100*(a/area_sphere) for a in areas]
	
	#SD create lists for labels and colors for plotting
	labels = [f"Area = {areas[i]:.3f} deg$^2$, or {area_percents[i]:.3f}% of sphere"
		for i in range(len(areas))]
	colors = ['blue', 'darkorange', 'green', 'red']
	
	
	#SD create plot of lat-lon rectangle
	fig = plt.figure(figsize=(12,10))
	ax = fig.add_subplot(111, projection="aitoff")
	
	#SD plot one rectangle at a time for each (dec_min, dec_max) pair
	#SD using defined function that plots each line of a lat-lon rectangle
	[latlon_sides_plotter(ra_min, ra_max, dec_mins[i], dec_maxes[i], colors[i], labels[i]) for i in range(4)]
	
	ax.grid(color='gray', linestyle='dashed')
	plt.xlabel('ra [deg]')
	plt.ylabel('dec [deg]')
	plt.legend(loc='upper right')
	plt.show()
	
	return



#SD defined function for populating the area inside a lat-lon rectangle with points
def latlon_populator(ra_min, ra_max, dec_min, dec_max, n=10000):
	"""Populates a sphere with n randomly generated points,
	and finds which ones fall within the area of a lat-lon rectangle.
	
	INPUTS
	------
	ra_min : :class:'astropy.units.quantity.Quantity'
		The lower right ascension bound of the lat-lon rectangle.
		See NOTES for acceptable units and range of values.
	ra_max: :class:'astropy.units.quantity.Quantity'
		The upper right ascension bound of the lat-lon rectangle.
		See NOTES for acceptable units and range of values.
	dec_min : :class:'astropy.units.quantity.Quantity'
		The lower declination bound of the lat-lon rectangle.
		See NOTES for acceptable units and range of values.
	dec_max: :class:'astropy.units.quantity.Quantity'
		The upper declination bound of the lat-lon rectangle.
		See NOTES for acceptable units and range of values.
	n : :class:'int' , Optional, default is 10000
		The number of points to be randomly generated on the sphere
	
	RETURNS
	-------
	:class:'numpy.ndarray'
		The right ascensions of the generated points that fall within the lat-lon rectangle.
		In units of radians.
	:class:'numpy.ndarray'
		The declinations of the generated points that fall within the lat-lon rectangle.
		In units of radians.
	
	NOTES
	-----
	- The inputted bounds must be astropy quantities in units of either degrees or radians.
	- The inputted ra bounds must be within the range -pi to pi rad (or equivalent for unit of choice).
	- The inputted dec bounds must be within the range -pi/2 to pi/2 rad (or equivalent for unit of choice).
	- Both outputs are in units of radians. Together, they give (ra,dec) coordinates
	  of the randomly generated points that fall within the rectangle.
	- The resulting plot will show up in a pop-up window.
	"""
	
	#SD create n random values of ra and dec:
	ra = (2*random(n) - 1) * np.pi * u.rad   #SD ranges from -pi to pi
	dec = (2*random(n) - 1) * np.pi/2 * u.rad   #SD ranges from -pi/2 to pi/2
	
	#SD find the (ra,dec) coords that fall within given lat-lon rectangle bounds
	mask = (ra >= ra_min) & (ra <= ra_max) & (dec >= dec_min) & (dec <= dec_max)
	ra_inside = ra[mask]
	dec_inside = dec[mask]
	
	#SD find area of rectangle
	area = latlon_area(ra_min, ra_max, dec_min, dec_max)
	
	#SD find fraction of the sphere's area that is within the rectangle
	area_sphere = (180/np.pi)*(180/np.pi) * 4*np.pi   #SD area of sphere is 4pi steradians
	area_percent = 100 * (area / area_sphere)
	
	#SD label for rectangle in figure
	lab = f"Area = {area:.3f} deg$^2$, or {area_percent:.3f}% of sphere"
	
	#SD plotting the points and the rectangle
	fig = plt.figure(figsize=(12,10))
	ax = fig.add_subplot(111, projection="aitoff")
	plt.scatter(ra_inside, dec_inside, s=5, label='randomly generated points')
	latlon_sides_plotter(ra_min, ra_max, dec_min, dec_max, label=lab)

	ax.grid(color='gray', linestyle='dashed')
	plt.xlabel('ra [deg]')
	plt.ylabel('dec [deg]')
	plt.legend(loc='upper right')
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
	
	
	#SD run defined function to find 4 lat-lon rectangles
	latlon_plotter(-45*u.deg, 45*u.deg)
	
	#SD run function to randomly populate points inside lat-lon rectangle with given bounds
	n_tot = 10000
	ra_in, dec_in = latlon_populator(ra_min, ra_max, dec_min, dec_max, n=n_tot)
	
	#SD find number of points that fell in the rectangle
	n_points = len(ra_in)
	n_points_percent = 100 * (n_points / n_tot)
	
	#SD find area of the lat-lon rectangle
	area = latlon_area(ra_min, ra_max, dec_min, dec_max)
	area_sphere = (180/np.pi)*(180/np.pi) * 4*np.pi   #SD area of sphere is 4pi steradians
	area_percent = 100 * (area / area_sphere) 
	
	print(f"Points falling within rectangle: {n_points}/{n_tot}, or {n_points_percent:.3f}% of the points.")
	print(f"Area of rectangle: {area:.3f} deg^2, or {area_percent:.3f}% of the sphere's total area.")

