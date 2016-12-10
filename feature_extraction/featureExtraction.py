import numpy as np
from edgeExtractor import EdgeExtractor
from colorHistogram import ColorHistogram

FEATURE_LOG = 'log/featurelog'

# TODO: Take in the number of training examples as a parameter
class FeatureExtractor():
  def __init__(self):
    self.feature_extractors = [
      EdgeExtractor(100, 200, 3, 1),
      ColorHistogram()
    ]

  def writeFeatures(self):
    output = open(FEATURE_LOG, 'w')

    # For every image, extract the features and write them to feature log
    for filename in os.listdir(os.path.join(os.path.dirname(__file__), 'images')):
      if filename.endswith('.png'):
        imgpath = os.path.join(os.path.dirname(__file__), 'images', filename)
        img = cv2.imread(imgpath)
        features = []
        for feature_extractor in self.feature_extractors:
          features.extend(feature_extractor.getFeatures(image))

        # Write the features
        for elem in features:
          output.write(str(elem) + ' ')
        output.write('\n')
    output.close()
