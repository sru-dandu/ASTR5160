import numpy as np
import matplotlib.pyplot as plt

"""This code takes two columns of values from a text file and plots them against each other."""

def main():

	# extracting data from text file
	data = np.loadtxt('/d/users/srujan/ASTR5160/week1/data.txt')

	# extracting the two columns from the data array
	x = data[:,0]
	y = data[:,1]

	# plotting the two columns against each other
	plt.plot(x, y)   # plotting a straight line
	plt.scatter(x, y, c='yellow', marker='+')   # plotting as yellow crosses
	plt.show()

if __name__ == "__main__":
	main()
