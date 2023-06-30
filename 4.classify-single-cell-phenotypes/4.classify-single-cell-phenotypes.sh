#!/bin/bash
jupyter nbconvert --to python 4a.classify-single-cell-phenotypes/4a.classify-single-cell-phenotypes.ipynb
python 4a.classify-single-cell-phenotypes/4a.classify-single-cell-phenotypes.py

jupyter nbconvert --to python 4b.derive-classification-profiles/4b.derive-classification-profiles.ipynb
python 4b.derive-classification-profiles/4b.derive-classification-profiles.py
