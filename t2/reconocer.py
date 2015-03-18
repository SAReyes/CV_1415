import sys
import pickle

import cv2
import numpy as np
from sys import argv

import func

if len(argv) != 2:
    print "argumentos invalidos"
    sys.exit(-1)

DESC_FILE = "descriptores.pickle"
file_obj = "img/reco2.pgm"
colors = {'circulo': (255, 129, 128),
          'rueda': (200, 0, 255),
          'desconocido': (100, 100, 100),
          'vagon': (125, 0, 0),
          'triangulo': (58, 128, 0),
          'rectangulo': (175, 128, 128),
          'multiple': (0, 255, 128)}


def find_class(contour, name, contours, i, img):
    mom, area, perimeter, hu_mom = \
        func.descriptors(contour)

    observado = np.insert(hu_mom[0:3], 0, (area, perimeter))
    observado = observado.reshape(1, observado.size)
    tall, _ = descriptores['means'].shape
    observado = np.repeat(observado, tall, axis=0)

    mahal = ((observado - descriptores['means']) ** 2) / (descriptores['vars'])

    print "mahal", mahal
    print "i", i, np.sum(mahal, axis=1)
    dummy = np.sum(mahal, axis=1) < 21.666
    dato = 'desconocido'
    color = dato
    figuras = np.select([dummy], [descriptores['names']])
    figura = [x for x in figuras if x != '0']
    if len(figura) == 1:
        dato = figura[0]
        color = dato
    elif len(figura) > 0:
        dato = figura
        color = 'multiple'

    print dato
    height, _, _ = img.shape
    mask = np.zeros(img.shape, np.uint8)
    cv2.drawContours(mask, contours, i, colors[color], cv2.cv.CV_FILLED)
    cv2.putText(mask, "objeto: " + str(dato), (5, height - 10), cv2.cv.CV_FONT_HERSHEY_PLAIN, 0.8, (0, 255, 0), 1)
    cv2.imshow(name, mask)
    # cv2.imshow(name, binary)


"""
    main
"""
if __name__ == "__main__":
    try:
        descriptores = pickle.load(open(DESC_FILE, 'rb'))
    except IOError:
        print "No se encontro el fichero", DESC_FILE
        sys.exit(-1)

    img = cv2.imread(file_obj)
    _, otsu = func.otsu(img)
    cv2.imshow("img", img)
    cv2.imshow("binary", otsu)

    contours, _ = func.contours(otsu)

    index = 0
    i = 0
    for contour in contours:
        if cv2.contourArea(contour) > 150:
            find_class(contour, "contorno" + str(index), contours, i, img)
            index += 1
        i += 1

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()