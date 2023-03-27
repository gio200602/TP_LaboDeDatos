import csv

#%%

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


def especies(lista_arboles):
    lista_especies = []
    for arbol in range(len(lista_arboles)):
        lista_especies.append(lista_arboles[arbol]['nombre_com'])
    conjunto_especies = set(lista_especies)
    return conjunto_especies

def contar_ejemplares(lista_arboles):
    espe_cies = especies(lista_arboles)
    dicc = dict()
    for elem in espe_cies:
        dicc[elem] = 0
    
    
    for arbol in lista_arboles:
       dicc[arbol["nombre_com"]] = dicc[arbol["nombre_com"]] + 1
    
    return dicc

def obtener_alturas(lista_arboles, especie):
    lista_de_alturas = []
    for arbol in lista_arboles:
        if arbol['nombre_com'] == especie:
            altura = arbol['altura_tot']
            lista_de_alturas.append(altura)
    return lista_de_alturas

""" def obtener_inclinaciones(lista_arboles, especie):
    inclinaciones = []
    for arbol in range(len(lista_arboles)):
        if lista_arboles[arbol]['nombre_com'] == especie:
            inclinaciones.append(lista_arboles[arbol]['inclinacio'])
    return inclinaciones """ 
# La modificamos por la versión de abajo porque queríamos obtener las inclinaciones como floats.

def obtener_inclinaciones(lista_arboles, especie):
    inclinaciones = []
    for arbol in range(len(lista_arboles)):
        if lista_arboles[arbol]['nombre_com'] == especie:
            inclinaciones.append(float(lista_arboles[arbol]['inclinacio']))
    return inclinaciones


def especimen_mas_inclinado(lista_arboles):
    espe_cies = especies(lista_arboles)
    max_inclinacion = 0 
    especie_mas_inclinada = ""
    for especie in espe_cies:
        inclinaciones = obtener_inclinaciones(lista_arboles, especie)
        if (max(inclinaciones)) > (max_inclinacion):
            max_inclinacion = max(inclinaciones)
            especie_mas_inclinada = especie
    return max_inclinacion, especie_mas_inclinada

def especie_promedio_mas_inclinada(lista_arboles):
    
    espe_cies = especies(lista_arboles)
    especie_mas_inclinada = ""
    mayor_promedio = 0
    for specie in espe_cies:
        
        promedio = (sum(obtener_inclinaciones(lista_arboles, specie))) / len((obtener_inclinaciones(lista_arboles, specie)))
        if promedio > mayor_promedio :
            mayor_promedio = promedio
            especie_mas_inclinada = specie
            
    return especie_mas_inclinada, mayor_promedio
        
        

#%%
    
gral_paz = [leer_parque('arbolado-en-espacios-verdes.csv', 'GENERAL PAZ'), 'General Paz']
los_andes = [leer_parque('arbolado-en-espacios-verdes.csv', 'ANDES, LOS'),'Los Andes']
centenario = [leer_parque('arbolado-en-espacios-verdes.csv', 'CENTENARIO'),'Centenario']

# --- Ejercicio 1:
print(len(leer_parque('arbolado-en-espacios-verdes.csv', 'GENERAL PAZ')))

# --- Ejercicio 3:

print(contar_ejemplares(los_andes[0]))

# --- Ejercicio 4:

parques = [gral_paz, los_andes, centenario]
max_arbol = []
proms = []
nombres = []
for parque in parques:
    data = obtener_alturas(parque[0], 'Jacarandá')

    max_arbol.append(max(data))
    proms.append(sum(data)/len(data))
    nombres.append(parque[1])

print('Medida', nombres)
print("max", max_arbol)
print("prom", proms)

# --- Ejercicio 6:
print(especimen_mas_inclinado(centenario[0]))

# --- Ejercicio 7:

print(especie_promedio_mas_inclinada(los_andes[0]))