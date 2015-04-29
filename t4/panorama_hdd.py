# coding=utf-8
import cv2
from sys import argv,exit
import os
import panorama

if __name__ == '__main__':
    if len(argv) != 5:
        print "Se necesitan dos parámetros: <descriptor> <directorio>"
        exit(-1)

    panorama.SHOW_MATCHES = True
    panorama.PREFIX_NAME = argv[3]
    print "Show_matches:", panorama.SHOW_MATCHES
    dir_path = argv[2]
    ftype = argv[1]
    panorama.MIN_MATCHED = int(argv[4])
    stacked = None
    for file in os.listdir(dir_path):
        print "file:", os.path.join(dir_path, file)
        img = cv2.imread(os.path.join(dir_path, file))
        img = panorama.resize_max(img, panorama.MAX_WIDTH)
        if img is not None:
            if stacked is None:
                stacked = img
            else:
                stacked = panorama.stack_images(stacked, img, ftype)
    cv2.imshow("Panorama", stacked)
    cv2.imwrite(panorama.PREFIX_NAME + "panorama.png", stacked)
    cv2.waitKey()