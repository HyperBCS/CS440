# mlp.py
# -------------

# mlp implementation
import util
import math
import random
import numpy as np
from copy import deepcopy
import sklearn.metrics as metrics
import math
PRINT = True


class MLPClassifier:
  """
  mlp classifier
  """
  def __init__( self, legalLabels, max_iterations):
    self.legalLabels = legalLabels
    self.type = "mlp"
    self.max_iterations = 20000

  # def sig(self,x,deriv=False):
  #   """Compute softmax values for each sets of scores in x."""
  #   e_x = np.exp(x - np.max(x))
  #   return e_x / e_x.sum()

  def sig(self,x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

  def one_hot(self, labels_train):
    '''Convert categorical labels 0,1,2,....9 to standard basis vectors in R^{10} '''
    y = np.zeros((len(self.legalLabels), len(labels_train)))
    for i, label in enumerate(labels_train):
        y[label, i] = 1.0
    return y
      
  def train( self, trainingData, trainingLabels, validationData, validationLabels ):
    X = np.empty([len(trainingData), len(trainingData[0])])
    Y = self.one_hot(trainingLabels)
    map_h = int(math.sqrt(len(trainingData[0])))
    for n, dd  in enumerate(trainingData):
      for key in trainingData[n]:
        X[n][map_h*key[0] + key[1]] = trainingData[n][key]
    print "done fixing data"
    L = np.asarray(trainingLabels)
    hidden_size = 300 # change
    train_size = len(trainingData)
    n, d = X.shape
    # append 1 for bias term
    self.V = np.random.normal(0,0.01,(hidden_size, d + 1)) #200 x 784 + 1
    self.W = np.random.normal(0,0.01,(len(self.legalLabels), hidden_size + 1)) #10 x 200 + 1
    Y = Y.T
    alpha = 0.01
    for i in range(self.max_iterations):
      if i % train_size == 0 and i >= train_size:
        print str((100 * i / (1.0 * self.max_iterations))) + "%"
        indices = np.arange(n)
        random.shuffle(indices)
        X = X[indices]
        Y = Y[indices]
        L = L[indices]
        alpha = alpha * 0.5

      x = X[i % train_size] #i_th shuffled element, should be 784 x 1
      
      y = Y[i % train_size]
      x = np.append(x, 1.0).reshape(785, 1) #785 x 1
      
      z_1 = np.append(np.asarray(self.V.dot(x)), 1.0) # (200 + 1 x 785) x (785 x 1)
      x_2 = z_1 * (z_1 > 0) #Fast ReLu 

      z_2 = self.W.dot(x_2)
      x_3 = np.clip(self.sig(z_2), 0.0001, 1e8) #clip for bad values
      # Cross Entropy
      J = -1.0 * np.sum(np.multiply(np.asmatrix(y), np.log(x_3)))
      J = np.asscalar(J)

      D = np.diag(np.asarray(x_3).reshape(-1)) - x_3.T.dot(x_3) #10 x 10
      dJ = -1.0 * np.divide(np.asmatrix(y), x_3) #1 x 10
      delta2 = D.dot(dJ.T) #10 x 1
      dW = delta2.dot(np.asmatrix(x_2)) #10 x 1 x 1 x 201

      dReLu = (z_1 > 0).astype(float) #201 x 1 
      d6 = delta2.T.dot(self.W) #delta2 x W
      d6d5 = np.multiply(d6, np.asmatrix(dReLu)) #delta2 x W * dReLu
      dV = d6d5.T[:-1].dot(x.T) #update

      self.W = self.W - alpha * dW
      self.V = self.V - alpha * dV

  def classify(self, data):
    ''' From model and data points, output prediction vectors ''' 
    X = np.empty([len(data), len(data[0])])
    map_h = int(math.sqrt(len(data[0])))
    for n, dd  in enumerate(data):
      for key in data[n]:
        X[n][map_h*key[0] + key[1]] = data[n][key]
    n, d = X.shape 
    X_1 = np.hstack((X, np.ones((n, 1))))
    VX = self.V.dot(X_1.T)
    Z_1 = np.vstack((VX, np.ones((1, VX.shape[1]))))
    X_2 = np.multiply(Z_1, (Z_1 > 0)) 
    Z_2 = self.W.dot(X_2)
    X_3 = self.sig(Z_2)
    return np.asarray(np.argmax(X_3, axis=0)).reshape(-1) 
    