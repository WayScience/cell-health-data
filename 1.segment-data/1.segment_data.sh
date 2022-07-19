#!/bin/bash
jupyter nbconvert --to python segment-cell-health-data.ipynb
python segment-cell-health-data.py