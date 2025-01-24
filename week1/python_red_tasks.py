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


