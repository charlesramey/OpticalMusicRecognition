from skimage import color
from skimage.feature import canny
from skimage.transform import hough_circle, hough_circle_peaks
from math import sqrt
import numpy as np

import imageio
import matplotlib.pyplot as plt


def filter_notes(notes, min_dist):
    def dist(a, b):
        return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
    bad = set()
    for i in range(len(notes)):
        for j in range(i):
            if dist(notes[i], notes[j]) < min_dist:
                bad.add(i)
    return [notes[i] for i in range(len(notes)) if i not in bad]


def find_notes(img, min_r=10, max_r=12):
    gray = color.rgb2gray(img)
    gray = np.array(gray)
    edges = canny(gray, sigma=0)
    plt.imshow(edges)
    plt.show()
    radii = np.arange(min_r, max_r, 1)
    hough_raw = hough_circle(edges, radii)
    accums, cx, cy, radii = hough_circle_peaks(hough_raw, radii)
    f = accums > 0.85 * np.max(accums)
    x = cx[f]
    y = cy[f]
    return filter_notes(list(zip(y, x)), max_r)


if __name__ == "__main__":
    im = imageio.imread("../inputs/test1.png")
    notes = find_notes(im)
    plt.imshow(im)
    plt.scatter([n[1] for n in notes], [n[0] for n in notes], marker='.', color='r')
    plt.show()
