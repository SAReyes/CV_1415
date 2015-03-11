import xml.etree.ElementTree as et

#Elementos para el xml queguarda informacion
FILE = "objetos.xml"
OBJECT = "Object"
MOM = "Mom"
AREA = "Area"
PERIMETRE = "Perimetre"
HUE_MOM = "HueMom"
MOM_M = "Mom_m"
AREA_M = "Area_m"
PERIMETRE_M = "Perimetre_m"
HUE_MOM_M = "HueMom_m"
MOM_V = "Mom_v"
AREA_V = "Area_v"
PERIMETRE_V = "Perimetre_v"
HUE_MOM_V = "HueMom_v"
NAME = "name"
NUM = "Num"

"""
    Lee la informacion de un objeto
"""
def readInfo (objectName, root):
    for object in root.iter(OBJECT):
        name = object.get(NAME)
        if name == objectName:
            return object.find(NUM).text, object.find(MOM).text, object.find(AREA).text, object.find(PERIMETRE).text,object.find(HUE_MOM).text, object.find(MOM_M).text, object.find(AREA_M).text, object.find(PERIMETRE_M).text,object.find(HUE_MOM_M).text, object.find(MOM_V).text, object.find(AREA_V).text, object.find(PERIMETRE_V).text,object.find(HUE_MOM_V).text
    return "-1"

"""
    Actualiza la informacion de media y varianza de un objeto
"""
def updateInfoM_V (objectName, mom_m, area_m, perimetre_m, hue_m, mom_v, area_v, perimetre_v, hue_v, file, root):
    for object in root.iter(OBJECT):
        name = object.get(NAME)
        if name == objectName:
            object.find(MOM_M).text = mom_m
            object.find(AREA_M).text = area_m
            object.find(PERIMETRE_M).text = perimetre_m
            object.find(HUE_MOM_M).text = hue_m
            object.find(MOM_V).text = mom_v
            object.find(AREA_V).text = area_v
            object.find(PERIMETRE_V).text = perimetre_v
            object.find(HUE_MOM_V).text = hue_v
            file.write(FILE)
            return
    return "-1"

"""
    Acualiza un valor la informacion de un objeto
"""
def updateInfo (objectName, num, nom, area, perimetre, hue, file, root):
    for object in root.iter(OBJECT):
        name = object.get(NAME)
        if name == objectName:
            object.find(NUM).text = object.find(NUM).text + ";" + num
            object.find(MOM).text = object.find(MOM).text + ";" + nom
            object.find(AREA).text = object.find(AREA).text + ";" + area
            object.find(PERIMETRE).text = object.find(PERIMETRE).text + ";" + perimetre
            object.find(HUE_MOM).text = object.find(HUE_MOM).text + ";" + hue
            file.write(FILE)
            return
    return "-1"

"""
    Crea el XML de un objeto y lo guarda
"""
def createInfo (objectName, num, mom, area, perimetre, hue, mom_m, area_m, perimetre_m, hue_m, mom_v, area_v, perimetre_v, hue_v,file, root):
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

    mom_mXML = et.SubElement(objectXML, MOM_M)
    mom_mXML.text = mom_m
    area_mXML = et.SubElement(objectXML, AREA_M)
    area_mXML.text = area_m
    perimetre_mXML = et.SubElement(objectXML, PERIMETRE_M)
    perimetre_mXML.text = perimetre_m
    hue_mXML = et.SubElement(objectXML, HUE_MOM_M)
    hue_mXML.text = hue_m

    mom_vXML = et.SubElement(objectXML, MOM_V)
    mom_vXML.text = mom_v
    area_vXML = et.SubElement(objectXML, AREA_V)
    area_vXML.text = area_v
    perimetre_vXML = et.SubElement(objectXML, PERIMETRE_V)
    perimetre_vXML.text = perimetre_v
    hue_vXML = et.SubElement(objectXML, HUE_MOM_V)
    hue_vXML.text = hue_v

    file.write(FILE)
