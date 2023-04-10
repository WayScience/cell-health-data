"""
Converting Sqlite files to parquet using pycyotminer's API
Erik Serrano, 2022

This script involves converting the downloaded sqlite data obtained from
figshare into parquet.
"""

from pathlib import Path
from typing import Union
import cytotable

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

    # obtain the sqlite file paths
    cytotable.convert()


if __name__ == "__main__":

    # Locating directory that contains downloaded sqlite files
    sqlite_dir_path = (
        Path(__file__).parent / "0.download-profiles-from-figshare/data"
    )
    if not sqlite_dir_path.is_dir():
        raise FileNotFoundError(
            "Unable to find directory containing sqlite files"
        )

    # collecting sqlite files from module 0
    glob_query = str(sqlite_dir_path / "*.sqlite")
    sqlite_paths = list(sqlite_dir_path.glob(glob_query))
    if not sqlite_paths:
        raise FileNotFoundError(
            "No sqlite files were found in module 0 data folder"
        )

    # converting every sqlite file to parquet
    print("Starting conversion")
    for sqlite_path in sqlite_paths:
        sqlite_path_obj = Path(sqlite_path)
        convert_to_parquet(sqlite_path_obj)
