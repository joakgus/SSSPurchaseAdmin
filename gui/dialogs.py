import os, shutil
from tkinter import *
from tkinter import filedialog, messagebox
from server.config import IMAGE_DIR
import time

def ask_item_details(initial=None) -> dict | None:
    popup = Toplevel()
    popup.title("Lägg till / Ändra vara")
    popup.geometry("400x300")
    popup.transient()
    popup.grab_set()

    confirmed = []
    result = {
        "name": "",
        "price": 0.0,
        "stand": "",
        "image": initial.get("image") if initial else ""
    }

    var_name = StringVar(value=initial.get("name") if initial else "")
    var_price = StringVar(value=str(initial.get("price")) if initial else "")
    var_stand = StringVar(value=initial.get("stand") if initial else "")
    var_image = StringVar(value=result["image"])

    Label(popup, text="Namn").pack(anchor="w", padx=20, pady=(10, 0))
    entry_name = Entry(popup, textvariable=var_name)
    entry_name.pack(padx=20, fill="x")
    popup.update_idletasks()
    entry_name.focus_force()

    Label(popup, text="Pris").pack(anchor="w", padx=20, pady=(10, 0))
    Entry(popup, textvariable=var_price).pack(padx=20, fill="x")

    Label(popup, text="Stånd").pack(anchor="w", padx=20, pady=(10, 0))
    Entry(popup, textvariable=var_stand).pack(padx=20, fill="x")

    def choose_image():
        path = filedialog.askopenfilename(filetypes=[("Bildfiler", "*.png *.jpg *.jpeg")])
        if path:
            var_image.set(path)

    frame_img = Frame(popup)
    frame_img.pack(padx=20, pady=10, fill="x")

    Label(frame_img, text="Bild:").pack(side=LEFT)
    Entry(frame_img, textvariable=var_image, state="readonly").pack(side=LEFT, expand=True, fill="x", padx=5)
    Button(frame_img, text="Välj...", command=choose_image).pack(side=RIGHT)

    def submit():
        name = var_name.get().strip()
        price_text = var_price.get().strip()
        stand = var_stand.get().strip()

        if not name:
            messagebox.showerror("Fel", "Du måste ange ett namn.")
            return

        if not stand:
            messagebox.showerror("Fel", "Du måste ange ett stånd.")
            return

        try:
            price = float(price_text)
        except ValueError:
            messagebox.showerror("Fel", "Ange ett giltigt pris (t.ex. 12.50)")
            return

        result["name"] = name
        result["price"] = price
        result["stand"] = stand

        # Copy image if needed
        image_path = var_image.get()
        if image_path and os.path.exists(image_path) and os.path.dirname(image_path) != IMAGE_DIR:
            ext = os.path.splitext(image_path)[1]
            filename = f"{name}_{int(time.time())}{ext}"
            dest = os.path.join(IMAGE_DIR, filename)
            shutil.copy(image_path, dest)
            result["image"] = filename
        elif initial and not image_path:
            result["image"] = initial.get("image", "")

        confirmed.append(True)
        popup.destroy()

    def cancel():
        popup.destroy()

    popup.bind("<Return>", lambda e: submit())
    popup.bind("<Escape>", lambda e: cancel())

    Button(popup, text="OK", command=submit).pack(pady=5)
    Button(popup, text="Avbryt", command=cancel).pack()

    popup.wait_window()
    return result if confirmed else None
