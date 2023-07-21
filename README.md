# Cell Health Data Processing

## Overview
This is a data repository storing instructions on how to:

0. Download the Cell Health Cell Painting dataset ([IDR0080](https://idr.openmicroscopy.org/webclient/?show=screen-2701))
1. Perform nuclei segmentation
2. Extract single cell embeddings
    - Using CellProfiler
    - Using DeepProfiler
3. Preprocess both kinds of embeddings using pycytominer
4. Classify single-cell phenotypes using models from the [phenotypic_profiling_model](https://github.com/WayScience/phenotypic_profiling_model/tree/main) repository.

These data were originally used as part of the publication [Way et al. 2021](https://doi.org/10.1091/mbc.E20-12-0784).

> Predicting cell health phenotypes using image-based morphology profiling
> Gregory P. Way, Maria Kost-Alimova, Tsukasa Shibue, William F. Harrington, Stanley Gill, Federica Piccioni, Tim Becker, Hamdah Shafqat-Abbasi, William C. Hahn, Anne E. Carpenter, Francisca Vazquez, and Shantanu Singh
> Molecular Biology of the Cell 2021 32:9, 995-1005

Note: Not all data are stored in this repository.
Some data are too large.

## Reproducibility
Specific code and steps used are available within each module folder.

The [Way Lab](https://www.waysciencelab.com/) always strives for readable, reproducible computational biology analyses and workflows. If you struggle to understand or reproduce anything in this repository please [file an issue](https://github.com/WayScience/cell-health-data/issues/new)!
