import os
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from .handlers import add_item, delete_item, edit_item
from .statistics import show_statistics
from .plots import open_variable_plot
from server.config import PRIMARY_COLOR, ACCENT_COLOR, BLACK, WHITE, IMAGE_DIR
from .export_excel import export_to_excel
import socket
import tkinter.scrolledtext as scrolledtext
import sys
import io

# Store everything printed
_console_buffer = io.StringIO()

class PersistentConsoleLogger(io.StringIO):
    def write(self, s):
        _console_buffer.write(s)
        return super().write(s)

# Redirect stdout and stderr early in the program
sys.stdout = sys.stderr = PersistentConsoleLogger()

def build_gui(root, container, state):
    selected_stand = StringVar()
    selected_stand.set("Alla stånd")
    state["selected_stand"] = selected_stand
    state["container"] = container  # ✅ for access during dropdown update

    dropdown = OptionMenu(root, selected_stand, "Alla stånd", command=lambda _: update_grid(container, selected_stand, state))
    dropdown.config(font=("Arial", 11), bg=ACCENT_COLOR, fg=BLACK)
    dropdown.pack(pady=5)

    state["dropdown"] = dropdown

    action_frame = state["action_frame"]

    button_inner = Frame(action_frame, bg=PRIMARY_COLOR)
    button_inner.pack()  # No side, so it's centered by default

    Button(button_inner, text="Lägg till vara", command=lambda: [
        add_item(state),
        update_dropdown(dropdown, selected_stand, state),
        update_grid(container, selected_stand, state)
    ], font=("Arial", 12, "bold"), fg=BLACK, bg=ACCENT_COLOR).pack(side=LEFT, padx=5)

    Button(button_inner, text="Visa statistik", command=show_statistics,
           font=("Arial", 12, "bold"), fg=WHITE, bg=PRIMARY_COLOR).pack(side=LEFT, padx=5)

    Button(button_inner, text="🧮 Anpassad graf", command=open_variable_plot,
           font=("Arial", 12), fg=WHITE, bg=PRIMARY_COLOR).pack(side=LEFT, padx=5)

    Button(button_inner, text="📤 Skapa Excel-fil", command=export_to_excel,
           font=("Arial", 12), fg=WHITE, bg=PRIMARY_COLOR).pack(side=LEFT, padx=5)

    Button(button_inner, text="❓ Hjälp", command=show_shortcuts_help,
           font=("Arial", 12), fg=WHITE, bg=PRIMARY_COLOR).pack(side=LEFT, padx=5)

    update_dropdown(dropdown, selected_stand, state)
    update_grid(container, selected_stand, state)

    # ⌨️ Keyboard Shortcuts
    root.bind_all("<Control-a>", lambda e: [
        add_item(state),
        update_dropdown(dropdown, selected_stand, state),
        update_grid(container, selected_stand, state)
    ])
    root.bind_all("<Control-s>", lambda e: show_statistics())
    root.bind_all("<Control-g>", lambda e: open_variable_plot())
    root.bind_all("<Control-p>", lambda e: export_to_excel())
    root.bind_all("<Control-h>", lambda e: show_shortcuts_help())
    root.bind_all("<Control-t>", lambda e: open_debug_console())
    root.bind_all("<Control-c>", lambda e: root.quit())

def open_debug_console():
    console_win = Toplevel()
    console_win.title("🛠️ Debug Console")
    console_win.geometry("600x400")

    output_box = scrolledtext.ScrolledText(console_win, wrap="word", bg="#111", fg="#FDD314", insertbackground="#FDD314")
    output_box.pack(expand=True, fill="both")

    # Insert previous output
    output_box.insert("end", _console_buffer.getvalue())
    output_box.see("end")

    # Also live update from now on
    class LiveLogger(io.StringIO):
        def write(self, s):
            output_box.insert("end", s)
            output_box.see("end")
            _console_buffer.write(s)
            return super().write(s)

    sys.stdout = sys.stderr = LiveLogger()
    print("📢 Debug Console activated.")

def get_local_ip():
    try:
        # This trick works on most LANs
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "Okänd"

def show_shortcuts_help():
    ip = get_local_ip()
    help_text = (
        f"Tangentbordsgenvägar:\n\n"
        f"🆕  Ctrl + A – Lägg till vara\n"
        f"📊  Ctrl + S – Visa statistik\n"
        f"📈  Ctrl + G – Anpassad graf\n"
        f"📤  Ctrl + P – Skapa Excel-fil\n"
        f"❓  Ctrl + H – Visa hjälp\n\n"
        f"📡 IP-adress för denna dator:\n  {ip}\n\n"
        f"💡 Skriv in denna IP-adress i appen när du startar den för att ansluta:{ip}"
    )
    messagebox.showinfo("Hjälp – Genvägar & IP", help_text)


def update_dropdown(dropdown, selected_stand, state):
    items = state["items"]
    menu = dropdown["menu"]
    menu.delete(0, "end")

    def select_and_update(stand):
        selected_stand.set(stand)
        update_grid(state["container"], selected_stand, state)

    menu.add_command(label="Alla stånd", command=lambda: select_and_update("Alla stånd"))

    stands = sorted(set(item.get("stand", "Okänt") for item in items))
    for stand in stands:
        menu.add_command(label=stand, command=lambda s=stand: select_and_update(s))



def update_grid(container, selected_stand, state):
    for widget in container.winfo_children():
        widget.destroy()
    state["thumb_refs"].clear()

    items = state["items"]
    visible = items if selected_stand.get() == "Alla stånd" else [i for i in items if i.get("stand") == selected_stand.get()]

    # Force geometry update to get accurate width
    container.update_idletasks()
    width = container.winfo_width() or 700
    item_width = 180
    cols = max(1, width // item_width)

    for idx, item in enumerate(visible):
        row, col = divmod(idx, cols)
        container.grid_columnconfigure(col, weight=1)

        frame = Frame(container, borderwidth=2, relief="ridge", padx=5, pady=5, bg=WHITE)
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        if item.get("image"):
            try:
                img_path = os.path.join(IMAGE_DIR, item["image"])
                img = Image.open(img_path)
                img.thumbnail((100, 100))
                tk_img = ImageTk.PhotoImage(img)
                state["thumb_refs"].append(tk_img)  # Prevent garbage collection
                Label(frame, image=tk_img, bg=WHITE).pack()
            except:
                pass

        Label(frame, text=item["name"], font=("Arial", 12, "bold"), bg=WHITE, fg=BLACK).pack()
        Label(frame, text=f"{item['price']:.2f} kr", fg=PRIMARY_COLOR, bg=WHITE).pack()
        Label(frame, text=f"Stånd: {item.get('stand', 'Okänt')}", font=("Arial", 9), bg=WHITE, fg=BLACK).pack()

        btn_frame = Frame(frame, bg=WHITE)
        btn_frame.pack(pady=5)

        Button(btn_frame, text="Ändra", fg=BLACK, bg=ACCENT_COLOR,
               activebackground=BLACK, activeforeground=WHITE,
               command=lambda i=item["id"]: [
                   edit_item(state, i),
                   update_dropdown(state["dropdown"], selected_stand, state),
                   update_grid(container, selected_stand, state)
               ]).pack(side=LEFT, padx=5)

        Button(btn_frame, text="Ta bort", fg=WHITE, bg=PRIMARY_COLOR,
               activebackground=BLACK, activeforeground=ACCENT_COLOR,
               command=lambda i=item["id"]: [
                   delete_item(state, i),
                   update_dropdown(state["dropdown"], selected_stand, state),
                   update_grid(container, selected_stand, state)
               ]).pack(side=LEFT, padx=5)
