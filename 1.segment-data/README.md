# Segment Cell Painting Images

In this module, we present our pipeline for segmenting nuclei and cyoplasm from the Cell Health data.

### Segmentation

We use the CellPose segmentation algorithim to segment the nuclei from each mitosis movie. 
CellPose was first introduced in [Stringer, C., Wang, T., Michaelos, M. et al., 2020](https://doi.org/10.1038/s41592-020-01018-x) and we use the [python implementation](https://github.com/mouseland/cellpose).

Stringer et al. trained the CellPose segmentation models on a diverse set of cell images and is therefore a good selection for our use case.
The CellPose python implementation was particularly useful for building reproducible pipelines.

After manually experiementing with CellPose on about 10 Cell Health nuclei images (various cell lines), we settled on the following parameters for CellPose nuclei segmentation:
- `model_type = "cyto"` This parameter forces CellPose to use the cytoplasm model, which we found segments nuclei in the Cell Health data significantly better than the nucleus model. 
More information about CellPose models can be found at https://cellpose.readthedocs.io/en/latest/models.html.
- `channels = [0,0]` This parameter forces the model to segment cells in grayscale (in the case of Cell Health data single channel images).
- `diameter = 80` This parameter indicates to the model that the average cell diameter is 80 pixels.
- `flow_threshold=0` This paramenter decreases the maximum allowed error of the flows for each mask (default is `flow_threshold=0.4`).
More information about CellPose settings can be found at https://cellpose.readthedocs.io/en/latest/settings.html.

After manually experiementing with CellPose on about 10 Cell Health cytoplasm images (various cell lines), we settled on the following parameters for CellPose cytoplasm segmentation:
- `model_type = "cyto"` This parameter forces CellPose to use the cytoplasm model for segmentation.
More information about CellPose models can be found at https://cellpose.readthedocs.io/en/latest/models.html.
- `channels = [1,3]` This parameter forces the model to segment cells using the nuclei and RNA channels of cell painting images. We overlay nuclei, ER, and RNA channels for CellPose with our `overlay_images()` function in [segment-cell-health-data.ipynb](segment-cell-health-data.ipynb).
- `diameter = 0` This parameter forces the CellPose model to estimate the diameter of cells being segmented.
- `flow_threshold=0` This paramenter decreases the maximum allowed error of the flows for each mask (default is `flow_threshold=0.4`).
- `cellprob_threshold=0.4` This parameter is used to determine ROIs (default is `cellprob_threshold=0`). More information about CellPose settings can be found at https://cellpose.readthedocs.io/en/latest/settings.html.

## Step 1: Setup Segmentation Environment

### Step 1a: Create Segmentation Environment

```sh
# Run this command to create the conda environment for Segmentation data
conda env create -f 1.segment-env.yml
```

### Step 1b: Activate Segmentation Environment

```sh
# Run this command to activate the conda environment for Segmentation data
conda activate 1.segment-data-cell-health
```

### Step 1c (Optional): Complete PyTorch GPU Setup

If you would like use PyTorch GPU when using CellPose, follow [these instructions](https://github.com/MouseLand/cellpose#gpu-version-cuda-on-windows-or-linux) to complete the PyTorch GPU setup.
We use PyTorch GPU while segmenting Cell Health data.

## Step 2: Execute Training Data Segmentation

```bash
# Run this script to segment Cell Health data
bash 1.segment-data.sh
```