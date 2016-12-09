import numpy as np
from edgeExtractor import EdgeExtractor

# TODO: Take in the number of training examples as a parameter
class FeatureExtractor():
  def __init__(self):
    self.feature_extractors = [
      EdgeExtractor(100, 200, 3, 1), # 1 total average feature
    ]

  # TODO: Write every feature for every image into a log file
  def writeFeatures(self):
    # features = np.array([])
    # for feature_extractor in self.feature_extractors:
    #   features = np.concatenate((features, feature_extractor.getFeatures(image)))
