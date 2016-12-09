from .. import base
import numpy as np
import cv2

class EdgeExtractor(base.BaseFeatureExtractor):
    def __init__(self, minVal, maxVal, aperture_size, scale_factor):
        self.minVal = minVal
        self.maxVal = maxVal
        self.aperture_size = aperture_size
        self.scale = scale_factor

    def getFeatures(self, img):
        # Resize the image to a scaled size
        resized_img = cv2.resize(img, (int(img.shape[1] * self.scale), int(img.shape[0] * self.scale)), 
                                 interpolation = cv2.INTER_AREA)
        
        # Perform edge extraction
        edges = cv2.Canny(resized_img, self.minVal, self.maxVal, self.aperture_size)
       
        return np.array([cv2.sumElems(edges)[0] / (255 * edges.shape[0] * edges.shape[1])]) # Sum of total elements

        # OUTPUT IMAGE FOR DEBUGGING
        #cv2.imwrite('./feature_extractors/macro/output/original.jpg', img)
        # cv2.imwrite('./feature_extractors/macro/output/edgetest.jpg', edges)
        
        # return np.ndarray.flatten(np.array(edges))