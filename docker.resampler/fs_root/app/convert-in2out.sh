#!/usr/bin/env bash

IFS=$'\n'

cd $(dirname $0)

rm data.csv/*
for file in data.in/*; do
    echo "converting $file to .csv"
    ./bin/xlsx_to_csv.sh "$file" data.csv/ 
done

rm data.resampled/*
for file in data.csv/*; do
    echo "resampling $file"
    ./bin/resample.py "$file" data.resampled
done

for file in data.resampled/*; do
    echo "converting $file to .xlsx"
    ./bin/csv_to_xlsx.sh "$file" data.out/
done
