"""
utils for classifying cells from Cell Health Data
"""

import pathlib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression


def classify_plate_cells(classifier, plate_load_path: pathlib.Path) -> pd.DataFrame:
    """
    classify cells in

    Parameters
    ----------
    classifier :
        sklearn classifier
    plate_load_path : pathlib.Path
        path to plate to load

    Returns
    -------
    plate_classifications : pd.DataFrame
        single cell dataframe with metadata and phenotypic class probabilities
    """

    # load in one row to create datatypes dictionary for faster loading
    first_row_data = pd.read_csv(plate_load_path, compression="gzip", nrows=1)
    metadata_cols = [col for col in first_row_data.columns if "efficientnet" not in col]
    feature_cols = [col for col in first_row_data.columns if "efficientnet" in col]

    # specify datatypes for metadata/feature columns
    metadata_dtypes = {metadata_col: str for metadata_col in metadata_cols}
    feature_dtypes = {feature_col: np.float32 for feature_col in feature_cols}
    # combine both dictionaries
    plate_dtypes = {**metadata_dtypes, **feature_dtypes}

    # load in csv with the specified column names/datatypes
    plate_data = pd.read_csv(
        plate_load_path, compression="gzip", dtype=plate_dtypes, low_memory=True
    )

    # combine metadatas and classifications dataframes
    cell_metadatas = plate_data[metadata_cols].reset_index(drop=True)
    cell_features = plate_data[feature_cols].values
    prediction_classes = classifier.classes_
    cell_classifications = pd.DataFrame(
        classifier.predict_proba(cell_features),
        columns=prediction_classes,
    ).reset_index(drop=True)
    return pd.concat([cell_metadatas, cell_classifications], axis=1)


def save_feature_classifications(phenotypic_profiling_model: LogisticRegression, normalized_plates_path: pathlib.Path, output_dir: pathlib.Path):
    
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # classify cells from each plate and save classifications
    for plate_load_path in normalized_plates_path.iterdir():
        print(f"Classifying feature data for {plate_load_path.name}...")
        plate = plate_load_path.name.strip("_normalized_single_cell.csv.gz")
        plate_classification_save_path = pathlib.Path(f"{output_dir}/{plate}_cell_classifications.csv.gz")
        
        plate_classifications = classify_plate_cells(phenotypic_profiling_model, plate_load_path)
        plate_classifications.to_csv(plate_classification_save_path, compression = "gzip")
        return