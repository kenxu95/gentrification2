import sys
import cv2
import numpy 
from edgeExtractor import EdgeExtractor
from colorHistogram import ColorHistogram
# from shapeExtractor import ShapeExtractor

imagename = sys.argv[1]
img = cv2.imread('images/' + imagename + '.png') #cv2.CV_8UC1

procedure = sys.argv[2]

features = None
if procedure == 'edges' or procedure == 'shapes':
  def edgeCallback(img, imagename):
    cv2.imwrite('images/' + imagename + 'Edges.png', img)
  ee = EdgeExtractor(100, 500, 1) #100, 200, 3, 3 (default)
  features = ee.getFeatures(img) #imagename, edgeCallback
  # if procedure == 'shapes':
    # def shapeCallback(img, imagename, contours):
      # cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
      # for cnt in contours:
      #   box = cv2.boxPoints(cv2.minAreaRect(cnt))
      #   cv2.drawContours(img, [box], 0, (0, 0, 255), 2)  
      # cv2.imwrite('images/' + imagename + 'Shapes.png', img)
    # she = ShapeExtractor()
    # features = she.getFeatures(edges, img, imagename, shapeCallback)

elif procedure == 'colors':
  colorHist = ColorHistogram()
  features = colorHist.getFeatures(img)

print features
