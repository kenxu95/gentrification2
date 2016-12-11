import cv2
import os

class TextureExtractor():
    
    def getFeatures(self, img, imagename = None, callback = None):
        #perform texture extraction
        
        #original image
        origim = img.copy()
        
        #convert image to greyscale                                                                                                                                   
        img = cv2.cvtColor( img, cv2.COLOR_RGB2GRAY )
        
        # Choose different blurring techniques
        # Blur image components
        # img = cv2.medianBlur(img, 5)
        # reduce unwanted noise
        features = cv2.bilateralFilter(img, 9, 75, 75)
            
        # Choose different thresholding techniques
        features = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,25,20)
        # _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Texture feature                                                                                                                                             
        totalArea = textures.shape[0] * textures.shape[1]
        features = [cv2.sumElems(textures)[0] / (255 * totalArea)]

        # Shape features                                                                                                                                              
        contours, hierachy = cv2.findContours(textures, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

        totalArea = img.shape[0] * img.shape[1]
        features.append(sum([cv2.contourArea(cnt) for cnt in contours]) / totalArea)
        features.append(sum([cv2.arcLength(cnt, True) for cnt in contours]) / totalArea)


        if callback:
            callback(origim, imagename, contours)

        # cv2.imwrite('test11.png', textures)

        return features
