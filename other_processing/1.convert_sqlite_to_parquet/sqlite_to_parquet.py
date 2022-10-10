"""
Converting Sqlite files to parquet using pycyotminer's API
Erik Serrano, 2022

This script involves converting the downloaded sqlite data obtained from
figshare into parquet.
"""

import glob
from pathlib import Path
from typing import Union
from pycytominer.cyto_utils.cells import SingleCells


def convert_to_parquet(sqlite_path: Union[str, Path]) -> None:
    """Converts sqlite_path to parquet files. Generated parquet files are
    stored in the `cell-health-parquet-data` directory

    Parameters
    ----------
    sqlite_path : Union[str, Path]
        Path to sqlite file

    Return
    ------
    None
        Generates parquet files in ../cell-health-parquet-data/ directory
    """

    # creating single cell object
    sql_url = f"sqlite:///{sqlite_path}"
    sc_p = SingleCells(
        sql_url,
        strata=["Image_Metadata_Plate", "Image_Metadata_Well"],
        image_cols=["TableNumber", "ImageNumber"],
    )

    # setting up output paths and naming
    f_name = Path(sqlite_path).stem
    save_dir = Path(__file__).parent / "cell_health_parquet_data"
    save_dir.mkdir(exist_ok=True)
    save_path = save_dir / f"{f_name}.parquet"

    # converting to parquet files
    print(f"Converting {sqlite_path.name} into parquet format")
    sc_p.merge_single_cells(
        sc_output_file=save_path,
        output_type="parquet",
        join_on=["Metadata_well_position", "Image_Metadata_Well"],
    )


if __name__ == "__main__":

    # Locating directory that contains downloaded sqlite files
    sqlite_dir_path = (
        Path(__file__).parent.parent / "0.download-profiles-from-figshare/data"
    )
    if not sqlite_dir_path.is_dir():
        raise FileNotFoundError(
            "Unable to find directory containing sqlite files"
        )

    # collecting sqlite files from module 0
    glob_query = str(sqlite_dir_path / "*.sqlite")
    sqlite_paths = glob.glob(glob_query)
    if len(sqlite_paths) == 0:
        raise FileNotFoundError(
            "No sqlite files were found in module 0 data folder"
        )

    # converting every sqlite file to parquet
    print("Starting conversion")
    for sqlite_path in sqlite_paths:
        sqlite_path_obj = Path(sqlite_path)
        convert_to_parquet(sqlite_path_obj)
