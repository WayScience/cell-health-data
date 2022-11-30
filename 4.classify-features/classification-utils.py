import pathlib
import numpy as np
import pandas as pd

def get_reagent_probabilities(classifier, plate_load_path: pathlib.Path):
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
    feature_cols = [col for col in first_row_data.columns if 'efficientnet' in col]
    prediction_classes = classifier.classes_
    
    print(f"Loading feature data for {plate_load_path.name}...")
    # create list of what columns to load in and what their datatypes are
    load_cols = []
    load_cols.append("Metadata_Reagent")
    df_dtype = {}
    df_dtype["Metadata_Reagent"] = str
    
    for feature_name in feature_cols:
        load_cols.append(feature_name)
        df_dtype[feature_name] = np.float32
    
    # load in csv with the specified column names/datatypes
    plate_data = pd.read_csv(plate_load_path, compression="gzip", usecols=load_cols, dtype=df_dtype, low_memory=True)
    
    print(f"Classifying feature data for {plate_load_path.name}...")
    
    unique_reagents = plate_data["Metadata_Reagent"].unique()
    plate_reagent_predictions = []

    for reagent in unique_reagents:
        # get classifier prediction probabilities for features values for each cell in reagent
        reagent_feature_data = plate_data.loc[plate_data["Metadata_Reagent"] == reagent][feature_cols].values
        reagent_predictions = classifier.predict_proba(reagent_feature_data)
        # average predition probabilities for the reagent
        reagent_predictions_median = np.mean(reagent_predictions, axis=0)
        # map 16 phenotypic classes to the 16 prediction values
        reagent_predictions_data = {"reagent": reagent}
        reagent_predictions_data.update(dict(zip(prediction_classes,reagent_predictions_median)))
        
        plate_reagent_predictions.append(reagent_predictions_data)
        
    return pd.DataFrame(plate_reagent_predictions)