import cv2
import numpy as np

imgOriginal = cv2.imread("./img/circulo1.pgm")
img = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2GRAY);

"""
    Pasamos la imagen a binario
    THRESH_BINARY_INV para que los objetos se vean en blanco y el fondo en negro
    El segundo parametro no se utiliza al usarse THRESH_OTSU.
"""
_, otsu = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
adaptative = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
    cv2.THRESH_BINARY_INV, 7, 1)
cv2.imshow('Otsu', otsu)
cv2.imshow('Img', img)
cv2.imshow('Adaptative', adaptative)

""" Contornos """
contours, hierarchy = cv2.findContours(otsu, cv2.RETR_TREE,
    cv2.CHAIN_APPROX_SIMPLE)

"""
    Dibujar los contornos: primero crea una matriz, luego dibuja los contornos
    imagen donde colocarlos, contornos, conturnos a dibujar (negativo -> dibuja
    todos), color del contorno a dibujar
"""
mask = np.zeros(otsu.shape, np.uint8)
cv2.drawContours(mask, contours, -1, 255)
cv2.imshow("Contornos", mask)

"""
    Area de la imagen, momento 00
"""
mom = cv2.moments(contours[0], 1)
print "Area: ", mom['m00']

"""
    Calcula el perimetro dado el contorno
"""
perimetre = cv2.arcLength(contours[0], False)
print "Perimetro: ", perimetre

"""
    Calcula los momentos invariantes
"""
hu_moments = cv2.HuMoments(mom)
print "Hu moments: ", hu_moments

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
