import cv2
import os

class textureExtractor():
    
    def getFeatures(self, img, imagename=None, callback=None):
        #perform texture extraction
        
        # Choose different blurring techniques
        #img = cv2.medianBlur(img, 5)
        #reduce unwanted noise
        features = cv2.bilateralFilter(img, 9, 75, 75)
            
        # Choose different thresholding techniques
        features= cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
        # _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return features
