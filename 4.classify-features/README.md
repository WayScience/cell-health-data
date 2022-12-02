# 3. Classify Features

In this module, we present our pipeline for classifying features.

### Feature Classification

We use a logistic regression model trained in [phenotypic_profiling](https://github.com/WayScience/phenotypic_profiling_model) to classify nucleus features from Cell Health Data.

The version of the classification model downloaded from `phenotypic_profiling` can be specified by the hash corresponding to a commit.
The current hash being used is `64cfc46ecd92f1956af199c81f8ecf4dc292718f` which corresponds to [phenotypic_profiling/64cfc46](https://github.com/WayScience/phenotypic_profiling_model/tree/64cfc46ecd92f1956af199c81f8ecf4dc292718f). The `hash` variable can be set in [`classify-features`](classify-features.ipynb) to change which version of `phenotypic_profiling` is being accessed.

## Step 1: Setup Feature Classification Environment

### Step 1a: Create Feature Classification Environment

```sh
# Run this command to create the conda environment for classifying features
conda env create -f 4.classify-features-env.yml
```

### Step 1b: Activate Classification Environment

```sh
# Run this command to activate the conda environment for classifying features
conda activate 4.classify-features-cell-health
```

## Step 3: Classify Cell Health Features

```bash
# Run this script to classify Cell Health features
bash 4.classify-features.sh
```
