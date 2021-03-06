import numpy as np
from scipy.ndimage import convolve
from scipy.ndimage.morphology import binary_erosion
from scipy.ndimage.morphology import binary_dilation
from skimage.color import gray2rgb
from myfunctions import count_gradient_changes
import matplotlib.pyplot as plt


# This class contains all the necessary functions to extract staff features
class StaffDetector:
    
    # Constructor
    def __init__(self, im):
        
        # Images
        self.im_original = im.copy()
        self.im_binary = None
        self.im_staves = None
        self.im_staves_subtracted = None
        self.im_staves_expanded = None
        self.im_staves_filled = None
        self.im_staves_separated = []
        self.im_staves_subtracted_separated = []
        self.im_staves_expanded_separated = []
        
        # Numerical Values
        self.line_height = 0
        self.staff_height = 0
        self.staff_indices = []
        
        # Functions
        self.isolate_staves()
        self.expand_staves()
        self.subtract_staves()
        self.fill_staves()
        self.separate_staves()
        self.get_staff_indices()
        self.get_staff_height()

    # Extracts staves from the sheet music
    def isolate_staves(self):
        
        print("Isolating Staves...")

        # Do binary thresholding
        t = 156
        im = np.where(self.im_original < t, 0, 1)

        self.im_binary = im.copy()

        # Do vertical derivative
        f = np.array([[-1, 0],
                      [ 1, 0]])
        im = convolve(im, f)
        im = np.where(im == 0, 0, 1)

        # plt.figure(dpi=500)
        # plt.imshow(im, cmap='Greys')
        # plt.title('Vertical Derivative')
        # plt.axis('off')
        # plt.savefig('vertical_derivative.jpg')

        # Do horizontal erosion then dilation
        f = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

        im = binary_erosion(im, f, iterations=5)
        # plt.figure(dpi=500)
        # plt.imshow(im, cmap='Greys')
        # plt.title('Horizontal Erosion')
        # plt.axis('off')
        # plt.savefig('horizontal_erosion.jpg')
        im = binary_dilation(im, f, iterations=500)
        # plt.figure(dpi=500)
        # plt.imshow(im, cmap='Greys')
        # plt.title('Horizontal Dilation')
        # plt.axis('off')
        # plt.savefig('horizontal_dilation.jpg')

        self.im_staves = im

    # Subtract the staff from the original image
    def subtract_staves(self):

        print("Subtracting Staves...")

        im = self.im_binary

        # Do vertical derivative
        f = np.array([[-1, 1],
                      [ 0, 0]])
        im = convolve(im, f)
        im = np.where(im == 0, 1.0, 0.0)

        # Do horizontal derivative
        f = np.array([[-1, 0],
                      [ 1, 0]])
        im = convolve(im, f)
        im = convolve(im, f)
        im = np.where(im == 0, 1.0, 0.0)

        '''
        # Erode staves vertically
        f = []
        for _ in range(3):
            f.append([0, 1, 0])
        f = np.array(f)

        staff = binary_erosion(self.im_staves_expanded.copy(), f, iterations=self.line_height+1)
        '''
        im = gray2rgb(im)

        self.im_staves_subtracted = im

    # Expands lines so that lines/spaces are same height
    def expand_staves(self):
       
        print("Expanding Staves...")
        
        # Get image
        im = self.im_staves.copy()
        
        # Get height of each space
        start = count_gradient_changes(im, 1)
        end = count_gradient_changes(im, 5)
        line_height = end-start
        self.line_height = int(line_height/2)
        
        # Expand each line until spaces/lines are same height.
        f = []
        for _ in range(self.line_height-2):
            f.append([0, 1, 0])
        f = np.array(f)
        
        # Expand through vertical dilation
        self.im_staves_expanded = binary_dilation(im, f)

    # Fills in the staves to make counting easier
    def fill_staves(self):
        
        print("Filling Staves...")
        
        # Get image
        im = self.im_staves.copy()
        
        # Get staff height
        start = count_gradient_changes(im, 1)
        end = count_gradient_changes(im, 10)
        staff_height = end-start
        staff_height = int(staff_height/2)
        
        # Vertical dilation
        f = []
        for _ in range(staff_height):
            f.append([0, 1, 0])
        f = np.array(f)
        self.im_staves_filled = binary_dilation(im, f)

    # Separates the staves apart
    def separate_staves(self):
        
        print("Separating Staves...")
        
        # Get image
        im = self.im_staves_filled.copy()
        im_original = self.im_original.copy()
        im_expanded = self.im_staves_expanded.copy()
        im_subtract = self.im_staves_subtracted.copy()
        
        # Get staff separation
        start = count_gradient_changes(im, 2)
        end = count_gradient_changes(im, 3)
        if end is None:
            staff_separation = start//3
        else:
            staff_separation = end-start
        staff_separation //= 3

        # Get row indexes to cut at
        n = 1
        cut_indices = []
        while True:
            dummy1 = count_gradient_changes(im, n)
            if dummy1 is None:
                break
        
            dummy2 = count_gradient_changes(im, n+1)
            if dummy2 is None:
                break
            
            indices = (dummy1-staff_separation, dummy2+staff_separation)
            cut_indices.append(indices)
            n += 2

        # Cut up staves
        c = np.shape(im_original)[1]//12
        for n in range(len(cut_indices)):
            slice_o = im_original[cut_indices[n][0]:cut_indices[n][1], c:]
            slice_e = im_expanded[cut_indices[n][0]:cut_indices[n][1], c:]
            slice_s = im_subtract[cut_indices[n][0]:cut_indices[n][1], c:]
            self.im_staves_separated.append(slice_o)
            self.im_staves_expanded_separated.append(slice_e)
            self.im_staves_subtracted_separated.append(slice_s)
        
    # Get the bounds for each line/space
    def get_staff_indices(self):
        
        print("Getting staff indices...")
        
        # Get images
        staves = self.im_staves_expanded_separated
        
        for im in staves:
            indices = []
            for n in range(1, 10):
                top_bound = count_gradient_changes(im, n)
                bottom_bound = count_gradient_changes(im, n+1)
                indices.append((bottom_bound, top_bound))
            indices.reverse()
            self.staff_indices.append(indices)
    
    # Get the height of the staff
    def get_staff_height(self):
        
        print("Getting staff height...")
        
        # Get image
        im = self.im_staves_filled
        self.staff_height = count_gradient_changes(im, 2) - count_gradient_changes(im, 1)

