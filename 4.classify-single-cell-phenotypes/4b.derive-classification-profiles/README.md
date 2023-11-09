# 4b. Derive Classification Profiles

In this module, we present our pipeline for creating classification profiles.

## Deriving Classification Profiles:

Follow the steps in [4.classify-single-cell-phenotypes/README.md](../README.md) to run this module.

## File Description

This module outputs tsv files that contain "classification profiles" for a particular model.
These profiles are generated from the single-cell classification probabilities generated in [4a.classify-single-cell-phenotypes](../4a.classify-single-cell-phenotypes/).
For each model, we find the mean of the single-cell classification probabilities across each perturbation and cell line to create a composite profile. 
This aggregated data provides a summarized view of cell behavior for each perturbation/cell line combination, as predicted by each model.

The contents of the tsv file containing the classification profiles for the `OutOfFocus` model predictions from are shown below:

| Metadata_pert_name | Metadata_cell_line | OutOfFocus | OutOfFocus Negative |
|--------------------|--------------------|------------|---------------------|
| AKT1-1             | A549               | 0.346      | 0.654               |
| AKT1-2             | A549               | 0.343      | 0.657               |
| ...          | ES2               | ...      | ...               |
| ARID1B-2           | A549               | 0.322      | 0.678               |

## File Structure

The output file structure of this module mirrors the structure of the models hosted at [phenotypic_profiling_model/2.train_model/models](https://github.com/WayScience/phenotypic_profiling_model/tree/main/2.train_model/models), with files containing classification profiles in place of the models.

The output file structure is as follows:

```
output_dir/
├── multi_class_models/
│ ├── final__CP__balanced__classification_profiles.tsv
│ ├── ...
│ └── shuffled_baseline__CP_and_DP__unbalanced__classification_profiles.tsv
├── single_class_models/
│ ├── Anaphase_models/
│ ├── ...
│ └── OutOfFocus_models/
│ | ├── final__CP__balanced__classification_profiles.tsv
│ | ├── ...
│ | └── shuffled_baseline__CP_and_DP__unbalanced__classification_profiles.tsv
```

Each model is identified by its `model_type`, `feature_type`, and `balance` which are the name of the model's folder (with `__` as a delimiter).
Single-class models are also stratified by the phenotypic class they are trained with (anaphase, out of focus, etc).