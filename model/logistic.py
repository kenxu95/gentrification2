import numpy as np
from sklearn import linear_model

class Logistic:
  def __init__(self):
    self.model = linear_model.LogisticRegression()

  def train(self, samples, response):
    return self.model.fit(samples, responses)

  def predict(self, samples):
    return self.model.predict(samples)