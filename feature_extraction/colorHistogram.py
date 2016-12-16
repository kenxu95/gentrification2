from matplotlib import pyplot as plt
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

      allBins = []
      lenHist = None
      for (chan, color) in zip(chans, colors):
        hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
        lenHist = len(hist)
        allBins.extend(hist)

      #   plt.plot(hist, color=color)
      #   plt.xlim([0, 256])
      # plt.show()

      allBins = [elem[0] for elem in allBins]
      c1 = [0] * 16
      c2 = [0] * 16
      c3 = [0] * 16
      for i in xrange(len(allBins)):
        if i / lenHist == 0:
          c1[(i % lenHist) / 16] += allBins[i]
        if i / lenHist == 1:
          c2[(i % lenHist) / 16] += allBins[i]
        if i / lenHist == 2:
          c3[(i % lenHist) / 16] += allBins[i]

      sumc1 = sum(c1)
      sumc2 = sum(c2)
      sumc3 = sum(c3)

      features1 = [int(x > (sumc1 / 16)) for x in c1]
      features2 = [int(x > (sumc2 / 16)) for x in c2]
      features3 = [int(x > (sumc3 / 16)) for x in c3]      
      return features1 + features2 + features3 

      # for i in xrange(lenHist):
      #   total = allBins[i][1] + allBins[i + lenHist][1] + allBins[i + 2 * lenHist][1]
      #   if total > 0:
      #     allBins[i][1] /= total
      #     allBins[i + lenHist][1] /= total
      #     allBins[i + 2 * lenHist][1] /= total
      #   else:
      #     allBins[i][1] = 1.0 / 3
      #     allBins[i + lenHist][1] = 1.0 / 3
      #     allBins[i + 2 * lenHist][1] = 1.0 / 3 

      # # Take the top 50 bins from each color (TOTAL: 150 features)
      # NUMTOP = 50
      # c1 = sorted(allBins[:lenHist], key=lambda x: x[1], reverse=True)[:NUMTOP]
      # c2 = sorted(allBins[lenHist: 2 * lenHist], key=lambda x: x[1], reverse=True)[:NUMTOP]
      # c3 = sorted(allBins[2 * lenHist:], key=lambda x: x[1], reverse=True)[:NUMTOP]

      # c1 = [x % lenHist for x in zip(*c1)[0]]
      # c2 = [x % lenHist for x in zip(*c2)[0]]     
      # c3 = [x % lenHist for x in zip(*c3)[0]]     
      # return c1 + c2 + c3
