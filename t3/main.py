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

print "Sobel"
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
module_show = np.abs(sobelx) + np.abs(sobely) #Aproximacion, mas rapida que hacer el calculo y bastante buena

#La operacion implementandola a mano, lo hace bien - o eso creo-
module_x = sobelx;
for i in range(len(sobelx)):
    for j in range(len(sobelx[i])):
        module_x[i][j] = np.abs(np.sqrt(sobelx[i][j]**2 + sobely[i][j]**2))


print module_x
cv2.imshow("Module", module_x)

#orientacion, lo hace bien pero con colores cambiados
ori = np.arctan2(sobely, sobelx)
ori_show = (ori/np.pi) * 128
ori_show2 = ori_show.astype(np.uint8)

"""
for i in range(len(sobelx)):
    for j in range(len(sobelx[i])):
        ori_show2[i][j] = (np.arctan2(sobely[i][j], sobelx[i][j])/np.pi)*128

print ori_show2
#ori_show2 = ori_show2.astype(np.uint8)
"""
cv2.imshow("Orientacion", ori_show2)

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
