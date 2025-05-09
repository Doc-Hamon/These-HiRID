# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 10:27:46 2024

@author: hamon
"""

path_in = "c:/Users/hamon/OneDrive/Bureau/hirid-a-high-time-resolution-icu-dataset-1.1.1/Data_of_interest\\All_Observation_GFR.csv"
IndexInterest = ['patientid','datetime','value','variableid', 'status'] 
d_type = {'patientid':int, 'value':float, 'variableid':int, 'status':int}
VariableInterest = [200, 100, 600, 120, 620, 110, 610, 1000, 4000, 8280, 30005010, 30005110, 30005075, 30005080, 10020000]
RenameVariable = {200 : 'Heart_Rate',
                  30005010 : 'Fluid_balance_IN',
                  30005110 : 'Fluid_balance_OUT',
                  30005075 : 'Infusion_of_saline_solution',
                  1000 : 'Cardiac_output',
                  30005080 : 'Intravenous_fluid_colloid_administration',
                  10020000 : 'Hourly_urine_volume'}

path_out = 'c:/Users/hamon/OneDrive/Bureau/hirid-a-high-time-resolution-icu-dataset-1.1.1/Data_of_interest\\Tableau_Longitudinal.csv'

import pandas as pd
import numpy as np

df = pd.read_csv(path_in, sep=',',usecols=IndexInterest, parse_dates=['datetime'], dtype=d_type)

#Sélection booléene des variable d'intérêt au sein de la colonne variableID
df = df[df['variableid'].isin(VariableInterest)]

df['time'] = pd.to_datetime(df['datetime']).dt.time
df['date'] = pd.to_datetime(df['datetime']).dt.date

df_pivot = df.pivot_table(index=['patientid', 'date', 'time'], columns=['variableid'], values='value')

#Prépare les opérations sur le time
df_pivot = df_pivot.reset_index(level=[1, 2])
df_pivot['time'] = df_pivot['time'].apply(lambda x: x.replace(second=0, microsecond=0))
df_pivot['time'] = pd.to_datetime(df_pivot['date'].astype(str) + ' ' + df_pivot['time'].astype(str))
df_pivot['hour'] = df_pivot['time'].apply(lambda x: x.replace(minute=0))

#Regroupe les lignes par le temps.
df_pivot = df_pivot.groupby(['patientid','time']).first().reset_index()

#Créer la variable xxx Arterial Pressure, si la pression existe en sanglant (100, 110, 120) et au brassard (600, 610, 620)
# la pression sanglante est préféré
df_pivot['Systolic_Arterial_Pressure'] = df_pivot[100].combine_first(df_pivot[600])

df_pivot['Diastolic_Arterial_Pressure'] = df_pivot[120].combine_first(df_pivot[620])

df_pivot['Mean_Arterial_Pressure'] = df_pivot[110].combine_first(df_pivot[610])

#Créer la variable Peripheral_oxygen_saturation, si les 2 existent choisi la 4000, sinon prend celle qui existe
if 4000 in df_pivot.columns and 8280 in df_pivot.columns:
    df_pivot['Peripheral_oxygen_saturation'] = df_pivot[4000].combine_first(df_pivot[8280])
elif 4000 in df_pivot.columns:
    df_pivot['Peripheral_oxygen_saturation'] = df_pivot[4000]
elif 8280 in df_pivot.columns:
    df_pivot['Peripheral_oxygen_saturation'] = df_pivot[8280]

#Renomme les colonnes restantes
df_pivot.rename(columns=RenameVariable, level=0, inplace=True, errors='coerce')

#Créer la variable Fluid_Balance, qui est la différence entre les entrées et les sorties
df_pivot['Fluid_Balance'] = df_pivot['Fluid_balance_IN'] - df_pivot['Fluid_balance_OUT']


#Supprime les colonnes dont on a plus besoin
df_pivot = df_pivot.drop(labels=[100, 600, 120, 620, 110, 610, 4000, 8280], axis = 1, errors='ignore')

#Filtre les colonnes selon une valeur maximal et minimale                                                               
def Filtre_Columns(df, col_limits):
    for col, (min_value, max_value) in col_limits.items():
        if col in df.columns:
            df[col] = df[col].where(df[col].between(min_value, max_value), np.nan)
    return df

col_limits = { 'Heart_Rate' : (0, 300),
              'Systolic_Arterial_Pressure' : (0,300),
              'Diastolic_Arterial_Pressure': (0, 300),
              'Mean_Arterial_Pressure': (0, 300),
              'Peripheral_oxygen_saturation': (0, 100),
              'Fluid_balance_IN': (0, 20000),
              'Fluid_balance': (-20000, 20000),
              'Fluid_balance_OUT': (0, 20000),
              'Infusion_of_saline_solution': (0, 20000),
              'Cardiac_output':(0, 100),
              'Intravenous_fluid_colloid_administration':(0, 2000),
              'Hourly_urine_volume' : (0, 5000)}

df_pivot = Filtre_Columns(df_pivot, col_limits)

#Créer la variable HRV 24h - 1h
df_pivot['HRV_SDNN_24h'] = np.nan
df_pivot['HRV_SDNN_24h'] = df_pivot.groupby(['patientid', 'date'])['Heart_Rate'].transform(lambda x: np.std(x, ddof=1))

df_pivot['HRV_SDNN_1h']= np.nan
df_pivot['HRV_SDNN_1h']= df_pivot.groupby(['patientid', 'hour'])['Heart_Rate'].transform(lambda x: np.std(x, ddof=1))

#Créer la variable Variabilité PAS 24h - 1h
df_pivot['SAP_SDNN_24h'] = np.nan
df_pivot['SAP_SDNN_24h'] = df_pivot.groupby(['patientid', 'date'])['Systolic_Arterial_Pressure'].transform(lambda x: np.std(x, ddof=1))

df_pivot['SAP_SDNN_1h']= np.nan
df_pivot['SAP_SDNN_1h']= df_pivot.groupby(['patientid', 'hour'])['Systolic_Arterial_Pressure'].transform(lambda x: np.std(x, ddof=1))

#Créer la variable Variabilité PAM 24h - 1h
df_pivot['MAP_SDNN_24h'] = np.nan
df_pivot['MAP_SDNN_24h'] = df_pivot.groupby(['patientid', 'date'])['Mean_Arterial_Pressure'].transform(lambda x: np.std(x, ddof=1))

df_pivot['MAP_SDNN_1h']= np.nan
df_pivot['MAP_SDNN_1h']= df_pivot.groupby(['patientid', 'hour'])['Mean_Arterial_Pressure'].transform(lambda x: np.std(x, ddof=1))

#Créer la variable Variabilité PAD 24h - 1h
df_pivot['DAS_SDNN_24h'] = np.nan
df_pivot['DAS_SDNN_24h'] = df_pivot.groupby(['patientid', 'date'])['Diastolic_Arterial_Pressure'].transform(lambda x: np.std(x, ddof=1))

df_pivot['DAS_SDNN_1h']= np.nan
df_pivot['DAS_SDNN_1h']= df_pivot.groupby(['patientid', 'hour'])['Diastolic_Arterial_Pressure'].transform(lambda x: np.std(x, ddof=1))

df_pivot = df_pivot.drop(columns=['hour','date']) 

df_pivot.to_csv(path_out, index=True)
