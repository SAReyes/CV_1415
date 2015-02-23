# Trabajo 1

La aplicación muestra cuatro ventanas en vivo:
* **camera:** la imagen de la camara
* **camera processed:** la imagen con un filtro aplicado en tiempo real
* **histogram:** el histograma de la imagen original
* **histogram processed:** el histograma de la imagen procesada

Comandos del teclado que escucha el programa, presionar la tecla cambia al estado deseado sin tener en cuenta el estado actual (el estado de las variables se guardan):
* **c:** aplica la funsion básica para editar el contraste `corr = img*gain + bias`, gain y bias configurable, volver a presionar la tecla aplica _CLAHE(Conrast Limited Adaptive Histogram Equalization)_ a la imagen donde el límite es configurable
* **h:** aplica una ecualizacion de histograma estandar de OpenCV
* **a:** aplica el filtro alien en el espacio YCrCB, volver a presionar la tecla cambia el espacio de color a HSV, el color del efecto es configurable
* **p:** aplica el filtro poster visto en clase, la cantidad de color es configurable
* **d:** aplica una distorción radial a la imagen, la constante de distorción es configurable (k<0 efecto cojín y k>0 efecto barril)
* **m:** aplica el filtro mean shift, el radio del espacio, el radio del color y el nivel de piramide configurable (notese que este filtro puede ser costoso computacionalmente)
* **n:** desactiva cualquier filtro
* **q:** cierra la aplicación

Los parámetros configurables se modifican con las teclas _1,2,3,4,5 y 6_ del numpad
