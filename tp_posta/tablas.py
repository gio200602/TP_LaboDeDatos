import pandas as pd
from inline_sql import sql, sql_val

#%%
df_original = pd.read_csv('/home/axel/Documentos/LaboDeDatos/Tp1/localidades-censales.csv')

""" Elimininamos columnas que vamos a trasladar a otras tablas y NULLs"""
#--------------------------------------------------------------
#Eliminamos primero las columnas "función" y "fuente" que no aportan nada:
df_original = df_original.drop(['funcion'], axis = 1) 
df_original = localidades_principal = df_original.drop(['fuente'], axis = 1)
#Eliminamos ahora las filas que puedan tener NULLs:
df_original = df_original.dropna()
#Creamos un nuevo DataFrame sin las columnas que vamos a trasladar a otras tablas:
localidades_principal = df_original.copy()
localidades_principal = localidades_principal.drop(['departamento_nombre'], axis = 1)
localidades_principal = localidades_principal.drop(['departamento_id'], axis = 1)
localidades_principal = localidades_principal.drop(['municipio_id'], axis = 1)
localidades_principal = localidades_principal.drop(['municipio_nombre'], axis = 1)
localidades_principal = localidades_principal.drop(['provincia_nombre'], axis = 1)
localidades_principal = localidades_principal.drop(['provincia_id'], axis = 1)
#--------------------------------------------------------------

localidades_principal.to_csv('localidades_principal.csv')

#%%
"""Desde el dataframe original extraemos las columnas que forman las nuevas tablas:"""
#%%

municipios_nombre = pd.DataFrame() #Creamos nuevo DataFrame vacío
municipios_nombre['municipio_id'] = df_original['municipio_id']
municipios_nombre['municipio_nombre'] = df_original['municipio_nombre']

municipios_nombre = sql^""" SELECT  DISTINCT *
                            FROM municipios_nombre"""

municipios_nombre.to_csv('municipios_nombre.csv')
#%%

localidades_censales_id_municipioid = pd.DataFrame()
localidades_censales_id_municipioid['id'] = df_original['id']
localidades_censales_id_municipioid['municipio_id'] = df_original['municipio_id']

localidades_censales_id_municipioid.to_csv('localidades_id_municipioid.csv')
#%%

municipio_a_depto = pd.DataFrame()
municipio_a_depto['municipio_id'] = df_original['municipio_id']
municipio_a_depto['departamento_id'] = df_original['departamento_id']

municipio_a_depto = sql^""" SELECT  DISTINCT *
                            FROM municipio_a_depto"""
                            
municipio_a_depto.to_csv('municipio_a_depto')


