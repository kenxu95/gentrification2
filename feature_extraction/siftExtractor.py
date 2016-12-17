import numpy as np 
import cv2

class SIFTExtractor():
    def __init__(self):
        pass

    def getFeatures(self, img, imagename=None, callback=None):
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        sift = cv2.SIFT() #features2d.SIFT_create()
        kp, des = sift.detectAndCompute(gray, None)
    
        img2 = cv2.drawKeypoints(gray,kp)
        print kp[0]
        print des[0]

        # For debugging
        if callback:
            callback(img2, imagename + 'keypoints')
        
        return []

        # width = mask.shape[0]
        # height = mask.shape[1]
        # totalArea = float(width * height)
        # features = [cv2.sumElems(mask)[0] / (255 * totalArea)]

        # sixteenths = [0] * 16
        # for x in xrange(4): # width
        #     for y in xrange(4): # height
        #         start_x = x * (width / 4)
        #         end_x = start_x + (width / 4)
        #         start_y = y * (height / 4)
        #         end_y = start_y + (height / 4)

        #         sixteenths[4 * x + y] = cv2.sumElems(mask[start_x : end_x, start_y : end_y])[0] / (255 * totalArea / 16)

        # features.extend(sixteenths)

        # # for x in xrange(width):
        # #   for y in xrange(height):
        # #       x_idx = x / (width / 4)
        # #       y_idx = y / (height / 4)
        # #       sixteenths[x_idx + y_idx * 4] += mask[x][y] / 255
        # # features.extend([x / (float(totalArea) / 16) for x in sixteenths])    

        # return features
