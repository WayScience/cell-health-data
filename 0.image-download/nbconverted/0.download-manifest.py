#!/usr/bin/env python
# coding: utf-8

# ## Download the manifest files
# 
# The IDR team curates two metadata files, which includes experimental details and downloadable file paths.
# 
# 1. Experimental details
# 2. Plate info (including file paths)
# 
# This notebook will download the relevant metadata file, and demonstrate how to extract file paths.

# In[1]:


import pathlib
import pandas as pd


# In[2]:


# The metadata files are stored on github
repo = "https://github.com/IDR/idr0080-way-perturbation"
commit = "74e537fecaa4690f0c98cb1e9a64b45d103de3e3"

github_dir = f"{repo}/raw/{commit}/screenA/"
output_dir = "manifest"

metadata_file = "idr0080-screenA-annotation.csv"
plate_file = "idr0080-screenA-plates.tsv"


# In[3]:


# Load metadata file and write to local disk
metadata_df = pd.read_csv(f"{github_dir}/{metadata_file}")

output_file = pathlib.Path(output_dir, metadata_file)
metadata_df.to_csv(output_file, sep=",", index=False)

print(metadata_df.shape)
metadata_df.head(2)


# In[4]:


# Load plate file
plate_df = pd.read_csv(f"{github_dir}/{plate_file}", sep="\t", header=None)

plate_df.columns = ["plate", "manifest_path"]

print(plate_df.shape)
plate_df.head(2)


# According to IDR instructions, only part of the file name is useful
# 
# > After removing the leading /uod/idr/filesets/idrNNN-author-description/, you can then download a subfolder using the same commands as above:

# In[5]:


# Strip this detail from the plate manifest and add as a column
idr_id = "idr0080-way-perturbation"
strip_id = f"/uod/idr/filesets/{idr_id}/"

plate_df = plate_df.assign(download_path = plate_df.manifest_path.str.replace(strip_id, ""))


# In[6]:


# Write to local disk
output_file = pathlib.Path(output_dir, plate_file)
plate_df.to_csv(output_file, sep=",", index=False)

plate_df.head(2)


# In[7]:


plate_df.download_path.tolist()

