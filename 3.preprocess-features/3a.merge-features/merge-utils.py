from importlib.resources import path
import math
import pathlib
import uuid

import pandas as pd


def format_cp_well(cp_well):
    row = int(cp_well[1:3])
    formatted_row = chr(64 + row)

    col = int(cp_well[4:6])

    return f"{formatted_row}{col}"


def format_cp_site(cp_site):
    # first, convert to int to remove any leading zeroes
    # next, convert to str to match DP format
    site = str(int(cp_site[1:3]))
    return site


def load_cp_feature_data(cp_output_path: pathlib.Path, plate: str):
    cp_plate_path = pathlib.Path(f"{cp_output_path}/Nuclei.csv")
    cp_plate_cell_1 = pd.read_csv(cp_plate_path, nrows=1)

    all_cols = cp_plate_cell_1.columns.to_list()
    cols_to_load = [
        "Metadata_Field",
        "Metadata_Well",
        "Location_Center_X",
        "Location_Center_Y",
    ]

    # We only want to get CP data from the feature modules below (_ ensures it is found as module name)
    cp_feature_modules = [
        "AreaShape_",
        "Granularity_",
        "Intensity_",
        "Neighbors_",
        "RadialDistribution_",
        "Texture_",
    ]

    # remove CP columns that dont have a feature module as a substring
    for col in all_cols:
        if any(col.startswith(feature_module) for feature_module in cp_feature_modules):
            cols_to_load.append(col)

    cp_plate = pd.read_csv(cp_plate_path, usecols=cols_to_load)

    # insert plate at beginning of dataframe
    # REMOVE WHEN WORKING WITH FINAL DATA
    cp_plate["Metadata_Plate"] = plate
    column_to_move = cp_plate.pop("Metadata_Plate")
    cp_plate.insert(0, "Metadata_Plate", column_to_move)

    # insert locations at beginning of dataframe
    # REMOVE WHEN WORKING WITH FINAL DATA
    column_to_move = cp_plate.pop("Location_Center_Y")
    cp_plate.insert(0, "Location_Center_Y", column_to_move)
    column_to_move = cp_plate.pop("Location_Center_X")
    cp_plate.insert(0, "Location_Center_X", column_to_move)

    # convert well and field to one usable for merging
    cp_plate["Metadata_Well"] = cp_plate["Metadata_Well"].apply(format_cp_well)
    cp_plate["Metadata_Field"] = cp_plate["Metadata_Field"].apply(format_cp_site)
    cp_plate = cp_plate.rename(columns={"Metadata_Field": "Metadata_Site"})

    return cp_plate


def full_loc_map(dp_coord: tuple, cp_image_data_locations: pd.Series) -> tuple:
    """
    helper function for merge_CP_DP_batch_data
    get cp_coord from cp_image_data_locations that is closest to dp_coord

    Parameters
    ----------
    dp_coord : tuple
        dp coord to find closest cp coord for
    cp_image_data_locations : pd.Series
        series of cp coords to get closest one from

    Returns
    -------
    tuple
        closest cp_coord to given dp_coord
    """
    return min(
        cp_image_data_locations,
        key=lambda cp_coord: math.hypot(
            cp_coord[0] - dp_coord[0], cp_coord[1] - dp_coord[1]
        ),
    )


def merge_CP_DP_image_data(
    cp_image_data: pd.DataFrame,
    dp_image_data: pd.DataFrame,
    add_cell_uuid: bool = True,
) -> pd.DataFrame:

    # covert x and y coordiantes to integers
    cp_image_data[["Location_Center_X", "Location_Center_Y"]] = cp_image_data[
        ["Location_Center_X", "Location_Center_Y"]
    ].apply(pd.to_numeric)
    dp_image_data[["Location_Center_X", "Location_Center_Y"]] = dp_image_data[
        ["Location_Center_X", "Location_Center_Y"]
    ].apply(pd.to_numeric)

    # check batch data have same number of rows (cells)
    # if batch data have different number of cells, raise an error because they must not have close segmentations
    if cp_image_data.shape[0] != dp_image_data.shape[0]:
        raise IndexError("Batch data have different number of rows (cells)!")

    # hide warning for pandas chained assignment
    # this hides the warnings produced by main necessary chained assingments with pandas (can't use .iloc[] for some operations)
    pd.options.mode.chained_assignment = None

    # get cp and dp column names
    cp_columns = cp_image_data.columns
    dp_columns = dp_image_data.columns
    # get metadata columns (columns that show up in both dataframes)
    metadata_columns = [col for col in cp_columns if col in dp_columns]

    # remove metadata columns from cp and dp columns
    cp_columns = set(cp_columns) - set(metadata_columns)
    dp_columns = set(dp_columns) - set(metadata_columns)

    # add CP and DP prefixes to their respective columns
    cp_image_data = cp_image_data.rename(
        columns={col: f"CP__{col}" for col in cp_columns}
    )
    dp_image_data = dp_image_data.rename(
        columns={col: f"DP__{col}" for col in dp_columns}
    )

    # create a location column with x and y coordinates as tuple
    cp_image_data["Full_Location"] = list(
        zip(
            cp_image_data["Location_Center_X"],
            cp_image_data["Location_Center_Y"],
        )
    )
    dp_image_data["Full_Location"] = list(
        zip(
            dp_image_data["Location_Center_X"],
            dp_image_data["Location_Center_Y"],
        )
    )

    # make location for dp match the closest cp location (distance minimized with hypotenuse)
    dp_image_data["Full_Location"] = dp_image_data["Full_Location"].map(
        lambda dp_coord: full_loc_map(dp_coord, cp_image_data["Full_Location"])
    )

    # drop metadata columns from DP before merge
    dp_image_data = dp_image_data.drop(columns=metadata_columns)

    # merge cp and dp data on location
    merged_image_data = pd.merge(cp_image_data, dp_image_data, on="Full_Location")

    # rename reagent and platemap columns (important metadata)
    merged_image_data = merged_image_data.rename(
        columns={
            "DP__Metadata_Reagent": "Metadata_Reagent",
            "DP__Metadata_Plate_Map_Name": "Metadata_Plate_Map_Name",
        }
    )

    # drop unecessary columns
    merged_image_data = merged_image_data.drop(
        columns=[
            "Full_Location",
            "DP__Metadata_DNA",
            "DP__Metadata_Reagent_Replicate",
            "DP__Metadata_Model",
        ]
    )

    # add cell uuid to merged data to give each cell a unique identifier
    if add_cell_uuid:
        cell_uuids = [uuid.uuid4() for _ in range(merged_image_data.shape[0])]
        merged_image_data.insert(loc=0, column="Metadata_Cell_UUID", value=cell_uuids)

    # sort columns into most readable format
    all_cols = merged_image_data.columns.to_list()
    sorted_cols = [
        [col for col in all_cols if "Location_" in col],
        [col for col in all_cols if "Metadata_" in col],
        [col for col in all_cols if "CP_" in col],
        [col for col in all_cols if "DP_" in col],
    ]
    # flatten sorted cols list
    sorted_cols = [col for sublist in sorted_cols for col in sublist]

    # add merged image data to the compilation list
    return merged_image_data[sorted_cols]