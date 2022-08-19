#!/bin/bash
jupyter nbconvert --to python preprocess-features.ipynb
python preprocess-features.py
