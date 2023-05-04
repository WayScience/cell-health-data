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

# set nuclei specifications
nuclei_model_specs = {
    "model_type": "cyto",
    "channels": [0, 0],
    "diameter": 80,
    "flow_threshold": 0,
    "cellprob_threshold": 0,
    "remove_edge_masks": True,
}

# set cytoplasm spcecifications
# although we do not perform cytoplasm segmentation here (yet),
# these are the specs we found produce the best cytoplasm segmentation on an image overlayed with segmenation-utils.overlay_channels()
cytoplasm_model_specs = {
    "model_type": "cyto",
    "channels": [1, 3],
    "diameter": 0,
    "flow_threshold": 0,
    "cellprob_threshold": 0.4,
    "remove_edge_masks": True,
}

cellpose_model = models.Cellpose(gpu=use_GPU, model_type=nuclei_model_specs["model_type"])

# iterate through plates in load path
for plate_path in load_path.iterdir():
        print(f"Segmenting plate {plate_path.name}")
        
        # iterate through image paths in plates (there should only be one)
        for image_folder_path in plate_path.iterdir():
            
            # create image folder that all segmentations will be saved in
            image_folder_save_path = pathlib.Path(f"{save_path}/{plate_path.name}/{image_folder_path.name}/")
            image_folder_save_path.mkdir(parents=True, exist_ok=True)
            
            # iterate through cell painting images in image folder
            for image_path in image_folder_path.iterdir():
                # skip images that are not channel 1 (DAPI, nuclei) images
                if (".tiff" not in image_path.name) or ("-ch1" not in image_path.name):
                    continue
                
                # get image ID with metadata about row, col, field
                image_ID = image_path.name.split("-")[0]
                # get save paths for masks and locations (center x, y) data
                nuc_masks_save_path = pathlib.Path(f"{image_folder_save_path}/{image_ID}-nuc-masks.tiff")
                nuc_locations_save_path = pathlib.Path(f"{image_folder_save_path}/{image_ID}-nuc-locations.tsv")

                # skip images that have already been segmented
                if nuc_masks_save_path.is_file() and nuc_locations_save_path.is_file():
                    print(f"Already segmented {image_path.name}")
                    continue
                
                print(f"Segmenting {image_path.name}")
                
                # get masks for image
                # masks are in image format, with a specific integer number coresponding to the mask for a particular cell
                nuclei_image = io.imread(image_path)
                masks, flows, style, diam = cellpose_model.eval(
                    nuclei_image,
                    diameter=nuclei_model_specs["diameter"],
                    channels=nuclei_model_specs["channels"],
                    flow_threshold=nuclei_model_specs["flow_threshold"],
                    cellprob_threshold=nuclei_model_specs["cellprob_threshold"],
                )
                masks = utils.remove_edge_masks(masks)
                
                # save masks
                io.imsave(nuc_masks_save_path, masks)
                
                # get center x,y data from masks
                outlines = utils.outlines_list(masks)
                objects_data = []
                for outline in outlines:
                    centroid = outline.mean(axis=0)
                    object_data = {
                        "Location_Center_X": centroid[0],
                        "Location_Center_Y": centroid[1],
                    }
                    objects_data.append(object_data)

                # compile and save locations data
                objects_data = pd.DataFrame(objects_data)
                objects_data.to_csv(nuc_locations_save_path, sep="\t", index=False)
                
print("All segmenting done!")

