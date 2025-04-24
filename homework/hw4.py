from astropy.table import Table
import numpy as np
from weekly_tasks.week10.imaging_classification import classify_func
import argparse
#SD the below modules are only needed if running _linefinder()
import matplotlib.pyplot as plt
from weekly_tasks.week12.bad_data import task3



def splendid_function(objs):
    """Finds objects that are quasars using flag cuts and color cuts.
    
    INPUTS
    ------
    objs : :class:'astropy.table.table.Table'
        An astropy table of objects to be checked if they are quasars.
    
    RETURNS
    -------
    :class:'numpy.ndarray'
        A boolean array of the same length as 'objs'.
        Indices containing 'True' correspond to quasars.
    """
    
    #SD call function to find g, r, z, W1 magnitudes
    #SD if flux <= 0, results in NaN for that object
    g, r, z, W1 = mag_finder(objs)

    #SD create the line separating quasars from stars
    #SD found by running _linefinder() and estimating by eye
    params = np.polyfit([-4, 6], [-6, 6], 1)
    f = np.poly1d(params)
    
    #SD call function to apply color cuts using a dividing line
    #SD between quasars and stars in r-W1 vs g-z space (line created by eye)
    quasar_mask = classify_func(g, r, z, W1, cutoff_eq=f)
    
    
    #SD create mask to remove NaN values
    g_notnan, r_notnan, z_notnan, W1_notnan = [~np.isnan(mag) for mag in [g, r, z, W1]]
    nan_mask = g_notnan & r_notnan & z_notnan & W1_notnan
    
    #SD create mask to remove objects labeled as PSOs in the file
    pso_mask = ~(objs['TYPE'] == 'PSO')
    
    #SD create mask to remove some bad data
    flag = 2**2 + 2**3 + 2**4 + 2**5 + 2**6 + 2**7 + 2**8
    bitmask = (objs['MASKBITS'] & flag) == 0
    
    #SD mask True/False array with nan_mask and bitmask
    #SD to remove bad data
    quasar_mask = quasar_mask & nan_mask & pso_mask & bitmask
    
    
    return quasar_mask
    




#SD function to find g, r, z, W1 magnitudes
def mag_finder(objs):
    """Find g, r, z, W1 magnitudes for objects in the given table.
    
    INPUTS
    ------
    objs : :class:'astropy.table.table.Table'
        An astropy table of objects for which the colors are to be found.
    
    RETURNS
    -------
    :class:'astropy.table.column.Column'
        An array of g magnitudes.
    :class:'astropy.table.column.Column'
        An array of r magnitudes.
    :class:'astropy.table.column.Column'
        An array of z magnitudes.
    :class:'astropy.table.column.Column'
        An array of W1 magnitudes.
    
    NOTES
    -----
    - If there are fluxes <= 0, resulting magnitudes will be NaN values.
    """
    
    #SD save column names of fluxes
    colnames = ['FLUX_G', 'FLUX_R', 'FLUX_Z', 'FLUX_W1']
    
    #SD calculate magnitudes
    g, r, z, W1 = [(22.5 - 2.5*np.log10(objs[col])) for col in colnames]
    
    return g, r, z, W1





#SD function to find line that separates stars from quasars in r-W1 vs g-z space
def _linefinder():
    """This is a test function to find the line separating stars from quasars
    in r-W1 vs g-z space.
    
    INPUTS
    ------
    None
    
    RETURNS
    -------
    'png file'
        A png file of a scatterplot in r-W1 vs g-z space is saved to current directory.
        It also has a line that separates stars and quasars, which was found by eye.
    """
    
    #SD run function to find relevant objects in sweeps,
    #SD and also find which of them are known quasars
    objs, qsos, _ = task3(r_max=19, PSF=False)
    
    #SD extract magnitudes from resulting objects
    g_objs, r_objs, z_objs, W1_objs = mag_finder(objs)
    g_qsos, r_qsos, z_qsos, W1_qsos = mag_finder(qsos)
    
    #SD plot the objects to find where the separation is
    #SD and plot a line by eye to mark that separation.
    #SD also highlight known quasars to check accuracy
    plt.scatter(g_objs-z_objs, r_objs-W1_objs, s=1)
    plt.scatter(g_qsos-z_qsos, r_qsos-W1_qsos, s=1)
    plt.plot([-4, 6], [-6, 6], c='red')   #SD line was found to go between the point (-4, -6) and (6, 6)
    plt.savefig('plot.png')
    
    return





if __name__ == '__main__':

    #SD description when passing -h
    parser = argparse.ArgumentParser(description="""Takes a file containing data of objects.
    Returns the number of quasars found in the datafile.
    This number is obtained using color cuts and flag cuts.""")
    
    #SD inputs
    parser.add_argument("datafile", type=str, nargs='?',
            default='/d/scratch/ASTR5160/data/legacysurvey/dr9/south/sweep/9.0/sweep-340p025-350p030.fits',
            help="""['str'] Datafile of objects to be scanned for quasars.
                    If none passed, a pre-selected sweep file is used as an example.""")
    args = parser.parse_args()
    
    
    #SD uncomment this to run test function to find line separating stars and quasars
    #_linefinder()
    
    
    #SD read in given datafile as an astropy table
    objs = Table.read(args.datafile)
    
    #SD run function to find quasars
    quasar_mask = splendid_function(objs)
    
    print("Number of quasars:", len(quasar_mask[quasar_mask==True]))








    
