import matplotlib.pyplot as plt
import numpy as np

from Model import nn_helper as helper, validation
from Model.Network import NeuralNetwork as nn_uf


def test_xor(verb=0, re_init=10, netstruc='ff'):
    tNN = nn_uf.nnp([2, 100, 1], reg=10 ** -10, netstruc=netstruc)
    X = np.array([[0, 0],
                  [0, 1],
                  [1, 0],
                  [1, 1]])
    Y = np.array([np.array([x[0] ^ x[1]]) for x in X])
    tNN.train(X, Y, epochs=100, verb=verb, batch_type=helper.GROUP,
              re_init=re_init, re_init_d=100)
    y_predict = tNN.predict(X)
    if verb > -1:
        helper.print_y(y_predict, Y)
    return np.mean(np.square(y_predict - Y))
np.random.seed(2)
test_xor()


def test_xor3(verb=0, **kwargs):
    tNN = nn_uf.nnp([3, 100, 100, 1], reg=10 ** -1)
    X = np.array([[0, 0, 0],
                  [0, 1, 0],
                  [1, 0, 0],
                  [1, 1, 0],
                  [0, 0, 1],
                  [0, 1, 1],
                  [1, 0, 1],
                  [1, 1, 1]])
    Y = np.array([np.array([x[0] ^ x[1] ^ x[2]]) for x in X])
    tNN.train(X, Y, epochs=3000, verb=verb, re_init=10, re_init_d=20,
              **kwargs)
    y_predict = tNN.predict(X)
    if verb > -1:
        print(Y.flatten())
        helper.print_y(y_predict, Y)
    return np.mean(np.square(y_predict - Y))
if 0:
    xor3_err = test_xor3(verb = 1,
                objective = 10**-10, del_thresh=10**-15,
                max_fail = 100, nudge = 100)
    print("xor3 error is: " + str(xor3_err))


# Does not yet work well. needs purelin transfer fcn
def test_sine(verb=0, netstruc='ff', **kwargs):
    tNN = nn_uf.nnp([1, 2000, 1], reg=10 ** -1, trans='tanh')
    X = np.array([np.array([x]) for x in np.arange(0, 2 * np.pi, .1)])
    Y = np.array([np.sin(x) + np.random.randn(x.shape[0]) * .001
                 for x in X])
    tNN.train(X, Y, epochs=2000, verb=verb, re_init=5, re_init_d=50, **kwargs)
    y_predict = tNN.predict(X)
    if verb > 0:
        print(Y.flatten())
        plt.plot(X, Y)
        plt.plot(X, y_predict)
        plt.show()
    if verb > -1:
        helper.print_y(y_predict, Y)
    return np.mean(np.square(y_predict - Y))
if 0:
    sine_error = test_sine(verb = 1, objective = 10**-10, del_thresh=10**-15,
                           max_fail = 100, nudge = 100)
    print('Sine error is: ', sine_error)

#need to visualize results
def x1dotx2(verb=0, **kwargs):
    tNN = nn_uf.nnp([2, 10, 1], reg=0, trans = 'tanh')
    X = np.array([np.array([x, c]) for x in np.linspace(-1, 1, 5)
                 for c in np.linspace(-1, 1, 5)])
    Y = np.array([np.array([x[0] * x[1]]) for x in X])
    tNN.train(X, Y, epochs=10000, verb=verb, re_init=10, re_init_d=10, **kwargs)
    y_predict = tNN.predict(X)
    if verb > 0:
        print(Y.flatten())
    if verb > -1:
        helper.print_y(y_predict, Y)
    return np.mean(np.square(y_predict - Y))
if 0:
    dot_err = x1dotx2(objective = 10**-10, del_thresh=10**-15, max_fail = 300, nudge = 300,
            verb = 1)
    print('dot error is: ', dot_err)
    
    
def x1plusx2squared(verb = 0, **kwargs):
    tNN = nn_uf.nnp([2, 10, 10, 1], reg=10 ** -10, trans = 'tanh')
    X = np.array([np.array([x, c]) for x in np.linspace(-1, 1, 10)
                 for c in np.linspace(-1, 1, 10)])
    Y = np.array([np.array([x[0] + (x[1]**2)]) for x in X])
    val_err = validation.kfoldvalidation(X, Y, tNN, k=4, graph=False, verb = verb, **kwargs)
    tNN.train(X, Y, verb = verb, **kwargs)
    y_predict = tNN.predict(X)
    if verb > 0:
        print(Y.flatten())
    if verb > -1:
        helper.print_y(y_predict, Y)
    return np.mean(np.square(y_predict - Y)), val_err
if 0:
    dot_err = x1plusx2squared(epochs=1000, re_init=3, re_init_d=20,
                             objective = 10**-5, del_thresh=10**-15, max_fail = 300, nudge = 300,
                             verb = 1)
    print('dot error is: ', dot_err)
