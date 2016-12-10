import numpy as np
import os
import cv2
import random
from edgeExtractor import EdgeExtractor
from colorHistogram import ColorHistogram

FEATURE_LOG = 'logs/featurelog'
FEATURE_EXTRACTORS = [
  EdgeExtractor(100, 500, 1),
  ColorHistogram()
]

def getLabelData():
  f = open('images/labels.csv')
  labels = []
  f.readline()
  for line in f:
    labels.append(float(line.split(',')[1]))
  f.close()
  return labels

def writeFeatures():
  output = open(FEATURE_LOG, 'w')

  # Read [id, label]'s'
  labels = getLabelData()

  # For every image, extract the features and write them to feature log
  count = 0
  lines = []
  for filename in os.listdir(os.path.join(os.path.dirname(__file__), 'images')):
    if filename.endswith('.png'):
      imgpath = os.path.join(os.path.dirname(__file__), 'images', filename)
      img = cv2.imread(imgpath)
      features = []
      for feature_extractor in FEATURE_EXTRACTORS:
        features.extend(feature_extractor.getFeatures(img))

      # Write the features
      line = os.path.splitext(filename)[0] + ' ' 
      for elem in features:
        line += str(elem) + ' '
      line += str(labels[int(os.path.splitext(filename)[0])])
      lines.append(line)
      count = count + 1
      print "Wrote " + str(count) + " feature vectors: (" + os.path.splitext(filename)[0] + ")"

  # Write the feature vectors to file (scrambled)
  random.shuffle(lines)
  for line in lines:
    output.write(line + '\n')
  output.close()


writeFeatures()