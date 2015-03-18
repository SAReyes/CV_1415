import cv2
import func
from sys import argv,exit
import pickle
import numpy as np
import pprint


if len(argv) < 3:
    print "Argumentos invalidos"
    exit(-1)

DESCRIPTORES = 'descriptores.pickle'
nData = 'data'
nMean = 'mean'
nVar = 'var'
DATA = [nData, nMean, nVar]
nArea = 'area'
nPer = 'perimeter'
DESC = ['']
cols = ['area', 'perimeter', 'hu_mom0', 'hu_mom1', 'hu_mom2', 'hu_mom3', 'hu_mom4', 'hu_mom5', 'hu_mom6']
cols = cols[0:5] #usar hasta el tercer momento invariante


def aprender(nom_fich, nom_obj, data):
    print "Fichero:", nom_fich
    print "objeto:", nom_obj

    img = cv2.imread(nom_fich)

    dummy_m = {nData: []}
    dummy_p = {nData: []}
    dummy_h = []

    # Obtiene la informacion de los objetos
    _, binary = func.otsu(img)
    contours, _ = func.contours(binary)
    _, area, perimeter, hu_mom = \
        func.descriptors(func.findBiggestContour(contours))
    # hu_mom_range = range(len(hu_mom))
    hu_mom_range = range(3)

    # Lee la informacion del objeto si existe
    try:
        dummy_m[nData] = data[nom_obj]['area'][nData]
        dummy_p[nData] = data[nom_obj]['perimeter'][nData]
        for i in hu_mom_range:
            dummy_h.append(data[nom_obj]['hu_mom' + str(i)])

        # hu_mom_f = data[nom_obj]['hu_mom']

        dummy_m[nData].append(area)
        dummy_p[nData].append(perimeter)
        for i in hu_mom_range:
            dummy_h[i][nData].append(hu_mom[i][0])
    except KeyError:
        data[nom_obj] = {}
        data[nom_obj]['area'] = {}
        data[nom_obj]['perimeter'] = {}
        for i in hu_mom_range:
            data[nom_obj]['hu_mom' + str(i)] = {}
        # data[nom_obj]['hu_mom'] = [{}]
        print "Sin informacion del objeto"

        dummy_m[nData] = [area]
        dummy_p[nData] = [perimeter]
        for i in hu_mom_range:
            dummy_h.append({nData: [hu_mom[i][0]]})

    # Obtiene la media de los parametros
    dummy_m[nMean] = np.mean(dummy_m[nData])
    dummy_p[nMean] = np.mean(dummy_p[nData])
    for i in hu_mom_range:
        dummy_h[i][nMean] = np.mean(dummy_h[i][nData])

    # Obtiene la varianza de los objetos
    dummy_m[nVar] = np.var(dummy_m[nData])
    dummy_p[nVar] = np.var(dummy_p[nData])
    for i in hu_mom_range:
        dummy_h[i][nVar] = np.var(dummy_h[i][nData])

    # Guarda la informacion en el fichero
    data[nom_obj]['area'] = dummy_m
    data[nom_obj]['perimeter'] = dummy_p
    for i in hu_mom_range:
        data[nom_obj]['hu_mom' + str(i)] = dummy_h[i]


if __name__ == "__main__":
    area_f = []

    try:
        # Cargamos el objeto donde se guarda la informacion
        info = pickle.load(open(DESCRIPTORES, 'rb'))
    except IOError:
        info = {"data": {}}

    for f in argv[1:len(argv) - 1]:
        print "========================="
        print "Aprendiendo:", f
        print "-------------------------"
        aprender(f, argv[len(argv) - 1], info["data"])
        print "DONE!"

    means_m = np.array(())
    vars_m = np.array(())
    for key in info["data"].keys():
        row_m = np.array(())
        row_v = np.array(())
        for desc in cols:
            row_m = np.append(row_m, info["data"][key][desc][nMean])
            row_v = np.append(row_v, info["data"][key][desc][nVar])

        if means_m.size == 0:
            means_m = np.array(row_m)
            vars_m = np.array(row_v)
        else:
            means_m = np.vstack((means_m, row_m))
            vars_m = np.vstack((vars_m, row_v))

    info['means'] = means_m
    info['vars'] = vars_m
    info['names'] = info["data"].keys()
    info['N'] = []
    for key in info['names']:
        info['N'].append(len(info['data'][key]['area']['data']))

    print "========================="
    print "Guardando descriptores en", DESCRIPTORES
    pickle.dump(info, open(DESCRIPTORES, 'wb'))
    print "DONE!"
    print "========================="
    pprint.pprint(info)
