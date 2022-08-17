# 3. Preprocess Features

In this module, we present our pipeline for preprocessing features.

### Feature Preprocessing

We use [PyCytominer](https://github.com/cytomining/pycytominer) to compile single-cell features.

We use [sklearn.preprocessing.StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html) to derive a normalizion scaler from all negative control features.
`StandardScaler()` standardizes features by removing the mean and scaling to unit variance.

[Caicedo et al, 2017](https://www.nature.com/articles/nmeth.4397) explain why the negative control features are a good normalization population for our use case:
> When choosing the normalizing population, we suggest the use of control samples (assuming that they are present in sufficient quantity), because the presence of dramatic phenotypes may confound results. This procedure is good practice regardless of the normalization being performed within plates or across the screen.

The `get_negative_control_index_df` function inside [preprocess-features-utils.py](preprocess-features-utils.py) creates a DeepProfiler-style `index.csv` file (saved in [norm_pop_index.csv](intermediate_files/norm_pop_index.csv)) with only the negative control wells.
We then use pycytominer to compile the features from these negative control wells and derive and `StandardScaler` with only the negative control features (saved in [negative_control_scaler.save](negative_control_scaler.save)).

After deriving a normalization scaler, we load features by plate and apply the normalization scaler to these plate features.
The normalized features from each plate are saved in `output_path/`.
It is necessary to normalize features by plate because we are unable to load the single-cell features for the entire screen into memory.

**Note:** The single-cell dataframes for each plate are first saved as uncompressed files with `pandas.to_csv`.
These uncompressed files are then compressed with [pigz-python](https://github.com/nix7drummer88/pigz-python) and the original, uncompressed files are deleted.
`Pigz-python` is the python implementation of [pigz](https://zlib.net/pigz/), which uses multiple cores to compress files.
This is significantly faster than the native `pandas` gzip compression.

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

Inside the notebook [preprocess-features.ipynb](preprocess-features.ipynb), the variables `features_output_dir` and `original_index_csv_path` need to be changed the reflect the paths of the features output directory and original index.csv file from the DeepProfiler project.
`output_path` needs to be changed to reflect the desired output directory for the normalized data.
We used an external harddrive and therefore needed to use specific paths.

## Step 3: Preprocess Cell Health Features

```bash
# Run this script to preprocess Cell Health features
bash 3.preprocess-features.sh
```
