#!/usr/bin/env python
# coding: utf-8

# # Classify Cell Health Nuclei Features
# 
# ### Import libraries

# In[1]:


import pathlib
import urllib.request
import joblib

import importlib
classification_utils = importlib.import_module("classification-utils")


# ### Download/load `phenotypic_profiling` model

# In[2]:


hash = "64cfc46ecd92f1956af199c81f8ecf4dc292718f"
file_url = f"https://raw.github.com/WayScience/phenotypic_profiling_model/{hash}/2.train_model/models/log_reg_model.joblib"
log_reg_model_path = pathlib.Path("log_reg_model.joblib")
urllib.request.urlretrieve(file_url, log_reg_model_path)
log_reg_model = joblib.load(log_reg_model_path)


# ### Get phenotypic class probabilities for each plate

# In[3]:


normlized_plates_path = pathlib.Path("/media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/cell-health-nuc-per-plate-normalized/")
classifications_save_path = pathlib.Path("plate_classifications/")
classifications_save_path.mkdir(exist_ok=True, parents=True)

# classify cells from each plate and save classifications
for plate_load_path in normlized_plates_path.iterdir():
    plate = plate_load_path.name.strip("_normalized_single_cell.csv.gz")
    plate_classification_save_path = pathlib.Path(f"{classifications_save_path}/{plate}_cell_classifications.csv.gz")
    
    plate_classifications = classification_utils.classify_plate_cells(log_reg_model, plate_load_path)
    
    print(f"Saving classifications at {plate_classification_save_path}...")
    plate_classifications.to_csv(plate_classification_save_path, compression = "gzip")

