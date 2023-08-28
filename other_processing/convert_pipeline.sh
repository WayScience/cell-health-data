#!/bin/bash
set -e

# download cell-health data
python ./0.download-profiles-from-figshare/download.py

# convert downloaded sqlite data into parquet dataset
python ./1.convert_sqlite_to_parquet/sqlite_to_parquet.py

# check data integrity
python ./1.convert_sqlite_to_parquet/check.py
