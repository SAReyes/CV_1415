import cv2
import numpy as np

img = cv2.imread('./ImagenesT2/poster.pgm')
cv2.imshow("Imagen", img)

"""
imgGaussian = cv2.GaussianBlur(img, (3,3), 0)
cv2.imshow("Gaussian", imgGaussian)
"""

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray", imgGray)

#Sobel eje x
sobelx = cv2.Sobel(imgGray, cv2.CV_8U, 1, 0, ksize = 3)
sobelx_show = sobelx/2 + 128
cv2.imshow("SobelX", sobelx_show)

#Sobel eje y
sobely = cv2.Sobel(imgGray, cv2.CV_8U, 0, 1, ksize = 3)
sobely_show = sobely/2 + 128
cv2.imshow("SobelY", sobely_show)
print sobely_show.dtype

#Modulo
module = np.abs(np.sqrt((sobelx)**2 + (sobely)**2)) #No se como hace numpy las operaciones pero no hace lo que esperaba que hiciera
module_show = np.abs(sobelx) + np.abs(sobely) #Aproximación, más rapida que hacer el calculo y bastante buena

#La operación implementandola a mano, lo hace bien - o eso creo-
module_x = sobelx
for i in range(len(sobelx)):
    for j in range(len(sobelx[i])):
        module_x[i][j] = np.abs(np.sqrt(sobelx[i][j]**2 + sobely[i][j]**2))


print module_x
cv2.imshow("Module", module_x)

#orientación, lo hace bien pero con colores cambiados
ori = np.arctan2(sobely, sobelx)
ori_show = (ori/np.pi) * 128
ori_show2 = ori_show.astype(np.uint8)
cv2.imshow("Orientacion", ori_show2)

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
