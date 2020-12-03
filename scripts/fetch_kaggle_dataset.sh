#!/usr/bin/env bash

kaggle competitions download -c trec-covid-information-retrieval -p data/
unzip -o data/trec-covid-information-retrieval.zip
rm -rf data/trec-covid-information-retrieval.zip