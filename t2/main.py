import cv2
import numpy as np
import pprint

AREA_MIN = 150


def draw_blob(contours, i, otsu):
    """
    dibuja el blob i en una ventana
    :param contours:
    :param i:
    :param otsu:
    :return:
    """
    mask = np.zeros(otsu.shape, np.uint8)
    cv2.drawContours(mask, contours, i, (155, 0, 255), cv2.cv.CV_FILLED)
    cv2.imshow("Contornos_" + str(i), mask)


def print_data(contour, i):
    """
    imprime por pantalla los descriptores de un contorno
    :param contour:
    :return:
    """
    """
        Area de la imagen, momento 00
    """
    print "======================================================"
    print "contorno:", i
    print "------------------------------------------------------"
    mom = cv2.moments(contour, 1)
    print "Mom:"
    pprint.pprint(mom)
    print "Area:", mom['m00']

    """
        Calcula el perimetro dado el contorno
    """
    perimetre = cv2.arcLength(contour, False)
    print "Perimetro: ", perimetre

    """
        Calcula los momentos invariantes
    """
    hu_moments = cv2.HuMoments(mom)
    print "Hu moments: ", hu_moments


imgOriginal = cv2.imread("./img/reco1.pgm")
img = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2GRAY);

"""
    Pasamos la imagen a binario
    THRESH_BINARY_INV para que los objetos se vean en blanco y el fondo en negro
    El segundo parametro no se utiliza al usarse THRESH_OTSU.
"""
_, otsu = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
adaptative = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY_INV, 7, 1)
show = np.hstack((img,otsu,adaptative))
cv2.imshow('Umbralizacion (img, otsu, adpatativo)', show)

""" Contornos """
contours, hierarchy = cv2.findContours(otsu, cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_SIMPLE)
"""
    Dibujar los contornos: primero crea una matriz, luego dibuja los contornos
    imagen donde colocarlos, contornos, conturnos a dibujar (negativo -> dibuja
    todos), color del contorno a dibujar
"""
mask = np.zeros(otsu.shape, np.uint8)
cv2.drawContours(mask, contours, -1, (155, 0, 255), cv2.cv.CV_FILLED)
cv2.imshow("Contornos", mask)

i = 0
for contour in contours:
    if cv2.contourArea(contour) > AREA_MIN:
        draw_blob(contours, i, otsu)
        print_data(contour, i)
    i += 1

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
