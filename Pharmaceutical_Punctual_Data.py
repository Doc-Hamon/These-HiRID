# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 10:55:25 2024

@author: hamon
"""
import pandas as pd
import numpy as np

path_in = "c:/Users/hamon/OneDrive/Bureau/hirid-a-high-time-resolution-icu-dataset-1.1.1/Data_of_interest\\All_Pharma_GFR.csv"
path_Name_Data = "/Users/hamon/OneDrive/Bureau/hirid-a-high-time-resolution-icu-dataset-1.1.1/Variables_Description.xlsx"
IndexInterest = ['patientid','pharmaid','givenat','givendose',] 
d_type = {'patientid':int, 'givendose':float, 'pharmaid':int, }

path_out = "c:/Users/hamon/OneDrive/Bureau/hirid-a-high-time-resolution-icu-dataset-1.1.1/Data_of_interest\\Pharmaceutical_Punctual.csv"

#Sélection des variables d'intérêt à partir du fichier "Variable_Descriptions"
XEL_Variables = pd.read_excel(path_Name_Data, sheet_name=1, usecols=['Longitudinal or Punctual', 'IDs'], dtype={'IDs' : np.int32}) 
XEL_Variables_Selected = XEL_Variables.pivot(columns='Longitudinal or Punctual', values='IDs')
XEL_Variables_Selected = XEL_Variables_Selected.drop(columns='longitudinal')
XEL_Variables_Selected = XEL_Variables_Selected.dropna(axis=0, how='any')

VariableIN = XEL_Variables_Selected['punctual']

#Créer le dictionnaire des variables à regrouper/Renommer
XEL_DICO = pd.read_excel(path_Name_Data, sheet_name=1, usecols=['Grouped','IDs'])
XEL_DICO = XEL_DICO[XEL_DICO['IDs'].isin(VariableIN)]     
XEL_DICO = XEL_DICO.groupby('Grouped')['IDs'].apply(lambda x: list(x))
XEL_DICO = XEL_DICO.to_dict()

#Créer le tableau 
df = pd.read_csv(path_in, sep=',', usecols=IndexInterest, parse_dates=['givenat'], dtype=d_type)
df = df[df['pharmaid'].isin(VariableIN)]
df['time'] = pd.to_datetime(df['givenat']).dt.time
df['date'] = pd.to_datetime(df['givenat']).dt.date

df_pivot = df.pivot_table(index=['patientid','date'], columns='pharmaid', values='givendose')

#Renommer les variables à regrouper :
mapping = {}
for key, cols in XEL_DICO.items():
    for col in cols:
        if col in df_pivot.columns:
            mapping[col] = key
df_pivot.rename(columns=mapping, inplace=True)

#Regroupe les colonnes avec le même noms
df_pivot.columns = df_pivot.columns.astype(str)
df_merged = df_pivot.groupby(df_pivot.columns, axis=1).mean()

#Conversion booléenne, ~ operator NOT (inverse True e False)
df_merged = ~np.isnan(df_merged)


df_merged.to_csv(path_out, index=True)
