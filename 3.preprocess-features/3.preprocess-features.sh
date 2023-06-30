#!/bin/bash

# convert and run notebook to merge CP and DP features
jupyter nbconvert --to python 3a.merge-features/3a.merge-cp-dp-features.ipynb
python 3a.merge-features/3a.merge-cp-dp-features.py

# convert and run notebook to normalize merged features by plate
jupyter nbconvert --to python 3b.normalize-features/3b.normalize-merged-features.ipynb
python 3b.normalize-features/3b.normalize-merged-features.py
