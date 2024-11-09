import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import cv2
import pandas as pd
from PIL import Image
from PIL.ExifTags import TAGS

from .config import EnvSettings

ENV = EnvSettings()


def create_summary_csv(processed_data: Dict[str, Any], folder_path: str):
    """
    Create a summary CSV for a folder.

    Args:
        processed_data (Dict[str,Any]): The processed data
        folder_path (str): The folder path
    """
    summary_data: List[pd.DataFrame] = []
    for image_index, image_datum in processed_data.items():
        summary_data.append(
            pd.DataFrame(
                {
                    "image_index": [image_index],
                    "animal": [image_datum["status"] == "animal"],
                    "adjacent": ["adjacency" in image_datum],
                    "contours": [image_datum["contours"]],
                    "reason": [image_datum["reason"]],
                    "error": ["error" in image_datum],
                }
            )
        )

    pd.concat(summary_data).to_csv(f"{folder_path}/summary_data.csv")


def datetime_difference(dt1: str, dt2: str) -> bool:
    """
    Compares two datetime strings and returns whether the absolute difference
    between them is less than a predefined tolerance.

    The function parses the input datetime strings in the format "YYYY-MM-DD HH:MM:SS",
    calculates the time difference between the two datetime objects, and checks if this
    difference is less than a specified tolerance, which is defined by
    `ENV.datetime_adjacency_tolerance`.

    Args:
        dt1 (str): The first datetime string in the format "YYYY-MM-DD HH:MM:SS".
        dt2 (str): The second datetime string in the format "YYYY-MM-DD HH:MM:SS".

    Returns:
        bool: True if the absolute time difference between `dt1` and `dt2` is less than
              the tolerance, otherwise False.
    """
    # Parse the datetime strings into datetime objects
    format_str = (
        "%Y-%m-%d %H:%M:%S"  # assuming the format is like "YYYY-MM-DD HH:MM:SS"
    )
    dt1_obj = datetime.strptime(dt1, format_str)
    dt2_obj = datetime.strptime(dt2, format_str)

    # Calculate the time difference between the two datetime objects
    time_diff = abs(dt1_obj - dt2_obj)

    # Return True if the difference is less than the tolerance
    return time_diff < timedelta(seconds=ENV.datetime_adjacency_tolerance)


def extract_datetime(image_path: str) -> str:
    """
    Extract the DateTime and Make metadata from the EXIF data of an image.

    Args:
        image_path (str): The file path of the image.

    Returns:
        str: The datetime
    """
    datetime_value = "1800-01-01"

    try:
        image = Image.open(image_path)
        exif_data = image.getexif()

        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)

            # Decode bytes to string if necessary
            if isinstance(value, bytes):
                value = value.decode()

            # Extract DateTime value
            if tag_name == "DateTime":
                datetime_value = value

    except Exception as e:
        # Handle potential errors (e.g., file not found, no EXIF data)
        datetime_value = "1800-01-01"

    return datetime_value


def find_max_image_path(folder_path: str) -> Optional[int]:
    """
    Find the image with the highest index in the specified folder by checking from the maximum index (9999)
    downwards until an image is found, following the naming convention defined by ENV.image_prefix and ENV.image_suffix.

    Args:
        folder_path (str): The folder where the images are stored.

    Returns:
        Optional[str]: The path of the image with the highest index, or None if no matching images are found.
    """
    # Start with the maximum index (9999) and decrement until an image is found
    for image_index in range(9999, -1, -1):
        image_path = f"{folder_path}/{ENV.image_prefix}_{str(image_index).zfill(4)}.{ENV.image_suffix}"

        if os.path.isfile(image_path):
            return image_index

    # Return None if no matching image is found
    print(f"Warning - No images found in {folder_path}")
    return None


def set_image_shape(path_to_file: str, image_max: int):
    """
    Get the "standard" image shape for this set of images.

    Note that some images may have different shapes at the start or end of the sequence

    Args:
        path_to_file (str): The directory path where the images are stored.
        image_max (int): The maximum image index to identify the middle image.

    Returns:
        int: The number of images that do not have the same dimensions as the middle image.
    """
    mid_image_index = str(int(image_max / 2)).zfill(4)
    mid_image_path = f"{path_to_file}IMG_{mid_image_index}.JPG"
    if os.path.isfile(mid_image_path):
        mid_image = cv2.imread(mid_image_path)
        ENV.image_size = mid_image.shape

    else:
        print(
            "Warning: Middle image not found to test shape. You may need to specify the image size directly in sherlock/model/config/EnvSettings.image_size"
        )
