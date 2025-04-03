# -*- coding: utf-8 -*-
# Python
"""
Created on Wed Aug 14 00:50:45 2024

@author: hamon
""" 

import pandas as pd

path_in = 'c:/Users/hamon/OneDrive/Bureau/hirid-a-high-time-resolution-icu-dataset-1.1.1/Data_of_interest/All_Observation_GFR.csv'
path_out = 'c:/Users/hamon/OneDrive/Bureau/hirid-a-high-time-resolution-icu-dataset-1.1.1/Data_of_interest/All_Observation_GFR_calcule.csv'
IndexInteret = ['patientid','datetime','value','variableid']
d_type = {'patientid':int, 'value':float, 'variableid':int}

# Lire le fichier CSV
df = pd.read_csv(path_in, sep=',', usecols=IndexInteret, parse_dates=['datetime'], dtype=d_type)


# Convertir la colonne 'datetime' en datetime puis extraire 'time' et 'date'
df['time'] = pd.to_datetime(df['datetime']).dt.time
df['date'] = pd.to_datetime(df['datetime']).dt.date

# Réorganiser les données en utilisant pivot_table pour aligner les variables avec leur date_time
df_pivot = df.pivot_table(index=['patientid', 'date'], columns=['variableid'], values='value')

# Créer une liste des colonnes à renommer
columns_to_rename = {
    20000600: 'Creat_Blood',
    24000572: 'Creat_U1',
    24000573: 'Creat_U2',
    10020000: 'Vol_U_Hourly'}

# Renommer les colonnes d'intérêt
df_pivot.rename(columns=columns_to_rename, level=0, inplace=True, errors='coerce')

# Rassembler les Creat_U1 et Creat_U2 en une seule colonne, si elles existent
if 'Creat_U1' in df_pivot.columns and 'Creat_U2' in df_pivot.columns:
    df_pivot['Creat_u'] = (df_pivot['Creat_U1'] + df_pivot['Creat_U2'])/2
elif 'Creat_U1' in df_pivot.columns:
    df_pivot['Creat_u'] = df_pivot['Creat_U1']
elif "Creat_U2" in df_pivot.columns:
    df_pivot['Creat_u'] = df_pivot['Creat_U2']
else:
    df_pivot['Creat_u'] = None

#Garde les colonnes d'intérêts
df_pivot = df_pivot.filter(items=['Creat_Blood', 'Vol_U_Hourly', 'Creat_u'], axis=1)

# Calculer la nouvelle variable DFG
if all(col in df_pivot.columns for col in ["Vol_U_Hourly", "Creat_u", "Creat_Blood"]):
    df_pivot['DFG'] = df_pivot['Vol_U_Hourly'] * df_pivot['Creat_u'] / (df_pivot['Creat_Blood'] * 60)
else:
    df_pivot['DFG'] = None

# Réinitialiser l'index pour remettre les colonnes en ordre
df_pivot = df_pivot.reset_index()

# Ajouter la colonne DFG à la deuxième position si elle existe
if 'DFG' in df_pivot.columns:
    cols = df_pivot.columns.tolist()
    cols.insert(2, cols.pop(cols.index('DFG')))  
    df_pivot = df_pivot[cols]

# Enregistrer le fichier CSV mis à jour
df_pivot.to_csv(path_out, index=False)
