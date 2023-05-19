# 2. Extract Features

In this module, we present our pipeline for extracting features from the Cell Health data.

# CellProfiler Feature Extraction

We use [CellProfiler](https://github.com/CellProfiler) (GUI, verstion `4.2.4`) to extract features from the Cell Health data. 

## Step 1: Setup CellProfiler Feature Extraction Environment

### Step 1a: Create CellProfiler Feature Extraction Environment

```sh
# Run this command to create the conda environment for CellProfiler feature extraction
conda env create -f 2.cp-feature-extraction-env.yml
```

### Step 1b: Activate Feature Extraction Environment

```sh
# Run this command to activate the conda environment for CellProfiler feature extraction

conda activate 2.cp-feature-extraction-cell-health
```

## Step 2: Define Project Paths

Inside the notebook [extract-cp-features.ipynb](CP-feature-extraction/extract-cp-features.ipynb), the variables `nuclei_images_load_path`, `all_data_load_path`, and `features_save_path` need to be changed to reflect the desired path to nuclei images, all data, and features respectively.

## Step 3: Extract Features with CellProfiler

We extract features for the Cell Health dataset by plate to best utilize machine memory.
In [extract-cp-features.ipynb](CP-feature-extraction/extract-cp-features.ipynb), we iterate through each plate in Cell Health and use `subprocess` to extract features with [CellProfiler headless](https://carpenter-singh-lab.broadinstitute.org/blog/getting-started-using-cellprofiler-command-line).

Features are output to `features_save_path` set above in step 3.

```bash
# Run this script to compile and run the DeepProfiler project
bash 2a.extract-cp-features.sh
```

**Note**: This CP run requires lots of memory and time.

# DeepProfiler Feature Extraction

We use [DeepProfiler](https://github.com/cytomining/DeepProfiler) (commit [`f12f39b`](https://github.com/cytomining/DeepProfiler/commit/f12f39b8a905b0bb40d343e21e89bfda537b710a)) to extract features from the Cell Health data. 

We use a [pretrained model](https://github.com/broadinstitute/luad-cell-painting/tree/main/outputs/efn_pretrained/checkpoint) from the [LUAD Cell Painting repository](https://github.com/broadinstitute/luad-cell-painting) with DeepProfiler.
[Caicedo et al., 2022](https://www.molbiolcell.org/doi/10.1091/mbc.E21-11-0538) trained this model to extract features from Cell Painting data.
This model extracts features from all 5 cell-painting channels (DNA, ER, RNA, AGP, Mito).

We use the [metadata file](../0.image-download/manifest/idr0080-screenA-annotation.csv) from idr-0080-way-pertubation downloaded from [IDR github](https://github.com/IDR/idr0080-way-perturbation/blob/74e537fecaa4690f0c98cb1e9a64b45d103de3e3/screenA/idr0080-screenA-annotation.csv).

We also use a similar config file to the one used in the [LUAD Cell Painting repository](https://github.com/broadinstitute/luad-cell-painting).
We make the following changes to this config file to create [cell_health_nuc_config.json](DP-feature-extraction/DP_files/cell_health_nuc_config.json).

Both:
- `"Allele" -> "Reagent"` While the LUAD study compared alleles across cell painting images, we compare the reagents that correspond to CRISPR perturbations among the different images.
- `dataset: images: {file format: tif, bits: 16, width: 1080, height: 1080} -> dataset: images: {file format: tiff, bits: 16, width: 2160, height: 2160}`: The image details need to reflect the Cell Health data.
- `prepare: implement: true -> prepare: implement: false` We do not prepare the Cell Health data with illumination correction or compression with Deep Profiler.

`cell_health_nuc_config.json`:
- `dataset: images: channels: [DNA, ER, RNA, AGP, Mito] -> dataset: images: channels: [DNA]` While the Cell Painting dataset has multiple channels for cell images, we are only interested in examining the DNA channel for the nuclei project.
- `dataset: locations: box_size: 96 -> dataset: locations: box_size: 256` This change expands the size of the box around each cell that DeepProfiler interprets. This change helps DeepProfiler interpret nuclei from Cell Health data with the same context as it uses to interpret cells in [mitocheck_data](https://github.com/WayScience/mitocheck_data).


## Step 1: Setup DeepProfiler Feature Extraction Environment

### Step 1a: Create DeepProfiler Feature Extraction Environment

```sh
# Run this command to create the conda environment for DeepProfiler feature extraction
conda env create -f 2.dp-feature-extraction-env.yml
```

### Step 1b: Activate Feature Extraction Environment

```sh
# Run this command to activate the conda environment for DeepProfiler feature extraction

conda activate 2.dp-feature-extraction-cell-health
```

## Step 2: Install DeepProfiler

### Step 2a: Clone Repository

Clone the DeepProfiler repository into 2.extract-features/ with 

```console
# Make sure you are located in 2.extract-features/DP-feature-extraction/
cd 2.extract-features/DP-feature-extraction/
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

Inside the notebook [compile-DP-projects.ipynb](DP-feature-extraction/compile-DP-projects.ipynb), the variable `nuc_project_path` needs to be changed to reflect the desired nuc DeepProfiler project locations.
We used an external harddrive and therefore needed to use specific paths.
These project paths will contain the DeepProfiler `config.json`, `index.csv`, cell locations, pre-trained model, and extracted features.

This path also needs to be set in [2b.extract-dp-features.sh](2b.extract-dp-features.sh) by replacing `path/to/DP_nuc_project` with the same path used to set `nuc_project_path`.

## Step 4: Compile and Run DeepProfiler Project

In order to extract features with DeepProfiler, a project needs to be set up with a certain file structure and files.
In [compile-DP-projects.ipynb](DP-feature-extraction/compile-DP-projects.ipynb) we create the necessary project structure.
We copy the config file ([cell_health_nuc_config.json](DP-feature-extraction/DP_files/cell_health_nuc_config.json)) to its corresponding project and the pretrained model ([efficientnet-b0_weights_tf_dim_ordering_tf_kernels_autoaugment.h5](DP-feature-extraction/DP_files/efficientnet-b0_weights_tf_dim_ordering_tf_kernels_autoaugment.h5)) to the project.
We also compile an `index.csv` file necessary for DeepProfiler to load each image and `nuclei-locations` files necessary for DeepProfiler to find the single cells in each image.

More information on DeepProfiler project structure and necessary files can be found at the [DeepProfiler wiki](https://github.com/cytomining/DeepProfiler/wiki/2.-Project-structure).

```bash
# Run this script to compile and run the DeepProfiler project
bash 2b.extract-dp-features.sh
```
