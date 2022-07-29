# from cellpose.io import logger_setup
from typing import Tuple
from cellpose import models, core, io, utils

import pathlib
import pandas as pd

import cv2
import numpy as np

import matplotlib.path as mplPath

def get_object_outlines(image: np.ndarray, model_specs: dict) -> pd.DataFrame:
    """finds outlines of objects using specs from model_specs and return pandas array with outlines of objects

    Args:
        image (np.ndarray): image with objects to segment
        model_specs (dict): specifications for cellpose segmentation

    Returns:
        pd.DataFrame: dataframe with object outlines
    """
    objects_data = []

    cellpose_model = models.Cellpose(gpu=True, model_type=model_specs["model_type"])
    masks, flows, styles, diams = cellpose_model.eval(
        image,
        diameter=model_specs["diameter"],
        channels=model_specs["channels"],
        flow_threshold=model_specs["flow_threshold"],
        cellprob_threshold=model_specs["cellprob_threshold"],
    )
    # remove cell masks if they are on the edge
    if model_specs["remove_edge_masks"]:
        masks = utils.remove_edge_masks(masks)
    
    outlines = utils.outlines_list(masks)
    for outline in outlines:
        object_data = {
            "Outline": outline,
        }
        objects_data.append(object_data)

    objects_data = pd.DataFrame(objects_data)
    return objects_data

def get_object_locations(image: np.ndarray, model_specs: dict) -> pd.DataFrame:
    """finds center X,Y of objects using specs from model_specs and return pandas array with center X,Y of objects

    Args:
        image (np.ndarray): image with objects to segment
        model_specs (dict): specifications for cellpose segmentation

    Returns:
        pd.DataFrame: dataframe with object center coords
    """
    objects_data = []

    cellpose_model = models.Cellpose(gpu=True, model_type=model_specs["model_type"])
    masks, flows, styles, diams = cellpose_model.eval(
        image,
        diameter=model_specs["diameter"],
        channels=model_specs["channels"],
        flow_threshold=model_specs["flow_threshold"],
        cellprob_threshold=model_specs["cellprob_threshold"],
    )
    # remove cell masks if they are on the edge
    if model_specs["remove_edge_masks"]:
        masks = utils.remove_edge_masks(masks)
    
    outlines = utils.outlines_list(masks)
    for outline in outlines:
        centroid = outline.mean(axis=0)
        object_data = {
            "Location_Center_X": centroid[0],
            "Location_Center_Y": centroid[1],
        }
        objects_data.append(object_data)

    objects_data = pd.DataFrame(objects_data)
    return objects_data


def overlay_channels(identifier: str, current_dir: pathlib.Path) -> np.ndarray:
    """overlays nuclei, ER, and RNA channels to help with CellPose segmentation

    Args:
        identifier (str): string of current field to overlay channels for
        current_dir (pathlib.Path): directory of current field

    Returns:
        np.ndarray: 3 channel image with nuclei, ER, RNA
    """
    # load all channel images
    channel_paths = []
    channel_images = []
    for image_file in current_dir.iterdir():
        if identifier in image_file.name:
            channel_paths.append(image_file)
    channel_paths = sorted(channel_paths)
    for channel_path in channel_paths:
        channel_image = np.array(cv2.imread(str(channel_path), 0))
        channel_images.append(channel_image)

    # channel multipliers are only useful for human interpretation of the overlayed images
    # channel brightness is irrelevant to CellPose segmentation
    # channel images 1,2,3 are DNA, ER, RNA respectively
    overlay = np.dstack(
        [channel_images[0] * 2, channel_images[1] * 1, channel_images[2] * 5]
    ).astype(np.uint8)

    return overlay


def get_nuc_cyto_data(nuc_locations: pd.DataFrame, cyto_outlines: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """produces nuclei and cytoplasm dataframes with corresponding cell IDs from nuclei locations and cytoplasm outlines

    Args:
        nuc_locations (pd.DataFrame): dataframe with nuclei center coords for certain image
        cyto_outlines (pd.DataFrame): dataframe with cytoplasm outline for same image as above

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: nuc_data and cyto_data with corresponding cell IDs and center coords for each object
    """
    nuc_data = []
    cyto_data = []
    
    # add Cell_ID column, each ID corresponds to index of outline entry
    cyto_outlines = cyto_outlines.reset_index()
    cyto_outlines = cyto_outlines.rename(columns={'index':'Cell_ID'})
    
    # iterate over all cytoplasm outlines
    for cyto_index, cyto_row in cyto_outlines.iterrows():
        cell_id = cyto_row["Cell_ID"]
        
        # create path (polygon) from outline to check if the nuclei are in this path
        outline = cyto_row["Outline"]
        cytoplasm_path = mplPath.Path(outline)
        # check if any of the nuclei are within cytoplasm path
        for nuc_index, nuc_row in nuc_locations.iterrows():
            nuc_center = (nuc_row["Location_Center_X"], nuc_row["Location_Center_Y"])
            # if nuclei is in cytoplasm path give it same cell ID as cytoplasm
            if cytoplasm_path.contains_point(nuc_center):
                current_nuc_data = {
                    "Cell_ID": cell_id,
                    "Location_Center_X": nuc_row["Location_Center_X"],
                    "Location_Center_Y": nuc_row["Location_Center_Y"],
                }
                nuc_data.append(current_nuc_data)
                
                # convert cytoplasm outline to center coords
                centroid = cyto_row["Outline"].mean(axis=0)
                current_cyto_data = {
                    "Cell_ID": cell_id,
                    "Location_Center_X": centroid[0],
                    "Location_Center_Y": centroid[1],
                    "Outline": cyto_row["Outline"].tolist(),
                }
                cyto_data.append(current_cyto_data)
    
    
    nuc_data = pd.DataFrame.from_dict(nuc_data)
    cyto_data = pd.DataFrame.from_dict(cyto_data)
    # drop duplicates because cytoplasm gets added multiple times if it has many nuclei in it
    cyto_data = cyto_data.drop_duplicates(subset="Cell_ID")
    
    return nuc_data, cyto_data

def segment_cell_health(
    data_path: pathlib.Path,
    save_path: pathlib.Path,
    nuclei_model_specs: dict,
    cytoplasm_model_specs: dict,
):
    """segments cell health data from data_path and save segmentation data in save_path using cellpose_model

    Args:
        data_path (pathlib.Path): load path for cell health data
        save_path (pathlib.Path): save path for segmentation data
        nuclei_model_specs (dict): specs for cellpose model to segment nuclei
        cytoplasm_model_specs (dict): specs for cellpose model to segment cytoplasm
    """

    for plate_path in data_path.iterdir():
        print(f"Segmenting plate {plate_path.name}")
        for image_folder in plate_path.iterdir():
            for image_file in image_folder.iterdir():
                if ".tiff" in image_file.name:
                    if "-ch1" in image_file.name:
                        # segment nuclei
                        nuc_save_path = f"{save_path}/{plate_path.name}/{image_folder.name}/{image_file.name}"
                        channel_metadata = image_file.name.split("-")[1]
                        nuc_save_path = nuc_save_path.replace(channel_metadata, "nuc-segmented.tsv")
                        nuc_save_path = pathlib.Path(nuc_save_path)

                        if not nuc_save_path.is_file():
                            print(f"Segmenting {nuc_save_path.name}")
                            nuc_save_path.parents[0].mkdir(parents=True, exist_ok=True)
                            nuclei_image = io.imread(image_file)
                            nuc_locations = get_object_locations(
                                nuclei_image, nuclei_model_specs
                            )
                            
                            # segment cytoplasm
                            identifier = nuc_save_path.name.split("-")[0]
                            cyto_save_path = f"{nuc_save_path.parents[0]}/{identifier}-cyto-segmented.tsv"
                            cyto_save_path = pathlib.Path(cyto_save_path)

                            print(f"Segmenting {cyto_save_path.name}")
                            overlay_image = overlay_channels(
                                identifier, image_folder
                            )
                            cyto_outlines = get_object_outlines(overlay_image, cytoplasm_model_specs)
                            
                            nuc_data, cyto_data = get_nuc_cyto_data(nuc_locations, cyto_outlines)
                            nuc_data.to_csv(nuc_save_path, sep="\t", index=False)
                            cyto_data.to_csv(cyto_save_path, sep="\t", index=False)
                            
                        else:
                            identifier = nuc_save_path.name.split("-")[0]
                            print(f"{identifier} has already been segmented!")
                            
                            