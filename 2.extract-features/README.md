# 2. Extract Features

In this module, we present our pipeline for extracting features from the Cell Health data.

### Feature Extraction

We use [DeepProfiler](https://github.com/cytomining/DeepProfiler), commit [`f12f39b`](https://github.com/cytomining/DeepProfiler/commit/f12f39b8a905b0bb40d343e21e89bfda537b710a), to extract features from the Cell Health data. 

We use a [pretrained model](https://github.com/broadinstitute/luad-cell-painting/tree/main/outputs/efn_pretrained/checkpoint) from the [LUAD Cell Painting repository](https://github.com/broadinstitute/luad-cell-painting) with DeepProfiler.
[Caicedo et al., 2022](https://www.molbiolcell.org/doi/10.1091/mbc.E21-11-0538) trained this model to extract features from Cell Painting data.
This model extracts features from all 5 cell-painting channels (DNA, ER, RNA, AGP, Mito).

We use the [metadata file](../0.image-download/manifest/idr0080-screenA-annotation.csv) from idr-0080-way-pertubation downloaded from [IDR github](https://github.com/IDR/idr0080-way-perturbation/blob/74e537fecaa4690f0c98cb1e9a64b45d103de3e3/screenA/idr0080-screenA-annotation.csv).

We also use a similar config file to the one used in the [LUAD Cell Painting repository](https://github.com/broadinstitute/luad-cell-painting).
We make the following changes to this config file to create [cell_health_nuc_config.json](DP_files/cell_health_nuc_config.json) and [cell_health_cyto_config.json](DP_files/cell_health_cyto_config.json).

Both:
- `"Allele" -> "Reagent"` While the LUAD study compared alleles across cell painting images, we compare the reagents that correspond to CRISPR perturbations among the different images.
- `dataset: images: {file format: tif, bits: 16, width: 1080, height: 1080} -> dataset: images: {file format: tiff, bits: 16, width: 2160, height: 2160}`: The image details need to reflect the Cell Health data.
- `prepare: implement: true -> prepare: implement: false` We do not prepare the Cell Health data with illumination correction or compression with Deep Profiler.

`cell_health_nuc_config.json`:
- `dataset: images: channels: [DNA, ER, RNA, AGP, Mito] -> dataset: images: channels: [DNA]` While the Cell Painting dataset has multiple channels for cell images, we are only interested in examining the DNA channel for the nuclei project.
- `dataset: locations: box_size: 96 -> dataset: locations: box_size: 256` This change expands the size of the box around each cell that DeepProfiler interprets. This change helps DeepProfiler interpret nuclei from Cell Health data with the same context as it uses to interpret cells in [mitocheck_data](https://github.com/WayScience/mitocheck_data).

`cell_health_cyto_config.json`:
- `dataset: locations: box_size: 96 -> dataset: locations: box_size: 128` This change expands the size of the box around each cell that DeepProfiler interprets. This change was recommended by Juan to improve performance.

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

Clone the DeepProfiler repository into 2.extract-features/ with 

```console
# Make sure you are located in 2.extract-features/
cd 2.extract-features/
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

## Step 3: Define Project Paths

Inside the notebook [compile-DP-projects.ipynb](compile-DP-projects.ipynb), the variables `nuc_project_path` and `cyto_project_path` need to be changed to reflect the desired nuc/cyto DeepProfiler project locations.
We used an external harddrive and therefore needed to use specific paths.
These project paths will contain the DeepProfiler `config.json`, `index.csv`, cell locations, pre-trained model, and extracted features.

## Step 4: Compile DeepProfiler Project

In order to profile features with DeepProfiler, a project needs to be set up with a certain file structure and files.
In [compile-DP-projects.ipynb](compile-DP-projects.ipynb) we create the necessary project structure.
We copy the config files ([cell_health_nuc_config.json](DP_files/cell_health_nuc_config.json)/[cell_health_cyto_config.json](DP_files/cell_health_cyto_config.json)) to their corresponding projects and the pretrained model ([efficientnet-b0_weights_tf_dim_ordering_tf_kernels_autoaugment.h5](DP_files/efficientnet-b0_weights_tf_dim_ordering_tf_kernels_autoaugment.h5)) to both projects.
We also compile an `index.csv` file necessary for DeepProfiler to load each image and `nuclei-locations` files necessary for DeepProfiler to find the single cells in each image.

More information on DeepProfiler project structure and necessary files can be found at the [DeepProfiler wiki](https://github.com/cytomining/DeepProfiler/wiki/2.-Project-structure).

```bash
# Run this script to compile the DeepProfiler projects
bash 2.compile-DP-projects.sh
```

## Step 5: Extract Features with DeepProfiler

Change `path/to/DP_nuc_project` and `path/to/DP_cyto_project` below to the `nuc_project_path` and `cyto_project_path` set in step 3.

```sh
# Run this script to extract features with DeepProfiler
python3 -m deepprofiler --gpu 0 --exp efn_pretrained --root path/to/DP_nuc_project --config cell_health_nuc_config.json profile
python3 -m deepprofiler --gpu 0 --exp efn_pretrained --root path/to/DP_cyto_project --config cell_health_cyto_config.json profile
```