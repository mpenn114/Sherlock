from .config import EnvSettings
from .sherlock import process_folder

ENV = EnvSettings()


def run_sherlock():
    """
    Run Sherlock on a range of folders.
    """
    root_path = ENV.root_directory
