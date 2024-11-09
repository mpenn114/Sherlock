# Note: This code is not really part of Sherlock, but has been included for completeness (mainly so I know where it is if I ever need to regenerate the test images)
# To run it, it requires the additional dependency piexif


import os
import random
from datetime import datetime

import piexif
from PIL import Image, ImageDraw

# Define folders and parameters
folders = {
    "test_images/folder_1": (50, (100, 60)),
    "test_images/folder_2": (30, (80, 60)),
}

# Ensure directories exist
for folder in folders:
    os.makedirs(folder, exist_ok=True)


def generate_image_with_blob(
    width: int, height: int, blob_radius: int = 5
) -> Image.Image:
    # Create a white image
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Random position for the black blob
    for _ in range(random.randint(0, 2)):
        blob_x = random.randint(blob_radius, width - blob_radius)
        blob_y = random.randint(blob_radius, height - blob_radius)

        # Draw black blob
        draw.ellipse(
            (
                blob_x - blob_radius,
                blob_y - blob_radius,
                blob_x + blob_radius,
                blob_y + blob_radius,
            ),
            fill="black",
        )

    return image


def save_image_with_exif(image: Image.Image, path: str, flash_value: int):
    # Initialize an empty EXIF dictionary
    exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "Interop": {}, "1st": {}}

    # Add DateTime and Make information to the EXIF metadata in the 0th IFD
    exif_dict["0th"][piexif.ImageIFD.Make] = "TestCamera"  # Example Make field
    exif_dict["0th"][piexif.ImageIFD.DateTime] = datetime.now().strftime(
        "%Y:%m:%d %H:%M:%S"
    )

    # Add Flash information to the Exif IFD (Exif is where Flash metadata is stored)
    exif_dict["Exif"][
        piexif.ExifIFD.Flash
    ] = flash_value  # Flash value to indicate day/night

    # Convert the EXIF dictionary to byte format
    exif_bytes = piexif.dump(exif_dict)

    # Save the image as JPEG with EXIF metadata
    image.save(path, "JPEG", exif=exif_bytes)


# Generate images with EXIF metadata
for folder, (num_images, size) in folders.items():
    for i in range(num_images):
        # Generate image with random blob
        img = generate_image_with_blob(*size)

        # Assign Flash value (24 for daytime, other for nighttime)
        flash_value = 24 if random.random() > 0.1 else 0

        # Save the image with EXIF metadata
        image_path = os.path.join(folder, f"image_{str(i+1).zfill(4)}.jpg")
        save_image_with_exif(img, image_path, flash_value)

print("Image generation and metadata saving complete.")
