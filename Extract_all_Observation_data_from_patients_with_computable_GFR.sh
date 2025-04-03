#!/bin/bash
path="/mnt/c/Users/hamon/OneDrive/Bureau/hirid-a-high-time-resolution-icu-dataset-1.1.1/raw_stage/observation_tables/csv"
path2="/mnt/c/Users/hamon/OneDrive/Bureau/hirid-a-high-time-resolution-icu-dataset-1.1.1"
path3="/mnt/c/Users/hamon/OneDrive/Bureau/hirid-a-high-time-resolution-icu-dataset-1.1.1/Data_of_interest"

#Create the head of the two files
head -n 1 ${path}/part-0.csv > ${path}/All_Observation.csv
head -n 1 ${path}/part-0.csv > ${path3}/All_Observation_GFR.csv

#Merging all the part-*.csv files.
before=$(date)
echo 'Merging HUGE file.'
for part_file in $(ls $path/part-*.csv)
do
	tail -n +2 $part_file >> ${path}/All_Observation.csv
done

after=$(date)
echo "$before"
echo "$after"

echo 'Getting info from HUGE file on GFR_computable patients.'
#Create the variable list_IDs from the file Log_Patients.IDs
# Log_Patients.IDs = Computable_GFR.IDs that has been create previously
list_IDs=$(cat ${path2}/Log_Patients.IDs | tr "\n" " " )

head -n 1 ${path}/part-0.csv > ${path3}/All_Observation_GFR.csv

echo 'Getting info from HUGE file on GFR_computable patients.'

#Create a hash table to selected the patients with the right IDs
time awk -v ids="$list_IDs" 'BEGIN {
    FS=",";
    split(ids, id_array, " ");
    for (i in id_array) {
        id_map[id_array[i]] = 1;
    }
}
{
    if ($3 in id_map) {
        print $0;
    }
}' ${path}/All_Observation.csv >> ${path3}/All_Observation_GFR.csv
