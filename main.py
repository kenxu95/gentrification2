import argparse
import os
import numpy as np
import sys
from feature_extraction.featureExtraction import featureExtraction
from model.svm import SVM
from model.logistic import Logistic

FEATURE_LOG = 'feature_extraction/images/featurelog'
PREDICTIONS_LOG = 'predictionsLog'

class Harness(object):
  def __init__(self, model):
    self.featureExtraction = featureExtraction()
    if model == 'svm':
      self.model = SVM()
    elif model == 'logistic':
      self.model = Logistic()
    else:
      print('no such model exists yet')
      1/0

  # Reads the features from the feature logs into (samples, labels, testsamples, testlabels)
  def readFeatureLogs(self):
    f = open(FEATURE_LOG)
    data = []
    for line in data:
      data.append(line.strip().split(' '))
    f.close()

    # Get the random test samples
    testingIndexes = random.sample(xrange(len(data)), 0.2 * len(data))
    training = [x for i, x in data if i not in testingIndexes]
    testing = [x for i, x in data if i in testingIndexes]

    samples = [line[:-1] for line in training]
    labels = [line[-1] for line in training]
    testSamples = [line[:-1] for line in testing]
    testlabels = [line[-1] for line in testing]
    return samples, labels, testSamples, testlabels

  # Writes predictions to file
  def writePredictions(self, predictions):
    f = open(PREDICTIONS_LOG, 'w')
    f.write(predictions)
    f.close()

  def run(self):
    # Write all the features and labels to log file
    print("Extracting features...")
    featureExtraction.writeFeatures()
    samples, labels, testsamples, testlabels = self.readFeatureLogs()

    print('Training...')
    try: classifier.train(samples, responses)
    except: 
      print 'Failed to train model', sys.exc_info()[0]
      return -1, 0
      
    print('Predicting...')
    try: predictions = classifier.predict(testsamples)
    except: 
      print 'Failed prediction', sys.exc_info()[0]
      return -1, 0

    print('Evaluating...')
    numCorrect = 0
    for idx, label in enumerate(testlabels):
      if label == predictions[idx]: numCorrect += 1

    print("Number of training examples: " + len(labels))
    print("Success rate: " +  float(numCorrect) / len(testlabels) + '. ' + numCorrect + 'out of ' + len(testlabels))

    # Write the predictions to file
    self.writePredictions(self, predictions)

##### END OF HARNESS CLASS #########

parser = argparse.ArgumentParser()
parser.add_argment('model', choices=['svm', 'logistic'])
args = parser.parse_args()

if __name__ == "__main__":
  print(os.path.abspath(__file__))
  harness = Harness(args.model)
  harness.run()


