import cv2
import numpy as np

"""
    Convierte la imagen a binaria con el metodo otsu
"""
def otsu(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    retval, otsu = cv2.threshold(imgGray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    return retval, otsu

"""
    Conviertela imagen a binaria ocn el metodo adaptativo
"""
def adaptative(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    adaptative = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV, 7, 1)
    return adaptative

"""
    Devuelve los contornos de una imagen
"""
def contours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE)
    return contours, hierarchy

"""
    Dibuja los contornos de una imagen
"""
def drawContoruse(img, contours):
    mask = np.zeros(img.shape, np.uint8)
    cv2.drawContours(mask, contours, -1, 255)
    cv2.imshow("Contornos", mask)

"""
    Devuelve los descriptores de una imagen, a partir de su contorno
    @return: momentos, area, perimtero, momentos invariantes
"""
def descriptors(contours):
    mom = cv2.moments(contours, 1)
    perimetre = cv2.arcLength(contours, False)
    hu_moments = cv2.HuMoments(mom)
    return mom, mom['m00'], perimetre, hu_moments
