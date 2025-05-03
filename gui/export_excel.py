import os
import json
from datetime import datetime
from tkinter import messagebox
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from server.config import PURCHASES_DIR

def export_to_excel():
    today = datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.join(PURCHASES_DIR, f"{today}.json")

    if not os.path.exists(file_path):
        messagebox.showinfo("Ingen data", f"Inga köp hittades för {today}.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        purchases = json.load(f)

    if not purchases:
        messagebox.showinfo("Tom fil", "Inga poster att exportera.")
        return

    # Create workbook and sheet
    wb = Workbook()
    ws = wb.active
    ws.title = f"Köp {today}"

    headers = ["Vara", "Stånd", "Antal", "Pris (kr)", "Totalt (kr)", "Tidpunkt"]
    ws.append(headers)

    for p in purchases:
        row = [
            p["name"],
            p["stand"],
            p["quantity"],
            p["price"],
            round(p["price"] * p["quantity"], 2),
            p["timestamp"]
        ]
        ws.append(row)

    # Auto-adjust column width
    for col in ws.columns:
        length = max(len(str(cell.value)) for cell in col)
        ws.column_dimensions[get_column_letter(col[0].column)].width = length + 2

    # Save to Desktop
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    filename = os.path.join(desktop, f"Kop_{today}.xlsx")
    wb.save(filename)

    messagebox.showinfo("Export klar", f"Excel-fil sparad på skrivbordet:\n{filename}")
