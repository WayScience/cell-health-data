"""
Converting Sqlite files to parquet using pycyotminer's API
Erik Serrano, 2022

This script involves converting the downloaded sqlite data obtained from
figshare into parquet.
"""

import pathlib
from typing import Union
import cytotable

def convert_to_parquet(file_path: Union[str, pathlib.Path]) -> None:
    """Converts sqlite_path to parquet files. Generated parquet files are
    stored in the `cell-health-parquet-data` directory

    Parameters
    ----------
    file_path : Union[str, Path]
        Path to sqlite file

    Return
    ------
    None
        Generates parquet files in ../cell-health-parquet-data/ directory
    """

    # obtain the sqlite file paths
    if isinstance(file_path, str):
        file_path = pathlib.Path(file_path).resolve(strict=True)

    parquet_dir = pathlib.Path("cell_health_parquet")
    parquet_dir.mkdir(exist_ok=True)



    dest_path = parquet_dir / f"{file_path.stem}.parquet"
    cytotable.convert(source_path=sqlite_path,
                      dest_path=str(dest_path),
                      dest_datatype="parquet",
                      source_datatype="sqlite")

    print(f"MESSAGE: {file_path.stem} has been converted into parquet file")


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
