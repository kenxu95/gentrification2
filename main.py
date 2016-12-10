import argparse
import os
import numpy as np
import sys
import random
from model.svm import SVM
from model.logistic import Logistic
from matplotlib import pyplot as plt

NUM_TRAINING = [10, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]
NUM_TESTING = 100
FEATURE_LOG = 'feature_extraction/logs/featurelog'
PREDICTIONS_LOG = 'predictionsLog'
NUMTRIALS = 5

class Harness(object):
  def __init__(self, model):
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
    for line in f:
      data.append([float(x) for x in line.strip().split(' ')])
    f.close()

    def getLabel(pop_density):
      if pop_density < 1000:
        return 1
      else:
        return 2

    xAxis = []
    yAxis = []
    plt.figure()
    plt.title("Learning Curve for Thresholded Population Density (3 features)")
    plt.xlabel("# of Training Examples")
    plt.ylabel("Success Rate")
    plt.ylim([0.4, 0.8])

    for i in xrange(NUMTRIALS):
      # Get the random test samples
      random.shuffle(data)

      testing = data[-NUM_TESTING:]
      for num_training in NUM_TRAINING:
        training = data[:num_training]

        samples = np.array([line[1:4] for line in training])
        labels = np.array([getLabel(line[-1]) for line in training])
        testsamples = ([line[1:4] for line in testing])
        testlabels = ([getLabel(line[-1]) for line in testing])

        print('Training...')
        try: self.model.train(samples, labels)
        except: 
          print 'Failed to train model', sys.exc_info()[0]
          return -1, 0
          
        print('Predicting...')
        try: predictions = self.model.predict(testsamples)
        except: 
          print 'Failed prediction', sys.exc_info()[0]
          return -1, 0

        print('Evaluating...')
        numCorrect = 0
        for idx, label in enumerate(testlabels):
          if label == predictions[idx]: numCorrect += 1

        xAxis.append(str(len(labels)))
        yAxis.append(str(float(numCorrect) / len(testlabels)))
        print "Number of training examples: " + str(len(labels))
        print "Success rate: " +  str(float(numCorrect) / len(testlabels)) + '. ' + str(numCorrect) + ' out of ' + str(len(testlabels))

      plt.plot(xAxis, yAxis)
      xAxis = []
      yAxis = []
    
    plt.show()

    # Write the predictions to file
    # self.writePredictions(predictions)


  # Writes predictions to file
  def writePredictions(self, predictions):
    f = open(PREDICTIONS_LOG, 'w')
    for prediction in predictions:
      f.write(str(predictions) + '\n\n')
    f.close()

  def run(self):
    # Write all the features and labels to log file
    print("Reading features...")
    self.readFeatureLogs() # AND TEST


##### END OF HARNESS CLASS #########

parser = argparse.ArgumentParser()
parser.add_argument('model', choices=['svm', 'logistic'])
args = parser.parse_args()

if __name__ == "__main__":
  print(os.path.abspath(__file__))
  harness = Harness(args.model)
  harness.run()


