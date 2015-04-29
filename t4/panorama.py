# -*- coding: utf-8 -*-

import cv2
import numpy as np
from sys import argv
from time import time

MIN_DISTANCE_TRANSFORMED = 100


def stack_images(img1, img2, type):
    start = time()
    ftype = type

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    # Computa los features
    kp1 = features(ftype, img1)
    kp2 = features(ftype, img2)
    t_start = time()
    goodMatch, all_matched = matcher(ftype, kp1, kp2)
    t_total = time() - t_start
    print "-+Tiempo [matcher]:", t_total, "segundos"

    # Eliminación de espurios usando RANSAC
    # ransac_matched, H = RANSAC_OCV(goodMatch, kp1[0], kp2[0])
    t_start = time()
    ransac_matched, H = RANSAC_OCV(goodMatch, kp1[0], kp2[0])
    t_total = time() - t_start
    print "-+Tiempo [findHomography]:", t_total, "segundos"

    # if np.sqrt(abs(H[0, 2]) ** 2 + abs(H[1, 2] ** 2)) < MIN_DISTANCE_TRANSFORMED and USING_CAMERA:
    #     return img1
    if len(ransac_matched) < int(MIN_MATCHED):
        return img1

    h1, w1, _ = img1.shape
    h2, w2, _ = img2.shape

    # dibuja las features post-ransac
    if SHOW_MATCHES:
        matched = drawMatch(gray1, gray2, kp1[0], kp2[0], ransac_matched)
        pre_ransac = drawMatch(gray1, gray2, kp1[0], kp2[0], goodMatch)
        cv2.imshow("Matched_Ransac", matched)
        cv2.imwrite(PREFIX_NAME + "_ransac.png", matched)
        cv2.imshow("Pre-ransac", pre_ransac)
        cv2.imwrite(PREFIX_NAME + "_full_features.png", pre_ransac)

    t_start = time()
    # Posiciona la imagen en el centro
    t1 = np.array((1, 0, w2, 0, 1, h2, 0, 0, 1)).reshape(3, 3)
    H = t1.dot(H)

    dummy = cv2.warpPerspective(img2, H, (w1 + w2 * 2, h1 + h2 * 2))
    # copia img2 al centro de la imagen
    tmp = np.array(np.nonzero(gray1))
    dummy[tmp[0, :] + h2, tmp[1, :] + w2, :] = img1[tmp[0, :], tmp[1, :], :]
    out = dummy
    # tmp_img = img1.astype(np.int16)
    # dummy[tmp[0, :] + h2, tmp[1, :] + w2, :] = (tmp_img[tmp[0, :], tmp[1, :], :] +dummy[tmp[0, :] + h2, tmp[1, :] + w2, :])/2

    # recorta zonas sin color
    dummy = np.argwhere(out)
    (ystart, xstart, _), (ystop, xstop, _) = dummy.min(0), dummy.max(0) + 1
    t_total = time() - t_start
    print "-+Tiempo [Construcción]:", t_total, "segundos"

    elapsed = time() - start
    print "+Tiempo [stack]:", elapsed, "segundos"

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
        cv2.line(out, (int(x1), int(y1)), (int(x2) + img1.shape[1], int(y2)),
                 (255, 0, 0), 1)

    return out


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
    if ftype == "ORB":
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(kp1[1], kp2[1])
        matches = sorted(matches, key=lambda x: x.distance)
        return matches, matches
    else:
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(kp1[1], kp2[1], k=2)
        goodMatch = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                goodMatch.append(m)
        return goodMatch, matches


def RANSAC_OCV(matches, kp1, kp2):
    src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

    # || dstPoints_i-convertPointsHomogeneous(H*srcPointsi) ||  >  ransacReprojThreshold
    H, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)
    matchesMask = mask.ravel().tolist()

    return [a for a, b in zip(matches, matchesMask) if b == 1], H


def RANSAC(matches, kp1, kp2, P):
    def max_tuple(a, b):
        if b > a:
            return b, a
        else:
            return a, b

    # TODO: Momentaneamente se está usando para calcular H, calcularla manualmente a partir de 4 puntos
    src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
    # matchesMask = mask.ravel().tolist()

    k = 2  # min puntos

    # kp1 => queryIdx
    # kp2 => trainIdx
    i = 0
    matchedVoteCount = 0.0
    matchesMask = None
    intentos = float("inf")
    while i < intentos:
        # print "Intentos:", intentos
        muestra = np.random.randint(len(matches), size=k)

        m = matches[muestra[0]]
        p1 = kp1[m.queryIdx].pt
        p2 = kp2[m.trainIdx].pt
        pendiente_test = np.arctan2(p1[1] - p2[1], p1[0] - p2[0])
        votes = []
        for match in matches:
            p1 = kp1[match.queryIdx].pt
            p2 = kp2[match.trainIdx].pt
            p_match = np.arctan2(p1[1] - p2[1], p1[0] - p2[0])
            # votes = np.abs(p_match - pendiente_test) < 0.1 and \
            #                 m.distance < P * match.distance

            # TODO: Mejorable, en lugar de for, usa matrices ...
            if np.abs(p_match - pendiente_test) < 0.1 and \
                            m.distance < 0.8 * match.distance:
                votes.append(1)
            else:
                votes.append(0)
        i += 1

        if (np.sum(votes) > matchedVoteCount):
            matchedVoteCount = np.sum(votes)
            matchesMask = votes
            p = float(matchedVoteCount) / len(votes)
            intentos = np.ceil(np.log(1 - P) / np.log(1 - p ** k))


    # print "Mask:", np.sum(matchesMask), len(matchesMask)
    return [a for a, b in zip(matches, matchesMask) if b == 1], None


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

# TODO: preguntar esto como argumento del script
MAX_WIDTH = 400.0
MAX_STACKED_WIDTH = 1000.0
MAX_STACKED_HEIGHT = 1000.0
USING_CAMERA = False
SHOW_MATCHES = False
PREFIX_NAME = ""
MIN_MATCHED = 50
if __name__ == '__main__':
    ftype = argv[1]
    PREFIX_NAME = argv[2]
    MIN_MATCHED = int(argv[3])
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("Panorama")
    stacked = None
    while True:
        _, frame = cap.read()
        cv2.imshow("Camera", frame)

        key = cv2.waitKey(30)

        if USING_CAMERA:
            if stacked is None:
                stacked = frame
            else:
                frame = resize_max(frame, MAX_WIDTH)
                stacked = stack_images(stacked, frame, ftype)

            cv2.imshow("Panorama", stacked)

        if compare_key(key, 'q'):
            break
        elif compare_key(key, 's'):
            USING_CAMERA = not USING_CAMERA
        elif compare_key(key, 'c') and not USING_CAMERA:
            if stacked is None:
                stacked = frame
            else:
                frame = resize_max(frame, MAX_WIDTH)
                stacked = stack_images(stacked, frame, ftype)

            cv2.imshow("Panorama", stacked)

    cv2.imwrite(PREFIX_NAME + "_panorama.png", stacked)
