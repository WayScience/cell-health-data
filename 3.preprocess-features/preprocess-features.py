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

DP_project_path = pathlib.Path("/media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/cell-health-nuc-DP")
features_output_dir = pathlib.Path(f"{DP_project_path}/outputs/efn_pretrained/features")
original_index_csv_path = pathlib.Path(f"{DP_project_path}/inputs/metadata/index.csv")

output_path = pathlib.Path("/media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/cell-health-nuc-per-plate-normalized/")
output_path.mkdir(parents=True, exist_ok=True)


# ### Convert index.csv to int values

# In[3]:


index_csv_path = pathlib.Path(f"{intermediate_files_dir}/index.csv")
# convert string values to int where possible (ex with well number)
# necessary because pycytominer reads index.csv file with `dtype=str`
original_index_csv = pd.read_csv(original_index_csv_path)
original_index_csv.to_csv(index_csv_path)


# ### Find negative controls for each plate, derive scalers from these negative controls, normalize entire plate with scaler, save normalized plate
# #### Only one plate (`SQ00014617`) is processsed in the jupyter notebook as an example. All other plate processed in `preprocess-features.py` file

# In[4]:


# get list of unique plates
plates = pd.read_csv(index_csv_path)["Metadata_Plate"].unique().tolist()

for plate in plates:
    print(f"Finding negative controls for plate {plate}")
    # create dataframe with normalization population (only negative controls for each plate)
    plate_normalization_index_csv = pathlib.Path(f"{intermediate_files_dir}/{plate}_norm_pop_index.csv")
    norm_index_df = preprocessUtils.get_negative_control_index_df(index_csv_path, annotations_path, plate)
    # save normalization population dataframe so pycytominer knows where to load normalization features from
    norm_index_df.to_csv(plate_normalization_index_csv, index=False)
    
    # create per-plate normalization scaler from the normalization population
    print(f"Deriving scaler for plate {plate}")
    scaler = preprocessUtils.get_normalization_scaler(plate_normalization_index_csv, features_output_dir)
    
    # get compiled normalized plate features
    plate_pop = preprocessUtils.normalize_plate(index_csv_path, scaler, features_output_dir, plate)
    
    # save compiled normalized plate features
    print(f"Saving plate {plate}")
    normalized_features_csv_path = pathlib.Path(f"{output_path}/{plate}_normalized_single_cell.csv.gz")
    plate_pop.to_csv(normalized_features_csv_path, index=False, compression='gzip')

