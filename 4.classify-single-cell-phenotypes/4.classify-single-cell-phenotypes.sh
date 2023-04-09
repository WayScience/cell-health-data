#!/bin/bash
jupyter nbconvert --to python classify-features.ipynb
python classify-features.py
