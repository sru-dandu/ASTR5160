import numpy as np
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
from sklearn import neighbors
from weekly_tasks.week12.bad_data import task3



def iris_problem(weeklytask=False):
    """Example code for the iris problem using the k-NN machine learning algorithm.
    
    INPUTS
    ------
    weeklytask : :class:'bool' ; Optional, default is False
        If True, returns percentage of the test irises that are classified as "virginica" by the k-NN algorithm.
        This is for the ASTR5160 Week 12 tasks.
    
    RETURNS
    -------
    :class:'float'
        Percentage of the test irises that are classified as "virginica" by the k-NN algorithm.
        Only returned if 'weeklytask' is set to True.
    
    NOTES
    -----
    - Two plots of sepal length vs sepal width get printed to screen
        - First plot: scatterplot of data, color-coded by iris type
        - Second plot: scatterplot made using k-NN with k=1
    - Code copied from Dr. Adam Myers' MLexample.html code
    """
    
    iris = load_iris()
    print(iris.DESCR)

    print("First few rows of the data:")
    colnames = "sepal_length sepal_width petal_length petal_width" 
    print(colnames)
    print(iris.data[:3])
    print("---------------------------------")
    print("Column statistics:")
    for i, j in enumerate(iris.data[0]):
          print("column: {}, mean: {:.2f}".format(i, np.mean(iris.data[..., i])))
    print("---------------------------------")
    print("Total number of rows: {}".format(len(iris.data)))
    print("Target classes (which type of iris): {}".format(iris.target))
    print("Target class names {}".format({i:j for i, j in enumerate(iris.target_names)}))

    fig, ax = plt.subplots(1, 1, figsize=(8,6))
    for i in range(3):
        target_class = iris.target == i
        ax.scatter(iris.data[target_class, 0], iris.data[target_class, 1], s=90, label=iris.target_names[i])
        ax.tick_params(labelsize=14)
        ax.set_xlabel("Sepal length (cm)", size=14)
        ax.set_ylabel("Sepal width (cm)", size=14)
        ax.legend(prop={'size': 14})
    plt.show()

    # ADM use the k-nearest neighbors algorithm (k-NN)
    # ADM with distances only to the nearest neighbor.
    knn = neighbors.KNeighborsClassifier(n_neighbors=1)
    knn.fit(iris.data, iris.target)
    print(colnames)
    mock_data = [5, 4, 1, 0]
    print(knn.predict([mock_data]), iris.target_names[knn.predict([mock_data])])
    mock_data = [6, 3, 4, 1]
    print(knn.predict([mock_data]), iris.target_names[knn.predict([mock_data])])

    # ADM let's map out the entire sepal_length/sepal_width space!
    # ADM (I'm restricting to just sepal_length and sepal_width as
    # ADM it's easier to picture a 2-D space than a 4-D space).
    n = 100000
    mock_data = []
    # ADM normally I don't condone appending to empty lists, but here
    # ADM I want to explicitly illustrate which columns I'm working
    # ADM on. This won't be a slow append, as it's only two columns.
    for i in range(2):
        print("working on column: {}".format(colnames.split()[i]))
        col_min = np.min(iris.data[..., i])
        col_max = np.max(iris.data[..., i])
        # ADM generate random points in the space corresponding to the
        # ADM iris measurement of interest.
        mock_meas = np.random.random(n)*(col_max - col_min) + col_min
        mock_data.append(mock_meas)
    # ADM we now have a list of n*2 measurements, 
    # ADM but we want an array of 2 columns and n rows.
    mock_data = np.reshape(mock_data, (2, n)).T
    print(mock_data)

    # ADM classify using the k-NN "black box"
    # ADM trained on the real-world iris data.
    # ADM but only use 2 columns as a simple illustration.
    knn = neighbors.KNeighborsClassifier(n_neighbors=1)
    knn.fit(iris.data[..., :2], iris.target)
    mock_target_class = knn.predict(mock_data)
    # ADM again, this for loop isn't strictly necessary, but
    # ADM it's a clear way to print the information to screen.
    for i in range(10):
        print(mock_data[i], mock_target_class[i], iris.target_names[mock_target_class[i]])

    # ADM let's plot the sepal_length, sepal_width space of the k-NN classifier.
    fig, ax = plt.subplots(1, 1, figsize=(8,6))
    for i in range(3):
        target_class = mock_target_class == i
        ax.scatter(mock_data[target_class, 0], mock_data[target_class, 1], s=10, label=iris.target_names[i])
        ax.tick_params(labelsize=14)
        ax.set_xlabel("Sepal length (cm)", size=14)
        ax.set_ylabel("Sepal width (cm)", size=14)
        ax.legend(prop={'size': 14})
    plt.show()
    
    
    #SD check if function is being run for the weekly task
    if weeklytask == False:
        return
        
    elif weeklytask == True:
        #SD percentage of test irises classified as 'virginica' by k-NN
        num_virginica = len(mock_data[mock_target_class==2])
        return 100 * num_virginica/n



def knn_quasar_classify(g_minus_z_given, r_minus_W1_given, returnplot=False):
    """Classifies objects as either quasars or stars using k-NN with g-z and r-W1 colors.
    
    INPUTS
    ------
    g_minus_z_given : :class:'list' or 'numpy.ndarray'
        The g-z colors for each object to be classified.
    r_minus_W1_given : :class:'list' or 'numpy.ndarray'
        The r-W1 colors for each object to be classified.
    returnplot : class:'bool' ; Optional, default is False
        If True, prints a scatterplot to screen with the training and test datasets.
    
    RETURNS
    -------
    :class:'numpy.ndarray'
        The inputted data, reformatted to be like a table.
        Each index is one object. Column 1 is is the g-z color, and column 2 is the r-W1 color.
    :class:'numpy.ndarray'
        The labels of each object in the first outputted numpy array.
        Quasars are labeled 'quasar', while stars are labeled 'star'.
    
    NOTES
    -----
    - The training set is made up of objects from the Legacy Survey sweep files
      within 3 degrees of (180 deg, 30 deg) and with an r mag < 20.
        - The subset of the dataset that are quasars were obtained by cross-matching the objects
          with a list of known quasars
        - The subset of the dataset that are stars were obtained by
          randomly pulling 500 objects from the overall dataset
    - The function will throw an error if individual ints or floats are given.
      If there is only one object's parameters to be inputted,
      put each parameter within a list or numpy.ndarray of length 1.
    """
    
    #SD call function from previous lecture's tasks
    psfobjs, qsos, idx = task3()
    
    #SD extract fluxes of psfobjs
    flux_mask = (psfobjs['FLUX_G'] > 0) & (psfobjs['FLUX_Z'] > 0) & (psfobjs['FLUX_R'] > 0) & (psfobjs['FLUX_W1'] > 0)
    psfobjs_flux_detected = psfobjs[flux_mask]
    
    #SD find magnitudes of psfobjs
    g_mag = 22.5 - 2.5*np.log10(psfobjs_flux_detected['FLUX_G'])
    z_mag = 22.5 - 2.5*np.log10(psfobjs_flux_detected['FLUX_Z'])
    r_mag = 22.5 - 2.5*np.log10(psfobjs_flux_detected['FLUX_R'])
    W1_mag = 22.5 - 2.5*np.log10(psfobjs_flux_detected['FLUX_W1'])
    
    #SD find g-z and r-W1 colors
    g_minus_z = g_mag - z_mag
    r_minus_W1 = r_mag - W1_mag
    #SD combine into one dataset
    color_data_psfobjs = np.array((g_minus_z, r_minus_W1)).T
    
    #SD mask to get color data for qsos objects
    color_data_qsos = color_data_psfobjs[idx]
    
    #SD get a random subset of psfobs objs' color data
    subset_idx = np.random.randint(0, len(color_data_psfobjs), 500)
    color_data_subset = color_data_psfobjs[subset_idx]
    
    #SD combine two datasets into overall dataset
    color_data_combined = np.vstack((color_data_qsos, color_data_subset))
    
    #SD create list of labels 'quasars' and 'stars'
    label_quasar = ['quasar'] * len(color_data_qsos)
    label_star = ['star'] * len(color_data_subset)
    label_combined = label_quasar + label_star
    
    #SD use k-NN algorithm
    knn = neighbors.KNeighborsClassifier(n_neighbors=1)
    knn.fit(color_data_combined, label_combined)
    
    #SD transform given dataset into correct format
    g_minus_z_given = np.array(g_minus_z_given)
    r_minus_W1_given = np.array(r_minus_W1_given)
    data_given = np.array((g_minus_z_given, r_minus_W1_given)).T
    #SD fit given data to training data using k-NN
    data_given_class = knn.predict(data_given)
    
    #SD return a plot if 'returnplot' is set to True
    if returnplot==True:
        plt.figure()
        plt.scatter(color_data_qsos[:,0], color_data_qsos[:,1], marker='o', c='blue', s=10, label='quasar')
        plt.scatter(color_data_subset[:,0], color_data_subset[:,1], marker='o', c='red', s=10, label='star')
        plt.scatter(data_given[data_given_class=='quasar', 0], data_given[data_given_class=='quasar', 1],
                    marker='D', c='blue', edgecolor='black', s=10, label='predicted quasar')
        plt.scatter(data_given[data_given_class=='star', 0], data_given[data_given_class=='star', 1],
                    marker='D', c='red', edgecolor='black', s=10, label='predicted star')
        plt.legend()
        plt.savefig('plot.png')
    
    return data_given, data_given_class



if __name__ == '__main__':

    ### TASK 1 (RED) ###
    
    print('TASK 1:')
    
    #SD call function to run iris problem example code
    classified_percent = iris_problem(weeklytask=True)

    print('Copied code for the iris problem into the function iris_problem().')
    print(f"{classified_percent}% of the test irises were classified as 'virginica' by the k-NN algorithm.")
    print('----------')
    
    
    
    ### TASK 2 (BLACK) ###
    
    #SD call function from previous lecture's tasks
    psfobjs, qsos, idx = task3()
    
    print('TASK 2:')
    print(f"There are {len(psfobjs)} point-source objects within 3 degrees of (180 deg, 30 deg) with an r-band magnitude < 20")
    print(f"There are {len(qsos)} objects within 3 degrees of (180 deg, 30 deg) with an r-band magnitude < 20 that we know for sure are quasars.")
    print('----------')



    ### TASK 3 (RED) ###
    
    print("TASK 3:")
    print("Wrote the function knn_quasar_classify(),")
    print("which uses k-nn to classify quasars and stars based on their g-z and r-W1 colors.")
    print('----------')
    
    
    
    
    
    
