#!/bin/bash

# convert notebook to python script
jupyter nbconvert --to python CP_feature_extraction/compile-DP-projects.ipynb

# run converted python script
python DP_feature_extraction/compile-DP-projects.py
