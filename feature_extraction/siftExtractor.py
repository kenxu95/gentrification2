import numpy as np 
import cv2
import matplotlib.pyplot as plt


class SIFTExtractor():
    def __init__(self):
        pass

    def getFeatures(self, img, imagename=None, callback=None):
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        sift = cv2.SIFT() #features2d.SIFT_create()
        kp, des = sift.detectAndCompute(gray, None)
        
        width = img.shape[0]
        height = img.shape[1]
        totalArea = float(width * height)
        features = [len(kp) / totalArea] # keypoint density

        sizes = [kpt.size for kpt in kp]
        octaves = [kpt.octave for kpt in kp]

        size_hist, _ = np.histogram(sizes, bins=10, range=(10,100))
        size_hist_sz = sum(size_hist)
        size_hist = [bar_height/float(size_hist_sz) for bar_height in size_hist]
        features.extend(size_hist)

        octaves_hist, _ = np.histogram(octaves, bins=10)
        octaves_hist_sz = sum(octaves_hist)
        octaves_hist = [bar_height/float(octaves_hist_sz) for bar_height in octaves_hist]
        features.extend(octaves_hist)

        # plt.hist(sizes, bins=10, range=(10,100), normed=True)  # plt.hist passes it's arguments to np.histogram
        # plt.title("Sizes")
        # plt.savefig(imagename + '-SIFT-size-histogram')

        img2 = cv2.drawKeypoints(gray,kp,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        # For debugging
        if callback:
            callback(img2, imagename + 'keypoints')
        
        return features
