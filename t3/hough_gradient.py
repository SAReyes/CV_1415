# coding=utf-8
"""
    Cálculo del punto de fuga usando la transformada de Hough con su
    gradiente
"""
import cv2
import numpy as np
import sys

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

votes_img = np.zeros((nrow,ncolum))
lower_mean = int(mean + ncolum * 0.1)
upper_mean = int(mean - ncolum * 0.1)

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
                #TODO: operaciones matriciales ...
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

                    """
                        Dibuja la linea que entre los puntos que corta esta recta
                        con las dos lineas que definene le horizonte
                    """
                    lower_x = int((-1)*((lower_mean*np.sin(ang) - rho)/np.cos(ang)))
                    upper_x = int((-1)*((upper_mean*np.sin(ang) - rho)/np.cos(ang)))
                    temp = np.zeros((nrow, ncolum))
                    cv2.line(temp,(lower_x,lower_mean),(upper_x,upper_mean),(1),10)
                    votes_img = votes_img + temp
                    # cv2.line(img,(lower_x,lower_mean),(upper_x,upper_mean),(255,0,0),1)



j = int(mean)
i = y_v
cross_size = int(ncolum * 0.1)
offset = 5


cv2.line(img, (i, j + offset), (i, j + offset + cross_size), (0, 0, 255),3)
cv2.line(img, (i + offset, j), (i + offset + cross_size, j), (0, 0, 255),3)
cv2.line(img, (i, j - offset), (i, j - offset - cross_size), (0, 0, 255),3)
cv2.line(img, (i - offset, j), (i - offset - cross_size, j), (0, 0, 255),3)

j = int(np.argmax(votes_img) / ncolum)
i = int(np.argmax(votes_img) % ncolum)
cv2.line(img, (i, j + offset), (i, j + offset + cross_size), (0, 255, 255),3)
cv2.line(img, (i + offset, j), (i + offset + cross_size, j), (0, 255, 255),3)
cv2.line(img, (i, j - offset), (i, j - offset - cross_size), (0, 255, 255),3)
cv2.line(img, (i - offset, j), (i - offset - cross_size, j), (0, 255, 255),3)

cv2.imshow("Punto de fuga", img)

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
