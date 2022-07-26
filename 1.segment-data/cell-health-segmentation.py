# from cellpose.io import logger_setup
from cellpose import models, core, io, utils

import pathlib
import pandas as pd

import cv2
import numpy as np

def get_object_outlines(image: np.ndarray, model_specs: dict) -> pd.DataFrame:
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
        [channel_images[0] * 2, channel_images[1] * 0, channel_images[2] * 5]
    ).astype(np.uint8)

    return overlay


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
                        nuc_save_path = nuc_save_path.replace(".tiff", "-segmented.tsv")
                        nuc_save_path = pathlib.Path(nuc_save_path)

                        if not nuc_save_path.is_file():
                            print(f"Segmenting {nuc_save_path.name}")
                            nuc_save_path.parents[0].mkdir(parents=True, exist_ok=True)
                            nuclei_image = io.imread(image_file)
                            nuc_locations = get_object_locations(
                                nuclei_image, nuclei_model_specs
                            )
                            nuc_locations.to_csv(nuc_save_path, sep="\t")
                        else:
                            print(f"{nuc_save_path.name} already exists!")

                        # segment cytoplasm
                        identifier = nuc_save_path.name.split("-")[0]
                        cyto_save_path = f"{nuc_save_path.parents[0]}/{identifier}-cyto-segmented.tsv"
                        cyto_save_path = pathlib.Path(cyto_save_path)

                        if not cyto_save_path.is_file():
                            print(f"Segmenting {cyto_save_path.name}")
                            overlay_image = overlay_channels(
                                identifier, image_folder
                            )
                            cyto_locations = get_object_locations(
                                overlay_image, cytoplasm_model_specs
                            )
                            cyto_locations.to_csv(cyto_save_path, sep="\t")
                        else:
                            print(f"{cyto_save_path.name} already exists!")
