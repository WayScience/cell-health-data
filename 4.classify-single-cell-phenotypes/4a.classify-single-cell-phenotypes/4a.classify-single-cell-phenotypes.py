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
import sys
import gc

import pandas as pd
import numpy as np

sys.path.append("../")
import classification_utils


# ### Define hard drive path and classifications output path
# 

# In[2]:


# external paths to normalized data and classifications
normalized_plates_path = pathlib.Path(
    "/media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/cell-health-nuc-merged-normalized"
)

classifications_save_path = pathlib.Path(
    "/media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/new-cell-health-plate-classifications"
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


from typing import Literal
from sklearn.linear_model import LogisticRegression


def get_probas_dataframe(
    plate_features: pd.DataFrame,
    model: LogisticRegression,
    feature_type: Literal["CP", "DP", "CP_and_DP", "CP_areashape_only", "CP_zernike_only"],
) -> pd.DataFrame:
    """
    Get probabilities for plate features from a phenotypic classification model

    Parameters
    ----------
    plate_features : pd.DataFrame
        plate features to classify
    model : LogisticRegression
        model to use for plate feature classification
    feature_type : str
        type of features to use for classification.
        CP, DP, CP_and_DP, CP_areashape_only, CP_zernike_only

    Returns
    -------
    pd.DataFrame
        dataframe with single-cell probabilities for classes from given model
    """
    
    all_cols = plate_features.columns.to_list()

    # determine which feature columns should be loaded depending on feature type
    if "CP" in feature_type:
        feature_cols = [col for col in all_cols if "CP__" in col]
        if "zernike_only" in feature_type:
            feature_cols = [col for col in feature_cols if "Zernike" in col]
        if "areashape_only" in feature_type:
            feature_cols = [col for col in feature_cols if "AreaShape" in col]
        if "_and_DP" in feature_type:
            feature_cols = [col for col in all_cols if "P__" in col]
    elif  "DP" in feature_type:
        feature_cols = [col for col in all_cols if "DP__" in col]

    # load these particular features and get the values
    single_cell_features = plate_features[feature_cols].values

    # get and return the predicted probabilities
    probas_dataframe = pd.DataFrame(
        model.predict_proba(single_cell_features),
        columns=model.classes_,
    ).reset_index(drop=True)

    return probas_dataframe


# In[4]:

good_plates = [
    "SQ00014610", "SQ00014611", "SQ00014612",
    "SQ00014614", "SQ00014615", "SQ00014616", "SQ00014618"
]
# iterate through plates so each plate data only needs to be loaded once
for normalized_plate_path in normalized_plates_path.iterdir():

    # get plate name from normalized data path
    plate = normalized_plate_path.name.split("-")[0]
    if plate in good_plates:
        continue
    print(f"Getting phenotypic_class_probabilities for plate {plate}...")

    # determine what type columns are
    all_cols = pd.read_csv(normalized_plate_path, nrows=1).columns.to_list()
    feature_cols = [col for col in all_cols if "P__" in col]
    metadata_cols = [col for col in all_cols if "P__" not in col]

    print("Loading plate feature data...")
    # load features
    col_types = {col: np.float32 for col in feature_cols}
    plate_features = pd.read_csv(
        normalized_plate_path, low_memory=True, usecols=feature_cols,
    )
    
    # load metadata
    print("Loading plate metadata...")
    col_types = {col: str for col in metadata_cols}
    plate_metadata = pd.read_csv(
        normalized_plate_path, low_memory=True, usecols=metadata_cols,
    )

    print("Getting multi-class model classifications...")
    for model_path in sorted(multi_class_models_dir.iterdir()):
        
        if "CP_areashape_only__balanced" not in model_path.name:
            continue
        print(model_path)

        # load current model
        model = joblib.load(model_path)

        # get information about the current model
        model_type = model_path.name.split("__")[0]
        feature_type = model_path.name.split("__")[1].replace(".joblib", "")

        # get phenotypic class probabilities for the given plate features
        plate_probas = get_probas_dataframe(
            plate_features, model, feature_type
        )

        # save plate probas with metadata
        save_dir_name = model_path.name.replace(".joblib", "")
        model_plate_probas_save_path = pathlib.Path(
            f"{classifications_save_path}/multi_class_models/{save_dir_name}/{plate}__cell_classifications.csv.gz"
        )
        model_plate_probas_save_path.parent.mkdir(exist_ok=True, parents=True)
        pd.concat([plate_metadata, plate_probas], axis=1).to_csv(
            model_plate_probas_save_path, compression="gzip"
        )
        
        del plate_probas
        gc.collect()
    
    del plate_features
    del plate_metadata
    gc.collect()


# In[ ]:


# print("Getting single-class model classifications...")
# for phenotypic_class_models_path in sorted(single_class_models_dir.iterdir()):
#     for model_path in sorted(phenotypic_class_models_path.iterdir()):

#         # load current model
#         model = joblib.load(model_path)

#         # get information about the current model
#         phenotypic_class = phenotypic_class_models_path.name.split("_")[0]
#         model_type = model_path.name.split("__")[0]
#         feature_type = model_path.name.split("__")[1].replace(".joblib", "")

#         # get phenotypic class probabilities for the given plate features
#         plate_probas = classification_utils.get_probas_dataframe(
#             plate_features, model, feature_type
#         )

#         # save plate probas with metadata
#         model_plate_probas_save_path = pathlib.Path(
#             f"{classifications_save_path}/single_class_models/{phenotypic_class}_models/{model_type}__{feature_type}/{plate}__cell_classifications.csv.gz"
#         )
#         model_plate_probas_save_path.parent.mkdir(exist_ok=True, parents=True)
#         pd.concat([plate_metadata, plate_probas], axis=1).to_csv(
#             model_plate_probas_save_path, compression="gzip", index=False
#         )

