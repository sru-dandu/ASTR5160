import numpy as np
import matplotlib.pyplot as plt

def f(x):
	"""
	Solves the quadratic function y = x^2 + 3x + 8.
	
	Parameters
	----------
	x: :class:`~numpy.ndarray`, `int`, or `float`
	   Value(s) to be plugged into the equation
	
	Returns
	-------
	:class:`~numpy.ndarray`, `int`, or `float`
		The value(s) resulting from the equation
	"""
	y = x**2 + 3*x + 8

	return y



def main():
	"""
	Plots f(x) (defined above).
	"""
	
	# creating a range of x values from 0 to 10
	x_array = np.arange(-100, 100, 0.01)
	
	# plotting the function
	plt.plot(x_array, f(x_array))
	plt.xlabel(r'$x$')
	plt.ylabel(r'$x^2 + 3x + 8$')
	plt.show()



if __name__ == "__main__":
	main()



