#!/usr/bin/env python
# coding: utf-8

# ### Import Libraries
# 

# In[1]:


import pathlib
import sys

import pandas as pd

sys.path.append("../")
import classification_utils


# ### Load Cell Health Profile Labels
# 

# In[2]:


cell_health_hash = (
    "30ea5de393eb9cfc10b575582aa9f0f857b44c59"  # hash from Jan 26th, 2022
)
cell_health_labels_link = f"https://raw.github.com/broadinstitute/cell-health/{cell_health_hash}/1.generate-profiles/data/consensus/cell_health_median.tsv.gz"

cell_health_labels = pd.read_csv(cell_health_labels_link, compression="gzip", sep="\t")
cell_health_labels


# ### Create Classification Profiles
# 

# In[3]:


# which cell lines correspond to whice plates (from Cell Health IDR metadata)
# Cell Health IDR link: https://idr.openmicroscopy.org/webclient/?show=screen-2701
cell_line_plates = {
    "A549": ["SQ00014610", "SQ00014611", "SQ00014612"],
    "ES2": ["SQ00014613", "SQ00014614", "SQ00014615"],
    "HCC44": ["SQ00014616", "SQ00014617", "SQ00014618"],
}


# In[4]:


# paths to set (data is loaded from/saved to external hard drive)
base_dir_path = pathlib.Path(
    "/media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/"
)
cell_health_plate_classifications = pathlib.Path(
    f"{base_dir_path}/cell-health-plate-classifications"
)
classification_profiles_save_dir = pathlib.Path(
    f"{base_dir_path}/cell-health-plate-classification-profiles"
)

MCM_classifications = pathlib.Path(
    f"{cell_health_plate_classifications}/multi_class_models"
)
SCM_classifications = pathlib.Path(
    f"{cell_health_plate_classifications}/single_class_models"
)
classification_profiles_save_dir.mkdir(exist_ok=True, parents=True)

# derive multi class model classification profiles
print("Deriving multi class model classification profiles")

# multi class models storage format is base_dir/model_type__feature_type.joblib
for model_classifications_dir in MCM_classifications.iterdir():

    # get information about the current model's classifications we are looking at
    model_type = model_classifications_dir.name.split("__")[0]
    feature_type = model_classifications_dir.name.split("__")[1].replace(".joblib", "")

    print(
        f"Deriving classification profiles for {model_type} model with {feature_type} features"
    )

    # derive classification profiles
    classification_profiles = classification_utils.create_classification_profiles(
        model_classifications_dir, cell_line_plates
    )

    # save classification profiles
    classification_profiles_save_path = pathlib.Path(
        f"{classification_profiles_save_dir}/multi_class_models/{model_classifications_dir.name}__classification_profiles.tsv"
    )
    classification_profiles_save_path.parent.mkdir(exist_ok=True, parents=True)
    classification_profiles.to_csv(
        classification_profiles_save_path, sep="\t", index=False
    )

# derive single class model classification profiles
print("Deriving single class model classification profiles")

# single class models storage format is base_dir/specific_phenotypic_class/model_type__feature_type.joblib
for phenotypic_class_dir in SCM_classifications.iterdir():
    print(f"Deriving classification profiles for {phenotypic_class_dir.name} models")
    for model_classifications_dir in phenotypic_class_dir.iterdir():

        # get information about the current model
        phenotypic_class = phenotypic_class_dir.name.split("_")[0]
        model_type = model_classifications_dir.name.split("__")[0]
        feature_type = model_classifications_dir.name.split("__")[1].replace(
            ".joblib", ""
        )

        print(
            f"Deriving classification profiles for {model_type} model with {feature_type} features"
        )

        # derive classification profiles
        classification_profiles = classification_utils.create_classification_profiles(
            model_classifications_dir, cell_line_plates
        )

        # save classification profiles
        classification_profiles_save_path = pathlib.Path(
            f"{classification_profiles_save_dir}/single_class_models/{phenotypic_class}/{model_classifications_dir.name}__classification_profiles.tsv"
        )
        classification_profiles_save_path.parent.mkdir(exist_ok=True, parents=True)
        classification_profiles.to_csv(
            classification_profiles_save_path, sep="\t", index=False
        )

