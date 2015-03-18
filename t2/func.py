import cv2
import numpy as np

def otsu(img):
    """
    Convierte la imagen a binaria con el metodo otsu
    """
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    retval, otsu = cv2.threshold(imgGray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    return retval, otsu

def adaptative(img):
    """
    Conviertela imagen a binaria ocn el metodo adaptativo
    """
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    adaptative = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV, 7, 1)
    return adaptative

def contours(img):
    """
    Devuelve los contornos de una imagen
    """
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE)
    return contours, hierarchy

def drawContoruse(img, contours):
    """
    Dibuja los contornos de una imagen
    :param img:
    :param contours:
    :return:
    """
    mask = np.zeros(img.shape, np.uint8)
    cv2.drawContours(mask, contours, -1, 255)
    cv2.imshow("Contornos", mask)


def findBiggestContour(contours):
    """
    Encuentra devuelve el contorno de mayor area
    :return: contorno
    """
    if len(contours) == 0:
        return -1

    areas = map(lambda c: cv2.contourArea(c), contours)
    area_max = max(areas)
    return contours[[e for e,v in enumerate(areas) if v == area_max][0]]

def descriptors(contours):
    """
    Devuelve los descriptores de una imagen, a partir de su contorno
    @return: momentos, area, perimtero, momentos invariantes
    """
    mom = cv2.moments(contours, 1)
    perimetre = cv2.arcLength(contours, True)
    hu_moments = cv2.HuMoments(mom)
    return mom, mom['m00'], perimetre, hu_moments.tolist()
