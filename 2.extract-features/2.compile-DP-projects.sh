#!/bin/bash
jupyter nbconvert --to python compile-DP-projects.ipynb
python compile-DP-projects.py
