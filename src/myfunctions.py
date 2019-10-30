import os
import numpy as np
from skimage import io


# Returns row index of c-th detected gradient change
def count_gradient_changes(im, c):
    count = 0
    previous_gradient = im[0][0]
    for n in range(1, len(im)):
        if im[n][0] == previous_gradient:
            continue
        previous_gradient = im[n][0]
        count += 1
        if count == c:
            return n
        
    return None


# Loads and returns formatted input
def get_input_im(filename):

    print("Getting input image...")
    
    # Change directory to correct folder
    directory = os.getcwd()
    directory = directory[:-4]
    os.chdir(directory + "\\inputs")
    
    # Load image as np array
    im = np.array(io.imread(filename))

    # Get rid of third dimension of it exists
    shape = np.shape(im)
    if len(shape) == 3:
        im = im[:, :, 0]
    
    # Move directory back to original folder
    os.chdir(directory)
    
    return im


def notes2foxdot(notes):
    pitches = []
    durations = []

    for n in notes:
        pitches.append(n.pitch)
        durations.append(n.duration)

    return pitches, durations
