#!/usr/bin/env python
# coding: utf-8

# # Compile DeepProfiler Project
# 
# ### Import libraries

# In[1]:


import pathlib
import pandas as pd

import importlib
DPutils = importlib.import_module("DP-project-utils")


# ### Define project path for DP projects

# In[2]:


nuc_project_path = pathlib.Path("/media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/cell-health-nuc-DP/")
cyto_project_path = pathlib.Path("/media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/cell-health-cyto-DP/")


# ### Compile nucleus DP project

# In[3]:


checkpoint_name = "efficientnet-b0_weights_tf_dim_ordering_tf_kernels_autoaugment.h5"
annotations_path = pathlib.Path("idr0080-screenA-annotation.csv")
images_load_path = pathlib.Path("/media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/cell-health/")

DPutils.compile_project(nuc_project_path, checkpoint_name, annotations_path, images_load_path, "nuc")


# ### Compile cytoplasm DP project

# In[4]:


checkpoint_name = "efficientnet-b0_weights_tf_dim_ordering_tf_kernels_autoaugment.h5"
annotations_path = pathlib.Path("../0.image-download/manifest/idr0080-screenA-annotation.csv")
images_load_path = pathlib.Path("/media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/cell-health/")

DPutils.compile_project(cyto_project_path, checkpoint_name, annotations_path, images_load_path, "cyto")

