from sklearn.utils.multiclass import unique_labels
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix
from matplotlib import pyplot as plt
from sklearn import svm, metrics
from PIL import Image
import numpy as np
import joblib
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

def preprocess(training_dir, testing_dir):
    x_ = []
    y_ = []
    x_test = []
    y_test = []
    for fig in os.listdir(training_dir):
        for example in os.listdir(training_dir + '\\' + fig):
            if 'png' in example:
                example_path = training_dir + '\\' + fig + '\\' + example
                im = Image.open(example_path).convert('LA')
                resized = scale(im, (32,32)).convert('LA')
                resized = np.array(resized)[:,:,0].reshape((32*32, )) / 255
                x_.append(resized)
                y_.append(fig)
    for fig in os.listdir(testing_dir):
        for example in os.listdir(testing_dir + '\\' + fig):
            if 'png' in example:
                example_path = testing_dir + '\\' + fig + '\\' + example
                im = Image.open(example_path).convert('LA')
                resized = scale(im, (32,32)).convert('LA')
                resized = np.array(resized)[:,:,0].reshape((32*32, )) / 255
                x_test.append(resized)
                y_test.append(fig)
    return (x_, y_, x_test, y_test)


def train_model(x_, y_, plot=False):
    mlp = MLPClassifier(activation='relu', hidden_layer_sizes=(25),
                    max_iter=480, alpha=1e-50,
                    solver='adam', verbose=10, 
                    tol=1e-4, random_state=1,
                    learning_rate_init=.01,
                    learning_rate='adaptive')
    mlp.fit(x_, y_)
    if plot:
        plt.plot(mlp.loss_curve_)
        plt.show()
    return mlp

def test_model(x_test, y_test, mlp, compute_metrics=True):
    expected = y_test
    print(mlp.predict(x_test))
    predicted = mlp.predict(x_test)
    if compute_metrics:
        print("Classification report for classifier %s:\n%s\n"
          % (mlp, metrics.classification_report(expected, predicted)))
        print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))


def main():
    #training_dir = input("Where is the training data stored? ")
    #testing_dir = input("Where is the testing data stored? ")
    #training_dir = "C:\\Users\\charles\\Desktop\\OpenOMR\\neuralnetwork\\training"
    #testing_dir = "C:\\Users\\charles\\Desktop\\OpenOMR\\neuralnetwork\\testing"
    training_dir = "C:\\Users\\charles\\Desktop\\training_notes_only"
    testing_dir = "C:\\Users\\charles\\Desktop\\testing_notes_only"
    print("NOW PREPROCESSING DATA")
    train_samples, train_labels, test_samples, test_labels = preprocess(training_dir, testing_dir)
    print("NOW TRAINING NEURAL NETWORK")
    neuralnetwork = train_model(train_samples, train_labels, plot=True)
    nn_filename = input("Enter filename to save the neural network: ")
    joblib.dump(neuralnetwork, nn_filename)
    print("NOW TESTING NEURAL NETWORK")
    test_model(test_samples, test_labels, neuralnetwork)
    return


if __name__ == '__main__':
    main()
