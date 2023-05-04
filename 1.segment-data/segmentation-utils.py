# from cellpose.io import logger_setup
from typing import Tuple
from cellpose import models, core, io, utils

import pathlib
import pandas as pd

import cv2
import numpy as np

import matplotlib.path as mplPath

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
