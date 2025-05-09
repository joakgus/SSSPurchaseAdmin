import os
import json
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
from server.config import PURCHASES_DIR

def parse_timestamp(ts: str):
    return datetime.fromisoformat(ts.replace("Z", ""))

def open_variable_plot():
    popup = Toplevel()
    popup.title("Skapa anpassad graf")
    popup.geometry("400x500")
    popup.configure(bg="#fff")

    Label(popup, text="Välj datum:", font=("Arial", 12, "bold")).pack(pady=5)
    listbox = Listbox(popup, selectmode=MULTIPLE, height=6)
    listbox.pack(padx=20, fill="x")

    purchase_files = sorted(f for f in os.listdir(PURCHASES_DIR) if f.endswith(".json"))
    for file in purchase_files:
        listbox.insert(END, file)

    Label(popup, text="X-Axel:", font=("Arial", 12)).pack(pady=5)
    x_var = StringVar(value="timestamp")
    x_options = ["timestamp", "stand", "name"]
    x_menu = ttk.Combobox(popup, values=x_options, textvariable=x_var, state="readonly")
    x_menu.pack()

    Label(popup, text="Y-Axel:", font=("Arial", 12)).pack(pady=5)
    y_var = StringVar(value="quantity")
    y_options = ["quantity", "revenue"]
    y_menu = ttk.Combobox(popup, values=y_options, textvariable=y_var, state="readonly")
    y_menu.pack()

    Label(popup, text="Gruppera efter:", font=("Arial", 12)).pack(pady=5)
    group_var = StringVar(value="name")
    group_options = ["name", "stand"]
    group_menu = ttk.Combobox(popup, values=group_options, textvariable=group_var, state="readonly")
    group_menu.pack()

    def on_submit():
        selected_indices = listbox.curselection()
        selected_files = [purchase_files[i] for i in selected_indices]
        if not selected_files:
            messagebox.showwarning("Ingen dag vald", "Välj minst ett datum för att visa graf.")
            return
        generate_variable_plot(x_var.get(), y_var.get(), group_var.get(), selected_files)

    Button(popup, text="Visa graf", command=on_submit, bg="#004728", fg="#fff").pack(pady=20)


def generate_variable_plot(x_axis: str, y_axis: str, group_by: str, files: list[str]):
    series = defaultdict(lambda: defaultdict(float))  # group -> x -> y

    for file in files:
        path = os.path.join(PURCHASES_DIR, file)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            continue

        for p in data:
            key = p.get(group_by, "Okänt")
            if x_axis == "timestamp":
                x_val = parse_timestamp(p["timestamp"]).replace(second=0, microsecond=0)
            else:
                x_val = p.get(x_axis, "Okänt")

            if y_axis == "quantity":
                y_val = p["quantity"]
            elif y_axis == "revenue":
                y_val = p["quantity"] * p["price"]
            else:
                y_val = 0

            series[key][x_val] += y_val

    # Plot
    plt.figure(figsize=(10, 5))
    for group, xys in series.items():
        x = sorted(xys.keys())
        y = [xys[v] for v in x]
        plt.plot(x, y, label=group)

    plt.title(f"{y_axis.capitalize()} över {x_axis}")
    plt.xlabel(x_axis.capitalize())
    plt.ylabel(y_axis.capitalize())
    plt.legend()
    plt.tight_layout()
    plt.gcf().autofmt_xdate()
    plt.show()

