# coding=utf-8
import cv2
import numpy as np
import sys

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


UMBRAL = 150

img = cv2.imread(sys.argv[1])

img = cv2.GaussianBlur(img, (3,3), 0)

#imagen a gris
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#Numero de colomunas y filas de la imagen
ncolum = len(imgGray[0])
nrow = len(imgGray)

#Linea del horizonte
mean = round(nrow / 2)

print mean

#Matriz de votos, iniciliazada a 0
k = 0
votos = []
while k < ncolum:
    votos.append(0)
    k=k+1

#cv2.imshow("Horizonte", imgGray)

#Valores de la votación
max_v = -1
y_v = 0
sobelx, sobely, module, ori = sobel(imgGray)

print "Calculando punto de fuga"
for i in range(len(imgGray)):
    """
        Calculo del punto de fuga, tomando que el punto de fuga
        es aquel punto donde se cortan las lineas de fuga.
        See: http://stackoverflow.com/questions/22831056/vanishing-point-detection-from-vanishing-line-using-hough-transform
    """
    for j in range(len(imgGray[i])):
        if module[i][j] >= UMBRAL:
            ang = ori[i][j]
            #Eliminamos las lineas verticales
            if (np.abs(np.cos(ang))<0.9 and np.abs(np.cos(ang))>0.1):
                """
                    Calcula los valores para representar la recta parametricamente
                    a la cual pertenece los puntos i,j
                """
                rho = j*np.cos(ang) + i*np.sin(ang)
                """
                    Despejamos donde corta la recta por la linea del horizonte
                """
                x = (-1)*((mean*np.sin(ang) - rho)/np.cos(ang))
                x = int(x)
                if x < ncolum and x >= 0:
                    """
                        Si el corte de la recta se encuentra dentro de la imagen
                        votamos por ese punto en la recta
                    """
                    votos[x]=votos[x] + 1
                    if (votos[x]>max_v):
                        max_v = votos[x]
                        y_v = x


#Dibuja una cruz
k = 0
while k < ncolum:
    imgGray[mean][k]=0
    k = k+1
k = 0
while k < nrow:
    imgGray[k][y_v]=0
    k=k+1

cv2.imshow("Punto de fuga", imgGray)

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
