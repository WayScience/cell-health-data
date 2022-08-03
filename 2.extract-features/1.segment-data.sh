#!/bin/bash
jupyter nbconvert --to compile-nuclei-project.ipynb
python segment-cell-health-data.py
