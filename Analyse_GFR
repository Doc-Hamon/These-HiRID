# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 10:32:01 2024

@author: hamon
"""
import pandas as pd

path_in = 'c:/Users/hamon/OneDrive/Bureau/hirid-a-high-time-resolution-icu-dataset-1.1.1/Data_of_interest/All_Observation_GFR_calcule.csv'
path_out = 'c:/Users/hamon/OneDrive/Bureau/hirid-a-high-time-resolution-icu-dataset-1.1.1/Data_of_interest/Analyse_DFG.csv'
ColonneInteret = ['Patientid', 'DFG', 'Creat_u', 'Creat_Blood', 'Vol_U_Hourly', 'date']

df = pd.read_csv(path_in, sep=',', parse_dates=['date'])                                                    
df = df.dropna(axis=0, how='any')

df_CreatBlood = df.filter(items=['Creat_Blood'], axis=1)
df_CreatBlood = df_CreatBlood.loc[(df_CreatBlood['Creat_Blood']>0) & (df_CreatBlood['Creat_Blood']<1000)]
densite_CreatBlood = df_CreatBlood.plot.kde(bw_method=0.3)

df_VolHourly = df.filter(items=['Vol_U_Hourly'], axis=1)
df_VolHourly = df_VolHourly.loc[(df_VolHourly['Vol_U_Hourly']>0) & (df_VolHourly['Vol_U_Hourly']<1000)]
densite_VolHourly = df_VolHourly.plot.kde(bw_method=0.3)

df_CreatU = df.filter(items=['Creat_u'], axis=1)
df_CreatU = df_CreatU.loc[(df_CreatU['Creat_u']>0) & (df_CreatU['Creat_u']<20000)]
densite_CreatU = df_CreatU.plot.kde(bw_method=0.3)

df_DFG = df.filter(items=['DFG'], axis=1)
df_DFG = df_DFG.loc[(df_DFG['DFG']>0) & (df_DFG['DFG']<1000)]
densite_DFG= df_DFG.plot.kde(bw_method=0.3)
