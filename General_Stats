#!/bin/bash

path="/mnt/c/Users/hamon/OneDrive/Bureau/hirid-a-high-time-resolution-icu-dataset-1.1.1/"
file="general_table.csv"

awk 'BEGIN{FS=","} $5 ~ "dead"' ${path}/${file} | cut -d',' -f1  | sort -g > ${path}/Dead.csv
awk 'BEGIN{FS=","} $5 ~ "alive"' ${path}/${file} | cut -d',' -f1  | sort -g > ${path}/Alive.csv
awk 'BEGIN{FS=","} $3 ~ "M"' ${path}/${file} | cut -d',' -f1  | sort -g > ${path}/Men.csv
awk 'BEGIN{FS=","} $3 ~ "F"' ${path}/${file} | cut -d',' -f1  | sort -g > ${path}/Women.csv

dead=$(cat ${path}/Dead.csv | wc -l)
alive=$(cat ${path}/Alive.csv | wc -l)
survival=$(awk '{printf("%.3f\n",$1/($1+$2))}' <<<" ${alive} ${dead} ")

women=$(cat ${path}/Women.csv | wc -l)
men=$(cat ${path}/Men.csv | wc -l)
w_ratio=$(awk '{printf("%.3f\n",$1/($1+$2))}' <<<" ${women} ${men} ")

printf "Alive count:		$alive
Dead count:		$dead
Survival rate:		$survival

Women count:		$women
Men count:		$men
Women ratio:		$w_ratio" > ${path}/general_stats.txt

printf "\n\nAverage age of patients:" >> ${path}/general_stats.txt
awk 'BEGIN{FS=","} { sum += $4 } END { if (NR > 0) print sum / NR }' ${path}/${file} >> ${path}/general_stats.txt
