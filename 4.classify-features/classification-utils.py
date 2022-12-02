import pathlib
import numpy as np
import pandas as pd

def classify_plate_cells(classifier, plate_load_path: pathlib.Path):
    """
    get class probabilities for features in a plate, averaged across reagent perturbation

    Parameters
    ----------
    classifier :
        sklearn classifier
    plate_load_path : pathlib.Path
        path to plate to load

    Returns
    -------
    _type_
        _description_
    """
    
    first_row_data = pd.read_csv(plate_load_path, compression="gzip", nrows=1)
    metadata_cols = [col for col in first_row_data.columns if 'efficientnet' not in col]
    feature_cols = [col for col in first_row_data.columns if 'efficientnet' in col]
    prediction_classes = classifier.classes_
    
    print(f"Loading feature data for {plate_load_path.name}...")
    # specify datatypes for all columns to make loading more efficient
    metadata_dtypes = {metadata_col: str for metadata_col in metadata_cols}
    feature_dtypes = {feature_col: np.float32 for feature_col in feature_cols}
    # combine both dictionaries
    plate_dtypes = metadata_dtypes | feature_dtypes
    
    # load in csv with the specified column names/datatypes
    plate_data = pd.read_csv(plate_load_path, compression="gzip", dtype=plate_dtypes, low_memory=True)
    
    print(f"Classifying feature data for {plate_load_path.name}...")
    
    cell_metadatas = plate_data[metadata_cols].reset_index(drop=True)
    cell_classifications = pd.DataFrame(classifier.predict_proba(plate_data[feature_cols].values), columns = prediction_classes).reset_index(drop=True)
    
    return pd.concat([cell_metadatas, cell_classifications], axis=1)