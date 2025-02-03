import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import argparse

def task1(m, b):
	"""Finds an array of y values, with error artificially added,
	using an array of randomly generated x values.
	
	PARAMETERS
	----------
	m : :class:`float` or `int`
		The slope of the linear equation 'y = mx + b'.
	b : :class:`float` or `int`
		The y-intercept of the linear equation 'y = mx + b'.
	
	RETURNS
	-------
	:class:`~numpy.ndarray`
		An array of 10 randomly generated float values between 1 and 10.
	:class:`~numpy.ndarray`
		An array of 10 float values obtained using the equation 'y = mx + b'.
		Noise is then artificially added (see NOTES).
	:class:`~numpy.ndarray`
		An array of errors for the noise that was artificially added to 'y'.
		Consists of the value '0.5' repeated 10 times.
	:class:`~numpy.ndarray`
		An array of the original values for 'y', 
		before noise was artificially added.
	
	NOTES
	-----
	- Noise is artificially added to y by using numpy.random.normal
	  to draw offsets from a Gaussian of std=0.5 centered on a given y value.
	"""
	
	#SD generating array of 10 random float values between 0 and 10
	x = np.random.uniform(0, 10, 10)
	
	#SD finding y using y = mx + b
	y_original = m*x + b
	
	#SD standard deviation used to create the noise in y
	#SD need it to be in array format for later
	y_err = 0.5 * np.ones(10)
	
	#SD creating noise in y
	y = np.random.normal(loc=y_original, scale=y_err)
	
	return x, y, y_err, y_original



def task2(x, y, y_err):
	"""Uses scipy.optimize.curve_fit() to fit a line to given data.
	
	PARAMETERS
	----------
	x : :class:`~numpy.ndarray`
		An array of 10 random float values between 1 and 10.
	y : :class:`~numpy.ndarray`
		An array of 10 float values.
		Linearly related to 'x', but has noise.
	y_err : :class:`~numpy.ndarray`
		An array of errors for the noise in 'y'.
	
	RETURNS
	-------
	:class:`float`
		The slope of the fitted line.
	:class:`float`
		The y-intercept of the fitted line.
	
	NOTES
	-----
	- Usually, errors are not required when using 
	  scipy.optimize.curve_fit(). However, this function requires it, 
	  since it is asked to be used in the homework.
	"""
	
	#SD defined the equation as a function to be used in curve_fit()
	def eq(x, m, b):
		return m*x + b
	
	#SD used curve_fit() on data
	#SD optional error on y included
	param, param_cov = curve_fit(eq, x, y, sigma=y_err)
	
	#SD extracting the params m and b from the results of cirve_fit()
	m2, b2 = param
	
	return m2, b2



def task3(x, y, y_err, y_original, m2, b2):
	"""Creates a figure with three plots:
		- y vs x as scatter plot
		- original y (without noise) vs x as line plot
		- fitted y vs x as line plot
	
	PARAMETERS
	----------
	x : :class:`~numpy.ndarray`
		An array of 10 random float values between 1 and 10.
	y : :class:`~numpy.ndarray`
		An array of 10 float values.
		Linearly related to 'x', but has noise.
	y_err: :class:`~numpy.ndarray`
		An array of errors for the noise in 'y'.
	y_original : :class:`~numpy.ndarray`
		An array of 10 float values. Linearly related to 'x'.
	m2: :class:`float`
		The slope of the line fitted to 'y' vs 'x'.
	b2 : :class:`float`
		The y-intercept of the line fitted to 'y' vs 'x'.
	
	RETURNS
	-------
	:class:`matplotlib.figure.Figure`
		Figure consisting of the three plots.
	
	NOTES
	-----
	- 'y' is just 'y_original' with artificially added noise
	  (see prior function task1())
	"""
	#SD solving for y values of fitted line
	y2 = m2*x + b2
	
	#SD plotting y w/ noise vs x as scatterplot, with errorbars on y
	plt.errorbar(x, y, yerr=y_err, fmt='o', c='black', label='data')
	#SD plotting original y vs x as line
	plt.plot(x, y_original, label='original line')
	#SD plotting fitted y vs x as line
	plt.plot(x, y2, label='fitted line')
	
	plt.legend()
	
	#SD get current figure
	figure = plt.gcf()
	
	plt.show()
	
	return figure



def task4(figure, name='hw0-plot.png'):
	"""Saves a figure to file.
	
	PARAMETERS
	----------
	figure : :class:`matplotlib.figure.Figure`
		Figure consisting of the three plots.
	name : :class:`str`, optional, defaults to 'hw0-plot.png'
		Name that the file should be saved under.
		
	RETURNS
	-------
	`graphic file`
		File containing figure. Defaults to .png, 
		but can be changed by passing the optional parameter 'name'.
	
	NOTES
	-----
	- All the default parameters of matplotlib.pyplot.savefig() 
	  are in effect. Only filename can be specified.
	"""
	
	return figure.savefig(name)



def main(m, b):
	"""Combines all the previous functions into one.
	See headers of previous functions for details.
	
	PARAMETERS
	----------
	m : :class:`float` or `int`
		The slope of the linear equation 'y = mx + b'.
	b : :class:`float` or `int`
		The y-intercept of the linear equation 'y = mx + b'.
	
	RETURNS
	-------
	`graphic file`
		File containing figure, named 'hw0-plot.png'.
	
	NOTES
	-----
	- The function task4() has an optional argument for filenames. 
	  However, with how main() is set up, a filename cannot be 
	  given from the command line; therefore, the filename cannot 
	  be changed from the default.
	"""
	
	#SD calls task1()
	x, y, y_err, y_original = task1(m, b)
	
	#SD calls task2()
	m2, b2 = task2(x, y, y_err)
	
	#SD calls task3()
	fig = task3(x, y, y_err, y_original, m2, b2)
	
	#SD calls task4()
	task4(fig)
	
	return



if __name__ == '__main__':
	
	#SD description when passing -h
	parser = argparse.ArgumentParser(description="Takes inputs of slope 'm' and y-intercept 'b'. Creates 10 random values between 1 and 10 for x values, and generates y values using linear equation 'y = mx + b'. Adds noise to y using a Gaussian centered at original y values with standard deviation of 0.5, and randomly pulling offset values. Fits a line to the data that has noise to get new fitted y values. Plots y w/ noise vs x as a scatter plot, with both original y vs x and fitted y vs x as lines, and saves figure as 'hw0-plot.png'.")
	
	#SD args that have to be passed
	parser.add_argument("m", type=float,
			help="['int' or 'float'] slope of linear equation 'y = mx + b'")
	parser.add_argument("b", type=float,
			help="['int' or 'float'] y-intercept of linear equation 'y = mx + b'")
	args = parser.parse_args()
	
	#SD call main function
	main(args.m, args.b)
