import numpy as np 
import cv2

class GreenExtractor():
	def __init__(self, minVal, maxVal, aperture_size):
		self.minVal = minVal
		self.maxVal = maxVal
		self.aperture_size = aperture_size

	def getFeatures(self, img, imagename=None, callback=None):
		# For debugging
		if callback:
            callback(edges, imagename)

		# Convert BGR to HSV
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		 
		# define range of blue color in HSV
		lower_blue = np.array([50,100,100])
		upper_blue = np.array([70,255,255])
		 
		# Threshold the HSV image to get only blue colors
		mask = cv2.inRange(hsv, lower_blue, upper_blue)
		 
		# Bitwise-AND mask and original image
		res = cv2.bitwise_and(frame,frame, mask= mask) 

		cv2.imshow('frame',frame)
		cv2.imshow('mask',mask)
		cv2.imshow('res',res)
		cv2.waitKey(5)
		 
		cv2.destroyAllWindows()

		length = img.shape[0]
		width = img.shape[1]
		area = length * width
		feature = [sum(mask)/area]
		print feature
		return feature
