"""
script: check.py

Checks if the downloaded data is neither different or corrupt. Here we use md5 hash to
ensure that the contents and integrity of the data is unchanged.
"""

import glob
import pathlib
from hashlib import md5
from typing import Optional, Union

# credit: https://sebest.github.io/post/a-quick-md5sum-equivalent-in-python/
def generate_md5_hash(
    fpath: Union[str, pathlib.Path], buffer_size: Optional[int] = 8192
) -> tuple[str, str]:
    """Creates a md5 hash of all contents within given file.

    Parameters
    ----------
    fpath : pathlib.Path
        path to file to hash

    buffer_size : int
        chuck of data loaded into memory when hashing. The higher the value, the
        more memory it uses. Default is 8192 bytes.
    Returns
    -------
    str
        md5 hash id that represents the file and it's contents

    Raises
    ------
    FileNotFoundError
        raised if invalid path or a non-file object is provided (E.G: directory)
    ValueError
        raised if provided file does not end with `.parquet`
    """
    # converting str into pathlib.Path object
    if isinstance(fpath, str):
        fpath = pathlib.Path(fpath)

    # Checking
    if not fpath.is_file():
        e_msg = f"Provided file {str(fpath)} is not valid or not a file"
        raise FileNotFoundError(e_msg)
    if fpath.suffix != ".parquet":
        raise ValueError("pathlib.Path provided does not point to a parquet file")

    # initializing hashing object
    md5_obj = md5(usedforsecurity=False)

    # opening file and loading contents based on buffer size
    with open(fpath, "rb") as infile:

        # creating a start point for while loop
        data = infile.read(buffer_size)

        # iterating all contents in data file until nothing is loaded
        while data:

            # updating md5 object with loaded data
            # loading the next set of data
            md5_obj.update(data)
            data = infile.read(buffer_size)

    # return the hash id as string
    return (md5_obj.hexdigest(), str(fpath))


def check_integrity(
    parquet_files: list[str], hashed_files_dict: dict[str, str]
):
    """Checks data integrity of converted sqlite files

    Parameters
    ----------
    parquet_files : list[str]
        list of parquet files paths
    hashed_files_dict : dict[str,str]
        contained file path and md5sum has as key value pairs
    Raises:
    """
    print("Checking parquet data integrity ")
    for parquet_file in parquet_files:
        file_name = pathlib.Path(parquet_file).name
        print(f"Checking {file_name}")

        # running md5sum in terminal
        md5hash, _ = generate_md5_hash(parquet_file)
        if hashed_files_dict[file_name] != md5hash:
            raise ValueError(f"Data discrepancy captured in {parquet_file}")


if __name__ in "__main__":
    # This script loads the predefined MD5 hash that has been generated from 
    # a previous study:
    # https://github.com/broadinstitute/cell-health/blob/master/0.download-data/md5_sums.txt
    #
    # and compares it with the generated MD5 hashes from the downloaded dataset.

    # loading in hashed parquet files and generated parquet files
    hash_check_file = pathlib.Path(__file__).parent / "hashed_parquet.txt"
    parquet_file_path = (
        pathlib.Path(__file__).parent.parent / "0.download-profiles-from-figshare/data"
    )

    parquet_data_dir = pathlib.Path(__file__).parent / "cell_health_parquet_data"
    parquet_files = glob.glob(f"{str(parquet_data_dir)}/*.parquet")
    print(parquet_files)
    hashed_files_dict = {}
    with open(file=hash_check_file, mode="r", encoding="utf-8") as f:
        for line in f:
            path, _hash = line.rstrip("\n").split()
            hashed_files_dict[path] = _hash

    check_integrity(parquet_files, hashed_files_dict)
