# svm.py
# -------------

# svm implementation
import util
from sklearn import svm
PRINT = True

class SVMClassifier:
  """
  svm classifier
  """
  def __init__( self, legalLabels):
    self.legalLabels = legalLabels
    self.type = "svm"
    self.clf = svm.SVC(gamma=0.001, C=100.)
      
  def train( self, trainingData, trainingLabels, validationData, validationLabels ):
    print "Starting svm"
    digits = []
    # transform data to fit scikit
    for i in range(len(trainingData)):
        digits.append(list(trainingData[i].values()))
    # fit data using scikit
    self.clf.fit(digits, trainingLabels) 
    print "Done fitting data"
    
  def classify(self, data ):
    guesses = []
    for datum in data:
      # fill predictions in the guesses list
      guesses.append(self.clf.predict([list(datum.values())]))
      
    return guesses

