import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

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



def task3(x, y, y_original, m2, b2):
	
	#SD solving for y values of fitted line
	y2 = m2*x + b2
	
	#SD plotting y w/ noise vs x
	plt.scatter(x, y, c='black', label='data')
	#SD plotting original y vs x
	plt.plot(x, y_original, label='original line')
	#SD plotting fitted y vs x
	plt.plot(x, y2, label='fitted line')
	
	plt.legend()
	
	#SD get current figure
	return plt.gcf()



def task4(figure, name='hw0-plot.png'):

	return figure.savefig(name)

