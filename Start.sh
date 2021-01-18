#!/bin/sh
now=$(date)


python3 CDC_Scrapper.py

sleep 5

if ls ${PWD}/Data/covid19_vaccinations_in_the_united_states.csv; then
    mv "${PWD}/Data/covid19_vaccinations_in_the_united_states.csv" "$PWD/Data/$now"
fi


