# -*- coding: utf-8 -*-

import cv2 
import numpy as np
from sys import argv
import os
from time import time

def drawMatch(img1, img2, kp1, kp2, match):
    """
        Dibuja dos imagenes con sus puntos de interes y sus correspondencia, 
        puesto que python para opencv no dispone de una función como tal que
        lo haga.
    """
    # Concatena ambas imagenes en una sola matriz, no usamos hstack para
    # permitir que sean de distinto tamaño
    out = np.zeros((max(img1.shape[0], img2.shape[0]), img1.shape[1] +\
        img2.shape[1], 3), dtype='uint8')
    out[:img1.shape[0], :img1.shape[1],:] = np.dstack([img1, img1, img1])
    out[:img2.shape[0], img1.shape[1]:img1.shape[1] + img2.shape[1], :] =\
        np.dstack([img2, img2, img2])

    # recorremos todas las coincidencias entre puntos de interes
    for i in match:
        img1_x = i.queryIdx
        img2_x = i.trainIdx
        
        #Posiciones x, y
        (x1, y1) = kp1[img1_x].pt
        (x2, y2) = kp2[img2_x].pt
        
        # Dibuja un circulo en las imagenes
        cv2.circle(out, (int(x1), int(y1)), 5, (255, 0, 0), 1)
        cv2.circle(out, (int(x2) + img1.shape[1], int(y2)), 5, (255, 0, 0), 1) 

        # Dibuja una linea entre los circulos
        cv2.line(out, (int(x1), int(y1)), (int(x2) + img1.shape[1], int(y2)),\
            (255, 0, 0), 1)
   
    cv2.imshow("Match", out)
    cv2.waitKey(0)
    
def features(ftype, img):
    """
    Calcula los puntos de interes de la imagen segundo el tipo de ftype : SHIFT
    SURF, ORB
    """
    start_time = time()
    if ftype == "SHIFT":
        sift = cv2.SIFT()
        kp1, des1 = sift.detectAndCompute(img, None)
        return (kp1, des1)
    elif ftype == "SURF":
        surf = cv2.SURF()
        kp1, des1 = surf.detectAndCompute(img, None)
        return (kp1, des1)
    elif ftype == "ORB":
        orb = cv2.ORB()
        kp1, des1 = orb.detectAndCompute(img, None)
        return (kp1, des1)
    else:
        print "No existe el tipo"
    elapsed_time = time() - start_time
    print "Tiempo en la ejecución " + elapsed_time

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

# Imagen de prueba
img1 = cv2.imread("./img.pgm")
img2 = cv2.imread("./img2.pgm")
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

ftype = argv[1]

print "Descriptor: " + ftype
kp1 = features(ftype, img1)
kp2 = features(ftype, img2)
goodMatch = matcher(ftype, kp1, kp2)

drawMatch(gray1, gray2, kp1[0], kp2[0], goodMatch)
