# 4a. Classify Single Cell Phenotypes

In this module, we present our pipeline for classifying single-cell phenotypes.

## Deriving Classifications

Follow the steps in [4.classify-single-cell-phenotypes/README.md](../README.md) to run this module.

## File Description

This module outputs compressed csv files that contain the classification probabilities of preprocessed Cell Health features output by [3.preprocess-features](../../3.preprocess-features/).
These classifications are derived per-plate by each of the models created in the [phenotypic_profiling](https://github.com/WayScience/phenotypic_profiling_model) repository.
These models include multi-class models (16 output probabilities, 1 for each phenotypic class) and single-class models (2 output probabilities, positive and negative probabilities for the model's particular phenotypic class).
For more information on model training and type see [phenotypic_profiling_model/2.train_model](https://github.com/WayScience/phenotypic_profiling_model/tree/main/2.train_model).

Each compressed csv file output by this module contains rows of single-cell metadata (location, perturbation, etc) and feature classification probabilities, as derived by the particular model.
There is one compressed csv file for each of the nine plates in the Cell Health dataset.
The contents of the compressed csv file containing `OutOfFocus` model predictions from plate `SQ00014613` are shown below:

| Location_Center_X | Location_Center_Y | Metadata_Site | Metadata_Well | Metadata_Plate | Metadata_Plate_Map_Name | Metadata_Reagent | OutOfFocus | OutOfFocus Negative |
|-------------------|-------------------|---------------|---------------|----------------|--------------------------|------------------|------------|---------------------|
| 1141.205          | 27.372            | 4             | G18           | SQ00014613     | SQ00014613_G18_04        | ARID1B-2         | 0.123      | 0.877               |
| 896.493           | 42.108            | 4             | G18           | SQ00014613     | SQ00014613_G18_04        | ARID1B-2         | 0.194      | 0.806               |
| 1571.713          | 30.771            | 4             | G18           | SQ00014613     | SQ00014613_G18_04        | ARID1B-2         | 0.191      | 0.809               |
| ...          | ...            | ...             | ...           | ...     | ...        | ...         | ...      | ...               |
| 1535.734          | 55.748            | 9             | P21           | SQ00014613     | SQ00014613_P21_09        | PSMA1-1         | 0.385      | 0.615               |

## File Structure

The output file structure of this module mirrors the structure of the models hosted at [phenotypic_profiling_model/2.train_model/models](https://github.com/WayScience/phenotypic_profiling_model/tree/main/2.train_model/models), with folders contianing plate classifications in place of the models.

The output structure is as follows:

```
output_dir/
├── multi_class_models/
│ ├── final__CP__balanced/
│ ├── ...
│ └── shuffled_baseline__CP_and_DP__unbalanced/
│ │ ├── SQ00014610__cell_classifications.csv.gz
│ │ ├── ...
│ │ └── SQ00014610__cell_classifications.csv.gz
├── single_class_models/
│ ├── Anaphase_models/
│ ├── ...
│ └── OutOfFocus_models/
│ | ├── final__CP__balanced/
│ | ├── ...
│ | └── shuffled_baseline__CP_and_DP__unbalanced/
│ | │ ├── SQ00014610__cell_classifications.csv.gz
│ | │ ├── ...
│ | │ └── SQ00014610__cell_classifications.csv.gz
```

Each model is identified by its `model_type`, `feature_type`, and `balance` which are the name of the model's folder (with `__` as a delimiter).
Single-class models are also stratified by the phenotypic class they are trained with (anaphase, out of focus, etc).