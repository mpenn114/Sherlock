from typing import Any, Dict, List, Tuple

import cv2
import numpy as np
from PIL import Image
from PIL.ExifTags import TAGS

from .config import EnvSettings

ENV = EnvSettings()


def make_background_image(
    folder_path: str, current_image_index: int
) -> Tuple[np.ndarray | None, int, bool]:
    """
    Make the background image from a set of images.

    Args:
        folder_path (str): The path to the image folder
        current_image_index (int): The current image index

    Returns:
        np.ndarray: The background image
        int: The maximum index used in the background image
        bool: Whether the background image was day or night
    """
    images: List[np.ndarray] = []

    for image_index in range(
        current_image_index, current_image_index + ENV.background_max_images
    ):
        image_path = f"{folder_path}/{ENV.image_prefix}_{str(image_index).zfill(4)}.{ENV.image_suffix}"
        image = cv2.imread(image_path)
        if isinstance(image, np.ndarray):

            if image_index == current_image_index:
                day_night_background = daytime_test(image, image_path)
            else:
                day_night_image = daytime_test(image, image_path)

                if day_night_image == day_night_background:
                    images.append(image)

                else:
                    # New day/night period
                    break
        else:
            day_night_background = False
            break
    if len(images) > 0:
        background_image = np.median(images, axis=0)
    else:
        background_image = None

    return background_image, image_index, day_night_background


def daytime_test(image: np.ndarray, image_path: str) -> bool:
    """
    Test whether or not the image is a daytime image.

    Args:
        image (np.ndarray): The image
        image_path (str): The image path

    Returns:
        bool: True if it is a daytime image
    """
    image_metadata = get_image_metadata(image_path)
    if "Flash" in image_metadata:
        return image_metadata["Flash"] == 24

    else:
        if not ENV.image_metadata_warning_shown:

            print('Warning: No field "Flash" found in image metadata')
            ENV.image_metadata_warning_shown = True

        return daytime_test_sample(image)


def daytime_test_sample(
    image, num_samples=50, threshold_count=10, contrast_threshold=20
):
    """
    Determine if an image was taken during the day based on random pixel sampling.

    Randomly samples pixels within the image and checks if the difference between
    the maximum and minimum color values exceeds a specified contrast threshold.
    If the count of pixels meeting this condition exceeds `threshold_count`,
    returns True (day); otherwise, False (not day).

    Args:
        image (numpy.ndarray): The input image as a 2D or 3D array.
        num_samples (int, optional): Number of random pixels to sample. Default is 50.
        threshold_count (int, optional): Minimum number of pixels required to classify
                                         the image as day. Default is 10.
        contrast_threshold (int, optional): The minimum contrast difference between max
                                            and min pixel values to consider a sample
                                            as high contrast. Default is 20.

    Returns:
        bool: True if the image is classified as day, False otherwise.
    """
    # Convert the image to dtype=int to prevent overflow in calculations
    image = image.astype(int)

    # Generate random indices for sampling
    y_indices = np.random.randint(0, image.shape[0], num_samples)
    x_indices = np.random.randint(0, image.shape[1], num_samples)

    # Extract random samples and calculate the color range for each sample
    samples = image[y_indices, x_indices]
    contrast = np.max(samples, axis=-1) - np.min(samples, axis=-1)

    # Count how many samples exceed the contrast threshold
    dcount = np.sum(contrast > contrast_threshold)

    # Determine if daytime based on the threshold count
    return dcount > threshold_count


def get_image_metadata(image_path: str) -> Dict[str, Any]:
    """
    Get metadata from an image.

    Args:
        image_path (str): The path to the image

    Returns:
        Dict[str,Any]: The metadata
    """
    image = Image.open(image_path)
    exif_data = image._getexif()

    if exif_data is None:
        if not ENV.image_metadata_warning_shown:
            print("Warning: Metadata could not be extracted")
            ENV.image_metadata_warning_shown = True
        return {}

    metadata = {TAGS.get(tag, tag): value for tag, value in exif_data.items()}

    return metadata
