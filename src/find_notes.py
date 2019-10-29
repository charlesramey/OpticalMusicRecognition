from skimage import color
from skimage.feature import canny
from skimage.transform import hough_circle, hough_circle_peaks
from math import sqrt
import numpy as np
import imageio
import matplotlib.pyplot as plt


def filter_notes(notes, min_dist):
    """
    Given a list of the note coordinates, removes the ones that are too close to another point
    :param notes: Coordinates of note centroids expressed as a list of tuples
    :param min_dist: The minimum allowed distance between centroids.
        If 2 centroids are closer than this, one will be destroyed.
    :return: The filtered list of note coordinates
    """
    def dist(a, b):
        return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
    bad = set()
    for i in range(len(notes)):
        for j in range(i):
            if dist(notes[i], notes[j]) < min_dist:
                bad.add(i)
    out = [notes[i] for i in range(len(notes)) if i not in bad]
    return sorted(out, key=lambda n: n[1])


def find_notes(img, min_r=10, max_r=12, thresh=0.85):
    """
    Find the centroids of the notes in an image. The image must be a single line of music, and must have the clef, key,
    and time signatures cropped out.
    :param img: The image of the line
    :param min_r: The smallest note-radius to search for
    :param max_r: The largest note-radius to search for
    :param thresh: The threshold for the hough transform cutoff, as a percent of the max response.
    :return: A list of tuples of the coordinates of the notes in (row, col) format
    """
    gray = color.rgb2gray(img)
    gray = np.array(gray)
    edges = canny(gray, sigma=3)
    radii = np.arange(min_r, max_r, 1)
    hough_raw = hough_circle(edges, radii)
    accums, cx, cy, radii = hough_circle_peaks(hough_raw, radii)
    f = accums > thresh * np.max(accums)
    x = cx[f]
    y = cy[f]
    return filter_notes(list(zip(y, x)), 2*max_r)


def make_note_converter(top_line, spacing):
    """
    Makes a function that converts coordinates into FoxDot notes
    :param top_line: The y-coordinate of the top line of the staff
    :param spacing: The space between lines of the staff
    :return: A function that takes as input a y-coordinate and returns a FoxDot note
    """
    def func(y):
        return int(12 - round(2 * (y - top_line) / spacing))

    return func


def plot_centroids(im, centroids):
    """
    Draw a matplotlib plot of the note centroids. For testing purposes.
    :param im: The sheet music image
    :param centroids: The centroids as returned by find_notes
    """
    plt.imshow(im)
    plt.scatter([n[1] for n in centroids], [n[0] for n in centroids], marker='x', color='r')
    plt.show()


if __name__ == "__main__":
    # test1_cropped: top20, space20
    # test3_cropped: top20, space23
    note_converter = make_note_converter(20, 23)
    im = imageio.imread("../inputs/test3_cropped.png")
    notes = find_notes(im)
    plot_centroids(im, notes)
    fd_notes = [note_converter(n[0]) for n in notes]
    print(fd_notes)
    from FoxDot import *
    p1 = Player()
    p1 >> piano(fd_notes)
    Clock.set_time(-1)
    Go()
