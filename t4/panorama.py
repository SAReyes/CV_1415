# -*- coding: utf-8 -*-

import cv2
import numpy as np
from sys import argv
from time import time

MIN_DISTANCE_TRANSFORMED = 100


def stack_images(img1, img2):
    start = time()
    ftype = argv[1]

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    # Computa los features
    kp1 = features(ftype, img1)
    kp2 = features(ftype, img2)
    goodMatch = matcher(ftype, kp1, kp2)

    # Eliminación de espurios usando RANSAC
    ransac_matched, H = RANSAC_OCV(goodMatch, kp1[0], kp2[0])

    if np.sqrt(abs(H[0, 2]) ** 2 + abs(H[1, 2] ** 2)) < MIN_DISTANCE_TRANSFORMED and not USING_CAMERA:
        return img1

    h1, w1, _ = img1.shape
    h2, w2, _ = img2.shape

    # dibuja las features post-ransac
    # drawMatch(gray1, gray2, kp1[0], kp2[0],ransac_matched)

    # Posiciona la imagen en el centro
    t1 = np.array((1, 0, w2, 0, 1, h2, 0, 0, 1)).reshape(3, 3)
    H = t1.dot(H)

    dummy = cv2.warpPerspective(img2, H, (w1 + w2 * 2, h1 + h2 * 2))
    # copia img2 al centro de la imagen
    tmp = np.array(np.nonzero(gray1))
    # tmp[0,:] += w2
    # tmp[1,:] += h2
    dummy[tmp[0, :] + h2, tmp[1, :] + w2, :] = img1[tmp[0, :], tmp[1, :], :]
    out = dummy

    # recorta zonas sin color
    dummy = np.argwhere(out)
    (ystart, xstart, _), (ystop, xstop, _) = dummy.min(0), dummy.max(0) + 1
    elapsed = time() - start
    print "Tiempo [stack]:", elapsed, "segundos"
    return out[ystart:ystop, xstart:xstop, :]


def drawMatch(img1, img2, kp1, kp2, match):
    """
        Dibuja dos imagenes con sus puntos de interes y sus correspondencia, 
        puesto que python para opencv no dispone de una función como tal que
        lo haga.
    """
    # Concatena ambas imagenes en una sola matriz, no usamos hstack para
    # permitir que sean de distinto tamaño
    out = np.zeros((max(img1.shape[0], img2.shape[0]), img1.shape[1] + \
                    img2.shape[1], 3), dtype='uint8')
    out[:img1.shape[0], :img1.shape[1], :] = np.dstack([img1, img1, img1])
    out[:img2.shape[0], img1.shape[1]:img1.shape[1] + img2.shape[1], :] = \
        np.dstack([img2, img2, img2])

    # recorremos todas las coincidencias entre puntos de interes
    for i in match:
        img1_x = i.queryIdx
        img2_x = i.trainIdx

        # Posiciones x, y
        (x1, y1) = kp1[img1_x].pt
        (x2, y2) = kp2[img2_x].pt

        # Dibuja un circulo en las imagenes
        cv2.circle(out, (int(x1), int(y1)), 5, (255, 0, 0), 1)
        cv2.circle(out, (int(x2) + img1.shape[1], int(y2)), 5, (255, 0, 0), 1)

        # Dibuja una linea entre los circulos
        cv2.line(out, (int(x1), int(y1)), (int(x2) + img1.shape[1], int(y2)), \
                 (255, 0, 0), 1)

    cv2.imshow("Match", out)


def features(ftype, img):
    """
    Calcula los puntos de interes de la imagen segundo el tipo de ftype : SHIFT
    SURF, ORB
    """

    detector = cv2.SIFT()
    if ftype == "SURF":
        detector = cv2.SURF()
    elif ftype == "ORB":
        detector = cv2.ORB()

    start_time = time()
    kp1, des1 = detector.detectAndCompute(img, None)
    elapsed_time = time() - start_time
    print "-+Tiempo [extacción features]: " + str(elapsed_time) + " segundos"
    return (kp1, des1)


def matcher(ftype, kp1, kp2):
    """
    Encuentra coincidencias entre los descriptiroes mediante fuerza bruta
    """
    RATIO = 0.75
    if ftype == "ORB":
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(kp1[1], kp2[1])
        matches = sorted(matches, key=lambda x: x.distance)
        return matches
    else:
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(kp1[1], kp2[1], k=2)
        goodMatch = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                goodMatch.append(m)
        return goodMatch


def RANSAC_OCV(matches, kp1, kp2):
    src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

    H, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)
    matchesMask = mask.ravel().tolist()

    return [a for a, b in zip(matches, matchesMask) if b == 1], H

# TODO: preguntar esto como argumento del script
MAX_WIDTH = 400.0
MAX_STACKED_WIDTH = 1000.0
MAX_STACKED_HEIGHT = 1000.0
USING_CAMERA = False
if __name__ == '__main__':

    def resize_max(src_img, width, heigth=float("inf")):
        h, w, _ = src_img.shape
        if w > width:
            ratio = width / w
            return cv2.resize(src_img, (0, 0), fx=ratio, fy=ratio, interpolation=cv2.INTER_AREA)
        elif h > heigth:
            ratio = heigth / h
            return cv2.resize(src_img, (0, 0), fx=ratio, fy=ratio, interpolation=cv2.INTER_AREA)

        return src_img

    def compare_key(key, char):
        return key & 0xff == ord(char)

    cap = cv2.VideoCapture(0)
    cv2.namedWindow("Panorama")
    stacked = None
    while True:
        _, frame = cap.read()
        cv2.imshow("Camera", frame)

        key = cv2.waitKey(30)

        if USING_CAMERA:
            if stacked == None:
                stacked = frame
            else:
                frame = resize_max(frame, MAX_WIDTH)
                stacked = stack_images(stacked, frame)

            cv2.imshow("Panorama", stacked)

        if compare_key(key, 'q'):
            break
        elif compare_key(key, 's'):
            USING_CAMERA = not USING_CAMERA
        elif compare_key(key, 'c') and not USING_CAMERA:
            if stacked == None:
                stacked = frame
            else:
                frame = resize_max(frame, MAX_WIDTH)
                stacked = stack_images(stacked, frame)

            cv2.imshow("Panorama", stacked)

    cv2.imwrite("panorama.png", stacked)
