import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

class LinearDiscAnalysis():
  def __init__(self):
    self.model = LinearDiscriminantAnalysis()
 
  def train(self, samples, responses):
    return self.model.fit(samples, responses)

  def predict(self, samples):
    return self.model.predict(samples)