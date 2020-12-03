#!/usr/bin/env bash

cd tools
rm -rf v9.0.8.zip
echo "[1] Fetching TREC Eval tool from NIST"
wget -q https://github.com/usnistgov/trec_eval/archive/v9.0.8.zip
unzip -qo v9.0.8.zip
echo "[2] Removing ZIP file, no longer needed"
rm -rf v9.0.8.zip
echo "[3] Installing TREC Eval tool" 
make -C trec_eval-9.0.8 install