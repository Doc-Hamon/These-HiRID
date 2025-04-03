# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 18:56:46 2025

@author: hamon
"""

import pandas as pd
import numpy as np

path_in = "c:/Users/hamon/OneDrive/Bureau/hirid-a-high-time-resolution-icu-dataset-1.1.1/Data_of_interest\\All_Pharma_GFR.csv"
path_in_weight = "c:/Users/hamon/OneDrive/Bureau/hirid-a-high-time-resolution-icu-dataset-1.1.1/Data_of_interest\\Tableau_Punctual.csv"
path_Name_Data = "/Users/hamon/OneDrive/Bureau/hirid-a-high-time-resolution-icu-dataset-1.1.1/Variables_Description.xlsx"
IndexInterest = ['patientid','pharmaid','givenat','givendose',] 
d_type = {'patientid':int, 'givendose':float, 'pharmaid':int, }

path_out = "c:/Users/hamon/OneDrive/Bureau/hirid-a-high-time-resolution-icu-dataset-1.1.1/Data_of_interest\\Pharmaceutical_Longitudinal.csv"

#Sélection des variables d'intérêt à partir du fichier "Variable_Descriptions"
XEL_Variables = pd.read_excel(path_Name_Data, sheet_name=1, usecols=['Variable_Name', 'IDs', 'Longitudinal or Punctual'], dtype={'IDs' : np.int32}) 
XEL_Variables = XEL_Variables[XEL_Variables['Longitudinal or Punctual'].str.contains("longitudinal")]
XEL_Variables = XEL_Variables.drop(columns='Longitudinal or Punctual')
XEL_Variables = XEL_Variables.dropna(axis=0, how='any')
XEL_DICO = XEL_Variables.groupby('Variable_Name')['IDs'].apply(lambda x: list(x))
XEL_DICO = XEL_DICO.to_dict()


#Sélection du Poids du patient
df_Weight = pd.read_csv(path_in_weight, sep=',', usecols=['patientid','Body_weight'])

#Sélection des variables pharmaceutiques
df = pd.read_csv(path_in, sep=',', usecols=IndexInterest, parse_dates=['givenat'], dtype=d_type)
df = df[df['pharmaid'].isin(XEL_Variables['IDs'])]
df['time'] = pd.to_datetime(df['givenat']).dt.time
df['date'] = pd.to_datetime(df['givenat']).dt.date

df_pivot = df.pivot_table(index=['patientid','date','time'], columns='pharmaid', values='givendose')

#Renommer les colonnes
mapping = {}
for key, cols in XEL_DICO.items():
    for col in cols:
        if col in df_pivot.columns:
            mapping[col] = key

df_pivot.rename(columns=mapping, inplace=True)
df_pivot.rename(columns=lambda x: x.replace('Â', '').strip(), inplace=True)

#Rajout de la colonne poids, et merge selon l'ID du patient
index_backup = df_pivot.index
df_pivot = df_pivot.reset_index(level=[1, 2])
df_pivot = df_pivot.merge(df_Weight, how='left', on=['patientid'], )
df_pivot = df_pivot.drop_duplicates(keep='first', subset = 'time')

#Prépare les opérations sur le time
df['time'] = pd.to_datetime(df['givenat']).dt.time
df_pivot['time'] = df_pivot['time'].apply(lambda x: x.replace(microsecond=0))
df_pivot['time'] = pd.to_datetime(df_pivot['date'].astype(str) + ' ' + df_pivot['time'].astype(str))


###Calcul mathématique des doses et Somme des colonnes
##NORADRENALINE
#Noradrenalin 10 µg/ml Bolus, 1 bolus est considéré être donné sur 1 minute
noradrenalin_cols = [
    'Noradrenalin 20 µg/ml Perfusor',
    'Noradrenalin 100 µg/ml Perfusor',
    'Noradrenalin 1mg/ml']

df_pivot['Noradrenalin'] = np.nan

valid_cols = [col for col in noradrenalin_cols if col in df_pivot.columns]

if valid_cols:
    df_pivot['Noradrenalin'] = df_pivot[valid_cols].sum(axis=1, min_count=1)
        
df_NOR20 = df_pivot[['patientid','date','time', 'Noradrenalin']].dropna()
df_NOR20['DeltaTimeN'] = df_NOR20.groupby(['patientid', 'date'])['time'].diff().dt.total_seconds()
df_NOR20.set_index(['patientid', 'date', 'time'], inplace=True)
df_NOR20 = df_NOR20.drop(columns = 'Noradrenalin')

df_pivot.set_index(['patientid', 'date', 'time'], inplace=True)
df_pivot = df_pivot.join(df_NOR20, how='left',).reset_index()

df_pivot['Noradrenalin'] = df_pivot['Noradrenalin']*60/(df_pivot['Body_weight']*df_pivot['DeltaTimeN'])

df_pivot['Noradrenalin 10 µg/ml Bolus'] = df_pivot['Noradrenalin 10 µg/ml Bolus']/df_pivot['Body_weight']

FinalSum = ['Noradrenalin','Noradrenalin 10 µg/ml Bolus']

df_pivot['Noradrenalin'] = df_pivot[FinalSum].sum(axis=1, min_count=1)

df_pivot = df_pivot.drop(columns=noradrenalin_cols, errors='ignore')
df_pivot = df_pivot.drop(columns='Noradrenalin 10 µg/ml Bolus', errors='ignore')


##ADRENALINE
# 1 bolus est considéré être donné sur 1 minute (Adre 100µg/mL bolus et Adre 10µg/mL Bolus)
adrenalin_cols = ['Adrenalin 1mg/ml', 'Adrenalin 20 µg/ml Perfusor', 'Adrenalin 100 µg/ml Perfusor']
adrenalin_Bolus = ['Adrenalin 100 µg/ml Bolus','Adrenalin 10 µg/ml Bolus']

df_pivot['Adrenalin'] = np.nan

valid_cols = [col for col in adrenalin_cols if col in df_pivot.columns]

if valid_cols:
    df_pivot['Adrenalin'] = df_pivot[valid_cols].sum(axis=1, min_count=1)
        
df_ADRE = df_pivot[['patientid','date','time', 'Adrenalin']].dropna()
df_ADRE['DeltaTimeA'] = df_ADRE.groupby(['patientid', 'date'])['time'].diff().dt.total_seconds()
df_ADRE.set_index(['patientid', 'date', 'time'], inplace=True)
df_ADRE = df_ADRE.drop(columns = 'Adrenalin')

df_pivot.set_index(['patientid', 'date', 'time'], inplace=True)
df_pivot = df_pivot.join(df_ADRE, how='left',).reset_index()

df_pivot['Adrenalin'] = df_pivot['Adrenalin']*60/(df_pivot['Body_weight']*df_pivot['DeltaTimeA'])

df_pivot['Adrenalin_Bolus'] = df_pivot[adrenalin_Bolus].sum(axis=1, min_count=1)
df_pivot['Adrenalin_Bolus'] = df_pivot['Adrenalin_Bolus']/df_pivot['Body_weight']

FinalSum = ['Adrenalin','Adrenalin_Bolus']

df_pivot['Adrenalin'] = df_pivot[FinalSum].sum(axis=1, min_count=1)

df_pivot = df_pivot.drop(columns=adrenalin_cols, errors='ignore')
df_pivot = df_pivot.drop(columns='Adrenalin_Bolus', errors='ignore')
df_pivot = df_pivot.drop(columns=adrenalin_Bolus, errors='ignore')

##DOBUTAMINE - conversion en gamma/kg/min ; *1000 conversion mg en µg, *60 conversion s en min
df_DOBU = df_pivot[['patientid','date','time', 'Dobutrex 250 mg/20ml']].dropna()
df_DOBU['DeltaTimeD'] = df_DOBU.groupby(['patientid', 'date'])['time'].diff().dt.total_seconds()
df_DOBU.set_index(['patientid', 'date', 'time'], inplace=True)
df_DOBU = df_DOBU.drop(columns = 'Dobutrex 250 mg/20ml')

df_pivot.set_index(['patientid', 'date', 'time'], inplace=True)
df_pivot = df_pivot.join(df_DOBU, how='left',).reset_index()

df_pivot['Dobutamine'] = df_pivot['Dobutrex 250 mg/20ml']*1000*60/(df_pivot['Body_weight']*df_pivot['DeltaTimeD'])

df_pivot = df_pivot.drop(columns = 'Dobutrex 250 mg/20ml')

##MILRINONE - conversion en gamma/kg/min ; *1000 conversion mg en µg, *60 conversion s en min
df_MILR = df_pivot[['patientid','date','time', 'Corotrop Inj Lsg 1mg/ml 10 ml']].dropna()
df_MILR['DeltaTimeM'] = df_MILR.groupby(['patientid', 'date'])['time'].diff().dt.total_seconds()
df_MILR.set_index(['patientid', 'date', 'time'], inplace=True)
df_MILR = df_MILR.drop(columns = 'Corotrop Inj Lsg 1mg/ml 10 ml')

df_pivot.set_index(['patientid', 'date', 'time'], inplace=True)
df_pivot = df_pivot.join(df_MILR, how='left',).reset_index()

df_pivot['Milrinone'] = df_pivot['Corotrop Inj Lsg 1mg/ml 10 ml']*1000*60/(df_pivot['Body_weight']*df_pivot['DeltaTimeM'])

df_pivot = df_pivot.drop(columns = 'Corotrop Inj Lsg 1mg/ml 10 ml')

##VASOPRESSINE - conversion en UI/kg/h ; *60*60 passage s à h
vasopressin_cols = ['Vasopressin inj 20 U/ml','Vasopressin inf 0.4 U/ml']

df_pivot['Vasopressin'] = np.nan

valid_cols = [col for col in vasopressin_cols if col in df_pivot.columns]

if valid_cols:
    df_pivot['Vasopressin'] = df_pivot[valid_cols].sum(axis=1, min_count=1)
    
df_VASO = df_pivot[['patientid','date','time', 'Vasopressin']].dropna()
df_VASO['DeltaTimeV'] = df_VASO.groupby(['patientid', 'date'])['time'].diff().dt.total_seconds()
df_VASO.set_index(['patientid', 'date', 'time'], inplace=True)
df_VASO = df_VASO.drop(columns = 'Vasopressin')

df_pivot.set_index(['patientid', 'date', 'time'], inplace=True)
df_pivot = df_pivot.join(df_VASO, how='left',).reset_index()

df_pivot['Vasopressin'] = df_pivot['Vasopressin']*60*60/(df_pivot['Body_weight']*df_pivot['DeltaTimeV'])

df_pivot = df_pivot.drop(columns = vasopressin_cols, errors='ignore')

##Propofol - conversion en mg/kg/h
#Bolus de Propofol sont considéré être donné sur 1 min
propofol_cols = ['Disoprivan 1% b','Disoprivan 2% b', 'Disoprivan 1%', 'Disoprivan 2%']
propofol_bolus =['Disoprivan 2% BOLUS b', 'Disoprivan BOLUS 2% 20mg/ml', 'Disoprivan 2% BOLUS']
df_pivot['Propofol'] = np.nan

valid_cols = [col for col in propofol_cols if col in df_pivot.columns]

if valid_cols:
    df_pivot['Propofol'] = df_pivot[valid_cols].sum(axis=1, min_count=1)
        
df_PROP = df_pivot[['patientid','date','time', 'Propofol']].dropna()
df_PROP['DeltaTimeP'] = df_PROP.groupby(['patientid', 'date'])['time'].diff().dt.total_seconds()
df_PROP.set_index(['patientid', 'date', 'time'], inplace=True)
df_PROP = df_PROP.drop(columns = 'Propofol')

df_pivot.set_index(['patientid', 'date', 'time'], inplace=True)
df_pivot = df_pivot.join(df_PROP, how='left',).reset_index()

df_pivot['Propofol'] = df_pivot['Propofol']*60*60/(df_pivot['Body_weight']*df_pivot['DeltaTimeP'])

valid_bolus = [col for col in propofol_bolus if col in df_pivot.columns]

if valid_bolus:
    df_pivot['Propofol_bolus'] = df_pivot[valid_bolus].sum(axis=1, min_count=1)
    df_pivot['Propofol_bolus'] = df_pivot['Propofol_bolus']/(df_pivot['Body_weight']*60)
    FinalSum = ['Propofol','Propofol_bolus']
    df_pivot['Propofol'] = df_pivot[FinalSum].sum(axis=1, min_count=1)

#Propofol - Somme sur 24h
df_pivot['Propofol24h'] = np.nan
propofol24 = propofol_bolus + propofol_cols
valid24_cols = [col for col in propofol24 if col in df_pivot.columns]
if valid24_cols:
    df_pivot["Propofol24h"] = df_pivot[valid24_cols].sum(axis=1, min_count=1)
    df_pivot["Propofol24h"] = df_pivot.groupby(['patientid', 'date'])['Propofol24h'].transform ('sum')
    
df_pivot = df_pivot.drop(columns=propofol_cols, errors='ignore')
df_pivot = df_pivot.drop(columns='Propofol_bolus', errors='ignore')
df_pivot = df_pivot.drop(columns=propofol_bolus, errors='ignore')

##Thiopental.
thiopental_cols = ['Pentothal inj 0.5g','Pentothal 1g Inf Lsg']
df_pivot['Thiopental'] = np.nan
valid_cols = [col for col in thiopental_cols if col in df_pivot.columns]

if valid_cols:
    df_pivot['Thiopental'] = df_pivot[valid_cols].sum(axis=1, min_count=1)
    
df_THIO = df_pivot[['patientid','date','time', 'Thiopental']].dropna()
df_THIO['DeltaTimeT'] = df_THIO.groupby(['patientid', 'date'])['time'].diff().dt.total_seconds()
df_THIO.set_index(['patientid', 'date', 'time'], inplace=True)
df_THIO = df_THIO.drop(columns = 'Thiopental')

df_pivot.set_index(['patientid', 'date', 'time'], inplace=True)
df_pivot = df_pivot.join(df_THIO, how='left',).reset_index()

df_pivot['Thiopental'] = df_pivot['Thiopental']*60*60/(df_pivot['Body_weight']*df_pivot['DeltaTimeT'])

df_pivot = df_pivot.drop(columns=thiopental_cols, errors='ignore')


##Phenobarbital
if 'Phenobarbital 200 mg/2ml' in df_pivot.columns:
    df_pivot['Phenobarbital'] = df_pivot['Phenobarbital 200 mg/2ml']
    df_PHEN = df_pivot[['patientid','date','time', 'Phenobarbital']].dropna()
    df_PHEN['DeltaTimePh'] = df_PHEN.groupby(['patientid', 'date'])['time'].diff().dt.total_seconds()
    df_PHEN.set_index(['patientid', 'date', 'time'], inplace=True)
    df_PHEN = df_PHEN.drop(columns = 'Phenobarbital')
    df_pivot.set_index(['patientid', 'date', 'time'], inplace=True)
    df_pivot = df_pivot.join(df_PHEN, how='left',).reset_index()
    df_pivot['Phenobarbital'] = df_pivot['Phenobarbital']*60*60/(df_pivot['Body_weight']*df_pivot['DeltaTimePh'])
    df_pivot = df_pivot.drop(columns='Phenobarbital 200 mg/2ml', errors='ignore')

#retire colonnes devenues inutiles, possible de les garder pour vérification.
AllDelta = ['DeltaTimeA','DeltaTimeD', 'DeltaTimeM', 'DeltaTimeN', 'DeltaTimeP', 'DeltaTimePh', 'DeltaTimeT',
            'DeltaTimeV']
df_pivot = df_pivot.drop(columns=AllDelta, errors='ignore')


df_pivot.to_csv(path_out, index=True)                                                                                    
