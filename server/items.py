import os
import json
from flask import Blueprint, jsonify, send_from_directory
from .config import ITEMS_FILE, IMAGE_DIR

items_bp = Blueprint("items", __name__)
_items_cache = []

def load_items():
    global _items_cache
    if os.path.exists(ITEMS_FILE):
        with open(ITEMS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Normalize 'stand' to always be a list
            for item in data:
                if isinstance(item.get("stand"), str):
                    item["stand"] = [item["stand"]]
                elif not isinstance(item.get("stand"), list):
                    item["stand"] = []
            _items_cache = data
    else:
        _items_cache = []

    return _items_cache


def save_items(items):
    with open(ITEMS_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

def get_cached_items():
    return _items_cache

@items_bp.route("/items", methods=["GET"])
def get_items():
    return jsonify(_items_cache)

@items_bp.route("/images/<filename>", methods=["GET"])
def get_image(filename):
    return send_from_directory(IMAGE_DIR, filename)

@items_bp.route("/stands", methods=["GET"])
def get_stands():
    all_stands = set()
    for item in _items_cache:
        stands = item.get("stands", [])
        if isinstance(stands, str):
            all_stands.add(stands)
        elif isinstance(stands, list):
            all_stands.update(stands)
    return jsonify(sorted(all_stands))
