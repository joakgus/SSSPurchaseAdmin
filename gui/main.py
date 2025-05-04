from tkinter import Tk, Frame, Canvas, Scrollbar, BOTH, RIGHT, Y, BOTTOM, X, LEFT, TOP
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

    # --- Bottom-fixed action bar ---
    action_frame = Frame(root, bg=PRIMARY_COLOR)
    action_frame.pack(side=BOTTOM, fill=X, pady=5)

    # --- Scrollable Canvas/Grid Container ---
    canvas_frame = Frame(root)
    canvas_frame.pack(side=TOP, fill=BOTH, expand=True)

    canvas = Canvas(canvas_frame, bg=PRIMARY_COLOR)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar = Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    container = Frame(canvas, bg=PRIMARY_COLOR)
    container_id = canvas.create_window((0, 0), window=container, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    container.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(container_id, width=e.width))

    # Enable mouse wheel scrolling (Windows & Mac/Linux)
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_linux_scroll(event):
        if event.num == 4:  # Scroll up
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Scroll down
            canvas.yview_scroll(1, "units")

    # Bind for Windows and macOS
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # Bind for Linux
    canvas.bind_all("<Button-4>", _on_linux_scroll)
    canvas.bind_all("<Button-5>", _on_linux_scroll)

    state = init_data()
    state["canvas"] = canvas
    state["action_frame"] = action_frame  # ✅ Give it to components

    build_gui(root, container, state)
    root.mainloop()
