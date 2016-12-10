import numpy as np
import cv2

class EdgeExtractor():
    def __init__(self, minVal, maxVal, aperture_size):
        self.minVal = minVal
        self.maxVal = maxVal
        self.aperture_size = aperture_size

    def getFeatures(self, img, imagename=None, callback=None):
        # Perform edge extraction
        edges = cv2.Canny(img, self.minVal, self.maxVal, self.aperture_size)

        # For debugging
        if callback:
            callback(edges, imagename)

        # Edge feature
        totalArea = edges.shape[0] * edges.shape[1]
        features = [cv2.sumElems(edges)[0] / (255 * totalArea)]
      
        # Shape features
        contours, hierachy = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        totalArea = img.shape[0] * img.shape[1]
        features.append(sum([cv2.contourArea(cnt) for cnt in contours]) / totalArea)
        features.append(sum([cv2.arcLength(cnt) for cnt in contours]) / totalArea)

        return features
        
