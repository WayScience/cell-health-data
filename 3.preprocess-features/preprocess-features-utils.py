from genericpath import isfile
from importlib.resources import path
import pathlib
import pandas as pd
import numpy as np
import pigz_python
import os

from pycytominer.cyto_utils import DeepProfiler_processing
from sklearn.preprocessing import StandardScaler

def get_negative_control_index_df(index_df_path: pathlib.Path, annotations_path: pathlib.Path, plate: str) -> pd.DataFrame:
    """
    create new df with only negative control images from original index df

    Parameters
    ----------
    index_df_path : pathlib.Path
        path to original index df used for DeepProfiler project
    annotations_path : pathlib.Path
        path to annotation metadata curated by IDR

    Returns
    -------
    pd.DataFrame
        new index df that only contains negative control images
    """
    # get index dataframe for the specified plate
    index_df = pd.read_csv(index_df_path, dtype=str, index_col=0)
    index_df = index_df[index_df["Metadata_Plate"] == plate]
    
    annotations = pd.read_csv(annotations_path)
    
    new_index_df = []
    
    # go through each row in orginal index df
    for index, row in index_df.iterrows():
        plate = row["Metadata_Plate"]
        well = row["Metadata_Well"]
        # if the image at row of original index df is a negative control, add it to new index df
        image_annotations = annotations.loc[
                    (plate == annotations["Plate"]) & (annotations["Well"] == well)
                ]
        control_type = image_annotations.iloc[0]["Control Type"]
        if control_type == "negative":
            new_index_df.append(row)
        
    return pd.DataFrame(new_index_df)

def get_normalization_scaler(norm_pop_index_df_path: pathlib.Path, features_output_dir: pathlib.Path) -> StandardScaler:
    """
    gets normalization scaler from index df

    Parameters
    ----------
    norm_pop_index_df_path : pathlib.Path
        path to index df to use as normalization population
    features_output_dir : pathlib.Path
        path to DeepProfiler features output directory

    Returns
    -------
    StandardScaler
        normalization scaler computed from normalization population
    """
    # load single cell dataframe for normalization population with PyCytominer
    deep_data = DeepProfiler_processing.DeepProfilerData(norm_pop_index_df_path, features_output_dir, filename_delimiter="/")
    deep_single_cell = DeepProfiler_processing.SingleCellDeepProfiler(deep_data)
    norm_pop = deep_single_cell.get_single_cells(output=True)
    
    # derive numpy array of features to use to create scaler
    derived_features = [col_name for col_name in norm_pop.columns.tolist() if "efficientnet" in col_name]
    features_arr = norm_pop[derived_features].to_numpy()
    
    # fit scaler to normalization population
    scaler = StandardScaler()
    scaler.fit(features_arr)
    
    return scaler


def normalize_plate(index_df_path: pathlib.Path, scaler: StandardScaler, features_output_dir: pathlib.Path, plate: str):
    """
    normalize features of DeepProfiler project by plate and save these normalized features in save_dir

    Parameters
    ----------
    index_df_path : pathlib.Path
        path to index df used in DeepProfiler project
    scaler : StandardScaler
        scaler to use for normalization
    features_output_dir : pathlib.Path
        path to DeepProfiler features output directory
    plate : str
        plate to normalize
    """
    
    print(f"Compiling plate {plate}")
    # get single cell dataframe for specific plate
    deep_data = DeepProfiler_processing.DeepProfilerData(index_df_path, features_output_dir, filename_delimiter="/")
    deep_data.index_df = deep_data.index_df.loc[deep_data.index_df['Metadata_Plate'] == plate]
    deep_single_cell = DeepProfiler_processing.SingleCellDeepProfiler(deep_data)
    plate_pop = deep_single_cell.get_single_cells(output=True, location_x_col_index = 1, location_y_col_index = 2)
    
    print(f"Normalizing plate {plate}")
    # transform features of plate with normalization scaler
    col_list = plate_pop.columns.tolist()
    derived_features = [col_name for col_name in col_list if "efficientnet" in col_name]
    features = plate_pop[derived_features].to_numpy()
    features = scaler.transform(features)
    features = pd.DataFrame(features, columns=derived_features)
    
    # replace original features of plate with normalized features
    metadata = [col_name for col_name in col_list if "efficientnet" not in col_name]
    metadata = plate_pop[metadata]
    plate_pop = pd.concat([metadata, features], axis=1)
    
    return plate_pop
    
