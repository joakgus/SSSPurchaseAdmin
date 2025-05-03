from tkinter import Tk, Frame, BOTH
from server.config import PRIMARY_COLOR
from .components import build_gui
from .handlers import init_data
import sys
import os

def start_gui():
    root = Tk()
    root.title("SSSAdmin")
    root.geometry("1920x1080")
    root.configure(bg=PRIMARY_COLOR)

    # ✅ Set icon for taskbar (Windows only)
    if sys.platform == "win32":
        icon_path = os.path.join(os.path.dirname(__file__), "..", "app.ico")
        icon_path = os.path.abspath(icon_path)
        try:
            root.iconbitmap(icon_path)
        except Exception as e:
            print("⚠️ Kunde inte sätta ikon:", e)

    container = Frame(root, bg=PRIMARY_COLOR)
    container.pack(fill=BOTH, expand=True)

    state = init_data()
    build_gui(root, container, state)

    root.mainloop()
