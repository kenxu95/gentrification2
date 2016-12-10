# from matplotlib import pyplot as plt
import numpy as np
import cv2
import math
import operator

# TODO: More fancy shapes?
class ShapeExtractor():
    def __init__(self):
      pass

    def getFeatures(self, edges, img, imagename=None, shapeCallback=None):
      contours, hierachy = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
      totalArea = img.shape[0] * img.shape[1]

      # Create the feature vector
      features = []
      features.append(sum([cv2.contourArea(cnt) for cnt in contours]) / totalArea)
      features.append(sum([cv2.arcLength(cnt) for cnt in contours]) / totalArea)

      if shapeCallback:
        shapeCallback(img, imagename, contours)
      return features
