import csv

''' def leer_parque(nombre_archivo, parque):
    f = open(nombre_archivo)
    filas = csv.reader(f)
    data = []
    encabezado = next(filas)
    for fila in filas: 
        registro = dict(zip(encabezado, fila))
        if registro['espacio_ve'] == parque:
            data.append(registro)
    return data 
            
print(len(leer_parque('arbolado-en-espacios-verdes.csv', 'GENERAL PAZ'))) '''

def leer_parque(nombre_archivo, parque):
    f = open(nombre_archivo)
    filas = csv.reader(f)
    data = []
    encabezado = next(filas)
    for fila in filas: 
        registro = dict(zip(encabezado, fila))
        if registro['espacio_ve'] == parque:
            registro['altura_tot'] = float(registro['altura_tot'])
            data.append(registro)
            
    return data  
#print(leer_parque('arbolado-en-espacios-verdes.csv', 'GENERAL PAZ'))

def obtener_alturas(lista_arboles, especie):
    lista_de_alturas = []
    for arbol in lista_arboles:
        if arbol['nombre_com'] == especie:
            altura = arbol['altura_tot']
            lista_de_alturas.append(altura)
    return lista_de_alturas

gral_paz = [leer_parque('arbolado-en-espacios-verdes.csv', 'GENERAL PAZ'), 'General Paz']
los_andes = [leer_parque('arbolado-en-espacios-verdes.csv', 'EJERCITO DE LOS ANDES'),'Los Andes']
centenario = [leer_parque('arbolado-en-espacios-verdes.csv', 'CENTENARIO'),'Centenario']
parques = [gral_paz, los_andes, centenario]
max_arbol = []
proms = []
nombres = []
for parque in parques:
    data = obtener_alturas(parque[0], 'Jacarandá')

    max_arbol.append(max(data))
    proms.append(sum(data)/len(data))
    nombres.append(parque[1])
    
   
# print('Medida', nombres)
# print("max", max_arbol)
# print("prom", proms)
            
