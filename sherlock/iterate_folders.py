import os
from pathlib import Path

from .config import EnvSettings
from .sherlock import process_folder

ENV = EnvSettings()


def run_sherlock(root_path: str = ENV.root_directory):
    """
    Run Sherlock on a range of folders.

    Args:
        root_path (str): The root path
    """
    # Run folder if it meets conditions
    folder_path = Path(root_path)
    file_count = len(list(folder_path.glob(f"*{ENV.image_suffix}")))
    if (
        file_count > ENV.min_images_process
        and root_path.split("/")[-1] != "positive_images"
    ):
        print(f"Running folder {root_path}")

        process_folder(root_path)

    # Process subfolders
    if os.path.isdir(root_path):
        for folder in os.listdir(root_path):
            run_sherlock(f"{root_path}/{folder}")
