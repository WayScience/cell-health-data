#!/bin/bash
jupyter nbconvert --to python classify-single-cell-phenotypes.ipynb
python classify-single-cell-phenotypes.py
