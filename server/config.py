import os

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

PRIMARY_COLOR = "#004728"
ACCENT_COLOR = "#FDD314"
BLACK = "#000000"
WHITE = "#FFFFFF"

IMAGE_DIR = os.path.join(ROOT_DIR, "images")
ITEMS_FILE = os.path.join(ROOT_DIR, "items.json")
PURCHASES_DIR = os.path.join(ROOT_DIR, "purchases")

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(PURCHASES_DIR, exist_ok=True)
