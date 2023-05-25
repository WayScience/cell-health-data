#!/usr/bin/env python
# coding: utf-8

# ### Import Libraries
# 

# In[1]:


import pathlib
import joblib
import importlib

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from pycytominer.cyto_utils import DeepProfiler_processing

normalization_utils = importlib.import_module("normalization-utils")


# ### Set Load/Save Paths
# 

# In[2]:


# paths to load merged features,index, and annotations from
merged_features_save_path = pathlib.Path(
    "/media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/cell-health-nuc-merged/"
)
dp_index_path = pathlib.Path(
    "/media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/cell-health-nuc-DP/inputs/metadata/index.csv"
)
annotations_path = pathlib.Path(
    "../0.image-download/manifest/idr0080-screenA-annotation.csv"
)

# path to save normalized merged features to
normalized_merged_features_save_path = pathlib.Path(
    "/media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/cell-health-nuc-merged-normalized/"
)
normalized_merged_features_save_path.mkdir(parents=True, exist_ok=True)
scaler_save_dir = pathlib.Path("normalization-scalers/")
scaler_save_dir.mkdir(parents=True, exist_ok=True)


# ### Normalize merged single-cell data
# 

# In[3]:


for merged_single_cell_plate_path in merged_features_save_path.iterdir():
    # get only plate name from merged features file name
    plate = merged_single_cell_plate_path.name.split("-")[0]
    print(f"Normalizing plate {plate}...")

    # load in one row to create datatypes dictionary for faster loading
    first_row_data = pd.read_csv(
        merged_single_cell_plate_path, compression="gzip", nrows=1
    )
    metadata_cols = [col for col in first_row_data.columns if "P__" not in col]
    feature_cols = [col for col in first_row_data.columns if "P__" in col]

    # specify datatypes for metadata/feature columns
    metadata_dtypes = {metadata_col: str for metadata_col in metadata_cols}
    feature_dtypes = {feature_col: np.float32 for feature_col in feature_cols}
    # combine both dictionaries
    plate_dtypes = {**metadata_dtypes, **feature_dtypes}

    # load plate single-cell data
    print(f"Loading single-cell data...")
    plate_merged_single_cells = pd.read_csv(
        merged_single_cell_plate_path,
        compression="gzip",
        dtype=plate_dtypes,
        low_memory=True,
    )

    # create per-plate normalization scaler from the normalization population
    print(f"Deriving normalization scaler...")
    plate_scaler = normalization_utils.get_normalization_scaler(
        plate_merged_single_cells
    )
    # save normalization scaler
    scaler_save_path = pathlib.Path(
        f"{scaler_save_dir}/{plate}-merged-normalization-scaler.joblib"
    )
    joblib.dump(plate_scaler, scaler_save_path)

    # apply scaler to all single cell feature data
    print(f"Applying normalization scaler...")
    # get normalized feature data
    feature_cols = [
        col for col in plate_merged_single_cells.columns.to_list() if "P__" in col
    ]
    features = plate_merged_single_cells[feature_cols].values
    features = plate_scaler.transform(features)
    features = pd.DataFrame(features, columns=feature_cols)
    # get metadata for all single cells
    metadata_cols = [
        col for col in plate_merged_single_cells.columns.to_list() if "P__" not in col
    ]
    metadata = plate_merged_single_cells[metadata_cols]

    # combine metadata and normalized features for all single cells (replace other single cell dataframe to not keep two dfs in memory)
    plate_merged_single_cells = pd.concat([metadata, features], axis=1)

    # compress and save merged single-cell data
    print(f"Saving normalized features...")
    normalized_merged_plate_single_cells_save_path = pathlib.Path(
        f"{normalized_merged_features_save_path}/{plate}-normalized-merged-single-cell.csv.gz"
    )
    plate_merged_single_cells.to_csv(
        normalized_merged_plate_single_cells_save_path, compression="gzip", index=False
    )

