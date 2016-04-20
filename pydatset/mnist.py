import os
import struct
import numpy as np
from numpy import genfromtxt
import pandas as pd

"""
Loosely inspired by https://gist.github.com/akesling/5358964
which is GPL licensed.
"""


def get_data(dataset_path, mode='std'):
    '''
    mode:
        std => standard dataset
        kaggle => kaggle dataset
    '''
    if mode is 'std':
        pass
    elif mode is 'kaggle':
        read = read_kaggle_version
    else:
        raise ValueError("mode must be 'std' or 'kaggle'")

    X_train, y_train = read('training', dataset_path)
    X_test, y_test = read('testing', dataset_path)

    return {
        'X_train': X_train, 'y_train': y_train,
        'X_test': X_test, 'y_test': y_test,
    }


def read(dataset="training", path="../MNIST"):
    """
    Python function for importing the MNIST data set.  It returns an iterator
    of 2-tuples with the first element being the label and the second element
    being a numpy.uint8 2D array of pixel data for the given image.
    """

    if dataset is "training":
        fname_img = os.path.join(path, 'train-images-idx3-ubyte')
        fname_lbl = os.path.join(path, 'train-labels-idx1-ubyte')
    elif dataset is "testing":
        fname_img = os.path.join(path, 't10k-images-idx3-ubyte')
        fname_lbl = os.path.join(path, 't10k-labels-idx1-ubyte')
    else:
        raise ValueError("dataset must be 'testing' or 'training'")

    # Load everything in some numpy arrays
    with open(fname_lbl, 'rb') as flbl:
        magic, num = struct.unpack(">II", flbl.read(8))
        lbl = np.fromfile(flbl, dtype=np.int8)

    with open(fname_img, 'rb') as fimg:
        magic, num, rows, cols = struct.unpack(">IIII", fimg.read(16))
        img = np.fromfile(fimg, dtype=np.uint8).reshape(
            len(lbl), 1, rows, cols)

    return img, lbl


def read_kaggle_version(dataset="training", path="../MNIST"):
    '''
    Read the csv mnist files provided by kaggle:
    https://www.kaggle.com/c/digit-recognizer/
    '''
    if dataset is "training":
        fname = os.path.join(path, 'train.csv')
        data = pd.read_csv(fname, delimiter=",", dtype=np.int8).values
        lbl = data[:, 0]
        img = data[:, 1:].reshape(-1, 1, 28, 28)

    elif dataset is "testing":
        fname = os.path.join(path, 'test.csv')
        data = pd.read_csv(fname, delimiter=",").values
        lbl = None
        img = data.reshape(-1, 1, 28, 28)
    else:
        raise ValueError("dataset must be 'testing' or 'training'")
    return img, lbl
