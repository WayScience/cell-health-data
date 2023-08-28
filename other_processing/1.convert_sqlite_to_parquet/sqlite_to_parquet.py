"""
Converting Sqlite files to parquet using pycyotminer's API
Erik Serrano, 2022

This script involves converting the downloaded sqlite data obtained from
figshare into parquet.
"""

import pathlib
import cytotable


def convert_to_parquet(file_path: str) -> None:
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
    if not isinstance(file_path, str):
        raise ValueError("`file_path` must be ")

    # setting up file paths
    file_path_obj = pathlib.Path(file_path)
    parquet_dir = pathlib.Path("cell_health_parquet")
    parquet_dir.mkdir(exist_ok=True)
    dest_path = parquet_dir / f"{file_path_obj.stem}.parquet"

    # Since this is cell-health data, we need to use sqlite-clean before 
    # submitting to cytotable.convert()
    # 
    # Here is the related issue:
    # https://github.com/cytomining/CytoTable/issues/38
    #
    # This step will be removed once this issue is solved.

    # converting cell-health sqlite data into parquet files
    cytotable.convert(
        source_path=file_path,
        dest_path=str(dest_path),
        dest_datatype="parquet",
        source_datatype="sqlite",
    )

    print(f"MESSAGE: {file_path.stem} has been converted into parquet file")


if __name__ == "__main__":
    # Locating directory that contains downloaded sqlite files
    sqlite_dir_path = (
        pathlib.Path(__file__).parent.parent
        / "0.download-profiles-from-figshare/data"
    ).resolve(strict=True)

    # checking if the provided path is a directory
    if not sqlite_dir_path.is_dir():
        raise FileNotFoundError(
            "Unable to find directory containing sqlite files"
        )

    # collecting sqlite files from module 0
    sqlite_paths = list(sqlite_dir_path.glob("*.sqlite"))
    if not sqlite_paths:
        raise FileNotFoundError(
            "No sqlite files were found in module 0 data folder"
        )

    # converting every sqlite file to parquet
    print("Starting conversion")
    for sqlite_path in sqlite_paths:
        sqlite_path_obj = str(pathlib.Path(sqlite_path).resolve(strict=True))
        convert_to_parquet(sqlite_path_obj)
