import numpy as np 
import cv2

class GreenExtractor():
	def __init__(self):
		pass

	def getFeatures(self, img, imagename=None, callback=None):
		
		# Convert BGR to HSV
		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		 
		# define range of blue color in HSV
		lower_blue = np.array([50,10,10])
		upper_blue = np.array([70,255,255])
		 
		# Threshold the HSV image to get only blue colors
		mask = cv2.inRange(hsv, lower_blue, upper_blue)
		 
		# Bitwise-AND mask and original image
		res = cv2.bitwise_and(img, img, mask = mask) 

		# For debugging
		if callback:
			callback(img, imagename + 'orig')
			callback(mask, imagename + 'mask')
			callback(res, imagename + 'res')
		 
		width = mask.shape[0]
		height = mask.shape[1]
		totalArea = float(width * height)
		features = [cv2.sumElems(mask)[0] / (255 * totalArea)]

		sixteenths = [0] * 16
		for x in xrange(4): # width
			for y in xrange(4): # height
				start_x = x * (width / 4)
				end_x = start_x + (width / 4)
				start_y = y * (height / 4)
				end_y = start_y + (height / 4)

				sixteenths[4 * x + y] = cv2.sumElems(mask[start_x : end_x, start_y : end_y])[0] / (255 * totalArea / 16)

		features.extend(sixteenths)

		# for x in xrange(width):
		# 	for y in xrange(height):
		# 		x_idx = x / (width / 4)
		# 		y_idx = y / (height / 4)
		# 		sixteenths[x_idx + y_idx * 4] += mask[x][y] / 255
		# features.extend([x / (float(totalArea) / 16) for x in sixteenths])	

		return features
