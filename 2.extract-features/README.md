# 3. Extract Features

In this module, we present our pipeline for extracting features from the Cell Health data.

### Feature Extraction

We use [DeepProfiler](https://github.com/cytomining/DeepProfiler), commit [`f12f39b`](https://github.com/cytomining/DeepProfiler/commit/f12f39b8a905b0bb40d343e21e89bfda537b710a), to extract features from the Cell Health data. 

We use a [pretrained model](https://github.com/broadinstitute/luad-cell-painting/tree/main/outputs/efn_pretrained/checkpoint) from the [LUAD Cell Painting repository](https://github.com/broadinstitute/luad-cell-painting) with DeepProfiler.
[Caicedo et al., 2022](https://www.molbiolcell.org/doi/10.1091/mbc.E21-11-0538) trained this model to extract features from Cell Painting data.
This model extracts features from all 5 cell-painting channels (DNA, ER, RNA, AGP, Mito).

We use the [metadata file](idr0080-screenA-annotation.csv) from idr-0080-way-pertubation download from [IDR github](https://github.com/IDR/idr0080-way-perturbation/blob/74e537fecaa4690f0c98cb1e9a64b45d103de3e3/screenA/idr0080-screenA-annotation.csv).

## Step 1: Setup Feature Extraction Environment

### Step 1a: Create Feature Extraction Environment

```sh
# Run this command to create the conda environment for feature extraction
conda env create -f 2.feature-extraction-env.yml
```

### Step 1b: Activate Feature Extraction Environment

```sh
# Run this command to activate the conda environment for Deep Profiler feature extraction

conda activate 2.feature-extraction-cell-health
```

## Step 2: Install DeepProfiler

### Step 2a: Clone Repository

Clone the DeepProfiler repository into 3.extract_features/ with 

```console
# Make sure you are located in 3.extract_features/
cd 2.extract_features/
git clone https://github.com/cytomining/DeepProfiler.git
```

### Step 2b: Install Repository

Install the DeepProfiler repository with

```console
cd DeepProfiler/
pip install -e .
```

### Step 2c (Optional): Complete Tensorflow GPU Setup

If you would like use Tensorflow GPU when using DeepProfiler, follow [these instructions](https://www.tensorflow.org/install/pip#3_gpu_setup) to complete the Tensorflow GPU setup.
We use Tensorflow GPU while processing mitocheck data.

## Step 3: Compile DeepProfiler Project

```bash
# Run this script to compile the DeepProfiler project
bash 
```



## Step 4: Extract Features with DeepProfiler

```sh
# Run this script to extract features with DeepProfiler
python3 -m deepprofiler --gpu 0 --exp efn_pretrained --root /media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/cell-health-nuc-DP/ --config cell_health_nuclei_config.json profile
```

**Note:** `--root` has to be set to the path of the DeepProfiler project