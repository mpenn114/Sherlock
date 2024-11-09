import numpy as np


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
            """
            self._initialized: bool = True

            # The root directory for the images
            self.root_directory: str = "."

            # The prefix for the image files
            self.image_prefix: str = "IMG"

            # The suffix for the image files
            self.image_suffix: str = "JPG"

            # The minimum number of images in a folder to process it
            self.min_images_process: int = 1

            # Warn if metadata cannot be found
            self.image_metadata_warning_shown: bool = False

            # Max number of images to use in each background
            self.background_max_images: int = 100

            # Minimum number of images to count as a viable background
            self.min_background_used: int = 5

            # Number of pixels to sample per image
            self.sample_size: int = 5000

            # Number of iterations of bounce algorithm
            self.bounces: int = 4

            # Upper bound for color threshold
            self.colour_upper: np.ndarray = np.array([255, 255, 255])

            # Lower bound for color threshold
            self.colour_lower: np.ndarray = np.array([0, 0, 0])

            # Max range of color parameters for grayscale
            self.greyscale_parameter: int = 75

            # How far away from background to be a disturbance
            self.background_tol_day: int = 75

            # How far away from background to be a disturbance at night
            self.background_tol_night: int = 10

            # The default image size (overridden as code runs)
            self.image_size: tuple[int, int, int] = (1080, 720, 3)

            # Whether to count pixels before accepting an animal
            self.count_pixels: bool = True

            # Number of pixels to sample to assess disturbance proportion
            self.pixel_samples: int = 100

            # Minimum proportion of pixels as disturbance for contour acceptance
            self.disturbance_tol: float = 0.1

            # Area in pixels squared required for contour acceptance (day)
            self.size_tol_day: int = 30000

            # Area in pixels squared required for contour acceptance (night)
            self.size_tol_night: int = 5000

            # Secondary color upper bound for contour assessment
            self.secondary_color_upper: np.ndarray = np.array([75, 75, 75])

            # Secondary color lower bound for contour assessment
            self.secondary_color_lower: np.ndarray = np.array([0, 0, 0])

            # Tolerance for secondary color in contours
            self.secondary_colour_tol: float = 0.05

            # Whether to save images
            self.save_images: bool = False

            # Number of adjacent images to record as positives
            self.adjacency: int = 1

            # Run code for this execution
            self.run_code: int = 1

            # Time tolerance for datetime adjacency
            self.datetime_adjacency_tolerance: int = 20
