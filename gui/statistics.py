import os
import json
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from collections import defaultdict
from server.config import PURCHASES_DIR, WHITE, BLACK, ACCENT_COLOR

def show_statistics():
    today = datetime.now().strftime("%Y-%m-%d")
    path = os.path.join(PURCHASES_DIR, f"{today}.json")

    if not os.path.exists(path):
        messagebox.showinfo("Ingen data", f"Inga köp hittades för {today}.")
        return

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    summary = defaultdict(lambda: {"quantity": 0, "revenue": 0.0})
    total_quantity = 0
    total_revenue = 0.0

    for p in data:
        key = f"{p['name']} ({p['stand']})"
        qty = p["quantity"]
        rev = qty * p["price"]
        summary[key]["quantity"] += qty
        summary[key]["revenue"] += rev
        total_quantity += qty
        total_revenue += rev

    popup = Toplevel()
    popup.title(f"Statistik för {today}")
    popup.configure(bg=WHITE)

    Label(popup, text="Vara (Stånd)", font=("Arial", 10, "bold"), bg=WHITE, fg=BLACK).grid(row=0, column=0, padx=10, pady=5, sticky=W)
    Label(popup, text="Antal", font=("Arial", 10, "bold"), bg=WHITE, fg=BLACK).grid(row=0, column=1, padx=10)
    Label(popup, text="Totalt", font=("Arial", 10, "bold"), bg=WHITE, fg=BLACK).grid(row=0, column=2, padx=10)

    for idx, (key, stats) in enumerate(summary.items(), start=1):
        Label(popup, text=key, bg=WHITE, fg=BLACK).grid(row=idx, column=0, sticky=W, padx=10)
        Label(popup, text=stats["quantity"], bg=WHITE, fg=BLACK).grid(row=idx, column=1)
        Label(popup, text=f"{stats['revenue']:.2f} kr", bg=WHITE, fg=BLACK).grid(row=idx, column=2)

    # Add total summary
    Label(popup, text="Totalt för dagen:", font=("Arial", 10, "bold"), bg=WHITE, fg=BLACK).grid(row=idx+1, column=0, sticky=W, padx=10, pady=(10, 0))
    Label(popup, text=total_quantity, font=("Arial", 10, "bold"), bg=WHITE, fg=BLACK).grid(row=idx+1, column=1, pady=(10, 0))
    Label(popup, text=f"{total_revenue:.2f} kr", font=("Arial", 10, "bold"), bg=WHITE, fg=BLACK).grid(row=idx+1, column=2, pady=(10, 0))

    Button(popup, text="Stäng", command=popup.destroy, bg=ACCENT_COLOR, fg=BLACK).grid(row=idx+2, column=0, columnspan=3, pady=10)
