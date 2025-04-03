#!/bin/bash

path="/mnt/c/Users/hamon/OneDrive/Bureau/hirid-a-high-time-resolution-icu-dataset-1.1.1/raw_stage/observation_tables/csv"
name="Selected"

printf 'Selected Events:
Creat_Blood="20000600"
Creat_U1="24000572"
Creat_U2="24000573"
Vol_U_Hourly="10020000"' > All_${name}.log

#Retrieve columns names from part-0.csv
head -n 1 part-0.csv > ${path}/All_${name}.csv

# $file goes through all the "observation-tables.csv"
for file in $(ls $path)
do
# awk arguments:	
# -v: Giving variable to awk
# FS: File (column) separator
# $0 in awk is the whole line, $8 is the eighth file
	time awk 	-v Creat_Blood="20000600" \
				-v Creat_U1="24000572" \
				-v Creat_U2="24000573" \
				-v Vol_U_Hourly="10020000" \
				'BEGIN{FS=","} $8 ~ Creat_Blood "|" Creat_U1 "|" Creat_U2 "|" Vol_U_Hourly' \
				"${path}/${file}" >> ${path}/All_${name}.csv
done
echo ">>----------------<<"

echo "No filter:"
cat ${path}/All_${name}.csv | cut -d',' -f3  | sort -g | uniq | wc -l

# (µmol/L)
printf "With urinary creatinin:\n"
awk 'BEGIN{FS=","} $8 ~ "24000572" "|" "24000573"' ${path}/All_${name}.csv | cut -d',' -f3  | sort -g | uniq | wc -l
awk 'BEGIN{FS=","} $8 ~ "24000572" "|" "24000573"' ${path}/All_${name}n.csv | cut -d',' -f3  | sort -g | uniq > Urinary_Creat.IDs 
printf "    patients IDs written to Urinary_Creat.IDs\n"

# (µmol/L)
printf "With plasma creatinin:\n"
awk 'BEGIN{FS=","} $8 ~ "20000600"' ${path}/All_${name}.csv | cut -d',' -f3  | sort -g | uniq | wc -l
awk 'BEGIN{FS=","} $8 ~ "20000600"' ${path}/All_${name}.csv | cut -d',' -f3  | sort -g | uniq > Plasma_Creat.IDs 
printf "    patients IDs written to Plasma_Creat.IDs\n"


# (mL/h)
printf "With Urinary hourly volume:\n"
awk 'BEGIN{FS=","} $8 ~ "10020000"' ${path}/All_${name}.csv | cut -d',' -f3  | sort -g | uniq | wc -l
awk 'BEGIN{FS=","} $8 ~ "10020000"' ${path}/All_${name}.csv | cut -d',' -f3  | sort -g | uniq > Hourly_Urine.IDs
printf "    patients IDs written to Hourly_Urine.IDs\n"

printf "All three available:\n"
join -t',' <(join -t',' <(sort Urinary_Creat.IDs) <(sort Plasma_Creat.IDs)) <(sort Hourly_Urine.IDs) | wc -l
join -t',' <(join -t',' <(sort Urinary_Creat.IDs) <(sort Plasma_Creat.IDs)) <(sort Hourly_Urine.IDs) > Computable_GFR.IDs
printf "    patients IDs written to Computable_GFR.IDs\n"

cat Urinary_Creat.IDs | sort -g > Urinary_Creat.IDs
cat Plasma_Creat.IDs | sort -g > Plasma_Creat.IDs
cat Hourly_Urine.IDs | sort -g > Hourly_Urine.IDs
cat Computable_GFR.IDs | sort -g > Computable_GFR.IDs 
