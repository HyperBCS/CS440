# mlp.py
# -------------

# mlp implementation
import util
import math
import random
from copy import deepcopy
import math
PRINT = True

class MLPClassifier:
  """
  mlp classifier
  """
  def __init__( self, legalLabels, max_iterations):
    self.legalLabels = legalLabels
    self.type = "mlp"
    self.max_iterations = max_iterations
    self.weights = {}
    for label in legalLabels:
      self.weights[label] = util.Counter() # this is the data-structure you should use

  def setWeights(self, weights):
    assert len(weights) == len(self.legalLabels);
    self.weights == weights;

  def sig(self,err,deriv=False):
    if deriv:
      return err * (1 - err)
    return 1/(1 + math.exp(err))
      
  def train( self, trainingData, trainingLabels, validationData, validationLabels ):
    # Create hidden network
    print(type(trainingData))
    for iteration in range(self.max_iterations):
      print "Starting iteration ", iteration, "..."
      for i in range(len(trainingData)):
          y = trainingLabels[i]
          data = trainingData[i]
          tmp_weights = util.Counter()
          # Create a weight for every label and forward pass
          for l in self.legalLabels:
            # Dot product xi * wi to get scalar value, or sum 
            tmp_weights[l] = self.weights[l].__mul__(data)
          # Return the label with the highest score
          y_p = tmp_weights.argMax()
          # Normalized error
          error = (tmp_weights[y] - tmp_weights[y_p]) / max(1,tmp_weights[y_p])
          # fine error delta
          err_delta = self.sig(error)
          # print error
          # Multiply error by sigmoid function to get derivative
          error_delta = err_delta * self.sig(err_delta,True)
          data2 = util.Counter()
          for key in data:
            data2[key] = data[key] * err_delta
          
          # update the weights with the new delta
          self.weights[y].__radd__(data2)
    
  def classify(self, data ):
    guesses = []
    for datum in data:
      vectors = util.Counter()
      for l in self.legalLabels:
        vectors[l] = self.weights[l] * datum
      guesses.append(vectors.argMax())
    return guesses