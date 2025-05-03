from server.items import load_items, save_items
from server.config import IMAGE_DIR
import os, shutil
from tkinter import simpledialog, filedialog, messagebox
from datetime import datetime

def init_data():
    items = load_items()
    return {"items": items, "thumb_refs": []}

def add_item(state):
    items = state["items"]
    name = simpledialog.askstring("Ny vara", "Vad heter varan?")
    if not name:
        return

    try:
        price = float(simpledialog.askstring("Pris", f"Vad kostar '{name}'?"))
    except:
        messagebox.showerror("Fel", "Ange ett giltigt pris (t.ex. 12.50)")
        return

    stand = simpledialog.askstring("Stånd", "Vilket stånd tillhör varan?") or "Okänt"

    image_file = ""
    image_path = filedialog.askopenfilename(title="Välj bild", filetypes=[("Bildfiler", "*.png *.jpg *.jpeg")])
    if image_path:
        ext = os.path.splitext(image_path)[1]
        image_file = f"{name}_{int(datetime.now().timestamp())}{ext}"
        shutil.copy(image_path, os.path.join(IMAGE_DIR, image_file))

    item = {
        "id": max([i["id"] for i in items], default=0) + 1,
        "name": name,
        "price": price,
        "image": image_file,
        "stand": stand
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
