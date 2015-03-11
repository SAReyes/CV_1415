import cv2
import func
import sys
import xml.etree.ElementTree as et
import funcXML

# Fichero xml donde se guardan los ficheros
xml_File = et.parse(funcXML.FILE)
root = xml_File.getroot()

funcXML.createInfo("test", "1", "mom", "area", "perimetre", "hue", xml_File, root)
print funcXML.readInfo("test", root)
funcXML.updateInfo("test", "2", "mom2", "area2", "perimetre2", "hue2", xml_File, root)
print funcXML.readInfo("test", root)
