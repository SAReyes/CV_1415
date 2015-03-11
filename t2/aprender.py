import cv2
import func
import sys
import xml.etree.ElementTree as et
import funcXML

# Fichero xml donde se guardan los ficheros
xml_File = et.parse(funcXML.FILE)
root = xml_File.getroot()

# Busca la informacion del resto de objetos estudiados
info = funcXML.readInfo(sys.argv[2], root)
print info
