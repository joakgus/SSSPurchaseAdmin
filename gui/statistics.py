import os
import json
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from collections import defaultdict
from server.config import PURCHASES_DIR, WHITE, BLACK, ACCENT_COLOR

def show_statistics():
    # Gather all available purchase files (assumes filenames like YYYY-MM-DD.json)
    files = sorted(
        f for f in os.listdir(PURCHASES_DIR)
        if f.endswith(".json")
    )

    if not files:
        messagebox.showinfo("Ingen data", "Inga köpfiler hittades.")
        return

    # Popup to select one or more dates
    select_popup = Toplevel()
    select_popup.title("Välj datum för statistik")
    select_popup.geometry("300x400")

    Label(select_popup, text="Markera en eller flera datum:").pack(pady=10)

    listbox = Listbox(select_popup, selectmode=MULTIPLE, height=15)
    for file in files:
        listbox.insert(END, file.replace(".json", ""))
    listbox.pack(padx=20, pady=10, fill=BOTH, expand=True)

    def generate_summary():
        selected = [listbox.get(i) for i in listbox.curselection()]
        select_popup.destroy()

        if not selected:
            return

        all_data = []
        for date in selected:
            path = os.path.join(PURCHASES_DIR, f"{date}.json")
            try:
                with open(path, "r", encoding="utf-8") as f:
                    all_data.extend(json.load(f))
            except:
                continue

        if not all_data:
            messagebox.showinfo("Ingen data", "Inga köp hittades för de valda datumen.")
            return

        summary = defaultdict(lambda: {"quantity": 0, "revenue": 0.0})
        total_quantity = 0
        total_revenue = 0.0

        for p in all_data:
            key = f"{p['name']} ({p['stand']})"
            qty = p["quantity"]
            rev = qty * p["price"]
            summary[key]["quantity"] += qty
            summary[key]["revenue"] += rev
            total_quantity += qty
            total_revenue += rev

        popup = Toplevel()
        popup.title(f"Statistik för {', '.join(selected)}")
        popup.configure(bg=WHITE)

        Label(popup, text="Vara (Stånd)", font=("Arial", 10, "bold"), bg=WHITE, fg=BLACK).grid(row=0, column=0, padx=10, pady=5, sticky=W)
        Label(popup, text="Antal", font=("Arial", 10, "bold"), bg=WHITE, fg=BLACK).grid(row=0, column=1, padx=10)
        Label(popup, text="Totalt", font=("Arial", 10, "bold"), bg=WHITE, fg=BLACK).grid(row=0, column=2, padx=10)

        for idx, (key, stats) in enumerate(summary.items(), start=1):
            Label(popup, text=key, bg=WHITE, fg=BLACK).grid(row=idx, column=0, sticky=W, padx=10)
            Label(popup, text=stats["quantity"], bg=WHITE, fg=BLACK).grid(row=idx, column=1)
            Label(popup, text=f"{stats['revenue']:.2f} kr", bg=WHITE, fg=BLACK).grid(row=idx, column=2)

        Label(popup, text="Totalt:", font=("Arial", 10, "bold"), bg=WHITE, fg=BLACK).grid(row=idx+1, column=0, sticky=W, padx=10, pady=(10, 0))
        Label(popup, text=total_quantity, font=("Arial", 10, "bold"), bg=WHITE, fg=BLACK).grid(row=idx+1, column=1, pady=(10, 0))
        Label(popup, text=f"{total_revenue:.2f} kr", font=("Arial", 10, "bold"), bg=WHITE, fg=BLACK).grid(row=idx+1, column=2, pady=(10, 0))

        Button(popup, text="Stäng", command=popup.destroy, bg=ACCENT_COLOR, fg=BLACK).grid(row=idx+2, column=0, columnspan=3, pady=10)

    Button(select_popup, text="Visa statistik", command=generate_summary, bg=ACCENT_COLOR, fg=BLACK).pack(pady=10)
    Button(select_popup, text="Avbryt", command=select_popup.destroy).pack()

