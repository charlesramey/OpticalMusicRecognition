from skimage import color
from skimage.feature import canny
from skimage.transform import hough_circle, hough_circle_peaks
import numpy as np

import imageio
import matplotlib.pyplot as plt


def find_notes(img):
    gray = color.rgb2gray(img)
    edges = canny(gray, sigma=3)
    plt.imshow(edges)
    plt.show()
    radii = np.arange(10, 15, 1)
    hough_raw = hough_circle(edges, radii)
    accums, cx, cy, radii = hough_circle_peaks(hough_raw, radii, total_num_peaks=20)
    plt.imshow(img)
    plt.scatter(cx, cy, marker='.')
    plt.show()


im = imageio.imread("../inputs/test1_cropped.png")
find_notes(im)
