import numpy as np
from sklearn.ensemble import RandomForestClassifier

class RandomForest:
  def __init__(self):
    self.model = RandomForestClassifier(n_estimators=300, max_features=30, max_depth=10, min_samples_leaf=5)  # Change this parameter
 
  def train(self, samples, responses):
    return self.model.fit(samples, responses)

  def predict(self, samples):
    return self.model.predict(samples)