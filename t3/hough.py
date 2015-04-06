# coding=utf-8
import cv2
import numpy as np

def convert_float(array):
    """
        convierte una imagen en 32F o 64F a 8U, reescalando
        los valores, el mínimo se queda en 0 y el máximo en 255

        se hace de forma manual ya que opencv para python no
        dispone de Mat's
    """
    dummy = array + np.abs(np.min(array))
    return (dummy / np.max(dummy) * 255).astype(np.uint8)

def sobel(img):
    """
    Calcula sobel y la informacion asociada, modulo y orientacion
    """
    sobelx_d = cv2.Sobel(imgGray, cv2.CV_32F, 1, 0, ksize = 3)
    sobely_d = cv2.Sobel(imgGray, cv2.CV_32F, 0, 1, ksize = 3)
    module = modulo(sobelx_d, sobely_d)
    ori = np.arctan2(sobely_d, sobelx_d)
    return sobelx_d, sobely_d, module, ori

def modulo(imgx, imgy):
    # modulo_dummy = imgx
    # for i in range(len(imgx)):
    #     for j in range(len(imgy[i])):
    #         modulo_dummy[i][j] = np.abs(np.sqrt(imgx[i][j]**2 + imgy[i][j]**2))
    return np.abs(imgx) + np.abs(imgy)


UMBRAL = 1

img = cv2.imread('./ImagenesT2/pasillo1.pgm')

#img = cv2.GaussianBlur(img, (3,3), 0)

#imagen a gris
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#Linea del horizonte
mean = len(imgGray) / 2

#Tabla de votos 1 fila x columnas de programa
ncolum = len(imgGray[0])
nrow = len(imgGray)

sobelx, sobely, module, ori = sobel(imgGray)

for i in range(len(imgGray)):
    for j in range(len(imgGray[i])):
        if module[i][j] >= UMBRAL:
            x = j - ncolum/2
            y = nrow/2 - i
            theta = ori[i][j]
            rho = x * np.cos(theta) + y * np.sin(theta)
            #Eliminamos las lineas verticales
            if (theta != np.pi/2):
