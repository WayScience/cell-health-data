from importlib.resources import path

import pandas as pd
from sklearn.preprocessing import StandardScaler

def get_normalization_scaler(plate_merged_single_cells: pd.DataFrame) -> StandardScaler:
    """
    get normalization scaler from single cell dataframe

    Parameters
    ----------
    plate_merged_single_cells : pd.DataFrame
        dataframe with all single cells from plate

    Returns
    -------
    StandardScaler
        normalization scaler for merged feature cells
    """
    
    # find all cells that have had no reagent applied
    negative_control_single_cells = plate_merged_single_cells.loc[plate_merged_single_cells['Metadata_Reagent'] == "ARID1B-2"] # CHANGE TO "no-reagent"
    # get features for these negative control cells
    feature_cols = [col for col in negative_control_single_cells.columns.to_list() if "P__" in col]
    negative_control_feature_data = negative_control_single_cells[feature_cols].values
    # fit normalization scaler
    plate_scaler = StandardScaler()
    plate_scaler.fit(negative_control_feature_data)
    
    return plate_scaler