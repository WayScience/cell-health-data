"""
utils for classifying cells from Cell Health Data
"""

import pathlib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression


def get_probas_dataframe(plate_features: pd.DataFrame, model: LogisticRegression, feature_type: str) -> pd.DataFrame:
    """
    Get probabilites for plate features from a phenotypic classification model

    Parameters
    ----------
    plate_features : pd.DataFrame
        plate features to classify
    model : LogisticRegression
        model to use for plate feature classification
    feature_type : str
        type of features to use for classification.
        CP, DP, or CP_and_DP

    Returns
    -------
    pd.DataFrame
        dataframe with single-cell probabilities for classes from given model
    """

    # determine which feature columns should be loaded depending on feature type
    # if there is no "and" we can use feature type as prefix
    if "and" not in feature_type:
        cols_to_load = [
            col
            for col in plate_features.columns.to_list()
            if f"{feature_type}__" in col
        ]
    # if there is an "and" we should all features (which all have "P__" prefix)
    else:
        cols_to_load = [
            col for col in plate_features.columns.to_list() if "P__" in col
        ]

    # load these particular features and get the values
    single_cell_features = plate_features[cols_to_load].values
    
    # get and return the predicted probabilities
    probas_dataframe = pd.DataFrame(
        model.predict_proba(single_cell_features),
        columns=model.classes_,
    ).reset_index(drop=True)
    
    return probas_dataframe
