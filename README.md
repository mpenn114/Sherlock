# Sherlock
This repository contains a code package, Sherlock, which provides an easy-to-use tool for processing camera trapping images.

Its aim is to remove false positive images - that is, principally, images where the camera has been triggered by a very small disturbances, such as a plant blowing in the wind. If images containing a specific species is being targeted, it also allows for the user to easily customise parameters to set the colour of the deisred animals. This can help to filter out images containing other animals, and thus increase the accuracy of the code.

This code is aimed to be usable by someone with no prior coding experience. To help this, a guide to installing Python (the language which Sherlock is written in) is provided at the end of this readme.

# Introduction

Sherlock is designed to run through multiple folder of images, and requires only the root folder of these images. It will then look through all subfolders and process each image contained in them.

A description of the method behind this code can be found at

https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.14254

Note that this code is now at version 2 - previous notebook-based implementations can be found within the sherlock_v1 folder.

# Running Sherlock

You can copy the code for Sherlock onto your computer by opening a new Jupyter notebook on your computer Then, there should be a textbox with your cursor inside it. If you have Git installed on your computer (which you can install from here https://github.com/git-guides/install-git), you can copy the code for Sherlock by copying

!git clone https://github.com/mpenn114/Sherlock

into this textbox, and then pressing the run button (which is a button in the row of buttons above the textbox - it looks like a "play" button). You should then be able to see a folder called "sherlock" on the left hand side of the screen. Double-click on this folder to open it, and then double-click on the file "main_notebook.ipynb" to open the notebook for Sherlock. This should then appear on the right hand window.

Below is the list of variables which can be configured for Sherlock. You can change these variables by editing the values in the following file:

sherlock/config.py

Note that in particular, you will need to change the root_directory variable, and perhaps the image prefix and image suffix. There are also a range of other variables which can be adjusted to optimise the performance of the code.

Note also that Sherlock saves its outputs and, if it is restarted, will not reprocess previously-processed images, provided the variable run_code is kept the same.

# Variables

| Name                        | Default Value                  | Description                                                                           |
|-----------------------------|--------------------------------|---------------------------------------------------------------------------------------|
| `root_directory`            | `"."`                           | The root directory for the images.                                                   |
| `image_prefix`              | `"IMG"`                        | The prefix for the image files                                                        |
| `image_suffix`              | `"JPG"`                        | The suffix for the image files                                                        |
| `min_images_process`        | `1`                            | The minimum number of images in a folder in order to process it                                |                                                  |
| `background_max_images`     | `100`                          | Max number of images to use when creating a background image.                                     |
| `min_background_used`       | `5`                            | Minimum number of images to count as a viable background (otherwise all images associated with it are returned as positive)                             |
| `sample_size`               | `5000`                         | Number of pixels to sample per image. Higher numbers lead to more accuracy, but will slow down the code                                              |
| `bounces`                   | `4`                            | Number of iterations of the bounce algorithm. Higher numbers lead to more contours being merged (which can be unhelpful if this number is too high). Higher numbres also slow down the code                                             |
| `colour_upper`              | `np.array([255, 255, 255])`   | Upper bound of color range to use when sampling pixels. **Note that these are in BGR not RGB**. The default value will accept all pixels.                                                          |
| `colour_lower`              | `np.array([0, 0, 0])`         | Lower bound of color range when sampling pixels. **Note that these are in BGR not RGB**. The default value will accept all pixels                                                          |
| `greyscale_parameter`       | `75`                           | Max range of colors in a pixel to be accepted. Setting to 256 will accept all pixels.                                                      |
| `background_tol_day`        | `75`                           | Minimum distance from background for a pixel to be accepted in daytime.                          |
| `background_tol_day`        | `75`                           | Minimum distance from background for a pixel to be accepted at night.     
| `image_size`                | `(1080, 720, 3)`               | The default image size; overridden as code runs                                       |
| `count_pixels`              | `True`                         | Whether or not to count pixels in a contour before accepting                   |
| `pixel_samples`             | `100`                          | Number of pixels to sample to assess disturbance proportion                           |
| `disturbance_tol`           | `0.1`                          | Minimum proportion of pixels that are a disturbance for contour acceptance            |
| `size_tol_day`              | `30000`                        | Required area (in pixels squared) for a contour to be accepted as an animal in daytime|
| `size_tol_night`            | `5000`                         | Required area at night                                                                |
| `secondary_color_upper`     | `np.array([75, 75, 75])`      | Secondary color upper bound for contour assessment (used only after contours have been created)                                   |
| `secondary_color_lower`     | `np.array([0, 0, 0])`         | Secondary color lower bound                                                           |
| `secondary_colour_tol`      | `0.05`                         | Tolerance for the proportion of pixels satisfying secondary color constraints in contours                                             |
| `save_images`               | `False`                        | Whether or not to save images (saved images will include contours marked on)                                                       |
| `adjacency`                 | `1`                            | Number of adjacent images to record as positives  (provided they satisfy the datetime tolerance)                                    |                                                   |
| `datetime_adjacency_tolerance` | `20`                     | Max of seconds between the accepted image and another image to count as adjacent
| `run_code`                  | `1`                            | The run code for this execution                                                    |

<h3> Installing Python, Anaconda and Jupyter Lab </h3>

Anaconda (and thus, Python) can be installed by visiting:

Windows: https://docs.anaconda.com/anaconda/install/windows/

Mac: https://docs.anaconda.com/anaconda/install/mac-os/

Linux: https://docs.anaconda.com/anaconda/install/linux/

Once Anaconda has been installed, you should be able to find "Anaconda Prompt", and open it to get a command window. Type 

conda install -c conda-forge jupyterlab

into this window and press enter to install Jupyter Lab

<h3> Opening Jupyter Lab </h3>

To open Jupyter Lab, open Anaconda Prompt, type in 

jupyter lab

and then press enter. It should open in your web browser (note: you do not need an Internet connection to do this, or to run any of this code, except the section immediately following)

