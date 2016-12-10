import cv2
import os

def getThresholdedImage(imagepath):
    img = cv2.imread(imagepath, cv2.CV_8UC1)
    # Choose different blurring techniques
    #img = cv2.medianBlur(img, 5)
    img = cv2.bilateralFilter(img, 9, 75, 75)
            
    # Choose different thresholding techniques
    img= cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
    # _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return img
