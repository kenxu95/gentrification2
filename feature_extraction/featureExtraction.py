import numpy as np
import os
import cv2
import random
from edgeExtractor import EdgeExtractor
from colorHistogram import ColorHistogram
from textureExtractor import TextureExtractor
from greenExtractor import GreenExtractor

FEATURE_LOG = 'logs/featurelog'
FEATURE_EXTRACTORS = [
  EdgeExtractor(100, 500, 1),
  ColorHistogram(),
  TextureExtractor(),
  GreenExtractor()
]

def convertToFloat(x):
  if x == '':
    return 0
  else:
    return float(x)

def calcThreshold(labels, i):
  colArr = [line[i] for line in labels]
  colArr.sort()
  return colArr[len(colArr) / 2]

# Gentrification index (9)
# % housing units that are 5+ units (10)
# % renter-occupied (12)
# % of workers taking public transportation (13)
# Median Gross Income (14)
# % Non-family households (16)
# % of renters paying of 35% (18)
# Income Diversity (19)
# Gini index (20)
# Population Density (21)

def getLabelData():
  f = open('images/labels2.csv')
  labels = []
  f.readline()
  for line in f:
    lineArr = line.split(',')
    labels.append([convertToFloat(x) for x in lineArr[9:11] + lineArr[12:15] + lineArr[16:17] + lineArr[18:22]])
  f.close()

  # Split all the non-gentrification values into top 50% and bottom 50%
  for i in xrange(len(labels[0])):
    thresh = calcThreshold(labels, i)
    for line in labels:
      line[i] = str(1) if line[i] < thresh else str(2)
  return labels

def writeFeatures():
  output = open(FEATURE_LOG, 'w')

  # Read [id, label]'s'
  labels = getLabelData()

  # For every image, extract the features and write them to feature log 
  count = 0
  for filename in os.listdir(os.path.join(os.path.dirname(__file__), 'images')):
    if filename.endswith('.png') and os.path.splitext(filename)[0] != 'Stanford':
      imgpath = os.path.join(os.path.dirname(__file__), 'images', filename)
      img = cv2.imread(imgpath)
      features = []
      for feature_extractor in FEATURE_EXTRACTORS:
        features.extend(feature_extractor.getFeatures(img))

      # Write the features
      line = os.path.splitext(filename)[0] + ' ' 
      for elem in features:
        line += str(elem) + ' '
      line += " ".join(labels[int(os.path.splitext(filename)[0]) - 1])
      output.write(line + '\n')

      count = count + 1
      print "Wrote " + str(count) + " feature vectors: (" + os.path.splitext(filename)[0] + ")"
  output.close()


writeFeatures()