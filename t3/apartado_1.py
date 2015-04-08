# coding=utf-8
"""
    Trabajo 3, Computer Vision @ Unizar 2014-15
        Punto 1: Gradiente horizontal, vertical, su módulo y su orientación
    __author__: Reyes Apaestegui, Sergio Adrian (642535)
    __author__: Navarro Torres, Agustín (587570)

    derivadas de sobel (tutorial opencv):
        http://docs.opencv.org/doc/tutorials/imgproc/imgtrans/sobel_derivatives/sobel_derivatives.html
        *el kernel y el módulo se explica en el fragmento: #Formulation

"""
import cv2
import numpy as np

def normalize(array):
    """
        convierte una imagen en 32F o 64F a 8U, reescalando
        los valores, el mínimo se queda en 0 y el máximo en 255

        se hace de forma manual ya que opencv para python no
        dispone de Mat's
    """
    # como los valores no se encuentran entre -255 y 255 ¿9 bits, cómo?
    # es preferible usar esto, aunque sea un poco más bestia, funciona 100%
    dummy = array - np.min(array)
    return (dummy / np.max(dummy) * 255).astype(np.uint8)

def main():
    img = cv2.imread('./gradient/poster.pgm')
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Image in gray scale", imgGray)

    # reducción de ruido sobre la imagen en griz
    imgGray = cv2.GaussianBlur(imgGray, (3, 3), 0)

    ############################################################
    ##                      Gradientes                        ##
    ############################################################
    # Se aplica sobel con 32F para mantener el signo, usar cualquier
    # tipo de dato unsigned (8U, 16U) trunca la derivada

    # Sobel eje x
    sobelx = cv2.Sobel(imgGray, cv2.CV_32F, 1, 0, ksize=3)
    sobelx_show = normalize(sobelx)
    cv2.imshow("SobelX", sobelx_show)

    # Sobel eje y
    # opencv usa un kernel inverso para el vertical
    # kernel de opencv:
    # -1 -2 -1
    # 0  0  0
    # 1  2  1
    sobely = cv2.Sobel(imgGray, cv2.CV_32F, 0, 1, ksize=3)
    sobely_show = normalize(sobely)
    cv2.imshow("SobelY", sobely_show)

    ############################################################
    ##                      Módulo                            ##
    ############################################################
    # module = np.sqrt((sobelx) ** 2 + (sobely) ** 2)
    # forma simplificada del cálculo de arriba ^
    module_show = np.abs(sobelx) + np.abs(sobely)
    module = normalize(module_show)
    cv2.imshow("Module", module)


    ############################################################
    ##                      Orientanción                      ##
    ############################################################
    # cambia un poco, pero por el sobely
    ori = np.arctan2(sobely, sobelx)
    cv2.imshow("Orientacion", normalize(ori))

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()