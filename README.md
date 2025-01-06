# These-HiRID

Step by Step : 

1/ In the dataset Hirid, compute patients who's can have a mesurate GFR, (have the same day a urinary creatinine, a blood creatinine, and hourly volume) 
Use "Patient_with_computable_GFR", in bash 

2/ Extract from the dataset "Observationnal data" the data of the patient that can have a mesurate GFR 
Use "Extract_all_Observation_data_from_computable_patient" in bash

2bis/ Do the same thing with the Pharmaceutical Data
"Extract_all_Pharma_data_from_computable_patient" in bash

2ter/ The same with General Data

3/Calcul the GFR from the patient :
Use "Calcul_DFG"

4/ Create a new data set with the variable of interest, from Observationnal Data
Use "Tableau Longitudinal"
