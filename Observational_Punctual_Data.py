# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 14:07:52 2024

@author: hamon
"""

path_in = "c:/Users/hamon/OneDrive/Bureau/hirid-a-high-time-resolution-icu-dataset-1.1.1/Data_of_interest\\All_Observation_GFR.csv"
IndexInterest = ['patientid','datetime','value','variableid', 'status'] 
d_type = {'patientid':int, 'value':float, 'variableid':int, 'status':int}
VariableIN = [410, 7100, 400, #Temperature
              700, 15001441, 960, #Central Veinous Pressure
              510, 15004303, 15001597, #Intra Cranial Pressure
              24000836, 20000900, 24000548, #Hemoglobine
              20000500, 24000520, 24000833, 24000867, #K+ blood
              20000400, 24000519, 24000658, 24000835, 24000866, #Na+ blood
              24000439, 24000521, #Cl- blood
              24000572, 24000573, #Creat_U
              20005110, 24000523, 24000585, #Glucose Blood
              15001166, 15001552 ,10020000 , 10000100,10000200 ,10000300 , 15001565 , 10000400 ,
              10000450 , 20004200 , 24000524 , 20000300 , 20001200 , 20000200 ,
              20000800 ,20004100 ,20000600 ,20003200 ,24000754 ,20000700 ,
              20000110 , 24000665 , 30000140,
              20002200, 24000569, 24000570
]   
              
ColonneDROP = [410, 7100, 400,
              700, 15001441, 960,
              510, 15004303, 15001597,
              24000836, 20000900, 24000548,
              20000500, 24000520, 24000833, 24000867,
              20000400, 24000519, 24000658, 24000835, 24000866,
              24000439, 24000521,
              24000572, 24000573,
              20005110, 24000523, 24000585, ]

path_out = 'c:/Users/hamon/OneDrive/Bureau/hirid-a-high-time-resolution-icu-dataset-1.1.1/Data_of_interest\\Tableau_Punctual.csv'

import pandas as pd
import numpy as np

df = pd.read_csv(path_in, sep=',',usecols=IndexInterest, parse_dates=['datetime'], dtype=d_type )

df['time'] = pd.to_datetime(df['datetime']).dt.time
df['date'] = pd.to_datetime(df['datetime']).dt.date

#Sélection booléene des variable d'intérêt au sein de la colonne variableID
df = df[df['variableid'].isin(VariableIN)]

df_pivot = df.pivot_table(index=['patientid', 'date'], columns=['variableid'], values='value')

#Créer la variable Température
df_pivot['Temperature'] = np.nan
if 410 in df_pivot.columns:
    df_pivot['Temperature'] = df_pivot[410]
if 7100 in df_pivot.columns:
    df_pivot['Temperature'] = df_pivot['Temperature'].combine_first(df_pivot[7100])
if 400 in df_pivot.columns:
    df_pivot['Temperature'] = df_pivot['Temperature'].combine_first(df_pivot[400])
    
#Créer la variable Pression Veineuse Centrale
df_pivot['Central_Veinous_Pressure'] = np.nan
if 700 in df_pivot.columns:
    df_pivot['Central_Veinous_Pressure'] = df_pivot[700]
if 15001441 in df_pivot.columns:
    df_pivot['Central_Veinous_Pressure'] = df_pivot['Central_Veinous_Pressure'].combine_first(df_pivot[15001441])
if 960 in df_pivot.columns:
    df_pivot['Central_Veinous_Pressure'] = df_pivot['Central_Veinous_Pressure'].combine_first(df_pivot[960])
    
#Créer la variable Intracranial pressure
df_pivot['IntraCranial_Pressure'] = np.nan
if 510 in df_pivot.columns:
    df_pivot['IntraCranial_Pressure'] = df_pivot[510]
if 15004303 in df_pivot.columns:
    df_pivot['IntraCranial_Pressure'] = df_pivot['IntraCranial_Pressure'].combine_first(df_pivot[15004303])
if 15001597 in df_pivot.columns:
    df_pivot['IntraCranial_Pressure'] = df_pivot['IntraCranial_Pressure'].combine_first(df_pivot[15001597])

#Créer la variable Hémoglobine
df_pivot['Hemoglobine'] = df_pivot[24000836].combine_first((df_pivot[20000900]).combine_first(df_pivot[24000548]))

#Créer la variable Potassium
df_pivot['Potassium_blood'] = np.nan
if 20000500 in df_pivot.columns:
    df_pivot['Potassium_blood'] = df_pivot[20000500]
if 24000520 in df_pivot.columns:
    df_pivot['Potassium_blood'] = df_pivot['Potassium_blood'].combine_first(df_pivot[24000520])
if 24000833 in df_pivot.columns:
    df_pivot['Potassium_blood'] = df_pivot['Potassium_blood'].combine_first(df_pivot[24000833])
if 24000867 in df_pivot.columns:
    df_pivot['Potassium_blood'] = df_pivot['Potassium_blood'].combine_first(df_pivot[24000867])
    
#Créer la variable Sodium
df_pivot['Sodium_blood'] = np.nan
if 20000400 in df_pivot.columns:
    df_pivot['Sodium_blood'] = df_pivot[20000400]
if 24000519 in df_pivot.columns:
    df_pivot['Sodium_blood'] = df_pivot['Sodium_blood'].combine_first(df_pivot[24000519])
if 24000658 in df_pivot.columns:
    df_pivot['Sodium_blood'] = df_pivot['Sodium_blood'].combine_first(df_pivot[24000658])
if 24000835 in df_pivot.columns:
    df_pivot['Sodium_blood'] = df_pivot['Sodium_blood'].combine_first(df_pivot[24000835])
if 24000866 in df_pivot.columns :
    df_pivot['Sodium_blood'] = df_pivot['Sodium_blood'].combine_first(df_pivot[24000866])

#Créer la variable Chlore
df_pivot['Chlore_blood'] = np.nan
if 24000439 in df_pivot.columns:
    df_pivot['Chlore_blood'] = df_pivot[24000439]
if 24000521 in df_pivot.columns:
    df_pivot['Chlore_blood'] = df_pivot['Chlore_blood'].combine_first(df_pivot[24000521])
    
#Créer la variable Créatinine urinaire
df_pivot['Creatinine_urine'] = np.nan
if 24000572 in df_pivot.columns:
    df_pivot['Creatinine_urine'] = df_pivot[24000572]
if 24000573 in df_pivot.columns:
    df_pivot['Creatinine_urine'] = df_pivot['Creatinine_urine'].combine_first(df_pivot[24000573])

#Créer la variable Glycémie
df_pivot['Glucose_blood'] = np.nan
if 20005110 in df_pivot.columns:
    df_pivot['Glucose_blood'] = df_pivot[20005110]
if 24000523 in df_pivot.columns:
    df_pivot['Glucose_blood'] = df_pivot['Glucose_blood'].combine_first(df_pivot[24000523])
if 24000585 in df_pivot.columns:
    df_pivot['Glucose_blood'] = df_pivot['Glucose_blood'].combine_first(df_pivot[24000585])
    
#Retirer l'ensemble des colonnes sans utilités :
df_pivot = df_pivot.drop(columns=ColonneDROP, errors='ignore')

#Renomme les colonnes restantes :
RenameVariable = {15001166 : 'Circadian_rhythm',
                  15001552 : 'Ventilator_Airway_Code',
                  10020000 : 'Hourly_urine_volume',
                  10000100 : 'GSC_verbal_response',
                  10000200 : 'GSC_motor_response',
                  10000300 : 'GSC_Eye_response',
                  15001565 : 'RASS',
                  10000400 : 'Body_weight',
                  10000450 : 'Body_height',
                  20004200 : 'Bicarbonate_blood',
                  24000524 : 'Lactate_blood',
                  20000300 : 'pH_Arterial_blood',
                  20001200 : 'pCO2_Arterial_blood',
                  20000200 : 'pO2_Arterial_blood',
                  20000800 : 'SatO2_Arterial_blood',
                  20004100 : 'Urea_blood',
                  20000600 : 'Creatinine_blood',
                  20003200 : 'Sodium_urine',
                  24000754 : 'Urea_urine',
                  20000700 : 'Leucocyte_blood',
                  20000110 : 'Platelets_blood',
                  24000665 : 'Cortisol_blood',
                  30000140 : 'Appache_2',
                  20002200 : 'C_reactive_protein',
                  24000569 : 'Natriuretic_peptide_B_prohormone_NTerminal',
                  24000570 : 'Procalcitonin'}    

df_pivot.rename(columns=RenameVariable, level=0, inplace=True, errors='coerce')

#Créer la variable BMI
df_pivot['BMI'] = df_pivot['Body_weight']/((df_pivot['Body_height']/100)**2)

#Créer la variable Glasgow Total
df_pivot['GSC_Total'] =  df_pivot['GSC_Eye_response'] + df_pivot['GSC_motor_response'] + df_pivot['GSC_verbal_response']

#Filtre les valeurs des colonnes
def Filtre_Columns(df, col_limits):
    for col, (min_value, max_value) in col_limits.items():
        if col in df.columns:
            df[col] = df[col].where(df[col].between(min_value, max_value), np.nan)
    return df

col_limits = { 'Temperature' : (0, 45),
              'Central_Veinous_Pressure' : (-20,100),
              'Hourly_urine_volume': (0, 5000),
              'GSC_Eye_response': (1, 4),
              'GSC_motor_response': (1, 6),
              'GSC_verbal_response': (1, 5),
              'RASS': (-5, 5),
              'IntraCranial_Pressure': (0, 200),
              'Body_weight': (0, 500),
              'Body_height': (0,275),
              'Hemoglobine': (0, 270),
              'Bicarbonate_blood': (0, 50),
              'Lactate_blood':(0, 40),
              'pH_Arterial_blood':(6, 8.8),
              'pCO2_Arterial_blood':(0,170),
              'pO2_Arterial_blood':(0, 500),
              'SatO2_Arterial_blood':(0,100),
              'Potassium_blood':(0, 20),
              'Sodium_blood':(90, 190),
              'Chlore_blood':(50, 150),
              'Urea_blood':(0, 120),
              'Creatinine_blood':(0, 2000),
              'Sodium_urine':(0, 300),
              'Creatinine_urine':(0, 30000),
              'Glucose_blood':(0, 145),
              'Leucocyte_blood':(0, 150),
              'Platelets':(0, 1500),
              'Cortisol_blood':(0, 1000),
              'Apache_2':(0,71),
              'BMI' : (0, 150),
              'GSC_Total' : (3, 15),
              'C_reactive_protein' : (0, 10000),
              'Natriuretic_peptide_B_prohormone_NTerminal' : (0, 100000),
              'Procalcitonin' : (0, 10000),
              }

df_pivot = Filtre_Columns(df_pivot, col_limits)

#Créer la variable J-X : correspondd au nombre de jour depuis l'admission
df_pivot['Days_from_admission'] = np.nan

path_General_Data = "c:/Users/hamon/OneDrive/Bureau/hirid-a-high-time-resolution-icu-dataset-1.1.1/Data_of_interest/general_table_GFR.csv"
df_general_data = pd.read_csv(path_General_Data, sep=',', usecols=['patientid', 'sex', 'age', 'admissiontime'])

df_pivot = df_pivot.reset_index()
df_pivot =  df_pivot.merge(df_general_data, how = 'left', on=['patientid'])

df_pivot['date'] = pd.to_datetime(df_pivot['date'])
df_pivot['admissiontime'] = pd.to_datetime(df_pivot['admissiontime'])

df_pivot['Days_from_admission'] = (df_pivot['date'] - df_pivot['admissiontime']).dt.days + 1

df_pivot = df_pivot.drop(columns ='admissiontime')


df_pivot.to_csv(path_out, index=True)
