# from cellpose.io import logger_setup
from cellpose import models, core, io, utils

import pathlib
import pandas as pd

import cv2
import numpy as np

def overlay_channels(current_image: str, current_dir: pathlib.Path) -> np.ndarray:
    """overlays nuclei, ER, and RNA channels to help with CellPose segmentation

    Args:
        current_image (str): string of current field to overlay channels for
        current_dir (pathlib.Path): directory of current field

    Returns:
        np.ndarray: 3 channel image with nuclei, ER, RNA
    """
    # load all channel images
    channel_paths = []
    channel_images = []
    for image_file in current_dir.iterdir():
        if current_image in image_file.name:
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


def get_cytoplasm_locations(
    overlay_image: np.ndarray, cellpose_model: models.Cellpose
) -> pd.DataFrame:
    """finds center X,Y of cytoplasm and saves as tsv file

    Args:
        overlay_image (np.ndarray): overlay image with nuclei and RNA channels
        cellpose_model (models.Cellpose): cellpose model for segmenting nuclei

    Returns:
        pd.DataFrame: dataframe with cytoplasm center coords
    """
    nuclei_data = []

    # use cellpose to get nuclei outlines
    frame_image = overlay_image
    masks, flows, styles, diams = cellpose_model.eval(
        frame_image,
        diameter=0,
        channels=[1, 3],
        flow_threshold=0,
        cellprob_threshold=0.4,
    )
    outlines = utils.outlines_list(masks)

    for outline in outlines:
        centroid = outline.mean(axis=0)
        nucleus_data = {
            "Location_Center_X": centroid[0],
            "Location_Center_Y": centroid[1],
        }
        nuclei_data.append(nucleus_data)

    nuclei_data = pd.DataFrame(nuclei_data)
    return nuclei_data


def get_nuclei_locations(
    DNA_image_path: pathlib.Path, cellpose_model: models.Cellpose
) -> pd.DataFrame:
    """finds center X,Y of nuclei and saves as tsv file

    Args:
        DNA_image_path (pathlib.Path): path to DNA channel image
        cellpose_model (models.Cellpose): cellpose model for segmenting nuclei

    Returns:
        pd.DataFrame: dataframe with nuclei center coords
    """
    nuclei_data = []

    # use cellpose to get nuclei outlines
    frame_image = io.imread(DNA_image_path)
    masks, flows, styles, diams = cellpose_model.eval(
        frame_image, diameter=80, channels=[0, 0], flow_threshold=0
    )
    outlines = utils.outlines_list(masks)

    for outline in outlines:
        centroid = outline.mean(axis=0)
        nucleus_data = {
            "Location_Center_X": centroid[0],
            "Location_Center_Y": centroid[1],
        }
        nuclei_data.append(nucleus_data)

    nuclei_data = pd.DataFrame(nuclei_data)
    return nuclei_data


def segment_cell_health(
    data_path: pathlib.Path,
    save_path: pathlib.Path,
    cellpose_model_DNA: models.Cellpose,
    cellpose_model_cyto: models.Cellpose,
):
    """segments cell health data from data_path and save segmentation data in save_path using cellpose_model

    Args:
        data_path (pathlib.Path): load path for cell health data
        save_path (pathlib.Path): save path for segmentation data
        cellpose_model_DNA (models.Cellpose): cell pose model to use for segmenting DNA
        cellpose_model_actin (models.Cellpose): cell pose model to use for segmentating actin
    """

    for plate_path in data_path.iterdir():
        print(f"Segmenting plate {plate_path.name}")
        for image_folder in plate_path.iterdir():
            for image_file in image_folder.iterdir():
                if ".tiff" in image_file.name:
                    if "-ch1" in image_file.name:
                        # segment nuclei
                        nuc_save_path = str(image_file).replace(
                            "cell-health", "cell-health-segmented"
                        )
                        nuc_save_path = nuc_save_path.replace(".tiff", "-segmented.tsv")
                        nuc_save_path = pathlib.Path(nuc_save_path)

                        if not nuc_save_path.is_file():
                            print(f"Segmenting {nuc_save_path.name}")
                            nuc_save_path.parents[0].mkdir(parents=True, exist_ok=True)
                            nuc_locations = get_nuclei_locations(
                                image_file, cellpose_model_DNA
                            )
                            nuc_locations.to_csv(nuc_save_path, sep="\t")
                        else:
                            print(f"{nuc_save_path.name} already exists!")

                        # segment cytoplasm
                        current_image = nuc_save_path.name.split("-")[0]
                        cyto_save_path = f"{nuc_save_path.parents[0]}/{current_image}-cyto-segmented.tsv"
                        cyto_save_path = pathlib.Path(cyto_save_path)

                        if not cyto_save_path.is_file():
                            print(f"Segmenting {cyto_save_path.name}")
                            overlay_image = overlay_channels(
                                current_image, image_folder
                            )
                            cyto_locations = get_cytoplasm_locations(
                                overlay_image, cellpose_model_cyto
                            )
                            cyto_locations.to_csv(cyto_save_path, sep="\t")
                        else:
                            print(f"{cyto_save_path.name} already exists!")