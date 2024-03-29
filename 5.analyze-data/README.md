# 5. Analyze Data

In this module, we perform the analysis of model-generated data.

### Model Probability Analysis

We use the model phenotype probabilities generated from [non-shuffled](https://github.com/WayScience/phenotypic_profiling_model/blob/main/2.train_model/models/multi_class_models/final__CP_areashape_only__balanced.joblib) and [shuffled](https://github.com/WayScience/phenotypic_profiling_model/blob/main/2.train_model/models/multi_class_models/shuffled_baseline__CP__balanced.joblib) weighted logistic regression models, trained exclusively from [MitoCheck](https://github.com/WayScience/mitocheck_data) CellProfiler AreaShape morphology features. AreaShape morphology features were found to be the most promising for classifying MitoCheck phenotypes.

We compare the phenotype probabilities between each treated well and the remaining negative control wells on the corresponding plate.
Each treatment well and corresponding negative control well phenotype probabilities are only compared if the number of cells in these groups is above a given cell count threshold, where the default threshold is 50.
The group, treatment cells or control cells, are then randomly down-sampled depending on which of these groups has a larger population of cells.
Random sampling of the control cells is accomplished through stratification of cells by the cell count of the corresponding plate's wells.
After sampling the cell population, the cells from the treated and control groups are compared using the [KS test](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kstest.html) statistic.

## Step 1: Setup Analysis Environment

### Step 1a: Create Analysis Environment
```sh
# Run this command to create the conda environment for analyzing the data
conda env create -f environment.yml
```

### Step 1b: Activate Analysis Environment

```sh
# Run this command to activate the conda environment for analyzing the data
conda activate health-comp
```

## Step 2: Compare Model Predicted Probabilities
```sh
# Run this command to compare the model's predicted probabilities
python3 nbconverted/log_reg_class_balanced_areashape_analyze_well_predicted_probabilities.py
```
