# Download Cell Painting Images

The Cell Painting images are derived from 119 CRISPR perturbations in 3 different cell lines.

For more details about the dataset, see:

> Gregory P. Way, Maria Kost-Alimova, Tsukasa Shibue, William F. Harrington, Stanley Gill, Federica Piccioni, Tim Becker, Hamdah Shafqat-Abbasi, William C. Hahn, Anne E. Carpenter, Francisca Vazquez, and Shantanu Singh.
> Predicting cell health phenotypes using image-based morphology profiling.
> Molecular Biology of the Cell 2021 32:9, 995-1005. DOI: https://doi.org/10.1091/mbc.E20-12-0784.

These data are located on IDR with accession number 0080, and screen ID 2701 (https://idr.openmicroscopy.org/webclient/?show=screen-2701).

## Step 1 - Install docker

The first step to data access is to install docker.
Follow the instructions provided at https://docs.docker.com/get-docker/.

## Step 2 - Pull imagedata/download image

After installing docker, in your terminal simply run:

```bash
docker pull imagedata/download
```

This will download the docker image: https://hub.docker.com/r/imagedata/download

Note that a ["docker image"](https://docs.docker.com/get-started/overview/) is different than a "microscopy image".
An unfortunate name collision!

## Step 3 - Download manifest metadata files

The manifest file contains the paths to images from individual plates.
If you wish to download images from all plates, you do not need to follow this step (although we still recommend).

You can find links to all of the metadata files here: https://github.com/IDR/idr-metadata

- Identify your study of interest
- Click the link (github submodule) to be directed to the specific metadata repository
    - We're using this repo: https://github.com/IDR/idr0080-way-perturbation/
- Follow the instructions in [`0.download-manifest.ipynb`](0.download-manifest.ipynb)
    - This will download both the `plates` and `annotation` metadata files. The `plates`

## Step 4 - Download images

Now, we can use the docker image and manifest file paths to download the actual microscopy images!

### Step 4.1 - Test download

Test download first by download images from a single plate.
Use the following syntax:

```bash
# Make sure you are in the 0.image-download directory
cd 0.image-download

# Create and navigate into appropriate directories
mkdir -p images/SQ0001460 && cd images/

# Download data from one plate
docker run -ti --rm -v $(pwd):/data -e ASCP_LIMIT=100g imagedata/download idr0080 20200923-illumcorrected/SQ00014610 /data
```

### Step 4.2 - Complete download

```bash
# Run this script to download all images
bash 1.download-images.sh
```
