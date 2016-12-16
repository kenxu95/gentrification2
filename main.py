import argparse
import os
import numpy as np
import sys
import random
from model.svm import SVM
from model.logistic import Logistic
from model.randomForest import RandomForest
from model.linearDiscAnalysis import LinearDiscAnalysis
from matplotlib import pyplot as plt
from feature_extraction.getLabelStats import getMedianLabel

NUM_TRAINING = [10, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]
NUM_TESTING = 100
FEATURE_LOG = 'feature_extraction/logs/featurelog'
PREDICTIONS_LOG = 'predictionsLog'
NUMTRIALS = 10

class Harness(object):
  def __init__(self, model):
    if model == 'svm':
      self.model = SVM()
    elif model == 'logistic':
      self.model = Logistic()
    elif model == 'randomForest':
      self.model = RandomForest()
    elif model == 'linearDisc':
      self.model = LinearDiscAnalysis()
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

    # Get the threshold as the median value
    # thresh = getMedianLabel(11)
    # def getLabel(value):
    #   if value <= thresh:
    #     return 1
    #   else:
    #     return 2

    xAxis = [0] * len(NUM_TRAINING)
    yAxis = [0] * len(NUM_TRAINING)
    plt.figure()
    plt.title("CHANGEME")
    plt.xlabel("# of Training Examples")
    plt.ylabel("Success Rate")
    plt.ylim([0.15, 0.3])

    false1s = []
    false2s = []

    training_success = []

    # Use the same testing data every time
    random.seed(408)
    random.shuffle(data)
    testing = data[-NUM_TESTING:]

    deviation = 0
    numDeviation = 0
    for i in xrange(NUMTRIALS):

      # Shuffle the training data
      random.seed(140 + 15 * i)
      random.shuffle(data[:NUM_TRAINING[-1]])

      for num_training in NUM_TRAINING:
        training = data[:num_training]

        NUM_LABELS = 10
        LABEL_IDX = -10
        samples = np.array([line[1:-NUM_LABELS] for line in training])
        labels = np.array([line[LABEL_IDX] for line in training])
        testsamples = ([line[1:-NUM_LABELS] for line in testing])
        testlabels = ([line[LABEL_IDX] for line in testing])

        print('Training...')
        try: self.model.train(samples, labels)
        except: 
          print 'Failed to train model', sys.exc_info()[0]
          return -1, 0
        
        if num_training == 600:
          numTrainingCorrect = 0 
          try: training_predictions = self.model.predict(samples)
          except:
            print 'Failed training prediction', sys.exc_info()[0]
            return -1, 0
          for idx, label in enumerate(labels):
            if label == training_predictions[idx]:
              numTrainingCorrect += 1
            # elif abs(label - training_predictions[idx]) <= 1:
              # numTrainingCorrect += 1

            # deviation += abs(label - training_predictions[idx])
            # numDeviation += 1
          training_success.append(float(numTrainingCorrect) / 600)

        print('Predicting...')
        try: predictions = self.model.predict(testsamples)
        except: 
          print 'Failed prediction', sys.exc_info()[0]
          return -1, 0

        print('Evaluating...')
        numCorrect = 0
        num1 = 0
        num2 = 0
        false1 = 0
        false2 = 0
        for idx, label in enumerate(testlabels):
          if label == predictions[idx]: 
            numCorrect += 1
          # elif abs(label - predictions[idx]) <= 1:
            # numCorrect += 1

        xAxis[NUM_TRAINING.index(num_training)] = str(len(labels))
        yAxis[NUM_TRAINING.index(num_training)] += float(numCorrect) / len(testlabels)
        print "Number of training examples: " + str(len(labels))
        print "Success rate testing: " +  str(float(numCorrect) / len(testlabels)) + '. ' + str(numCorrect) + ' out of ' + str(len(testlabels))

        # Write the predictions to file
        self.writePredictions(predictions)

    plt.plot(xAxis, [y / NUMTRIALS for y in yAxis])
    plt.show()

    print "Success rate training: " + ", ".join([str(x) for x in training_success])
    # print "Average deviation: " + str(float(deviation) / numDeviation)

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
parser.add_argument('model', choices=['svm', 'logistic', 'randomForest', 'linearDisc'])
args = parser.parse_args()

if __name__ == "__main__":
  print(os.path.abspath(__file__))
  harness = Harness(args.model)
  harness.run()


