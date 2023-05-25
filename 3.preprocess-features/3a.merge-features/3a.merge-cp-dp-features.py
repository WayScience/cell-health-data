#!/usr/bin/env python
# coding: utf-8

# ### Import Libraries
# 

# In[1]:


import pathlib
import math
import uuid
import importlib
import itertools

import pandas as pd
from pycytominer.cyto_utils import DeepProfiler_processing

merge_utils = importlib.import_module("merge-utils")


# ### Set Load/Save Paths
# 

# In[2]:


# paths to load features/index from
cp_features_save_path = pathlib.Path(
    "/media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/cell-health-nuc-CP/"
)
dp_features_save_path = pathlib.Path(
    "/media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/cell-health-nuc-DP/outputs/efn_pretrained/features"
)
dp_index_path = pathlib.Path(
    "/media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/cell-health-nuc-DP/inputs/metadata/index.csv"
)

# path to save merged features to
merged_features_save_path = pathlib.Path(
    "/media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/cell-health-nuc-merged/"
)
merged_features_save_path.mkdir(parents=True, exist_ok=True)


# ### Merge Features
# 

# In[3]:


for cp_output_path in cp_features_save_path.iterdir():
    plate = cp_output_path.name
    print(f"Merging plate {plate} ...")

    # list where all merged image data will compiled
    merged_plate_single_cells = []

    # load single cell dataframe for CP data
    print("Loading CP features...")
    cp_plate_single_cells = merge_utils.load_cp_feature_data(cp_output_path, plate)

    # load single cell dataframe for DP data
    print("Loading DP features...")
    deep_data = DeepProfiler_processing.DeepProfilerData(
        dp_index_path, dp_features_save_path, filename_delimiter="/"
    )
    # get dp index for plate we are interested in
    deep_data.index_df = deep_data.index_df.loc[
        deep_data.index_df["Metadata_Plate"] == plate
    ]
    # convert site to int (instead of string beginning with 0) so DeepProfiler_processing can find output
    deep_data.index_df["Metadata_Site"] = pd.to_numeric(
        deep_data.index_df["Metadata_Site"]
    )
    deep_single_cell = DeepProfiler_processing.SingleCellDeepProfiler(deep_data)
    dp_plate_single_cells = deep_single_cell.get_single_cells(output=True)

    # iterate through each image in the plate (unique image for each plate, well, site combination)
    print("Merging features...")
    wells = dp_plate_single_cells["Metadata_Well"].unique()
    sites = dp_plate_single_cells["Metadata_Site"].unique()

    for well, site in itertools.product(wells, sites):

        # find single cell data for the well, site combination
        cp_image_single_cells = cp_plate_single_cells.loc[
            (cp_plate_single_cells["Metadata_Well"] == well)
            & (cp_plate_single_cells["Metadata_Site"] == site)
        ]
        dp_image_single_cells = dp_plate_single_cells.loc[
            (dp_plate_single_cells["Metadata_Well"] == well)
            & (dp_plate_single_cells["Metadata_Site"] == site)
        ]

        # get the merged single-cell image data and add this to the merged plate data
        merged_image_data = merge_utils.merge_CP_DP_image_data(
            cp_image_single_cells, dp_image_single_cells
        )
        merged_plate_single_cells.append(merged_image_data)

    # combine all merged image data into one dataframe for the entire plate
    merged_plate_single_cells = pd.concat(merged_plate_single_cells).reset_index(
        drop=True
    )

    # compress and save merged single-cell data
    print(f"Saving merged features...")
    merged_plate_single_cells_save_path = pathlib.Path(
        f"{merged_features_save_path}/{plate}-merged-single-cell.csv.gz"
    )
    merged_plate_single_cells.to_csv(
        merged_plate_single_cells_save_path, compression="gzip", index=False
    )

