import xml.etree.ElementTree as et

#Elementos para el xml queguarda informacion
FILE = "objetos.xml"
OBJECT = "Object"
MOM = "Mom"
AREA = "Area"
PERIMETRE = "Perimetre"
HUE_MOM = "HueMom"
NAME = "name"
NUM = "Num"

"""
    Lee la informacion de un objeto
"""
def readInfo (objectName, root):
    for object in root.iter(OBJECT):
        name = object.get(NAME)
        if name == objectName:
            return object.find(NUM).text, object.find(MOM).text, object.find(AREA).text, object.find(PERIMETRE).text,object.find(HUE_MOM).text
    return "-1"

"""
    Actualiza la informacion de un objeto
"""
def updateInfo (objectName, num, nom, area, perimetre, hue, file, root):
    for object in root.iter(OBJECT):
        name = object.get(NAME)
        if name == objectName:
            object.find(NUM).text = num
            object.find(MOM).text = nom
            object.find(AREA).text = area
            object.find(PERIMETRE).text = perimetre
            object.find(HUE_MOM).text = hue
            file.write(FILE)
            return
    return "-1"

"""
    Añade un valor la informacion de un objeto
"""
def updateInfo (objectName, num, nom, area, perimetre, hue, file, root):
    for object in root.iter(OBJECT):
        name = object.get(NAME)
        if name == objectName:
            object.find(NUM).text = num
            object.find(MOM).text = nom
            object.find(AREA).text = area
            object.find(PERIMETRE).text = perimetre
            object.find(HUE_MOM).text = hue
            file.write(FILE)
            return
    return "-1"

"""
    Crea el XML de un objeto y lo guarda
"""
def createInfo (objectName, num, mom, area, perimetre, hue, file, root):
    objectXML = et.Element(OBJECT)
    objectXML.set(NAME, objectName)
    root.append(objectXML)
    numXML = et.SubElement(objectXML, NUM)
    numXML.text = num
    momXML = et.SubElement(objectXML, MOM)
    momXML.text = mom
    areaXML = et.SubElement(objectXML, AREA)
    areaXML.text = area
    perimetreXML = et.SubElement(objectXML, PERIMETRE)
    perimetreXML.text = perimetre
    hueXML = et.SubElement(objectXML, HUE_MOM)
    hueXML.text = hue

    file.write(FILE)
