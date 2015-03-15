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
            return [object.find(NUM).text, object.find(MOM).text, \
                object.find(AREA).text, object.find(PERIMETRE).text,\
                object.find(HUE_MOM).text, object.find(MOM_M).text,\
                object.find(AREA_M).text, object.find(PERIMETRE_M).text,\
                object.find(HUE_MOM_M).text, object.find(MOM_V).text,\
                object.find(AREA_V).text, object.find(PERIMETRE_V).text,\
                object.find(HUE_MOM_V).text]
    return [-1]

"""
    Actualiza la informacion de media y varianza de un objeto
"""
def updateInfoM_V (objectName, mom_m, area_m, perimetre_m, hue_m, mom_v, area_v,\
    perimetre_v, hue_v, file, root):
    for object in root.iter(OBJECT):
        name = object.get(NAME)
        if name == objectName:
            object.find(MOM_M).text = str(mom_m)
            object.find(AREA_M).text = str(area_m)
            object.find(PERIMETRE_M).text = str(perimetre_m)
            object.find(HUE_MOM_M).text = str(hue_m)
            object.find(MOM_V).text = str(mom_v)
            object.find(AREA_V).text = str(area_v)
            object.find(PERIMETRE_V).text = str(perimetre_v)
            object.find(HUE_MOM_V).text = str(hue_v)
            file.write(FILE)
            return
    return -1

"""
    Acualiza un valor la informacion de un objeto
"""
def updateInfo (objectName, num, nom, area, perimetre, hue, file, root):
    for object in root.iter(OBJECT):
        name = object.get(NAME)
        if name == objectName:
            object.find(NUM).text = str(num)
            object.find(MOM).text = object.find(MOM).text + ";" + str(nom)
            object.find(AREA).text = object.find(AREA).text + ";" + str(area)
            object.find(PERIMETRE).text = object.find(PERIMETRE).text + ";" +\
                str(perimetre)
            object.find(HUE_MOM).text = object.find(HUE_MOM).text + ";" +\
                str(hue)
            file.write(FILE)
            return
    return -1

"""
    Crea el XML de un objeto y lo guarda
"""
def createInfo (objectName, num, mom, area, perimetre, hue, mom_m, area_m, \
    perimetre_m, hue_m, mom_v, area_v, perimetre_v, hue_v,file, root):
    objectXML = et.Element(OBJECT)
    objectXML.set(NAME, objectName)
    root.append(objectXML)
    numXML = et.SubElement(objectXML, NUM)
    numXML.text = str(num)
    momXML = et.SubElement(objectXML, MOM)
    momXML.text = str(mom)
    areaXML = et.SubElement(objectXML, AREA)
    areaXML.text = str(area)
    perimetreXML = et.SubElement(objectXML, PERIMETRE)
    perimetreXML.text = str(perimetre)
    hueXML = et.SubElement(objectXML, HUE_MOM)
    hueXML.text = str(hue)

    mom_mXML = et.SubElement(objectXML, MOM_M)
    mom_mXML.text = str(mom_m)
    area_mXML = et.SubElement(objectXML, AREA_M)
    area_mXML.text = str(area_m)
    perimetre_mXML = et.SubElement(objectXML, PERIMETRE_M)
    perimetre_mXML.text = str(perimetre_m)
    hue_mXML = et.SubElement(objectXML, HUE_MOM_M)
    hue_mXML.text = str(hue_m)

    mom_vXML = et.SubElement(objectXML, MOM_V)
    mom_vXML.text = str(mom_v)
    area_vXML = et.SubElement(objectXML, AREA_V)
    area_vXML.text = str(area_v)
    perimetre_vXML = et.SubElement(objectXML, PERIMETRE_V)
    perimetre_vXML.text = str(perimetre_v)
    hue_vXML = et.SubElement(objectXML, HUE_MOM_V)
    hue_vXML.text = str(hue_v)

    file.write(FILE)
