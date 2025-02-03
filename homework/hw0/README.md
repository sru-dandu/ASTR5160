# hw0.py

When a slope and y-intercept is inputted, the code outputs and saves a figure named 'hw0-plot.png'.

See below for details, or run "python hw0.py -h" in your command line.



### INPUTS

Run "python hw0.py m b" in command line, where:

* m: [type 'int' or 'float'] slope of linear equation 'y = m*x + b'
* b: [type 'int' or 'float'] y-intercept of linear equation 'y = m*x + b'



### STEPS

1. Array of x values is made by generating 10 random values between 1 and 10.
2. Corresponding y values are found using 'y = m*x + b'.
3. Noise is added to the y values. This is done for each y value by pulling a random value from a Gaussian centered at 'y' with standard deviation 0.5.
4. A line is fitted to the artificially created noise to find fitted y values.
5. Three plots are made:
	* scatter plot of y w/ noise vs x
	* linear plot of original y values vs x
	* linear plot of fitted y values vs x
6. Resulting figure of the three plots is saved as 'hw0-plot.png'.
