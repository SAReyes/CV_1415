import cv2
import func
import sys
import pickle
import numpy as np

if len(sys.argv) != 3:
    print "Argumentos invalidos"
else:
    area_f = []

    try:
        #Cargamos el objeto donde se guarda la informacion
        info = pickle.load(open('Objetos', 'rb'))
    except IOError:
        info = {}

    nomFich = sys.argv[1]
    nomObj = sys.argv[2]
    img = cv2.imread(nomFich)

    #Obtiene la informacion de los objetos
    _, binary = func.otsu(img)
    contours, _ = func.contours(binary)
    mom, area, perimetre, hu_mom = func.descriptors(contours[0])

    #Lee la informacion del objeto si existe
    try:
        mom_f = info[nomObj]['mom']
        area_f = info[nomObj]['area']
        perimetre_f = info[nomObj]['perimetre']
        hu_mom_f = info[nomObj]['hu_mom']
        area_f.append(area)
        perimetre_f.append(perimetre)
        hu_mom_f.append(hu_mom)
        mom_f.append(mom)
    except KeyError:
        info[nomObj] = {}
        area_f = [area]
        perimetre_f = [perimetre]
        hu_mom_f = [hu_mom]
        mom_f = [mom]
        print "Sin informacion del objeto"

    #Obtiene la media de los parametros
    mediaHu_mom = []
    mediaArea = np.mean(area_f)
    mediaPerimetro = np.mean(perimetre_f)
    hu_mom_t = np.array(hu_mom_f).transpose()
    for i in hu_mom_t[0]:
        mediaHu_mom.append(np.mean(i))

    #Obtiene la varianza de los objetos
    varianzaHu_mom = []
    varianzaArea = np.var(area_f)
    varianzaPerimetro = np.var(perimetre_f)
    for i in hu_mom_t[0]:
        varianzaHu_mom.append(np.var(i))

    #Guarda la informacion en el fichero
    info[nomObj]['mom'] = mom_f
    info[nomObj]['area'] = area_f
    info[nomObj]['perimetre'] = perimetre_f
    info[nomObj]['hu_mom'] = hu_mom_f
    info[nomObj]['mediaArea'] = mediaArea
    info[nomObj]['mediaPerimetro'] = mediaPerimetro
    info[nomObj]['mediaHu_mom'] = mediaHu_mom
    info[nomObj]['varianzaArea'] = varianzaArea
    info[nomObj]['varianzaPerimetro'] = varianzaPerimetro
    info[nomObj]['varianzaHu_mom'] = varianzaHu_mom

    print info

    pickle.dump(info, open('Objetos', 'wb'))
