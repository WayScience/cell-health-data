
```json

        "CONFIG_JOINS": """
            WITH Image_Filtered AS (
                SELECT
                    Metadata_ImageNumber,
                    Image_Metadata_Well,
                    Image_Metadata_Plate
                FROM
                    read_parquet('image.parquet')
                )
            SELECT
                *
            FROM
                Image_Filtered AS image
            LEFT JOIN read_parquet('cytoplasm.parquet') AS cytoplasm ON
                cytoplasm.Metadata_ImageNumber = image.Metadata_ImageNumber
            LEFT JOIN read_parquet('cells.parquet') AS cells ON
                cells.Metadata_ImageNumber = cytoplasm.Metadata_ImageNumber
                AND cells.Cells_Number_Object_Number = cytoplasm.Cytoplasm_Parent_Cells
            LEFT JOIN read_parquet('nuclei.parquet') AS nuclei ON
                nuclei.Metadata_ImageNumber = cytoplasm.Metadata_ImageNumber
                AND nuclei.Nuclei_Number_Object_Number = cytoplasm.Cytoplasm_Parent_Nuclei

```


_modified from [EmbeddedArtistry](https://embeddedartistry.com/blog/2017/08/04/a-github-pull-request-template-for-your-projects/)_
_referenced with modifications from [pycytominer](https://github.com/cytomining/pycytominer/blob/master/.github/PULL_REQUEST_TEMPLATE.md)_

# Description

This PR focuses adding CellProfiler legacy presets for `CytoTable`'s `convert()` function. 

**What motivated you to make this change?**

[Datasets](https://nih.figshare.com/articles/dataset/Cell_Health_-_Cell_Painting_Single_Cell_Profiles/9995672/1) produced by older version of [CellProfiler](https://github.com/CellProfiler/CellProfiler) (For example: ver 2.X) contain different naming schemes, hence causing errors with the current presets that exists within `CytoTable` 


This PR introduces a new preset called `cellprofiler_legacy`, which contains the correct presets allowing conversion from datasets produced from older versions of `CellProfiler` to `parquet` files.


## What is the nature of your change?

- [ ] Bug fix (fixes an issue).
- [X] Enhancement (adds functionality).
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected).
- [ ] This change requires a documentation update.

# Checklist

Please ensure that all boxes are checked before indicating that a pull request is ready for review.

- [X] I have read the [CONTRIBUTING.md](CONTRIBUTING.md) guidelines.
- [X] My code follows the style guidelines of this project.
- [X] I have performed a self-review of my own code.
- [X] I have commented my code, particularly in hard-to-understand areas.
- [ ] I have made corresponding changes to the documentation.
- [X] My changes generate no new warnings.
- [ ] New and existing unit tests pass locally with my changes.
- [ ] I have added tests that prove my fix is effective or that my feature works.
- [ ] I have deleted all non-relevant text in this pull request template.
