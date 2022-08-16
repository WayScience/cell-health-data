#!/usr/bin/env python
# coding: utf-8

# ### Import Libraries

# In[1]:


import pathlib
from pycytominer.cyto_utils import DeepProfiler_processing
import pandas as pd
import numpy as np
import joblib

import importlib
preprocessUtils = importlib.import_module("preprocess-features-utils")


# ### Specify File/Folder paths

# In[2]:


intermediate_files_dir = pathlib.Path("intermediate_files/")
intermediate_files_dir.mkdir(parents=True, exist_ok=True)

annotations_path = pathlib.Path("../0.image-download/manifest/idr0080-screenA-annotation.csv")

features_output_dir = pathlib.Path("/media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/cell-health-nuc-DP/outputs/efn_pretrained/features")
original_index_csv_path = pathlib.Path("/media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/cell-health-nuc-DP/inputs/metadata/index.csv")


# ### Convert index.csv to int values

# In[3]:


index_csv_path = pathlib.Path(f"{intermediate_files_dir}/index.csv")
# convert string values to int where possible (ex with well number)
# necessary because pycytominer reads index.csv file with `dtype=str`
original_index_csv = pd.read_csv(original_index_csv_path)
original_index_csv.to_csv(index_csv_path)


# ### Create index df with normalization population

# In[4]:


normalization_index_csv = pathlib.Path(f"{intermediate_files_dir}/norm_pop_index.csv")

norm_index_df = preprocessUtils.get_negative_control_index_df(index_csv_path, annotations_path)
norm_index_df.to_csv(normalization_index_csv, index=False)


# ### Create/save normalization scaler

# In[5]:


scaler_path = f"{intermediate_files_dir}/negative_control_scaler.sclr"

scaler = preprocessUtils.get_normalization_scaler(normalization_index_csv, features_output_dir)
joblib.dump(scaler, scaler_path)

scaler = joblib.load(scaler_path)


# ### Normalize and save Cell Health single cells by plate

# In[6]:


output_path = pathlib.Path("/media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/cell-health-nuc-normalized/")
preprocessUtils.normalize_by_plate(index_csv_path, scaler, features_output_dir, output_path)

