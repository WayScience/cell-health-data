# Cell Health Data Processing

This is a data repository storing instructions on how to:

1. Download the Cell Health Cell Painting dataset ([IDR0080](https://idr.openmicroscopy.org/webclient/?show=screen-2701))
2. Perform segmentation
3. Define a new single-cell focused dataset of isolated single cells
4. Compute single cell embeddings
    - Using CellProfiler
    - Using DeepProfiler
5. Process both kinds of embeddings using pycytominer

These data were originally used as part of the publication [Way et al. 2021](https://doi.org/10.1091/mbc.E20-12-0784).

> Predicting cell health phenotypes using image-based morphology profiling
> Gregory P. Way, Maria Kost-Alimova, Tsukasa Shibue, William F. Harrington, Stanley Gill, Federica Piccioni, Tim Becker, Hamdah Shafqat-Abbasi, William C. Hahn, Anne E. Carpenter, Francisca Vazquez, and Shantanu Singh
> Molecular Biology of the Cell 2021 32:9, 995-1005

Note: Not all data are stored in this repository.
Some data are too large.

## Step 1 - IDR Download

See `0.data-download` for more details.

```bash
# Make sure to follow all steps in `0.data-download/README.md` first
cd 0.data-download
bash download_images.sh
```

## Step 2 - Segmentation
