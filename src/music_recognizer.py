from sklearn.utils.multiclass import unique_labels
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix
from matplotlib import pyplot as plt
from sklearn import svm, metrics
from PIL import Image
import numpy as np
import os

def scale(image, max_size, method=Image.ANTIALIAS):
    """
    From: https://gist.github.com/fabeat/6621507
    resize 'image' to 'max_size' keeping the aspect ratio
    and place it in center of white 'max_size' image
    """
    image.thumbnail(max_size, method)
    offset = (int((max_size[0] - image.size[0]) / 2), int((max_size[1] - image.size[1]) / 2))
    back = Image.new("RGB", max_size, "white")
    back.paste(image, offset)
    return back

def preprocess(selected_regions):
    x_ = []
    for region in selected_regions:
        im = region
        resized = scale(im, (32,32)).convert('LA')
        resized = np.array(resized)[:,:,0].reshape((32*32, )) / 255
        x_.append(resized)
    return x_

def getDurations():
	durations = {'eighth_note': 0.5, 'quarter_note' : 1, 'half_note' : 2, 'whole_note' : 4}
	return None

def main():
	nn_filename = input("Where shall I load the neural net from? ")
	neuralnetwork = joblib.load(nn_filename)
	return None


if __name__ == '__main__':
	main()