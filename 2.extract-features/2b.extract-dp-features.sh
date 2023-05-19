#!/bin/bash

# convert notebook to python script
jupyter nbconvert --to python DP-feature-extraction/compile-DP-projects.ipynb

# run converted python script
python DP-feature-extraction/compile-DP-projects.py

# Run this script to extract features with DeepProfiler
python3 -m deepprofiler --gpu 0 --exp efn_pretrained --root path/to/DP_nuc_project --config cell_health_nuc_config.json profile