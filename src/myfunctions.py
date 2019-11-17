from matplotlib import cm
from skimage import io
from PIL import Image
import numpy as np
import os

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

def scale(image, max_size, method=Image.ANTIALIAS):
    """
    From: https://gist.github.com/fabeat/6621507
    resize 'image' to 'max_size' keeping the aspect ratio
    and place it in center of white 'max_size' image
    """
    image = Image.fromarray(np.uint8(cm.gist_earth(image)*255))
    image.thumbnail(max_size, method)
    offset = (int((max_size[0] - image.size[0]) / 2), int((max_size[1] - image.size[1]) / 2))
    back = Image.new("RGB", max_size, "white")
    back.paste(image, offset)
    return back

def preprocess(img):
    resized = scale(img, (21,48)).convert('LA')
    resized = np.array(resized)[:,:,0].reshape((21*48, )) / 255
    return resized