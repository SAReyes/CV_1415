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
# TODO: use matplotlib/pyplot to show static images as it is more organized

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
    img = cv2.imread('./ImagenesT2/poster.pgm')
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
    # TODO: Delete the line below this one before committing the assignment
    # #No se como hace numpy las operaciones pero no hace lo que esperaba que hiciera
    # module = np.sqrt((sobelx) ** 2 + (sobely) ** 2)
    # forma simplificada del cálculo de arriba ^
    module_show = np.abs(sobelx) + np.abs(sobely)
    module = normalize(module_show)
    cv2.imshow("Module", module)

    # La operacion implementandola a mano, lo hace bien - o eso creo-
    # module_x = sobelx;
    # for i in range(len(sobelx)):
    #     for j in range(len(sobelx[i])):
    #         module_x[i][j] = np.abs(np.sqrt(sobelx[i][j] ** 2 + sobely[i][j] ** 2))
    # Adrian: sólo necesitabas reajustar la matriz a una de tipo uint8,
    #         las dos versiones funcionan igual de bien
    # TODO: Delete this block of comment before committing the assignment


    ############################################################
    ##                      Orientanción                      ##
    ############################################################
    # cambia un poco, pero por el sobely
    ori = np.arctan2(sobely, sobelx)
    cv2.imshow("Orientacion", normalize(ori))

    # TODO: the orientation range is [-pi,pi] ... verify that
    # ori_show = (ori / np.pi) * 128
    # ori_show2 = ori_show.astype(np.uint8)
    # print np.min(ori), np.max(ori)

    # TODO: What should we do about all this code below? program the same with Schurr or, perhaps, Canny? as different scripts to show the differences?
    """
    for i in range(len(sobelx)):
        for j in range(len(sobelx[i])):
            ori_show2[i][j] = (np.arctan2(sobely[i][j], sobelx[i][j])/np.pi)*128

    print ori_show2
    #ori_show2 = ori_show2.astype(np.uint8)
    """

    """
    print "Schurr"
    #Scharr eje x
    scharrx = cv2.Scharr(imgGray, cv2.CV_8U, 1, 0)
    scharrx_show = scharrx/2 + 128
    cv2.imshow("ScharrX", scharrx_show)

    #Scharr eje y
    scharry = cv2.Scharr(imgGray, cv2.CV_8U, 0, 1)
    scharry_show = scharry/2 + 128
    cv2.imshow("ScharrY", scharry_show)
    print scharry_show.dtype

    #Modulo
    #module = np.abs(np.sqrt((sobelx)**2 + (sobely)**2)) #No se como hace numpy las operaciones pero no hace lo que esperaba que hiciera
    module_show = np.abs(scharrx) + np.abs(scharry) #Aproximacion, mas rapida que hacer el calculo y bastante buena

    #La operacion implementandola a mano, lo hace bien - o eso creo-
    module_x = sobely;
    for i in range(len(scharrx)):
        for j in range(len(scharrx[i])):
            module_x[i][j] = np.abs(np.sqrt(scharrx[i][j]**2 + scharry[i][j]**2))


    print module_x
    cv2.imshow("ModuleS", module_x)

    #orientacion, lo hace bien pero con colores cambiados
    ori = np.arctan2(scharry, scharrx)
    ori_show = (ori/np.pi) * 128
    ori_show2 = ori_show.astype(np.uint8)
    cv2.imshow("OrientacionS", ori_show2)
    """

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()