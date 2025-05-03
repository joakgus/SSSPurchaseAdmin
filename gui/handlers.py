from server.items import load_items, save_items
from server.config import IMAGE_DIR
import os, shutil
from tkinter import filedialog, messagebox, Toplevel, StringVar, Entry, Label, Button
from datetime import datetime
from .dialogs import ask_item_details

def init_data():
    items = load_items()
    return {"items": items, "thumb_refs": []}


def add_item(state):
    items = state["items"]
    result = ask_item_details()
    if not result:
        return

    item = {
        "id": max((i["id"] for i in items), default=0) + 1,
        **result
    }
    items.append(item)
    save_items(items)

def delete_item(state, item_id):
    items = state["items"]
    for i, item in enumerate(items):
        if item["id"] == item_id:
            if item.get("image"):
                img_path = os.path.join(IMAGE_DIR, item["image"])
                if os.path.exists(img_path):
                    os.remove(img_path)
            del items[i]
            save_items(items)
            break

def edit_item(state, item_id):
    items = state["items"]
    item = next((i for i in items if i["id"] == item_id), None)
    if not item:
        return

    updated = ask_item_details(item)
    if updated:
        item.update(updated)
        save_items(items)