import cv2
import func
import sys
import xml.etree.ElementTree as et
import funcXML

# Fichero xml donde se guardan los ficheros
xml_File = et.parse(funcXML.FILE)
root = xml_File.getroot()

funcXML.createInfo("test", "1", "mom", "area", "perimetre", "hue", "mom_m", "area_m", "perimetre_m", "hue_m", "mom_v", "area_v", "perimetre_v", "hue_v", xml_File, root)
print funcXML.readInfo("test", root)
funcXML.updateInfo("test", "2", "mom2", "area2", "perimetre2", "hue2", xml_File, root)
print funcXML.readInfo("test", root)
funcXML.updateInfoM_V("test", "mom3", "area3", "perimetre3", "hue3", "mom4", "area4", "perimetre4", "hue4", xml_File, root)
print funcXML.readInfo("test", root)
