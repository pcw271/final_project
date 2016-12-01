
import matplotlib.pyplot as plt
import six
from matplotlib import colors

import unittest
from Model.FeedForwardNetApps import *
from Model.FeedForwardNetwork.NetworkLayers import *


from dataprep.loader import *
from dataprep.transformer import *


def process_arrhythmia_supervised():

    csvloader = CSVLoader(target=[-1])
    datasetX, datasetY = csvloader.load_from_path('dataset/arrhythmia.data')
    print(datasetX.shape)
    tsX = TabularSchemaTransformer(
            [
                "numeric",          # Age
                "categorical",      # Sex
                "numeric",          # Height
                "numeric",          # Weight
                "numeric",          # QRS duration
                "numeric",          # P-R interval
                "numeric",          # Q-T interval
                "numeric",          # T interval
                "numeric",          # P interval
            ] +
            ["numeric"] * 12 +      # 10-21
            ["categorical"] * 6 +   # 22-27
            ["numeric"] * 252       # 28-279
            )
    tsY = TabularSchemaTransformer(["categorical"])

    # Normalize all numeric columns into [-1, 1] first.
    norm = ColumnNormalizer('negpos')
    # Replace all string values equal to '?' to NaN
    # Note that the '?''s in numeric fields are already replaced by NaNs
    # in TabularSchemaTransformer
    nv = NullValueTransformer('?')
    # Add a 'missing indicator' for each column with missing values
    ni = NullIndicatorTransformer()
    # Impute the NaN's in numeric fields by mean value
    mi = NumericImputationTransformer('mean')
    # One-hot categorical encoder.  PD.get_dummies() does all the magic
    ohe = OneHotEncoderTransformer()

    # A pipeline which does transformation one-by-one
    pipelineX = PipelineTransformer(tsX, norm, nv, ni, mi, ohe)
    # For labels we don't need to normalize them
    pipelineY = PipelineTransformer(tsY, nv, ni, mi, ohe)

    # Transform dataset
    processedX = pipelineX.transform(datasetX)
    processedY = pipelineY.transform(datasetY)
    return processedX, processedY

def process_abalone():

    csvloader = CSVLoader(target=[-1])
    datasetX, datasetY = csvloader.load_from_path('dataset/abalone.data')


    # Normalize all numeric columns into [-1, 1] first.
    norm = ColumnNormalizer('negpos')
    # Replace all string values equal to '?' to NaN
    # Note that the '?''s in numeric fields are already replaced by NaNs
    # in TabularSchemaTransformer

    # Add a 'missing indicator' for each column with missing values
    ni = NullIndicatorTransformer()
    # Impute the NaN's in numeric fields by mean value
    mi = NumericImputationTransformer('mean')
    # One-hot categorical encoder.  PD.get_dummies() does all the magic
    ohe = OneHotEncoderTransformer()

    # A pipeline which does transformation one-by-one
    pipelineX = PipelineTransformer(norm, ni, mi, ohe)
    # For labels we don't need to normalize them
    pipelineY = PipelineTransformer(ni, mi, ohe)

    # Transform dataset
    processedX = pipelineX.transform(datasetX)
    processedY = pipelineY.transform(datasetY)
    return processedX, processedY

def process_iris():

    csvloader = CSVLoader(target=[-1])
    datasetX, datasetY = csvloader.load_from_path('dataset/iris.data')


    # Normalize all numeric columns into [-1, 1] first.
    norm = ColumnNormalizer('negpos')
    # Replace all string values equal to '?' to NaN
    # Note that the '?''s in numeric fields are already replaced by NaNs
    # in TabularSchemaTransformer

    # Add a 'missing indicator' for each column with missing values
    ni = NullIndicatorTransformer()
    # Impute the NaN's in numeric fields by mean value
    mi = NumericImputationTransformer('mean')
    # One-hot categorical encoder.  PD.get_dummies() does all the magic
    ohe = OneHotEncoderTransformer()

    # A pipeline which does transformation one-by-one
    pipelineX = PipelineTransformer(norm, ni, mi, ohe)
    # For labels we don't need to normalize them
    pipelineY = PipelineTransformer(ni, mi, ohe)

    # Transform dataset
    processedX = pipelineX.transform(datasetX)
    processedY = pipelineY.transform(datasetY)
    return processedX, processedY

def autoencode_2d_3d(X, Y, visualize = 1):
    X = X / 2
    #print(X)
    #print(Y)
    #print(X.shape)
    #print(Y.shape)
    #print(Y.ndim)
    color_list = list(six.iteritems(colors.cnames))
    if Y.ndim == 1:
        rgb = [color_list[y*2 + 1][0] for y in Y]
    elif Y.ndim == 2:
        rgb = [color_list[4 * np.sum(
            [yi * (2 ** idx) for idx, yi in enumerate(y)])][0] for y in Y]
    else:
        visualize = 0
    #print(len(rgb))
    err = np.empty(2)
    fig = plt.figure()
    for d in [2, 3]:
        encoder = AutoEncoder(X, hidden_dim=d)
        #encoder.neuralnetworklearner.learning_rate = 1e-6
        #encoder.neuralnetworklearner.reg_const = 1e-2
        for ep in range(10):
            encoder.train(3)
            print(ep)
        reconstruction = encoder.predict()
        if visualize > 0:
            encoding_vals = encoder.get_encoding_vals()
            if d == 2:
                ax = fig.add_subplot(120 + d - 1)
                plt.scatter(encoding_vals[:, 0], encoding_vals[:, 1], color=rgb)
            if d == 3:
                ax = fig.add_subplot(120 + d - 1, projection='3d')
                ax.scatter(xs=encoding_vals[:, 0], ys=encoding_vals[:, 1],
                           zs=encoding_vals[:, 2], c=rgb)
            plt.title(str(2 ** 0 * 4) + ' Visible Variables \n With ' +
                      str(0) + ' Hidden Dimensions. Graphed in ' + str(d) + 'D')
        err[d-2] = np.mean(np.square(reconstruction - X))

    plt.show()
    return err[0], err[1]


def autoencode_abalone(visualize=1):

    X, Y = process_abalone()
    return autoencode_2d_3d(X, Y, visualize)

def autoencode_iris(visualize=1):

    X, Y = process_iris()
    return autoencode_2d_3d(X, Y, visualize)


def train_test_arrhythmia(d = 30, visualize=1):

    X, Y = process_arrhythmia_supervised()
    num_x = X.shape[0]
    color_list = list(six.iteritems(colors.cnames))
    rgb = [color_list[list(y).index(1)*3][0] for y in Y]

    NN = FeedForwardNetworkUI([X.shape[1], 100, Y.shape[1]],
                              trans_fcns="tanh", reg_const= 1e-6)
    for _ in range(10):
        NN.train(X, Y, epochs=10)
    y_predict = NN.predict(X)
    y_output = np.zeros_like(y_predict)
    for idx, yi in enumerate(y_predict):
        y_output[idx, np.argmax(yi)] = 1
    err = 0
    for yhat, y in zip(y_output, Y):
        if list(yhat) != list(y):
            err += 1/Y.shape[0]
    return err


class TestAutoEncodingData(unittest.TestCase):
    """
    unit tests for functions relating to the interval class
    These should be run by enterring the command "python -m unittest discover"
    from the root directory of this project
    """

    def test_autoencode_iris(self):
        np.random.seed(1)
        err_2d, err_3d = autoencode_iris(visualize=1)
        print(err_2d)
        print(err_3d)
        self.assertLess(err_2d, .1)
        self.assertLess(err_3d, .1)

    def test_autoencode_abalone(self):
        np.random.seed(1)
        err_2d, err_3d = autoencode_abalone(visualize=1)
        print(err_2d)
        print(err_3d)
        self.assertLess(err_2d, .1)
        self.assertLess(err_3d, .1)
