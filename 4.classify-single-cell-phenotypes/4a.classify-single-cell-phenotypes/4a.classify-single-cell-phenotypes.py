#!/usr/bin/env python
# coding: utf-8

# # Classify Cell Health Nuclei Features
# 
# ### Import libraries
# 

# In[1]:


import pathlib
import urllib.request
import joblib
import importlib

import pandas as pd
import numpy as np

classification_utils = importlib.import_module("../classification-utils")


# ### Define hard drive path and classifications output path
# 

# In[2]:


# external paths to normalized data and classifications
normalized_plates_path = pathlib.Path(
    "/media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/cell-health-nuc-merged-normalized"
)

classifications_save_path = pathlib.Path(
    "/media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/cell-health-plate-classifications"
)
classifications_save_path.mkdir(exist_ok=True, parents=True)

# path to multi-class and single-class models
multi_class_models_dir = pathlib.Path(
    "phenotypic_profiling_model/2.train_model/models/multi_class_models"
)
single_class_models_dir = pathlib.Path(
    "phenotypic_profiling_model/2.train_model/models/single_class_models"
)


# ### Derive and save phenotypic class probabilities
# 

# In[3]:


# iterate through plates so each plate data only needs to be loaded once
for normalized_plate_path in normalized_plates_path.iterdir():

    # get plate name from normalized data path
    plate = normalized_plate_path.name.split("-")[0]
    print(f"Getting phenotypic_class_probabilities for plate {plate}...")

    # determine what type columns are
    all_cols = pd.read_csv(normalized_plate_path, nrows=1).columns.to_list()
    feature_cols = [col for col in all_cols if "P__" in col]
    metadata_cols = [col for col in all_cols if "P__" not in col]

    print("Loading plate feature data...")
    # load features
    col_types = {col: np.float32 for col in feature_cols}
    plate_features = pd.read_csv(
        normalized_plate_path, low_memory=True, usecols=feature_cols
    )
    # load metadata
    print("Loading plate metadata...")
    col_types = {col: str for col in metadata_cols}
    plate_metadata = pd.read_csv(
        normalized_plate_path, low_memory=True, usecols=metadata_cols
    )

    print("Getting multi-class model classifications...")
    for model_path in sorted(multi_class_models_dir.iterdir()):

        # load current model
        model = joblib.load(model_path)

        # get information about the current model
        model_type = model_path.name.split("__")[0]
        feature_type = model_path.name.split("__")[1].replace(".joblib", "")

        # get phenotypic class probabilities for the given plate features
        plate_probas = classification_utils.get_probas_dataframe(
            plate_features, model, feature_type
        )

        # save plate probas with metadata
        model_plate_probas_save_path = pathlib.Path(
            f"{classifications_save_path}/multi_class_models/{model_type}__{feature_type}/{plate}__cell_classifications.csv.gz"
        )
        model_plate_probas_save_path.parent.mkdir(exist_ok=True, parents=True)
        pd.concat([plate_metadata, plate_probas], axis=1).to_csv(
            model_plate_probas_save_path, compression="gzip"
        )

    print("Getting single-class model classifications...")
    for phenotypic_class_models_path in sorted(single_class_models_dir.iterdir()):
        for model_path in sorted(phenotypic_class_models_path.iterdir()):

            # load current model
            model = joblib.load(model_path)

            # get information about the current model
            phenotypic_class = phenotypic_class_models_path.name.split("_")[0]
            model_type = model_path.name.split("__")[0]
            feature_type = model_path.name.split("__")[1].replace(".joblib", "")

            # get phenotypic class probabilities for the given plate features
            plate_probas = classification_utils.get_probas_dataframe(
                plate_features, model, feature_type
            )

            # save plate probas with metadata
            model_plate_probas_save_path = pathlib.Path(
                f"{classifications_save_path}/single_class_models/{phenotypic_class}_models/{model_type}__{feature_type}/{plate}__cell_classifications.csv.gz"
            )
            model_plate_probas_save_path.parent.mkdir(exist_ok=True, parents=True)
            pd.concat([plate_metadata, plate_probas], axis=1).to_csv(
                model_plate_probas_save_path, compression="gzip", index=False
            )

