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


# ### Download/load `phenotypic_profiling` models

# In[2]:


gh_hash = "44e2741058c4d38edc137dc2caf5ea1f94b02410"
final_model_file_url = f"https://raw.github.com/WayScience/phenotypic_profiling_model/{gh_hash}/2.train_model/models/log_reg_model.joblib"
shuffled_baseline_file_url = f"https://raw.github.com/WayScience/phenotypic_profiling_model/{gh_hash}/2.train_model/models/shuffled_baseline_log_reg_model.joblib"

models_path = pathlib.Path("phenotypic_profiling_models/")
models_path.mkdir(exist_ok=True, parents=True)

log_reg_model_path = pathlib.Path(f"{models_path}/log_reg_model.joblib")
urllib.request.urlretrieve(final_model_file_url, log_reg_model_path)
log_reg_model = joblib.load(log_reg_model_path)

shuffled_baseline_model_path = pathlib.Path(f"{models_path}/shuffled_baseline_log_reg_model.joblib")
urllib.request.urlretrieve(shuffled_baseline_file_url, shuffled_baseline_model_path)
shuffled_baseline_model = joblib.load(shuffled_baseline_model_path)


# ### Define hard drive path and classifications output path

# In[3]:


normalized_plates_path = pathlib.Path("/media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/cell-health-nuc-per-plate-normalized/")

classifications_save_path = pathlib.Path("plate_classifications/")
classifications_save_path.mkdir(exist_ok=True, parents=True)


# ### Derive and save phenotypic class probabilities

# In[4]:


# save final model classifications
final_model_classifications_save_path = pathlib.Path(f"{classifications_save_path}/final_model/")
classification_utils.save_feature_classifications(log_reg_model, normalized_plates_path, final_model_classifications_save_path)

# save shuffled baseline model classifications
shuffled_baseline_classifications_save_path = pathlib.Path(f"{classifications_save_path}/shuffled_baseline_model/")
classification_utils.save_feature_classifications(shuffled_baseline_model, normalized_plates_path, shuffled_baseline_classifications_save_path)

