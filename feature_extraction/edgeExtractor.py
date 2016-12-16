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

        # Edge feature
        totalArea = edges.shape[0] * edges.shape[1]
        features = [cv2.sumElems(edges)[0] / (255 * totalArea)]
      
        # Shape features
        contours, hierachy = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        totalArea = img.shape[0] * img.shape[1]
        features.append(sum([cv2.contourArea(cnt) for cnt in contours]) / totalArea)
        features.append(sum([cv2.arcLength(cnt, True) for cnt in contours]) / totalArea)

        # Identify shapes
        shapes = [0] * 16
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            if len(approx) <= 15:
                shapes[len(approx)] += 1
            else:
                shapes[-1] += 1
        features.extend(shapes)

        # CORNER: Run the Corner Harris algorithm on both edges and original image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        corner_img = cv2.cornerHarris(gray, 2, 3, 0.04)
        corner_edges = cv2.cornerHarris(edges, 2, 3, 0.04)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
        edges[corner_edges > 0.01 * corner_edges.max()] = [0, 0, 255] # FOR DISPLAYING

        # The indexes of the corners within the images 
        corner_img_indexes = np.where(corner_img > 0.01 * corner_img.max())
        corner_edges_indexes = np.where(corner_edges > 0.01 * corner_edges.max())

        # Add number of corners
        num_img_corners = len(corner_img_indexes[0])
        features.append(num_img_corners / totalArea)
        features.append(len(corner_edges_indexes[0]) / totalArea)

        if callback:
            callback(edges, imagename)

        return features
        
