import numpy as np
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
from sklearn import neighbors



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
        num_tot = len(mock_data)
        num_virginica = len(mock_data[mock_target_class==2])
        
        return 100 * num_virginica/num_tot



if __name__ == '__main__':

    ### TASK 1 (RED) ###
    
    print('TASK 1:')
    
    # SD call function to run iris problem example code
    classified_percent = iris_problem(weeklytask=True)

    print('Copied code for the iris problem into the function iris_problem().')
    print(f"{classified_percent}% of the test irises were classified as 'virginica' by the k-NN algorithm.")








