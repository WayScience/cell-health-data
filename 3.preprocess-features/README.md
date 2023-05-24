# 3. Preprocess Features

In this module, we present our pipeline for preprocessing features.

### Feature Preprocessing

We use [PyCytominer](https://github.com/cytomining/pycytominer) to compile DeepProfiler single-cell features.

We use [sklearn.preprocessing.StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html) to derive a normalizion scaler from all negative control features.
`StandardScaler()` standardizes features by removing the mean and scaling to unit variance.

[Caicedo et al, 2017](https://www.nature.com/articles/nmeth.4397) explain why the negative control features are a good normalization population for our use case:

> When choosing the normalizing population, we suggest the use of control samples (assuming that they are present in sufficient quantity), because the presence of dramatic phenotypes may confound results. This procedure is good practice regardless of the normalization being performed within plates or across the screen.

We derive a normalization scaler per plate and normalize each plate with their respective scaler so any plate batch effects are corrected.

In [3a.merge-cp-dp-features.ipynb](3a.merge-features/3a.merge-cp-dp-features.ipynb) we compile and merge all CellProfiler and DeepProfiler features for each plate.
**Note**: Loading and merging the features takes about 15 minutes per plate. 
Compressing and saving this merged data takes about 45 minutes per plate. 
Thus, this notebook takes about 9 hours to process all 9 plates.

In [3b.normalize-merged-features.ipynb](3b.normalize-features/3b.normalize-merged-features.ipynb) we derive a normalization scaler from all negative control cells and apply this scaler to all single-cell feature data for each plate.

## Step 1: Setup Feature Preprocessing Environment

### Step 1a: Create Feature Preprocessing Environment

```sh
# Run this command to create the conda environment for preprocessing features
conda env create -f 3.preprocess-features-env.yml
```

### Step 1b: Activate Preprocessing Environment

```sh
# Run this command to activate the conda environment for preprocessing features
conda activate 3.preprocess-features-cell-health
```

## Step 2: Define File/Folder Paths

In the notebooks [3a.merge-cp-dp-features.ipynb](3a.merge-features/3a.merge-cp-dp-features.ipynb) and [3b.normalize-merged-features.ipynb](3b.normalize-features/3b.normalize-merged-features.ipynb), any absolute paths in the `Set Load/Save Paths` sections need to be changed the reflect the paths of the projects and saved features/metadata.
We used an external harddrive and therefore needed to use absolute paths.

## Step 3: Preprocess Cell Health Features

```bash
# Run this script to preprocess Cell Health features
bash 3.preprocess-features.sh
```

**Note**: None of the Jupyter notebooks in this module have complete output as they were only used for testing and were only fully run after being converted to a python script (as done with [3.preprocess-features.sh](3.preprocess-features.sh)).
