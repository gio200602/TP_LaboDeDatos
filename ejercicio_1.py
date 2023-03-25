import csv

def leer_parque(nombre_archivo, parque):
    f = open(nombre_archivo)
    filas = csv.reader(f)
    data = []
    encabezado = next(filas)
    for fila in filas: 
        registro = dict(zip(encabezado, fila))
        if registro['espacio_ve'] == parque:
            data.append(registro)
    return data 
            
print(len(leer_parque('arbolado-en-espacios-verdes.csv', 'GENERAL PAZ')))