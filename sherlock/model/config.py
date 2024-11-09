import numpy as np
import pandas as pd


class EnvSettings:
    _instance = None

    def __new__(cls):
        """
        Ensure that EnvSettings is a singleton.
        """
        if cls._instance is None:
            cls._instance = super(EnvSettings, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            """
            Define the settings for the code.

            Args:
                file_path (str): The file path
            """
            self._initialized = True

            # Environment Variables
            self.root_directory = ""  # The root directory for the images
            self.image_prefix = "IMG"  # The prefix for the image files
            self.image_suffix = "JPG"  # The suffix for the image files
            self.min_images_process  = 1 # The minimum number of images in a folder to process it
            self.image_metadata_warning_shown = (
                False  # Warn if metadata cannot be found
            )

            self.background_max_images = (
                100  # Max number of images to use in each background
            )
            self.min_background_used = (
                5  # Minimum number of images to count as a viable background
            )
            self.sample_size = 5000  # Number of pixels to sample per image
            self.bounces = 4  # Number of iterations of bounce algorithm
            self.colour_upper = np.array([255, 255, 255])  # Upper bound
            self.colour_lower = np.array([0, 0, 0])  # Lower bound
            self.greyscale_parameter = 75  # Max range of colour parameters
            self.background_tol_day = (
                75  # How far away from background to be a disturbance
            )
            self.background_tol_night = 10  # How far away in night to be a disturbance
            self.testing_mode = False  # Whether or not we are testing the algorithm
            self.animal_data_path = (
                "animal_data.csv"  # The path to animal data if there is any
            )
            self.test_data_animals = pd.DataFrame({})  # Test data store
            self.no_animal_data_path = (
                "no_animal_data.csv"  # The path to animal data if there is any
            )
            self.test_data_no_animals = pd.DataFrame({})  # Test data store
            self.image_size = (
                1080,
                720,
                3,
            )  # The default image size. This is overriden as the code runs

            self.count_pixels = (
                True  # Whether or not to count pixels before accepting an animal
            )
            self.pixel_samples = (
                100  # How many pixels to sample to assess distrubance proportion
            )
            self.disturbance_tol = 0.1  # Minimum number of pixels that are a disturbance for a contour to be accepted
            self.size_tol_day = 30000  # The area in pixels squared required for a contour to be accepted as an animal
            self.size_tol_night = 5000  # The area at night

            self.secondary_color_upper = np.array(
                [75, 75, 75]
            )  # The secondary colour to look for when assessing contours
            self.secondary_color_lower = np.array([0, 0, 0])
            self.secondary_colour_tol = 0.05

            self.save_images = False  # Whether or not to save images
            self.adjacency = 1  # How many adjacent images to also record as positives
            self.run_code = 1  # The run code for this run

            self.datetime_adjacency_tolerance = 20
