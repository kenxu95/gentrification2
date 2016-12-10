# from matplotlib import pyplot as plt
import numpy as np
import cv2

class ColorHistogram():
    def __init__(self):
      pass

    def getFeatures(self, img):
      chans = cv2.split(img)
      colors = ("b", "g", "r")

      # plt.figure()
      # plt.title("'Flattened' Color Histogram")
      # plt.xlabel("Bins")
      # plt.ylabel("# of Pixels")

      features = []
      lenHist = None
      for (chan, color) in zip(chans, colors):
        hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
        lenHist = len(hist)
        features.extend(hist)

        # plt.plot(hist, color=color)
        # plt.xlim([0, 256])
      # plt.show()

      # Fixes the stupid return value
      features = [elem[0] for elem in features]
      for i in xrange(lenHist):
        total = features[i] + features[i + lenHist] + features[i + 2 * lenHist]
        if total > 0:
          features[i] /= total
          features[i + lenHist] /= total
          features[i + 2 * lenHist] /= total
        else:
          features[i] = 1.0 / 3
          features[i + lenHist] = 1.0 / 3
          features[i + 2 * lenHist] = 1.0 / 3 
      return features
