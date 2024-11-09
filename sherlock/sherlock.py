import json
import os
from typing import Any, Dict

import cv2
import numpy as np
import pandas as pd

from .background_image import make_background_image
from .config import EnvSettings
from .process_images import animal_finder
from .utils import (
    create_summary_csv,
    datetime_difference,
    extract_datetime,
    find_max_image_path,
    set_image_shape,
)

ENV = EnvSettings()


def process_folder(folder_path: str):
    """
    Process the images in a folder.

    Args:
        folder_path (str): The path to the folder
    """
    # Find max image
    max_image = find_max_image_path(folder_path)
    print(max_image)
    if not max_image:
        return

    # Set the shape
    set_image_shape(folder_path, max_image)

    # Read the stored image data in this folder
    json_path = f"{folder_path}/processed_data_{ENV.run_code}.json"
    if os.path.isfile(json_path):
        processed_data: Dict[str, Any] = json.load(open(json_path, "r"))
    else:
        processed_data = {"completed": False, "images": {}}

    image_index = 1
    while image_index < max_image + 1:
        if image_index in processed_data["images"]:
            print(f"Skipping image {image_index} as it has been previously processed")
            continue  # image already processed

        if not os.path.isfile(
            f"{folder_path}/{ENV.image_prefix}_{str(image_index).zfill(4)}.{ENV.image_suffix}"
        ):
            image_index += 1
            print(f"Skipping image {image_index} as it was not found")
            continue
        background_image, background_end_index, is_daytime = make_background_image(
            folder_path, image_index
        )
        used_images = background_end_index - image_index
        while image_index < background_end_index:

            if used_images < ENV.min_background_used:
                processed_data["images"][str(image_index)] = {
                    "status": "animal",
                    "reason": "insufficient background images",
                    "contours": 0,
                    "error": True,
                }
                print(
                    f"Skipping image {image_index} as insufficient background images (counting as true)"
                )
                image_index += 1
                continue
            else:
                image_path = f"{folder_path}/{ENV.image_prefix}_{str(image_index).zfill(4)}.{ENV.image_suffix}"
                image = cv2.imread(image_path)

                if image is None or background_image is None:
                    # Error processing image
                    if image_index in processed_data["images"]:
                        processed_data["images"][str(image_index)]["error"] = False
                    else:
                        processed_data["images"][str(image_index)] = {
                            "status": "error",
                            "error": True,
                            "contours": 0,
                        }
                    image_index += 1
                    continue
                image_static = image.copy()
                date_time = extract_datetime(image_path)
                lefts, rights, bottoms, tops = animal_finder(
                    image, background_image, is_daytime
                )
                size_tol = ENV.size_tol_day if is_daytime else ENV.size_tol_night
                background_tol = (
                    ENV.background_tol_day if is_daytime else ENV.background_tol_night
                )
                # Initialise animal found
                contours_found = 0
                # Test contours
                for i in range(len(lefts)):
                    region_width = rights[i] - lefts[i]
                    region_height = tops[i] - bottoms[i]

                    if region_width * region_height > size_tol:
                        if ENV.count_pixels == 1:

                            # Generate random sample positions using numpy
                            x_samples = np.random.randint(
                                lefts[i], rights[i], size=ENV.pixel_samples
                            )
                            y_samples = np.random.randint(
                                bottoms[i], tops[i], size=ENV.pixel_samples
                            )

                            # Extract image and background samples using vectorized operations
                            image_samples = image[x_samples, y_samples, :]
                            background_samples = background_image[
                                x_samples, y_samples, :
                            ]

                            # Calculate the pixel differences in a vectorized manner
                            pixel_diffs = np.abs(
                                image_samples.astype(int)
                                - background_samples.astype(int)
                            )
                            curr_dists = np.max(
                                pixel_diffs, axis=1
                            )  # Get max diff per pixel

                            # Check if any pixel meets the conditions
                            valid_pixels = np.all(
                                image_samples.astype(float) > ENV.colour_lower, axis=1
                            ) & np.all(
                                image_samples.astype(float) < ENV.colour_upper, axis=1
                            )

                            # Calculate the number of valid pixels
                            valid_pixel_count = np.sum(
                                (curr_dists > background_tol) & valid_pixels
                            )

                            # Check for black pixels
                            secondary_colour_pixels = np.sum(
                                np.all(
                                    image_samples.astype(float)
                                    < ENV.secondary_color_upper,
                                    axis=1,
                                )
                                & np.all(
                                    image_samples.astype(float)
                                    > ENV.secondary_color_lower,
                                    axis=1,
                                )
                            )

                            # Check if thresholds are exceeded
                            if (
                                valid_pixel_count / ENV.pixel_samples
                                > ENV.disturbance_tol
                                and secondary_colour_pixels / ENV.pixel_samples
                                > ENV.secondary_colour_tol
                            ):
                                contours_found += 1
                                if ENV.save_images:
                                    cv2.rectangle(
                                        image_static,
                                        (int(tops[i]), int(lefts[i])),
                                        (int(bottoms[i]), int(rights[i])),
                                        (0, 0, 255),
                                        4,
                                    )
                        else:
                            contours_found += 1
                            if ENV.save_images:
                                cv2.rectangle(
                                    image_static,
                                    (int(tops[i]), int(lefts[i])),
                                    (int(bottoms[i]), int(rights[i])),
                                    (0, 0, 255),
                                    4,
                                )

            if contours_found > 0:
                processed_data["images"][str(image_index)] = {
                    "status": "animal",
                    "reason": "contour found",
                    "contours": contours_found,
                }

                if ENV.save_images:
                    if not os.path.isdir(f"{folder_path}/positive_images/"):
                        os.mkdir(f"{folder_path}/positive_images/")

                    cv2.imwrite(
                        f"{folder_path}/positive_images/{ENV.image_prefix}_{str(image_index).zfill(4)}.{ENV.image_suffix}",
                        image_static,
                    )
            else:
                if image_index in processed_data["images"]:
                    processed_data["images"][str(image_index)]["contours"] = 0
                else:
                    processed_data["images"][str(image_index)] = {
                        "status": "no animal",
                        "reason": "no contour found",
                        "contours": 0,
                    }
            if contours_found > 0:
                for trial_index in range(
                    image_index - ENV.adjacency, image_index + ENV.adjacency
                ):
                    if trial_index <= 0 or trial_index > max_image:
                        continue
                    if date_time == "1800-01-01 00:00:00":
                        print("Error: Could not parse date from image metadata")
                    if trial_index == image_index:
                        continue

                    trial_image_path = f"{folder_path}/{ENV.image_prefix}_{str(image_index).zfill(4)}.{ENV.image_suffix}"
                    if not os.path.isfile(trial_image_path):
                        continue

                    trial_date_time = extract_datetime(trial_image_path)

                    if (
                        datetime_difference(trial_date_time, date_time)
                        < ENV.datetime_adjacency_tolerance
                    ):
                        if str(trial_index) in processed_data["images"]:
                            processed_data["images"][str(trial_index)][
                                "status"
                            ] = "animal"
                            processed_data["images"][str(trial_index)][
                                "adjacency"
                            ] = True
                            if (
                                processed_data["images"][str(trial_index)]["reason"]
                                == "no contour found"
                            ):
                                processed_data["images"][str(trial_index)][
                                    "reason"
                                ] = "adjacent"

                        else:
                            processed_data["images"][str(trial_index)] = {
                                "status": "animal",
                                "reason": "adjacent",
                                "contours": 0,
                                "adjacency": True,
                            }
            # Save JSON at each step
            json.dump(processed_data, open(json_path, "w"))
            print(f"Image {image_index} processed")
            image_index += 1
    processed_data["completed"] = True
    json.dump(processed_data, open(json_path, "w"))
    create_summary_csv(processed_data, folder_path)
