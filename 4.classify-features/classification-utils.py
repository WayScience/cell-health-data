import pathlib
import numpy as np
import pandas as pd

def get_reagent_probabilities(classifier, plate_load_path: pathlib.Path):
    
    print(f"Loading feature data for {plate_load_path.name}...")
    plate_data = pd.read_csv(plate_load_path, compression="gzip")
    
    print(f"Classifying feature data for {plate_load_path.name}...")
    
    feature_cols = [col for col in plate_data.columns if 'efficientnet' in col]
    unique_reagents = plate_data["Metadata_Reagent"].unique()
    prediction_classes = classifier.classes_

    plate_reagent_predictions = []

    for reagent in unique_reagents:    
        reagent_feature_data = plate_data.loc[plate_data["Metadata_Reagent"] == reagent][feature_cols].values
        reagent_predictions = classifier.predict_proba(reagent_feature_data)
        # average predition probabilities across perturbations for this plate
        reagent_predictions_median = np.mean(reagent_predictions, axis=0)
        # map 16 phenotypic classes to the 16 prediction values
        reagent_predictions_data = {"reagent": reagent}
        reagent_predictions_data.update(dict(zip(prediction_classes,reagent_predictions_median)))
        
        plate_reagent_predictions.append(reagent_predictions_data)
        
    return pd.DataFrame(plate_reagent_predictions)