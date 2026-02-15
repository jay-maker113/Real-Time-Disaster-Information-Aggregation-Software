import os

# -------------------------------------------
# Project directory configuration
# -------------------------------------------

# Directory of this constants file
constants_dir = os.path.dirname(os.path.abspath(__file__))

# Base project directory (one level up)
base_dir = os.path.dirname(constants_dir)

# Path to the assets folder
# This folder should contain images, emergency_contacts.json, etc.
ASSETS_DIR = os.path.join(base_dir, "assets")

# Global container for disaster bounding boxes
DISASTERBOXES = []
