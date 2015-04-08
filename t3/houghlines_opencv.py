# coding=utf-8
"""
    Cálculo del punto de fuga usando HoughLines
"""
import cv2
import os
from sys import argv
import numpy as np

HOUGH_THRESHOLD = 80
VERT_MULTIPLIER = float(argv[1])
CAM = False

image_index = 0
images = os.listdir("./vanishing_point")

cap = cv2.VideoCapture(0)

while True:
    if CAM:
        _, img = cap.read()
    else:
        img = cv2.imread(os.path.join("./vanishing_point",images[image_index]))

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.GaussianBlur(img_gray, (3, 3), 0)

    rows, cols = img_gray.shape

    canny = cv2.Canny(img, 150, 120, apertureSize=3)

    cv2.imshow("Canny", canny)

    lines = cv2.HoughLines(canny, 1, np.pi / 180, HOUGH_THRESHOLD)

    dummy = np.zeros((rows, cols)).astype(np.uint8)

    e = 0.1

    if not lines is None:
        for rho, theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x = rho * a
            y = rho * b
            x1 = int(x + 1000 * (-b))
            y1 = int(y + 1000 * (a))
            x2 = int(x - 1000 * (-b))
            y2 = int(y - 1000 * (a))
            m = np.abs(np.arctan2(y2 - y1, x2 - x1))
            if (m > e and m < np.pi / 2 - e*VERT_MULTIPLIER) or (m > np.pi / 2 + e*VERT_MULTIPLIER and m < np.pi - e):
                ALPHA = m
                temp = np.zeros((rows, cols))
                cv2.line(temp, (x1, y1), (x2, y2), (1), 10)
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0))
                dummy = dummy + temp

        max_voted = np.max(dummy)
        if max_voted > 30:
            HOUGH_THRESHOLD += 5
        elif max_voted < 10:
            HOUGH_THRESHOLD -= 5

        a_max = np.argmax(dummy)
        i = a_max % cols
        j = a_max / cols
        cross_size = int(rows * 0.1)
        offset = 5
        cv2.line(img, (i, j + offset), (i, j + offset + cross_size), (0, 0, 255),3)
        cv2.line(img, (i + offset, j), (i + offset + cross_size, j), (0, 0, 255),3)
        cv2.line(img, (i, j - offset), (i, j - offset - cross_size), (0, 0, 255),3)
        cv2.line(img, (i - offset, j), (i - offset - cross_size, j), (0, 0, 255),3)

    cv2.imshow(str(images[image_index]), img)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('c'):
        CAM = not CAM
        HOUGH_THRESHOLD = 80
    elif key & 0xFF == ord('i'):
        HOUGH_THRESHOLD = 80
        cv2.destroyWindow(images[image_index])
        image_index += 1
        image_index = image_index % len(images)