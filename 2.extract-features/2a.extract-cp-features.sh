#!/bin/bash

# convert notebook to python script
jupyter nbconvert --to python CP-feature-extraction/extract_cp_features.ipynb

# run converted python script
python CP-feature-extraction/extract_cp_features.py
