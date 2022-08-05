#!/usr/bin/env python
# coding: utf-8

# # Cell Health Data Segmentor
# ### Find center coordinates for cells from Cell Health data
# 
# #### Import libraries

# In[1]:


# from cellpose.io import logger_setup
from cellpose import models, core, io, utils

import pathlib
import pandas as pd

import cv2
import numpy as np

import importlib
chs = importlib.import_module("segmentation-utils")


# ### Set Up CellPose

# In[2]:


use_GPU = core.use_gpu()
print(">>> GPU activated? %d" % use_GPU)
# logger_setup();


# ### Segment Cell Health data

# In[3]:


# data_path needs to reflect the location of illumination corrected images after finishing 0.image-download
load_path = pathlib.Path(
    "/media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/cell-health/"
)
# save_path needs to reflect the desired location of the segmentation tsv files
save_path = pathlib.Path(
    "/media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/cell-health-segmented/"
)

nuclei_model_specs = {
    "model_type": "cyto",
    "channels": [0, 0],
    "diameter": 80,
    "flow_threshold": 0,
    "cellprob_threshold": 0,
    "remove_edge_masks": True,
}

cytoplasm_model_specs = {
    "model_type": "cyto",
    "channels": [1, 3],
    "diameter": 0,
    "flow_threshold": 0,
    "cellprob_threshold": 0.4,
    "remove_edge_masks": True,
}

chs.segment_cell_health(load_path, save_path, nuclei_model_specs, cytoplasm_model_specs)

