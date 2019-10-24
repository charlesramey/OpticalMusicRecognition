import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve
from scipy.ndimage.morphology import binary_erosion
from scipy.ndimage.morphology import binary_dilation
from myfunctions import countGradientChanges

#This method detects all sharps and returns their centrod location
def detect_sharps(im):
    
    #Get Image
    im = im.copy()
    shape = np.shape(im)
    
    plt.imshow(im)
    
