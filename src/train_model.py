from sklearn.model_selection import train_test_split
from sklearn.utils.multiclass import unique_labels
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix
from skimage.transform import resize
from matplotlib import pyplot as plt
from skimage.color import rgb2gray
from sklearn import svm, metrics
from skimage.io import imread
import numpy as np
import joblib
import os
import imageio
from sklearn.model_selection import learning_curve
from sklearn.model_selection import ShuffleSplit



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
                resized = scale(im, (48,21)).convert('LA')
                resized = np.array(resized)[:,:,0].reshape((32*32, )) / 255
                x_.append(resized)
                y_.append(fig)
    for fig in os.listdir(testing_dir):
        for example in os.listdir(testing_dir + '\\' + fig):
            if 'png' in example:
                example_path = testing_dir + '\\' + fig + '\\' + example
                im = Image.open(example_path).convert('LA')
                resized = scale(im, (48,21)).convert('LA')
                resized = np.array(resized)[:,:,0].reshape((32*32, )) / 255
                x_test.append(resized)
                y_test.append(fig)
    return (x_, y_, x_test, y_test)

def preprocess_durations(data_dir):
    X = []
    Y = []
    for fig in os.listdir(data_dir):
        for example in os.listdir(data_dir + '\\' + fig):
            if 'png' in example:
                example_path = data_dir + '\\' + fig + '\\' + example
                try:
                    print(example_path)
                    im = imageio.imread(example_path)
                    img = im.astype('float64')
                    resized = rgb2gray(img)
                    resized = resized / np.max(resized)
                    resized = resize(resized, (48,21), preserve_range=True)
                    resized = resized.flatten() / 225
                    #plt.imshow(resized.reshape((48,21)))
                    #plt.show()
                    X.append(resized)
                    Y.append(fig)
                except Exception as e:
                    print("Failed: {}".format(example_path))
    return (X, Y)

def lc_curve(X, y):
    title = "Learning Curves"
    fig, axes = plt.subplots(1, 1, figsize=(5, 5))
    cv = ShuffleSplit(n_splits=10, test_size=0.2, random_state=0)
    estimator = MLPClassifier(activation='relu', hidden_layer_sizes=(200,200),
                    max_iter=600, alpha=1e-4,
                    solver='adam', verbose=20, 
                    tol=1e-8, random_state=1,
                    learning_rate_init=.01,
                    learning_rate='adaptive')

    train_sizes, train_scores, test_scores = \
        learning_curve(estimator, X, y, cv=cv, n_jobs=4,
                       train_sizes=np.linspace(.1, 1.0, 7))
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()
    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                         train_scores_mean + train_scores_std, alpha=0.1,
                         color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                         test_scores_mean + test_scores_std, alpha=0.1,
                         color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
                 label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
                 label="Cross-validation score")
    plt.legend(loc="best")
    plt.xlabel("Training examples")
    plt.ylabel("Accuracy")
    plt.show()

def train_model(x_, y_, plot=False):
    mlp = MLPClassifier(activation='relu', hidden_layer_sizes=(200,),
                    max_iter=10000, alpha=1e-4,
                    solver='adam', verbose=20, 
                    tol=1e-8, random_state=1,
                    learning_rate_init=.0001,
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
    duration_data = "C:\\Users\\charles\\Downloads\\thresholded_dataset"
    print("NOW PREPROCESSING DATA")
    X, Y = preprocess_durations(duration_data)
    train_samples, test_samples, train_labels, test_labels = train_test_split(X, Y, test_size=0.10, random_state=42)
    #train_samples, train_labels, test_samples, test_labels = preprocess(training_dir, testing_dir)
    print("NOW TRAINING NEURAL NETWORK")
    neuralnetwork = train_model(train_samples, train_labels, plot=True)
    nn_filename = input("Enter filename to save the neural network: ")
    joblib.dump(neuralnetwork, nn_filename)
    print("NOW TESTING NEURAL NETWORK")
    test_model(test_samples, test_labels, neuralnetwork)
    #print("NOW COMPUTING LEARNING CURVES")
    #lc_curve(X, Y)
    return


if __name__ == '__main__':
    main()
