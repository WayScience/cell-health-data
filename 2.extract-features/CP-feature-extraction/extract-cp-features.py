#!/usr/bin/env python
# coding: utf-8

# ### Import libraries

# In[1]:


import pathlib
import subprocess


# ### Extract CP features from each plate

# In[2]:


# data paths need to be changed to reflect the location of nuclei and segmentation mask images and feature save path
nuclei_images_load_path = pathlib.Path(
    "/media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/cell-health"
)
all_data_load_path = pathlib.Path(
    "/media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/"
)
features_save_path = pathlib.Path(
    "/media/roshankern/63af2010-c376-459e-a56e-576b170133b6/data/cell-health-nuc-CP/"
)

# path to CellProfiler pipeline
pipeline_path = pathlib.Path("process-cell-health.cppipe")
# iterate through plates in load path
for plate_path in nuclei_images_load_path.iterdir():
    print(f"Extracting CP features for plate {plate_path.name}...")

    # iterate through image paths in plates (there should only be one)
    for image_folder_path in plate_path.iterdir():

        # features folder that extracted CP features will be saved to
        features_folder_path = pathlib.Path(
            f"{features_save_path}/{plate_path.name}"
        )
        features_folder_path.mkdir(exist_ok=True, parents=True)

        # file to log CP output
        log_file_path = pathlib.Path(
            f"{features_save_path}/{plate_path.name}/CP_plate_run.log"
        )

        # extract features for particular plate
        with open(
            log_file_path,
            "w",
        ) as cellprofiler_output_file:
            # run CellProfiler for a illumination correction pipeline
            command_components = [
                "cellprofiler",
                "-c",
                "-r",
                "-p",
                str(pipeline_path.absolute()),
                "-o",
                str(features_folder_path.absolute()),
                "-i",
                f"{all_data_load_path.absolute()}",
                "-g",
                f"Metadata_Plate={plate_path.name}",
            ]
            command = " ".join(command_components)
            subprocess.run(
                command_components,
                stdout=cellprofiler_output_file,
                stderr=cellprofiler_output_file,
                check=True,
            )
            print(
                f"The CellProfiler run has been completed for {plate_path.name}. Please check log file for any errors."
            )

