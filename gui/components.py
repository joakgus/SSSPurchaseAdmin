import os
from tkinter import *
from PIL import Image, ImageTk
from .handlers import add_item, delete_item
from .statistics import show_statistics
from .plots import open_variable_plot
from server.config import PRIMARY_COLOR, ACCENT_COLOR, BLACK, WHITE, IMAGE_DIR


def build_gui(root, container, state):
    selected_stand = StringVar()
    selected_stand.set("Alla stånd")
    state["selected_stand"] = selected_stand
    state["container"] = container  # ✅ for access during dropdown update

    dropdown = OptionMenu(root, selected_stand, "Alla stånd", command=lambda _: update_grid(container, selected_stand, state))
    dropdown.config(font=("Arial", 11), bg=ACCENT_COLOR, fg=BLACK)
    dropdown.pack(pady=5)

    state["dropdown"] = dropdown

    Button(root, text="Lägg till vara", command=lambda: [
        add_item(state),
        update_dropdown(dropdown, selected_stand, state),
        update_grid(container, selected_stand, state)
    ], font=("Arial", 12, "bold"), fg=BLACK, bg=ACCENT_COLOR).pack(pady=5)

    Button(root, text="Visa statistik", command=show_statistics,
           font=("Arial", 12, "bold"), fg=WHITE, bg=PRIMARY_COLOR).pack(pady=2)

    Button(root, text="🧮 Anpassad graf", command=open_variable_plot,
           font=("Arial", 12), fg=WHITE, bg=PRIMARY_COLOR).pack(pady=2)

    update_dropdown(dropdown, selected_stand, state)
    update_grid(container, selected_stand, state)

    # Redraw on resize
    container.bind("<Configure>", lambda event: update_grid(container, selected_stand, state))


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

        Button(frame, text="Ta bort", fg=WHITE, bg=PRIMARY_COLOR,
               activebackground=BLACK, activeforeground=ACCENT_COLOR,
               command=lambda i=item["id"]: [
                   delete_item(state, i),
                   update_dropdown(state["dropdown"], selected_stand, state),
                   update_grid(container, selected_stand, state)
               ]).pack(pady=5)
