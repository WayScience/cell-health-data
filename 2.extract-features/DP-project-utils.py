from importlib.resources import path
import pandas as pd
import pathlib
import shutil

from PIL import Image
import os


def copy_DP_files(
    project_path: pathlib.Path,
    config_name: str,
    checkpoint_name: str,
):
    """copy config and checkpoint files to their necessary location in DP project (located at project path)

    Args:
        project_path (pathlib.Path): path for DP project
        config_name (str): name of config file to copy
        checkpoint_name (str): name of checkpoint file to copy
    """

    # copy config file to DP project
    config_load_path = pathlib.Path(f"DP_files/{config_name}")
    config_save_path = pathlib.Path(f"{project_path}/inputs/config/{config_name}")
    config_save_path.parents[0].mkdir(parents=True, exist_ok=True)
    shutil.copyfile(config_load_path, config_save_path)

    # copy checkpoint file to DP project
    checkpoint_load_path = pathlib.Path(f"DP_files/{checkpoint_name}")
    checkpoint_save_path = pathlib.Path(
        f"{project_path}/outputs/efn_pretrained/checkpoint/{checkpoint_name}"
    )
    checkpoint_save_path.parents[0].mkdir(parents=True)
    shutil.copyfile(checkpoint_load_path, checkpoint_save_path)


def get_well_name(row: int, col: int) -> str:
    """get well name from row and col
    example: row 2, column 3 -> B3

    Args:
        row (int): row number
        col (int): col number

    Returns:
        str: well name
    """
    # convert row number to corresponding capitalized character in alphabet (via ASCII number) (1=A, 2=B, etc)
    return f"{chr(row+64)}{col}"


def compile_index_csv(
    images_load_path: pathlib.Path,
    DP_images_path: pathlib.Path,
    annotations: pd.DataFrame,
    object: str,
) -> pd.DataFrame:
    """compiles index csv (image metadata, channel image locations, reagent)

    Args:
        images_load_path (pathlib.Path): path to load images from 
        DP_images_path (pathlib.Path): path to DP project images folder
        annotations (pd.DataFrame): IDR study annotations metadata
        object (str): object to compile index csv for, must be "nuc" or "cyto"

    Returns:
        pd.DataFrame: index csv dataframe
    """

    index_csv_data = []

    for plate_path in images_load_path.iterdir():
        for image_folder in plate_path.iterdir():
            for image_file in image_folder.iterdir():
                # skip files without channel 1 in name
                if "ch1" not in image_file.name:
                    continue
                
                # get row and column number for image
                row = int(image_file.name[1:3])
                col = int(image_file.name[4:6])
                
                # get image metadata
                plate = plate_path.name
                well = get_well_name(row, col)
                site = image_file.name[7:9]
                
                # get reagent value for image
                image_annotations = annotations.loc[
                    (plate == annotations["Plate"]) & (annotations["Well"] == well)
                ]
                reagent = image_annotations.iloc[0]["Reagent Identifier"]
                if pd.isna(reagent):
                    reagent = "no reagent"
                
                # compile nuc file data
                if object == "nuc":
                    file_data = {
                        "Metadata_Plate": plate,
                        "Metadata_Well": well,
                        "Metadata_Site": site,
                        "Plate_Map_Name": f"{plate}_{well}_{site}",
                        "DNA": os.path.relpath(image_file, DP_images_path),
                        "Reagent": reagent,
                        "Reagent_Replicate": 1,
                    }
                    
                # compile cyto file data
                if object == "cyto":
                    channels = ["DNA", "ER", "RNA", "AGP", "Mito"]
                    channel_paths = []
                    
                    file_data = {
                        "Metadata_Plate": plate,
                        "Metadata_Well": well,
                        "Metadata_Site": site,
                        "Plate_Map_Name": f"{plate}_{well}_{site}",
                    }
                    
                    for index, channel in enumerate(channels):
                        channel_path = pathlib.Path(str(image_file).replace("ch1", f"ch{index+1}"))
                        file_data[channel]= os.path.relpath(channel_path, DP_images_path)
                    
                    file_data["Reagent"] = reagent
                    file_data["Reagent_Replicate"] = 1

                index_csv_data.append(file_data)

    return pd.DataFrame(index_csv_data)


def compile_training_locations(
    index_csv_path: pathlib.Path,
    segmentation_data_path: pathlib.Path,
    save_path: pathlib.Path,
    object: str,
):
    """compile well_frame-site-Nuclei.csv file with cell locations, save to in save_path/plate/ folder

    Args:
        index_csv_path (pathlib.Path): path to index.csv file for DeepProfiler project
        segmentation_data_path (pathlib.Path): path to segmentations folder with .tsv locations files
        save_path (pathlib.Path): path to save location files
        object (str): object to find segmentation locations for, must be "nuc" or "cyto"
    """
    index_csv = pd.read_csv(index_csv_path)
    for index, row in index_csv.iterrows():
        plate = row["Metadata_Plate"]
        well = row["Metadata_Well"]
        site = row["Metadata_Site"]

        # get identifier string for image
        identifier = row["DNA"].split("/")[-1].split("-")[0]

        # `Nuclei.csv` is hardcoded to be the expected file name for DeepProfiler
        locations_save_path = pathlib.Path(
            f"{save_path}/{plate}/{well}-{site}-Nuclei.csv"
        )

        # skip a field if its locations have already been determined
        if locations_save_path.is_file():
            print(f"{plate} + {identifier} already has locations compiled!")
        else:

            print(f"Compiling locations for {plate} + {identifier}")
            frame_segmentations_path = pathlib.Path(
                f"{segmentation_data_path}/{plate}/Images/{identifier}-{object}-segmented.tsv"
            )

            # handle errors for no locations file/no data
            try:
                frame_segmentations = pd.read_csv(
                    frame_segmentations_path, delimiter="\t"
                )
            except:
                print(f"No segmentation data for {frame_segmentations_path.name}")
                continue
            try:
                frame_segmentations = frame_segmentations[
                    ["Cell_ID", "Location_Center_X", "Location_Center_Y"]
                ]
            except KeyError:
                print(f"No segmentations for {frame_segmentations_path}")
                continue
            frame_segmentations = frame_segmentations.rename(
                columns={
                    "Location_Center_X": "Nuclei_Location_Center_X",
                    "Location_Center_Y": "Nuclei_Location_Center_Y",
                }
            )

            locations_save_path.parents[0].mkdir(parents=True, exist_ok=True)
            frame_segmentations.to_csv(locations_save_path, index=False)


def compile_project(
    project_path: pathlib.Path,
    checkpoint_name: str,
    annotations_path: pathlib.Path,
    images_load_path: pathlib.Path,
    object: str,
):
    """compile DP project

    Args:
        project_path (pathlib.Path): path to compile DP project to
        checkpoint_name (str): name of checkpoint to use in DP project (must be located in DP_files/)
        annotations_path (pathlib.Path): path to IDR annotations data
        images_load_path (pathlib.Path): path to load images to extract features from
        object (str): object to compile project for, must be "nuc" or "cyto"
    """
    # make project dir
    project_path.mkdir(parents=True, exist_ok=True)
    
    # copy necessary DP files from DP_files/ to DP project
    config_name = f"cell_health_{object}_config.json"
    copy_DP_files(project_path, config_name, checkpoint_name)
    
    # compile and save index.csv file to DP project
    annotations = pd.read_csv(annotations_path)
    index_save_path = pathlib.Path(f"{project_path}/inputs/metadata/index.csv")
    index_save_path.parents[0].mkdir(parents=True, exist_ok=True)
    print("compiling index.csv file...")
    DP_images_path = pathlib.Path(f"{project_path}/inputs/images")
    index_csv = compile_index_csv(images_load_path, DP_images_path, annotations, object)
    index_csv.to_csv(index_save_path, index=False)
    print("index.csv file saved!")

    # compile and save locations to DP project
    segmentation_data_path = pathlib.Path(
        "/media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/cell-health-segmented/"
    )
    locations_save_path = pathlib.Path(f"{project_path}/inputs/locations/")
    print("Compiling locations!")
    compile_training_locations(
        index_save_path, segmentation_data_path, locations_save_path, object
    )
    print("Done compiling locations!")
    