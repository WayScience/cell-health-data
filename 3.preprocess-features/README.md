# 3. Preprocess Features

In this module, we present our pipeline for preprocessing features.

### Feature Preprocessing

We use [PyCytominer](https://github.com/cytomining/pycytominer) to compile single-cell features.

We use [sklearn.preprocessing.StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html) to derive a normalizion scaler from all negative control features.
`StandardScaler()` standardizes features by removing the mean and scaling to unit variance.

[Caicedo et al, 2017](https://www.nature.com/articles/nmeth.4397) explain why the negative control features are a good normalization population for our use case:
> When choosing the normalizing population, we suggest the use of control samples (assuming that they are present in sufficient quantity), because the presence of dramatic phenotypes may confound results. This procedure is good practice regardless of the normalization being performed within plates or across the screen.

We derive a normalization scaler per plate and normalize each plate with their respective scaler so any plate batch effects are corrected for.
Inside [preprocess-features.ipynb](preprocess-features.ipynb), we iterate through every plate and complete the following:
1) Find all negative control wells for the specified plate.
2) Compile features from the negative control wells.
3) Derive a normalization scaler from the negative control well features.
4) Apply the normalization scaler to the entire plate.
5) Save the compiled normalized plate features inside `output_path/`.

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

## Step 2: Define File/Folder paths

Inside the notebook [preprocess-features.ipynb](preprocess-features.ipynb), the variables `DP_project_path` and `output_path` need to be changed the reflect the paths of the DeepProfiler project to load features/metadata from and the desired save location for normalized features output.
We used an external harddrive and therefore needed to use specific paths.

## Step 3: Preprocess Cell Health Features

```bash
# Run this script to preprocess Cell Health features
bash 3.preprocess-features.sh
```
