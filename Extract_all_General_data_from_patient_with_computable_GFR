#!/bin/bash
path="/mnt/c/Users/hamon/OneDrive/Bureau/hirid-a-high-time-resolution-icu-dataset-1.1.1"
path2="/mnt/c/Users/hamon/OneDrive/Bureau/hirid-a-high-time-resolution-icu-dataset-1.1.1/Data_of_interest"

#Create the head the file
head -n 1 ${path}/general_table.csv > ${path2}/general_table_GFR.csv

#Create the variable list_IDs from the file Log_Patients.IDs
# Log_Patients.IDs = Computable_GFR.IDs that has been create previously
list_IDs=$(cat ${path}/Log_Patients.IDs | tr "\n" " " )

#Create a hash table to selected the patients with the right IDs
time awk -v ids="$list_IDs" 'BEGIN {
    FS=",";
    split(ids, id_array, " ");
    for (i in id_array) {
        id_map[id_array[i]] = 1;
    }
}
{
    if ($1 in id_map) {
        print $0;
    }
}' ${path}/general_table.csv >> ${path2}/general_table_GFR.csv
