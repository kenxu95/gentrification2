import numpy as np
from sklearn import svm

class SVM:
  def __init__(self, C = 1, gamma = 0.5):
    self.model = svm.SVC()  
 
  def train(self, samples, responses):
    return self.model.fit(samples, responses)

  def predict(self, samples):
    return self.model.predict(samples)