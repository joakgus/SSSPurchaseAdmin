import os
import sys

def get_data_dir():
    if getattr(sys, 'frozen', False):
        # PyInstaller production
        base = os.path.dirname(sys.executable)
    else:
        # Dev mode
        base = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base, "data")

PRIMARY_COLOR = "#004728"
ACCENT_COLOR = "#FDD314"
BLACK = "#000000"
WHITE = "#FFFFFF"

DATA_DIR = get_data_dir()
ITEMS_FILE = os.path.join(DATA_DIR, "items.json")
IMAGE_DIR = os.path.join(DATA_DIR, "images")
PURCHASES_DIR = os.path.join(DATA_DIR, "purchases")

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(PURCHASES_DIR, exist_ok=True)
