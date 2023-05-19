#!/bin/bash
jupyter nbconvert --to python DP_feature_extraction/compile-DP-projects.ipynb
python DP_feature_extraction/compile-DP-projects.py
