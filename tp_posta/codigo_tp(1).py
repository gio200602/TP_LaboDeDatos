import pandas as pd
from inline_sql import sql, sql_val
import matplotlib.pyplot as plt

import seaborn as sns


#%%
localidades = pd.read_csv('/home/axel/Documentos/LaboDeDatos/Tp1/localidades-censales.csv')
clae2 = pd.read_csv("/home/axel/Documentos/LaboDeDatos/Tp1/Entrega/diccionario_clae2.csv")
cod_departamento = pd.read_csv("/home/axel/Documentos/LaboDeDatos/Tp1/Entrega/diccionario_cod_depto.csv")
median = pd.read_csv("/home/axel/Documentos/LaboDeDatos/Tp1/Entrega/w_median_depto_priv_clae2(1).csv")
padron = pd.read_csv("/home/axel/Documentos/LaboDeDatos/Tp1/padron-de-operadores-organicos-certificados.csv", encoding="windows-1252")

""" Elimininamos NULLs y columnas que vamos a trasladar a otras tablas """
#--------------------------------------------------------------
#Eliminamos primero las columnas "función" y "fuente" que no aportan nada:
localidades = localidades.drop(['funcion'], axis = 1) 
localidades = localidades.drop(['fuente'], axis = 1)
#Eliminamos ahora las filas que puedan tener NULLs:
localidades = localidades.dropna()
#Creamos un nuevo DataFrame sin las columnas que vamos a trasladar a otras tablas:
localidades = sql^"""SELECT  categoria,centroide_lat,centroide_lon, departamento_id, departamento_nombre, municipio_id,
                               municipio_nombre, id AS localidad_id, nombre AS localidad_nombre
                               FROM localidades"""
#Ponemos todos los nombres en mayúsculas
localidades = sql^"""SELECT categoria,centroide_lat,centroide_lon,departamento_id,
                            UPPER(departamento_nombre) AS departamento_nombre,
                            municipio_id, UPPER(municipio_nombre) AS municipio_nombre,
                            localidad_id, UPPER(localidad_nombre) AS localidad_nombre, 
                            FROM localidades """

#Eliminamos las tildes de los departamentos para unificar los valores con las demás tablas
localidades = sql^"""SELECT categoria,centroide_lat,centroide_lon,departamento_id, 
                            REPLACE(departamento_nombre,'Á','A') AS departamento_nombre,municipio_id,
                            municipio_nombre, localidad_id,localidad_nombre
                            FROM localidades"""
localidades = sql^"""SELECT categoria,centroide_lat,centroide_lon,departamento_id, 
                            REPLACE(departamento_nombre,'É','E') AS departamento_nombre,municipio_id,
                            municipio_nombre, localidad_id,localidad_nombre
                            FROM localidades"""
localidades = sql^"""SELECT categoria,centroide_lat,centroide_lon,departamento_id, 
                            REPLACE(departamento_nombre,'Í','I') AS departamento_nombre,municipio_id,
                            municipio_nombre, localidad_id,localidad_nombre
                            FROM localidades"""
localidades = sql^"""SELECT categoria,centroide_lat,centroide_lon,departamento_id, 
                            REPLACE(departamento_nombre,'Ó','O') AS departamento_nombre,municipio_id,
                            municipio_nombre, localidad_id,localidad_nombre
                            FROM localidades"""
localidades = sql^"""SELECT categoria,centroide_lat,centroide_lon,departamento_id, 
                            REPLACE(departamento_nombre,'Ú','U') AS departamento_nombre,municipio_id,
                            municipio_nombre, localidad_id,localidad_nombre
                            FROM localidades"""   

#--------------------------------------------------------------
municipios = sql^"""SELECT DISTINCT municipio_id, municipio_nombre, departamento_id
                    FROM localidades"""                     
#--------------------------------------------------------------                            

municipios.to_csv('municipios.csv')
localidades = sql^ """ SELECT centroide_lat, centroide_lon, municipio_id,
                                localidad_id, localidad_nombre
                                FROM localidades"""
localidades.to_csv('localidades.csv')

#%%


#%%
#Renombramos 'codigo_departamento_indec' como departamento_id y 'nombre_departamento_indec' como departamento_nombre para que tengan
#nombres mas cortos y declarativos
departamentos = sql ^  """
                 SELECT codigo_departamento_indec AS departamento_id, nombre_departamento_indec AS departamento_nombre,
                 id_provincia_indec AS prov_id
                 FROM cod_departamento
                """
#Ponemos todos los nombres en mayúsculas
departamentos = sql^"""SELECT departamento_id, UPPER(departamento_nombre) AS departamento_nombre, prov_id
                            FROM departamentos """

#Eliminamos las tildes en los deptos para unificar valores con las demás tablas
departamentos = sql^"""SELECT departamento_id,REPLACE(departamento_nombre,'Á','A') AS departamento_nombre,
                            prov_id
                            FROM departamentos"""
departamentos = sql^"""SELECT departamento_id, REPLACE(departamento_nombre,'É','E') AS departamento_nombre,
                            prov_id
                            FROM departamentos""" 
departamentos = sql^"""SELECT departamento_id, REPLACE(departamento_nombre,'Í','I') AS departamento_nombre,
                            prov_id
                            FROM departamentos"""
departamentos = sql^"""SELECT departamento_id, REPLACE(departamento_nombre,'Ó','O') AS departamento_nombre,
                            prov_id
                            FROM departamentos"""
departamentos = sql^"""SELECT departamento_id, REPLACE(departamento_nombre,'Ú','U') AS departamento_nombre,
                            prov_id
                            FROM departamentos"""                            
#--------------------------------------------------------------  
departamentos.to_csv('departamentos.csv', index = False)

#%%

codigos_distintos = sql^"""SELECT *
                 FROM cod_departamento
                 INNER JOIN localidades
                 ON id_provincia_indec = provincia_id AND
                 nombre_departamento_indec = departamento_nombre
                 WHERE codigo_departamento_indec != departamento_id """
nombres_distintos = sql^"""SELECT *
                 FROM cod_departamento
                 INNER JOIN localidades
                 ON id_provincia_indec = provincia_id AND
                 codigo_departamento_indec = departamento_id
                 WHERE nombre_departamento_indec != departamento_nombre """

cod_departamento = sql^""" SELECT a.departamento_id AS codigo_departamento, a.departamento_nombre
                       AS nombre_departamento, b.id_provincia_indec, 
                       b.nombre_provincia_indec
                       FROM cod_departamento AS b, localidades AS a """
                
prov_deptos = sql^"""SELECT * FROM provincias
                            INNER JOIN departamentos
                            ON departamentos.prov_id = provincias.prov_id
                            """
prov_deptos_muni = sql^"""SELECT * FROM prov_deptos
                INNER JOIN municipios
           
                ON prov_deptos.departamento_id = municipios.departamento_id"""
ubicaciones_completo = sql^"""SELECT * FROM prov_deptos_muni
                INNER JOIN localidades
           
                ON prov_deptos_muni.municipio_id =  localidades.municipio_id"""
#%%
"""Ahora vamos a borrar las columnas "pais_id", "localidad" y "pais" del padrón 
porque no nos aportan información relevante. Además borramos la columna "provincia",
porque con el Prov_id es suficiente y evitamos así redundancia""" 

padron=padron.drop(['pais_id'], axis = 1)
padron=padron.drop(['pais'], axis = 1)
padron=padron.drop(['provincia'], axis = 1)

padron=padron.drop(['localidad'], axis = 1)

#Creamos la relación externa "certificadores" para relacionar id's y nombres
certificadores = sql^"""
                    SELECT DISTINCT Certificadora_id AS certificadora_id, certificadora_deno AS 
                    certificadora_nombre
                    FROM padron
                    """

#Hacemos algo similar para las categorías
categorias = sql^"""
                    SELECT DISTINCT categoria_id, categoria_desc AS categoria_nombre
                    FROM padron
                    """
"""Ahora quitamos los "nombres" de los certificadores y categorías, ya que están en una tabla aparte,
y nos quedamos solo con los id's correspondientes"""
padron=padron.drop(['certificadora_deno'], axis = 1)
padron=padron.drop(['categoria_desc'], axis = 1)

#Renombramos la columna razón social quitándole la tilde a la o.
padron.rename(columns = {'razón social':'razon_social'}, inplace = True)

#Creamos nueva tabla para relacionar establecimientos y los productos que venden
productos=sql^"""
                    SELECT DISTINCT razon_social,establecimiento,productos
                    FROM padron

                    ORDER BY razon_social,establecimiento
                    """
productos["productos"]=productos["productos"].str.split(", ")
productos= productos.explode("productos").reset_index(drop=True)
productos["productos"]=productos["productos"].str.split(" Y ")
productos= productos.explode("productos").reset_index(drop=True)
productos["productos"]=productos["productos"].str.split("+")
productos= productos.explode("productos").reset_index(drop=True)
padron=padron.drop(['productos'], axis = 1)
padron=padron.drop(['establecimiento'], axis = 1)



#Corregimos un error de ortografía 
padron = sql^"""
                    SELECT DISTINCT provincia_id AS prov_id, 
                    departamento,REPLACE(rubro, 'AGICULTURA', 'AGRICULTURA') as rubro,
                                    categoria_id,Certificadora_id,razon_social
                    FROM padron
                    ORDER BY departamento,rubro,categoria_id,Certificadora_id,razon_social
                    """ 

"""Ahora, dado que en la tabla del padrón hay inconsistencias en la columna de departamentos (hay nombres de departamentos,
ciudades o localidades), vamos a solucionar eso haciendo INNER JOIN de esta columna con las tablas de 
departamentos, localidades y municipios, y en caso de que haya localidades y municipios que concuerden, las reemplazaremos
por sus correspondientes departamentos"""

son_departamentos = sql^""" SELECT padron.prov_id, departamento, rubro, categoria_id,
                            Certificadora_id, razon_social     
                            FROM padron
                            INNER JOIN departamentos
                            ON departamento = departamentos.departamento_nombre AND
                            departamentos.prov_id = padron.prov_id """
padron_sin_deptos = sql^"""SELECT * FROM padron
                            EXCEPT
                            SELECT * FROM son_departamentos """


                                            
son_municipios = sql^ """ SELECT padron_sin_deptos.prov_id, departamento, rubro, categoria_id,
                            Certificadora_id, razon_social     
                            FROM padron_sin_deptos
                            INNER JOIN ubicaciones_completo
                            ON departamento = ubicaciones_completo.municipio_nombre AND 
                            padron_sin_deptos.prov_id = ubicaciones_completo.prov_id
                            """ 
padron_sin_municipios =  sql^"""SELECT * FROM padron_sin_deptos
                            EXCEPT
                            SELECT * FROM son_municipios """
son_localidades = sql^ """ SELECT padron_sin_municipios.prov_id, departamento, 
                            rubro, categoria_id,
                            Certificadora_id, razon_social     
                            FROM padron_sin_municipios
                            INNER JOIN ubicaciones_completo
                            ON departamento = ubicaciones_completo.localidad_nombre AND 
                            padron_sin_municipios.prov_id = ubicaciones_completo.prov_id
                            """ 

"""Ahora que tenemos en claro cuáles valores de la columna "departamento" son departamentos,
cuáles son "municipios" y cuáles "localidades", podemos, en los casos que corresponda, asignar los
departamentos que no estaban"""

padron_final_1 = sql^"""SELECT *
                FROM padron_sin_municipios
                INNER JOIN localidades
                ON departamento = localidades.localidad_nombre"""
padron_final_1 = sql^"""SELECT prov_id, departamento, rubro,
                categoria_id, Certificadora_id, razon_social
                FROM padron_final_1"""
padron_final_2 = sql^"""SELECT *
                FROM padron_sin_departamentos
                INNER JOIN municipios
                ON departamento = municipios.municipio_nombre"""
padron_final_2 = sql^"""SELECT prov_id, departamento, rubro,
                categoria_id, Certificadora_id, razon_social
                FROM padron_final_2"""                
padron = sql^"""SELECT * FROM padron_final_1
                      UNION
                      SELECT * FROM padron_final_2
                      UNION
                      SELECT* FROM son_departamentos"""
#%%                      




#Dividimos las columnas de 'clae2' y 'clae2_desc' por un lado y letra y letra_desc por el otro.
#Renombramos 'clae2_desc' como 'rubro' y 'clae2' como 'rubro_id' para que tengan nombres mas declarativos

rubros = sql ^ """
                 SELECT DISTINCT clae2 AS rubro_id, clae2_desc AS rubro
                 FROM clae2
                 ORDER BY rubro_id
                """


#Hacemos lo mismo con 'letra' y 'letra_desc' renombrandolos como 'actividad_id' y 'actividad'
#A su vez arreglamos el problema del NULL en la actividad 'Otros' asignandole la letra 'Z'

actividades = sql ^ """
                 SELECT DISTINCT CASE WHEN letra IS NULL THEN 'Z' ELSE letra END AS actividad_id, letra_desc AS actividad
                 FROM clae2
                 ORDER BY actividad_id
                """

#A la tabla original de clae2 solo le vamos a dejar la columna de rubro_id y la de actividad_id, para evitar redundancia

clae2 = sql ^ """ SELECT clae2 AS rubro_id, CASE WHEN letra IS NULL THEN 'Z' ELSE letra  END AS actividad_id
                  FROM clae2 """


#Hacemos lo mismo con 'id_provincia_indec' y 'nombre_provincia_indec' renombrandolos como
# 'prov_id' y 'prov_nombre' respectivamente

provincias = sql ^ """
                 SELECT DISTINCT id_provincia_indec AS prov_id, nombre_provincia_indec AS prov_nombre
                 FROM cod_departamento
                 ORDER BY prov_id
                """


"""La misma idea la aplicamos con departamentos, renombrando codigo_departamento_indec como departamento_id y
nombre_departamento_indec como departamento_nombre"""
departamentos = sql^"""SELECT DISTINCT codigo_departamento_indec AS departamento_id, 
                       nombre_departamento_indec AS departamento_nombre
                       FROM cod_departamento """
                       
#Ahora la tabla original de cod_depto queda solo con las columnas de id's correspondientes, para evitar redundancia

prov_departamento = sql ^ """
                 SELECT DISTINCT codigo_departamento_indec AS departamento_id,id_provincia_indec AS prov_id
                 FROM cod_departamento
                 ORDER BY departamento_id
                """
#%%

#Renombramos las columnas de 'codigo_departamento_indec', 'id_provincia_indec', 'clae2' y 'w_median' para que 
#tengan nombres declarativos
#Eliminamos la columna 'id_provincia_indec' pues ya tenemos la relacion prov_departamento
#Eliminamos los registros que tengan NULLS en el departamento y salario mediano<0
#ACLARAR QUE ASUMIMOS O INTERPRETAMOS QUE GANADERIA(ACTIVIDAD CON MAS OPERADORES) ESTA INCLUIDA EN RUBRO_id=1

salarios = sql ^  """
                 SELECT DISTINCT fecha,codigo_departamento_indec AS departamento_id, clae2 AS rubro_id,
                 w_median AS salario_mediano
                 FROM median
                 WHERE salario_mediano>0 AND departamento_id IS NOT NULL
                 ORDER BY fecha, departamento_id, rubro_id, salario_mediano
                """


#Creamos una tabla que es igual a la de salarios original, salvo que en vez
#del id de la provincia tiene el nombre. Esto nos va a servir para luego hacer
#comparaciones y filtrar por provincia de una manera más fácil de entender
salarios_con_provincias = sql ^ """
                 SELECT DISTINCT fecha,s.departamento_id, prov_nombre,p.prov_id,rubro_id,salario_mediano
                 FROM salarios AS s, prov_departamento AS d, provincias AS p
                 WHERE d.departamento_id=s.departamento_id AND p.prov_id=d.prov_id
                 ORDER BY fecha,s.departamento_id,prov_nombre,rubro_id,salario_mediano
                """
#Ahora obtenemos los salarios por cada año (lo hacemos con una función de pandas
# que resultó más cómoda, pero con SQL lo haríamos usando "SELECT" y filtrando con 
# "LIKE")
salarios2014 = salarios_con_provincias[salarios_con_provincias['fecha'].str.startswith('2014')]
salarios2015 = salarios_con_provincias[salarios_con_provincias['fecha'].str.startswith('2015')]
salarios2016 = salarios_con_provincias[salarios_con_provincias['fecha'].str.startswith('2016')]
salarios2017 = salarios_con_provincias[salarios_con_provincias['fecha'].str.startswith('2017')]
salarios2018 = salarios_con_provincias[salarios_con_provincias['fecha'].str.startswith('2018')]
salarios2019 = salarios_con_provincias[salarios_con_provincias['fecha'].str.startswith('2019')]
salarios2020 = salarios_con_provincias[salarios_con_provincias['fecha'].str.startswith('2020')]
salarios2021 = salarios_con_provincias[salarios_con_provincias['fecha'].str.startswith('2021')]
salarios2022 = salarios_con_provincias[salarios_con_provincias['fecha'].str.startswith('2022')]
salarios2023 = salarios_con_provincias[salarios_con_provincias['fecha'].str.startswith('2023')]

#Luego, obtenemos el promedio salarial por rubro, provincia, y año
salario_promedio_2014 = sql ^  """
                 SELECT DISTINCT prov_nombre,rubro_id, AVG(salario_mediano) AS promedio2014
                 FROM salarios2014
                 GROUP BY prov_nombre,rubro_id
                 ORDER BY prov_nombre,rubro_id
                """

salario_promedio_2015 = sql ^  """
                 SELECT DISTINCT prov_nombre,rubro_id,AVG(salario_mediano) AS promedio2015
                 FROM salarios2015
                 GROUP BY prov_nombre,rubro_id
                 ORDER BY prov_nombre,rubro_id
                """
salario_promedio_2016 = sql ^  """
                 SELECT DISTINCT prov_nombre,rubro_id,AVG(salario_mediano) AS promedio2016
                 FROM salarios2016
                 GROUP BY prov_nombre,rubro_id
                 ORDER BY prov_nombre,rubro_id
                """
salario_promedio_2017 = sql ^  """
                 SELECT DISTINCT prov_nombre,rubro_id, AVG(salario_mediano) AS promedio2017
                 FROM salarios2017
                 GROUP BY prov_nombre,rubro_id
                 ORDER BY prov_nombre,rubro_id
                """

salario_promedio_2018 = sql ^  """
                 SELECT DISTINCT prov_nombre,rubro_id, AVG(salario_mediano) AS promedio2018
                 FROM salarios2018
                 GROUP BY prov_nombre,rubro_id
                 ORDER BY prov_nombre,rubro_id
                """
salario_promedio_2019 = sql ^  """
                 SELECT DISTINCT prov_nombre,rubro_id, AVG(salario_mediano) AS promedio2019
                 FROM salarios2019
                 GROUP BY prov_nombre,rubro_id
                 ORDER BY prov_nombre,rubro_id
                """

salario_promedio_2020 = sql ^  """
                 SELECT DISTINCT prov_nombre,rubro_id, AVG(salario_mediano) AS promedio2020
                 FROM salarios2020
                 GROUP BY prov_nombre,rubro_id
                 ORDER BY prov_nombre,rubro_id
                """

salario_promedio_2021 = sql ^  """
                 SELECT DISTINCT prov_nombre,rubro_id, AVG(salario_mediano) AS promedio2021
                 FROM salarios2021
                 GROUP BY prov_nombre,rubro_id
                 ORDER BY prov_nombre,rubro_id
                """

salario_promedio_2022 = sql ^  """
                 SELECT DISTINCT prov_nombre,rubro_id, AVG(salario_mediano) AS promedio2022
                 FROM salarios2022
                 GROUP BY prov_nombre,rubro_id
                 ORDER BY prov_nombre,rubro_id
                """

salario_promedio_2023 = sql ^  """
                 SELECT DISTINCT prov_nombre,rubro_id, AVG(salario_mediano) AS promedio2023
                 FROM salarios2023
                 GROUP BY prov_nombre,rubro_id
                 ORDER BY prov_nombre,rubro_id
                """

#Juntamos en una tabla todos los promedios
# top24 = sql ^ """
#                   SELECT DISTINCT p1.prov_nombre as Provincia,promedio2014,promedio2015,promedio2016,promedio2017,promedio2018,
#                                   promedio2019,promedio2020,promedio2021,promedio2022,promedio2023
#                   FROM salario_promedio_2014 AS p1, salario_promedio_2015 AS p2, salario_promedio_2016 AS p3,
#                   salario_promedio_2017 AS p4, salario_promedio_2018 AS p5,salario_promedio_2019 AS p6,
#                   salario_promedio_2020 AS p7, salario_promedio_2021 AS p8,salario_promedio_2022 AS p9,
#                   salario_promedio_2023 AS p10
#                   WHERE p1.prov_nombre=p2.prov_nombre AND p1.prov_nombre=p3.prov_nombre AND p1.prov_nombre=p4.prov_nombre
#                         AND p1.prov_nombre=p5.prov_nombre AND p1.prov_nombre=p6.prov_nombre AND p1.prov_nombre=p7.prov_nombre
#                         AND p1.prov_nombre=p8.prov_nombre AND p1.prov_nombre=p9.prov_nombre AND p1.prov_nombre=p10.prov_nombre
#                   GROUP BY p1.prov_nombre,promedio2014,promedio2015,promedio2016,promedio2017,promedio2018,
#                           promedio2019,promedio2020,promedio2021,promedio2022,promedio2023
#                   ORDER BY p1.prov_nombre
#                 """


consultaSQL28 = """
                 SELECT DISTINCT '2014' as Año,AVG(salario_mediano) AS promedio_nacional
                 FROM salarios2014
                """

nac14 = sql ^ consultaSQL28
#print(nac14)

consultaSQL28 = """
                 SELECT DISTINCT '2015' as Año,AVG(salario_mediano) AS promedio_nacional
                 FROM salarios2015
                """

nac15 = sql ^ consultaSQL28
#print(nac15)

consultaSQL28 = """
                 SELECT DISTINCT '2016' as Año,AVG(salario_mediano) AS promedio_nacional
                 FROM salarios2016
                """

nac16 = sql ^ consultaSQL28
#print(nac16)

consultaSQL28 = """
                 SELECT DISTINCT '2017' as Año,AVG(salario_mediano) AS promedio_nacional
                 FROM salarios2017
                """

nac17 = sql ^ consultaSQL28
#print(nac17)

consultaSQL28 = """
                 SELECT DISTINCT '2018' as Año,AVG(salario_mediano) AS promedio_nacional
                 FROM salarios2018
                """

nac18 = sql ^ consultaSQL28
#print(nac18)

consultaSQL28 = """
                 SELECT DISTINCT '2019' as Año,AVG(salario_mediano) AS promedio_nacional
                 FROM salarios2019
                """

nac19 = sql ^ consultaSQL28
#print(nac19)

consultaSQL28 = """
                 SELECT DISTINCT '2020' as Año,AVG(salario_mediano) AS promedio_nacional
                 FROM salarios2020
                """

nac20 = sql ^ consultaSQL28
#print(nac20)

consultaSQL28 = """
                 SELECT DISTINCT '2021' as Año,AVG(salario_mediano) AS promedio_nacional
                 FROM salarios2021
                """

nac21 = sql ^ consultaSQL28
#print(nac21)

consultaSQL28 = """
                 SELECT DISTINCT '2022' as Año,AVG(salario_mediano) AS promedio_nacional
                 FROM salarios2022
                """

nac22 = sql ^ consultaSQL28
#print(nac22)

consultaSQL28 = """
                 SELECT DISTINCT '2023' as Año,AVG(salario_mediano) AS promedio_nacional
                 FROM salarios2023
                """

nac23 = sql ^ consultaSQL28
#print(nac23)

consultaSQL28 = """
                 SELECT DISTINCT *
                 FROM nac14
                 UNION
                 SELECT DISTINCT *
                 FROM nac15
                 UNION
                 SELECT DISTINCT *
                 FROM nac16
                 UNION
                 SELECT DISTINCT *
                 FROM nac17
                 UNION
                 SELECT DISTINCT *
                 FROM nac18
                 UNION
                 SELECT DISTINCT *
                 FROM nac19
                 UNION
                 SELECT DISTINCT *
                 FROM nac20
                 UNION
                 SELECT DISTINCT *
                 FROM nac21
                 UNION
                 SELECT DISTINCT *
                 FROM nac22
                 UNION
                 SELECT DISTINCT *
                 FROM nac23
                 ORDER BY Año
                """
#Punto i, sección v:
nac_tot = sql ^ consultaSQL28
promedio_salario = nac_tot['promedio_nacional'].median()
x = nac_tot['promedio_nacional'].std()
nac_tot['promedio_nacional'].plot(kind = 'kde')

plt.axvline(nac_tot['promedio_nacional'].mean(), color = 'orange')#la media
#naranja

plt.axvline(nac_tot['promedio_nacional'].median() , color = 'red')#mediana
#roja

plt.axvline(nac_tot['promedio_nacional'].quantile(0.5) , color = 'blue' , linestyle = '--')
#cuantil 50, en azul
plt.axvline(nac_tot['promedio_nacional'].quantile(0.25) , color = 'green')
#cuartil 25 en verde 
plt.axvline(nac_tot['promedio_nacional'].quantile(0.75) , color = 'violet')
#cuartil 75 en violeta
plt.axvline(nac_tot['promedio_nacional'].mean()+nac_tot['promedio_nacional'].std(), color='black' , linestyle='-.')

plt.axvline(nac_tot['promedio_nacional'].mean()-nac_tot['promedio_nacional'].std(), color='black' , linestyle='-.')

plt.show()

plt.close()

cod_depto = pd.read_csv("diccionario_cod_depto.csv")


#Consultas punto a)

provincias_sin_operadores = sql^"""
                 SELECT DISTINCT prov_id
                 FROM provincias
                 EXCEPT
                 SELECT DISTINCT provincia_id
                 FROM padron
                """
provincias_sin_operadores1 = sql^"""
                 SELECT DISTINCT p.prov_id, pr.prov_nombre as provincia
                 FROM provincias_sin_operadores AS p
                 INNER JOIN provincias as pr
                 ON pr.prov_id=p.prov_id
                """

#Consultas punto b)
departamentos_de_padron =sql^"""
                    SELECT DISTINCT departamento
                    FROM padron
                    """
departamentos_sin_operadores = sql^"""
                 SELECT DISTINCT UPPER(departamento_nombre) as departamentos
                 FROM departamentos
                 EXCEPT
                 SELECT DISTINCT departamento
                 FROM padron
                """

#Consultas punto c)
#ACLARAR QUE NO SEPARAMOS LOS RUBROS MIXTOS YA QUE NO VARIARIA MUCHO
ranking_operadores = sql^"""
                 SELECT DISTINCT rubro,COUNT() as cantidad
                 FROM padron
                 GROUP BY rubro
                 ORDER BY cantidad DESC
                """


actividad_con_mas_operadores =sql^"""
                 SELECT DISTINCT r1.rubro, r1.cantidad
                 FROM ranking_operadores as r1
                 WHERE r1.cantidad=(
                 SELECT MAX(r2.cantidad)
                 FROM ranking_operadores as r2
                 )
                """

#Consultas punto d)


#Sacamos el promedio anual de agricultura y lo ordenamos del mas reciente al mas antiguo

agricultura_promedio_anual= sql^"""
                 SELECT DISTINCT fecha,AVG(salario_mediano) as promedio
                 FROM salarios
                 WHERE fecha LIKE '2022%' AND rubro_id=1
                 GROUP BY fecha
                 ORDER BY fecha DESC
                """

#Graficos punto a)
operadores_por_provincia= sql^"""
                 SELECT DISTINCT prov_nombre as provincia,COUNT() as operadores
                 FROM padron
                 INNER JOIN provincias
                 ON prov_id=provincia_id
                 GROUP BY prov_nombre
                 ORDER BY prov_nombre ASC
                """

#uso scatterplot para graficar
sns.scatterplot(data=operadores_por_provincia, y="provincia", x="operadores")
plt.show()
plt.close()

#Graficos punto b)


boceto = sql^"""
                 SELECT razon_social,establecimiento, COUNT() as cantidad
                 FROM productos
                 GROUP BY razon_social,establecimiento
                 ORDER BY razon_social,establecimiento
                """

boceto2 =sql^"""
                 SELECT prov_nombre,p.razon_social,p.establecimiento,cantidad
                 FROM padron as p,boceto as b, provincias as pr
                 WHERE p.razon_social=b.razon_social AND p.establecimiento=b.establecimiento AND pr.prov_id=p.provincia_id
                 GROUP BY prov_nombre,p.razon_social,p.establecimiento,cantidad
                 ORDER BY prov_nombre,p.razon_social,p.establecimiento,cantidad
                """

boceto3 =sql^"""
                 SELECT prov_nombre as provincia,cantidad
                 FROM boceto2
                """

# grafico con bloxplot para cada provincia individual
boceto3_buenos=boceto3[boceto3['provincia'] == 'Buenos Aires']
sns.boxplot(data=boceto3_buenos).set(title ='productos por operador en buenos aires')
plt.show()
plt.close()
#boceto3.to_csv('produccion_por_prov.csv')

boceto3_cata=boceto3[boceto3['provincia'] == 'Catamarca']
sns.boxplot(data=boceto3_cata).set(title ='productos por operador en Catamarca')
plt.show()
plt.close()

boceto3_chaco=boceto3[boceto3['provincia'] == 'Chaco']
sns.boxplot(data=boceto3_chaco).set(title ='productos por operador en Chaco')
plt.show()
plt.close()

boceto3_chubut=boceto3[boceto3['provincia'] == 'Chubut']
sns.boxplot(data=boceto3_chubut).set(title ='productos por operador en Chubut')
plt.show()
plt.close()

boceto3_cord=boceto3[boceto3['provincia'] == 'Cordoba']
sns.boxplot(data=boceto3_cord).set(title ='productos por operador en Cordoba')
plt.show()
plt.close()

boceto3_corr=boceto3[boceto3['provincia'] == 'Corrientes']
sns.boxplot(data=boceto3_corr).set(title ='productos por operador en Corrientes')
plt.show()
plt.close()

boceto3_entre=boceto3[boceto3['provincia'] == 'Entre Rios']
sns.boxplot(data=boceto3_entre).set(title ='productos por operador en Entre Rios')
plt.show()
plt.close()

boceto3_form=boceto3[boceto3['provincia'] == 'Formosa']
sns.boxplot(data=boceto3_form).set(title ='productos por operador en Formosa')
plt.show()
plt.close()

boceto3_juj=boceto3[boceto3['provincia'] == 'Jujuy']
sns.boxplot(data=boceto3_juj).set(title ='productos por operador en Jujuy')
plt.show()
plt.close()

boceto3_pampa=boceto3[boceto3['provincia'] == 'La Pampa']
sns.boxplot(data=boceto3_pampa).set(title ='productos por operador en La Pampa')
plt.show()
plt.close()

boceto3_rioja=boceto3[boceto3['provincia'] == 'La Rioja']
sns.boxplot(data=boceto3_rioja).set(title ='productos por operador en La Rioja')
plt.show()
plt.close()

boceto3_mend=boceto3[boceto3['provincia'] == 'Mendoza']
sns.boxplot(data=boceto3_mend).set(title ='productos por operador en Mendoza')
plt.show()
plt.close()

boceto3_mision=boceto3[boceto3['provincia'] == 'Misiones']
sns.boxplot(data=boceto3_mision).set(title ='productos por operador en Misiones')
plt.show()
plt.close()

boceto3_neu=boceto3[boceto3['provincia'] == 'Neuquen']
sns.boxplot(data=boceto3_neu).set(title ='productos por operador en Neuquen')
plt.show()
plt.close()

boceto3_negro=boceto3[boceto3['provincia'] == 'Rio Negro']
sns.boxplot(data=boceto3_negro).set(title ='productos por operador en Rio Negro')
plt.show()
plt.close()

boceto3_salta=boceto3[boceto3['provincia'] == 'Salta']
sns.boxplot(data=boceto3_salta).set(title ='productos por operador en Salta')
plt.show()
plt.close()

boceto3_juan=boceto3[boceto3['provincia'] == 'San Juan']
sns.boxplot(data=boceto3_juan).set(title ='productos por operador en San Juan')
plt.show()
plt.close()

boceto3_luis=boceto3[boceto3['provincia'] == 'San Luis']
sns.boxplot(data=boceto3_luis).set(title ='productos por operador en San Luis')
plt.show()
plt.close()

boceto3_cruz=boceto3[boceto3['provincia'] == 'Santa Cruz']
sns.boxplot(data=boceto3_cruz).set(title ='productos por operador en Santa Cruz')
plt.show()
plt.close()

boceto3_estero=boceto3[boceto3['provincia'] == 'Santiago Del Estero']
sns.boxplot(data=boceto3_estero).set(title ='productos por operador en Santiago Del Estero')
plt.show()
plt.close()

boceto3_fuego=boceto3[boceto3['provincia'] == 'Tierra Del Fuego']
sns.boxplot(data=boceto3_fuego).set(title ='productos por operador en Tierra Del Fuego')
plt.show()
plt.close()

boceto3_tucu=boceto3[boceto3['provincia'] == 'Tucuman']
sns.boxplot(data=boceto3_tucu).set(title ='productos por operador en Tucuman')
plt.show()
plt.close()

#Graficos punto c)
salarios_2022_agri= sql^"""
                 SELECT DISTINCT prov_nombre, salario_mediano
                 FROM salarios_con_provincias
                 WHERE fecha LIKE '2022%' AND rubro_id=1
               
                """
               
salarios_agri_prov = sql^"""
                 SELECT prov_nombre, AVG(salario_mediano) as salario_prom
                 FROM salarios_2022_agri
                 GROUP BY prov_nombre
                 ORDER BY prov_nombre DESC
                 
                """
               
salarios_por_prov= sql^"""
                 SELECT provincia, operadores, salario_prom
                 FROM salarios_agri_prov
                 INNER JOIN operadores_por_provincia
                 ON provincia=prov_nombre
                 
                """
sns.regplot(data=salarios_por_prov , y="salario_prom", x="operadores")
plt.show()
plt.close()

#punto j, iv:
salarios2023 = salarios_con_provincias[salarios_con_provincias['fecha'].str.startswith('2023')]
salario_promedio_2023 = sql ^  """
                 SELECT DISTINCT prov_id,rubro_id, AVG(salario_mediano) AS promedio2023
                 FROM salarios2023
                 GROUP BY prov_id,rubro_id
                 ORDER BY prov_id,rubro_id
                """
sns.violinplot(data=salario_promedio_2023,x="prov_id",y="promedio2023").set(title ='Salarios promedio por provincia')