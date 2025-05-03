from tkinter import Tk, Frame, BOTH
from server.config import PRIMARY_COLOR
from .components import build_gui
from .handlers import init_data

def start_gui():
    root = Tk()
    root.title("Varuregister")
    root.geometry("700x750")
    root.configure(bg=PRIMARY_COLOR)

    container = Frame(root, bg=PRIMARY_COLOR)
    container.pack(fill=BOTH, expand=True)

    state = init_data()
    build_gui(root, container, state)

    root.mainloop()
