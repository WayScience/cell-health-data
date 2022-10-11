"""
Download Single Cell Cell Painting Profiles in parallel
Erik Serrano, 2022
Modified from a script written by Gregory Way, 2019
https://github.com/broadinstitute/cell-health/blob/master/0.download-data/download.py

These data were output from a CRISPR and Cell Painting experiment.
A microscope took pictures of all cells under several CRISPR perturbations.
The data were processed by a custom CellProfiler pipeline.
In the pipeline, we measured several morphology features for every single cell.
We then aggregated the output of CellProfiler using cytominer-database.
Cytominer-database compiles all single cell profiles into a single `sqlite` database.
We uploaded the `sqlite` files to NIH Figshare, where they are publicly available:
https://nih.figshare.com/articles/dataset/Cell_Health_-_Cell_Painting_Single_Cell_Profiles/9995672/1.

This pipeline introduces an newer version of the cell health dataset (version 6)
. Downloaded sqlite files are converted into parquet files providing improved
efficiency in data storage and retrieval.

*Important Note*
These files are large (~130 GB Total).
"""
from typing import Union
from pathlib import Path
import multiprocessing as mp
import requests


def download_sqlite_file(filename: Union[str, Path], url: str):
    """Downloads Single-Cell Cell painting profiles from Figshare data
    repository

    Parameters
    ----------
    filename : Union[str, Path]
        Path to store downloaded profiles
    url : str
        Url that downloads specific profile data.

    Returns
    -------
    None
        All downloaded profiles will be stored in the `./data` directory
    """

    if isinstance(filename, str):
        filename = Path(filename)

    plate_name = filename.name
    print(f"Now downloading... {plate_name}")
    with requests.get(url, stream=True) as sql_request:
        sql_request.raise_for_status()
        with open(filename, "wb") as sql_fh:
            for chunk in sql_request.iter_content(chunk_size=786432000):
                if chunk:
                    assert isinstance(chunk, object)
                    sql_fh.write(chunk)


if __name__ == "__main__":

    # file to downloaded
    # -- plate name with figshare ID
    file_info = {
        "SQ00014610": "18028784",
        "SQ00014611": "18508583",
        "SQ00014612": "18505937",
        "SQ00014613": "18506036",
        "SQ00014614": "18031619",
        "SQ00014615": "18506108",
        "SQ00014616": "18506912",
        "SQ00014617": "18508316",
        "SQ00014618": "18508421",
    }

    # creating data directory
    download_dir_obj = Path(__file__).parent / "data"
    download_dir_obj.mkdir(exist_ok=True)

    # collect all function inputs in a list
    func_params_list = []
    for plate in file_info:
        figshare_id = file_info[plate]
        filename = download_dir_obj / f"{plate}.sqlite"
        if filename.is_file():
            continue
        url = f"https://nih.figshare.com/ndownloader/files/{figshare_id}"
        func_params_list.append([filename, url])

    # initializing parallelization
    n_jobs = len(file_info)
    if n_jobs > mp.cpu_count():
        n_jobs = mp.cpu_count()
    with mp.Pool(processes=n_jobs) as pool:
        pool.starmap(download_sqlite_file, func_params_list)
        pool.close()
        pool.join()
