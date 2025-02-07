import os
import sys

def resource_path(relative_path):
    """ Get the absolute path to a resource, handling PyInstaller builds. """
    if getattr(sys, 'frozen', False):  # Detect if running as a PyInstaller bundle
        base_path = sys._MEIPASS  # Extracted temp folder
    else:
        base_path = os.path.abspath(".")  # Normal script execution

    return os.path.join(base_path, relative_path)
