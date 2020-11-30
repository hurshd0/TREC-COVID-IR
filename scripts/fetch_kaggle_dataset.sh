#!/usr/bin/env bash

kaggle competitions download -c trec-covid-information-retrieval -p data/
unzip -o trec-covid-information-retrieval.zip
rm -rf trec-covid-information-retrieval.zip