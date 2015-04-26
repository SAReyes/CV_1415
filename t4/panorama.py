#-*- coding: utf-8 -*-
import cv2
import numpy as np
from time import time

def features(ftype, img):
    """
    Calcula los puntos de interes de la imagen segundo el tipo de ftype : SHIFT
    SURF, ORB
    """
    start_time = time()
    if ftype == "SHIFT":
        sift = cv2.SIFT()
        kp1, des1 = sift.detectAndCompute(img, None)
        elapsed_time = time() - start_time
        print "Tiempo en la ejecución: " + str(elapsed_time) + " segundos"
        return (kp1, des1)
    elif ftype == "SURF":
        surf = cv2.SURF()
        kp1, des1 = surf.detectAndCompute(img, None)
        elapsed_time = time() - start_time
        print "Tiempo en la ejecución: " + str(elapsed_time) + " segundos"
        return (kp1, des1)
    elif ftype == "ORB":
        orb = cv2.ORB()
        kp1, des1 = orb.detectAndCompute(img, None)
        elapsed_time = time() - start_time
        print "Tiempo en la ejecución: " + str(elapsed_time) + " segundos"
        return (kp1, des1)
    else:
        print "No existe el tipo"

def matcher(ftype, kp1, kp2):
    """
    Encuentra coincidencias entre los descriptiroes mediante fuerza bruta
    """
    RATIO = 0.75
    if ftype == "SHIFT" or ftype == "SURF":
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(kp1[1], kp2[1], k = 2)  
        goodMatch = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                goodMatch.append(m)
        return goodMatch
    else:
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)
        matches = bf.match(kp1[1], kp2[1])
        matches = sorted(matches, key = lambda x:x.distance)
        return matches

# Read image
img1 = cv2.imread('./image1.jpg')
img2 = cv2.imread('./image2.jpg')
# convert to Gray scale
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

kp1 = features('SURF', gray1)
kp2 = features('SURF', gray2)

match = matcher('SURF', kp1, kp2)

obj = []
scene = []
for i in match:
    obj.append(kp1[0][i.queryIdx].pt)
    scene.append(kp2[0][i.trainIdx].pt)

# Solución cerda para que lo trague la función de opencv
obj = np.array(obj)
scene = np.array(scene)
# Encuentra la homografia de la imagen 
h = cv2.findHomography(obj, scene, method= cv2.RANSAC)
# Aplica la transformación a una imagen
result = cv2.warpPerspective(img1, h[0], (img1.shape[0] + img2.shape[0],\
    img1.shape[1]))
#result[img1.shape[0]:] = img2
print result.shape
print img1.shape
print img2.shape
cv2.imshow('test', result)
cv2.waitKey()
