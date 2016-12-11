import numpy as np 
import cv2

class GreenExtractor():
	def __init__(self):
		pass

	def getFeatures(self, img, imagename=None, callback=None):
		# For debugging
		

		# Convert BGR to HSV
		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		 
		# define range of blue color in HSV
		lower_blue = np.array([50,10,10])
		upper_blue = np.array([70,255,255])
		 
		# Threshold the HSV image to get only blue colors
		mask = cv2.inRange(hsv, lower_blue, upper_blue)
		 
		# Bitwise-AND mask and original image
		res = cv2.bitwise_and(img, img, mask = mask) 

		if callback:
			callback(img, 'original')
			callback(mask, 'mask')
			callback(res, 'res')

		# cv2.imshow('frame', img)
		# cv2.imshow('mask', mask)
		# cv2.imshow('res', res)
		# cv2.waitKey(5)
		 
		# cv2.destroyAllWindows()

		width = img.shape[0]
		height = img.shape[1]
		area = width * height
		greenPixelCount = 0
		for x in range(width):
			for y in range(height):
				greenPixelCount += mask[x][y]/255
		features = [greenPixelCount/float(area)]
		return features
