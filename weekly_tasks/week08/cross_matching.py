from astropy.table import Table
import matplotlib.pyplot as plt
import os
from astropy.coordinates import SkyCoord
from astropy import units as u
#importing python file in directory
from weekly_tasks.week08 import sdssDR9query



#SD function that takes array of RA,DEC coords and find relevant sweep files
#SD used for Task 6
def sweep_func(ra_input, dec_input, directory='/d/scratch/ASTR5160/data/legacysurvey/dr9/north/sweep/9.0'):
    '''Returns all sweep files in a given directory that are needed to find objects corresponding to the given coordinates.
    
    INPUTS
    ------
    ra_input : :class:'list' or 'numpy.ndarray' or 'astropy.table.column.Column'
        Right ascensions of objects to be found using sweep files.
    
    dec_input : :class:'list' or 'numpy.ndarray' or 'astropy.table.column.Column'
        Declinations of objects to be found using sweep files.
    
    directory : :class:'str', optional, defaults to "/d/scratch/ASTR5160/data/legacysurvey/dr9/north/sweep/9.0"
        Directory that sweep files are in.
    
    RETURNS
    -------
    :class:'list'
        List of sweep files needed for finding the objects with given coordinates.
    '''
    #SD getting list of fits files within specified directory
    files = [f for f in os.listdir(directory) if f.endswith('.fits')]

    #SD extracting range intervals from filenames
    ramin = []
    decmin = []
    ramax = []
    decmax = []
    for f in files:
        #SD extract lower ra range
        ra = float(f[6:9])
        ramin.append(ra)
        #SD ra ranges are intervals of 10 deg
        ramax.append(ra + 10)
        
        #SD extract lower ra range
        dec = float(f[10:13])
        #SD check if dec should be negative
        if f[9] == 'm':
            dec *= -1
        decmin.append(dec)
        #SD dec ranges are intervals of 5 deg
        decmax.append(dec + 5)


    #SD find which coordinates from input correspond to sweep file ranges
    files_matched = []
    #SD iterate over each file
    for i in range(len(files)):
        
        #SD iterate over each obj coord
        for ii in range(len(ra_input)):
            
            #SD extract each ra and dec
            ra = ra_input[ii]
            dec = dec_input[ii]
            
            #SD check if coords are within bounds
            if ramin[i] < ra < ramax[i] and decmin[i] < dec < decmax[i]:
                files_matched.append(files[i])
                break
    
    
    return files_matched


#SD run code for tasks only if module is being run as a script
if __name__ == '__main__':
    
    ### TASK 1 (BLACK) ###
    
    #SD read in fits file
    objs = Table.read('/d/scratch/ASTR5160/data/first/first_08jul16.fits')
    
    #SD extract ra and dec from file
    ra = objs['RA']
    dec = objs['DEC']
    
    #SD plot ra vs dec
    plt.scatter(ra, dec, s=1)
    
    #SD labeling the plot
    plt.xlabel('ra [deg]')
    plt.ylabel('dec [deg]')
    plt.title('Task 1: ra vs dec')
    
    plt.show()
    
    print('Task 1:')
    print('See plot.')
    print('----------')
    
    
    
    ### TASK 2 (BLACK) ###
    
    print('Task 2:')
    print("Tried out the 'sdssDR9query.py' module.")
    print('----------')
    
    
    
    ### TASK 3 (RED) ###
    
    #SD extract first 100 coords
    ra_small = ra[:100]
    dec_small = dec[:100]
    
    print('Task 3:')
    #print('Creating file...')
    
    #SD query the coords and append results to file
    #for i in range(len(ra_small)):
        #os.system(f"python sdssDR9query.py {ra_small[i]} {dec_small[i]} >> query-results.txt")
    
    #print('Created the query results file.')
    print('I commented out the code that creates the file since I have already created and saved it.')
    print('----------')
    
    
    
    ### TASK 4 (BLACK) ###
    
    #SD read in two fits files
    objs2 = Table.read('/d/scratch/ASTR5160/data/legacysurvey/dr9/north/sweep/9.0/sweep-000m005-010p000.fits')
    objs3 = Table.read('/d/scratch/ASTR5160/data/legacysurvey/dr9/north/sweep/9.0/sweep-000p000-010p005.fits')
    
    #SD printing the astropy tables to examine them
    #print(objs2)
    #print(objs3)
    
    print('Task 4:')
    print('I examined two of the fits files in the specified directory.')
    print('----------')
    
    
    
    ### TASK 5 (BLACK) ###
    
    #SD save the directory that the sweep files are in
    directory = '/d/scratch/ASTR5160/data/legacysurvey/dr9/north/sweep/9.0'
    
    #SD get all fits files in directory
    files = [f for f in os.listdir(directory) if f.endswith('.fits')]
    
    #SD read in all files as astropy tables
    #objs_all = [Table.read(directory + '/' + f) for f in files]
    
    print('Task 5:')
    print('This takes forever. I commented it out.')
    print('----------')
    
    
    
    ### TASK 6 (RED) ###
    
    #SD run the defined function with the first 100 objs from data file
    files_matched = sweep_func(ra_small, dec_small)
    
    print('Task 6:')
    print('Here are the sweep files that need to be read:')
    #SD list comprehension for printing out filenames one at a time
    [print(f'{files_matched.index(fi) + 1}. {fi}') for fi in files_matched]
    print('----------')
    
    
    
    ### TASK 7 (BLACK) ###
    
    #SD save ra and dec as SkyCoord object
    coords = SkyCoord(ra_small, dec_small, unit=u.deg)
    
    #SD add directory path to list of filenames
    files_matched_long = [directory + '/' + f for f in files_matched]
    
    print('Task 7:')
    
    #SD find indices of objects from data file that match objects from sweep files
    match_indices1 = []
    match_indices2 = []
    for dirpath in files_matched_long:
    
        #SD counter to keep track of how far along the code is when running
        print('Currently reading sweep file', files_matched_long.index(dirpath)+1)
        
        #SD save fits files as astropy tables
        sweep = Table.read(dirpath, format='fits')
            
        #SD extract coords from tables and save as SkyCoord object
        sweep_coords = SkyCoord(sweep['RA'], sweep['DEC'], unit=u.deg)
            
        #SD find indicies where dataset and sweep files match
        idx1, idx2, d2, d3 = sweep_coords.search_around_sky(coords, 1*u.arcsec)
        
        match_indices1.append(idx1)
        match_indices2.append(idx2)
    
    
    print('These are the indices of the first 100 objects in the dataset that match each sweep file:')
    
    #SD printing the indices corresponding to each sweep file separately
    for i in range(len(match_indices1)):
        print(f'File {i+1}:')
        print(f'indices of dataset: {match_indices1[i]}')
        print(f'indices of sweep file: {match_indices2[i]}')
        
    print('----------')


