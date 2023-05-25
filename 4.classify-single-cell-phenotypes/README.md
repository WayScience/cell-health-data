# 4. Classify Single Cell Phenotypes

In this module, we present our pipeline for classifying features.

### Feature Classification

We use the models trained in [phenotypic_profiling](https://github.com/WayScience/phenotypic_profiling_model) to classify nucleus features from Cell Health Data.
The final models have the highest average cross-validated F1 score while the shuffled baseline models were trained on feature values shuffled independent of their feature label (and thus serve as a baseline for training on features with no correlation).

The specified classification models will be downloaded to [phenotypic_profiling_models/](phenotypic_profiling_models) and loaded from these files.

## Step 1: Setup Feature Classification Environment

### Step 1a: Create Feature Classification Environment

```sh
# Run this command to create the conda environment for classifying features
conda env create -f 4.classification-env.yml
```

### Step 1b: Activate Classification Environment

```sh
# Run this command to activate the conda environment for classifying features
conda activate 4.classify-single-cell-phenotypes
```

## Step 2: Download Models from `phenotypic_profiling_model`

We use models from the [phenotypic_profiling_model](https://github.com/WayScience/phenotypic_profiling_model) repository to derive the single-cell phenotypes.
Use the commands below to download the [models/](https://github.com/WayScience/phenotypic_profiling_model/tree/main/2.train_model/models) folder from this repository.

```sh
# Run these commands to download models from phenotypic_profiling_model

# make sure you are inside 4.classify-single-cell-phenotypes/
cd 4.classify-single-cell-phenotypes/

# make download directory
mkdir phenotypic_profiling_model
cd phenotypic_profiling_model

# set up folder as github repo
git init
git remote add origin https://github.com/WayScience/phenotypic_profiling_model.git

# enable git repo to download specific directories
git config core.sparseCheckout true

# set folder to be downloaded
echo "2.train_model/models" > .git/info/sparse-checkout 

# download this folder from the repo
git pull origin cp-feature-refactor # cp-feature-refactor should be changed to main once PR is merged
```

## Step 3: Define Folder Paths

Inside the notebook [classify-single-cell-phenotypes.ipynb](classify-single-cell-phenotypes.ipynb), the variable `normlized_plates_path` needs to be changed the reflect the paths of the normalized features from [3.preprocess-features](3.preprocess-features).
The variable `classifications_save_path` also needs to be set to specify where the model classficiations are saved.
We used an external harddrive and therefore needed to use specific paths.

## Step 3: Classify Cell Health Features

```sh
# Run this script to classify Cell Health features
bash 4.classify-single-cell-phenotypes.sh
```
