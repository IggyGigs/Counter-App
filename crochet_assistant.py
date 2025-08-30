import tkinter as tk
import tkinter.font as tkFont
import threading
from pynput import keyboard

special_keys = {
    "ctrl_l": "ctrl",
    "ctrl_r": "ctrl",
    "control_l": "ctrl",
    "control_r": "ctrl",
    "shift_l": "shift",
    "shift_r": "shift",
    "alt_l": "alt",
    "alt_r": "alt",
    "space": "space",
    "enter": "enter",
    "tab": "tab",
    # etc?
}

# Themes
themes = {
    "Dark": {"bg": "#29292b", "fg": "#c7c7d1", "sb":"#212124", "hv_bg":"#101012", "hv_fg":"#c7c7d1"},
    "Light": {"bg": "#c0c0cc", "fg": "#2a2a2e", "sb":"#d8d8e8", "hv_bg":"#c3c3d4", "hv_fg":"#2a2a2e"},
    "High Contrast": {"bg": "#12121a", "fg": "#eeff00", "sb":"black", "hv_bg":"white", "hv_fg":"black"},
    "Pikmin Special": {"bg": "#7a1461", "fg": "#fff173", "sb":"#a3107e", "hv_bg":"#940c72", "hv_fg":"#fff173"},
    "Facade": {"bg": "#facade", "fg":"#ff63a4", "sb":"#f5b3ce", "hv_bg":"#fcdeeb", "hv_fg":"#ff63a4"},
    "Baby Blue": {"bg":"#b6e4fc", "fg":"#45beff", "sb":"#edf9ff", "hv_bg":"#29b5ff","hv_fg":"#cde9f7"},
    "Evil": {"bg":"#260000", "fg":"#ff0000", "sb":"#690000", "hv_bg":"#e30000","hv_fg":"#500000"}
}
current_theme = "Dark"

# Logic
count = 0
stitch_count = 0
target_key = "ctrl"

prereset_count = 0
prereset_stitch = 0

def increment():
    global count
    count += 1
    label.config(text=f"{count}")

# Theme changer
def set_theme(theme_name):
    global current_theme
    current_theme = theme_name
    theme = themes[theme_name]

    root.config(bg=theme["bg"])
    rows_label.config(bg=theme["bg"], fg=theme["fg"])
    label.config(bg=theme["bg"], fg=theme["fg"])
    stitches_label.config(bg=theme["bg"], fg=theme["fg"])
    s_label.config(bg=theme["bg"], fg=theme["fg"])
    counter_frame.config(bg=theme["bg"])
    button_frame.config(bg=theme["bg"])
    row_undo_button.config(bg=theme["bg"])

    row_undo_button.itemconfig(1, fill=themes[current_theme]["sb"])
    row_undo_button.itemconfig(2, fill=themes[current_theme]["fg"])

    sidebar.config(bg=theme.get("sb",theme["bg"]))
    for b in sidebar_buttons:
        b.config(bg=theme.get("sb",theme["bg"]), fg=theme["fg"], activebackground=theme["sb"])

    for canvas in circular_buttons:
        canvas.itemconfig(1, fill=themes[current_theme]["sb"])
        canvas.itemconfig(2, fill=themes[current_theme]["fg"])
        canvas.config(bg=themes[current_theme]["bg"])

    for i, btn in enumerate(theme_option_buttons):
        if isinstance(btn, tk.Canvas):
            theme_name = list(themes.keys())[i]
            btn.itemconfig(btn.oval_id, fill=themes[theme_name]["bg"])
            btn.config(bg=themes[current_theme]["sb"])

            for item in btn.find_all():
                if btn.type(item) == "text":
                    btn.delete(item)

            if theme_name == current_theme:
                fg_color = themes[current_theme]["fg"]
                diameter = int(btn["width"])
                btn.create_text(
                    diameter // 2 - 1,
                    diameter // 2 - 1,
                    text=":3",
                    fill=fg_color,
                    font=("Roboto Mono", diameter // 2, "bold")
                )
        else:
            btn.config(bg=themes.get("sb", theme["bg"]), fg=theme["fg"])
    theme_frame.config(bg=themes[current_theme]["sb"])

# Sidebar animation
sidebar_open = False
sidebar_width = 0

# Theme options expand/collapse
theme_options_visible = False

def toggle_theme_options():
    global theme_options_visible
    if theme_options_visible:
        theme_frame.place_forget()
        for b in theme_option_buttons:
            b.pack_forget()
        theme_options_visible = False
    else:
        theme_frame.place(x=sidebar.winfo_width(), y=-5)
        for b in theme_option_buttons:
            b.pack(pady=2, fill="x")
        theme_options_visible = True

# Keybind options
def change_keybind():
    prompt = tk.Toplevel(root)
    prompt.title("Press a key")
    prompt.geometry("300x100")
    prompt.attributes('-topmost', True)

    label = tk.Label(prompt, text="Press the key you want to use.\nClose the window to cancel.")
    label.pack(pady=20)

    def on_key_press(event):
        global target_key
        key_name = event.keysym.lower()
        # Map it if it's a special key
        target_key = special_keys.get(key_name, key_name)
        key_button.config(text=f"key: {target_key.upper()}")
        prompt.destroy()

    prompt.bind("<Key>", on_key_press)

def subtract_row():
    global count
    count -= 1
    label.config(text=f"{count}")

def reset():
    global count, stitch_count, prereset_count, prereset_stitch
    prereset_count = count
    prereset_stitch = stitch_count
    count = 0
    stitch_count = 0
    label.config(text=f"{count}")
    s_label.config(text=f"{stitch_count}")

def undo_reset():
    global count, stitch_count, prereset_count, prereset_stitch
    count = prereset_count
    stitch_count = prereset_stitch
    label.config(text=f"{count}")
    s_label.config(text=f"{stitch_count}")

# Function
def on_press(key):
    try:
        if hasattr(key, "char") and key.char:  # regular characters
            pressed = key.char.lower()
        elif hasattr(key, "name"):  # special keys
            pressed = special_keys.get(key.name.lower(), key.name.lower())
        else:
            return

        if pressed == target_key:
            increment()
    except AttributeError:
        pass

def start_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# Main
root = tk.Tk()
root.title("Crochet Assistant")

window_width = 600
window_height = 400

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_x = (screen_width // 2) - (window_width // 2)
window_y = (screen_height // 2) - (window_height // 2) - 200

root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")
root.attributes('-topmost', True)

# Set global font to Roboto Mono
roboto_mono = tkFont.Font(family="Roboto Mono", size=12)
root.option_add("*Font", roboto_mono)

# Counter frame
counter_frame = tk.Frame(root, bg=themes[current_theme]["bg"])
counter_frame.place(x=42, relx=0.5, y=150, anchor="center")

# Stitch button frame
button_frame = tk.Frame(root, bg=themes[current_theme]["bg"])
button_frame.place(x=42, relx=0.5, y=320, anchor="center")

# Stitch buttons
button_specs = [
    ("+1", 0, 0), ("+5", 0, 1), ("+10", 0, 2),
    ("-1", 1, 0), ("-5", 1, 1), ("-10", 1, 2)
]
circular_buttons = []

def create_circular_button(parent, text, command=None, diameter=50, alone=False, fontSize=12):
    canvas = tk.Canvas(parent, width=diameter, height=diameter, highlightthickness=0, bg=themes[current_theme]["bg"])
    oval = canvas.create_oval(2, 2, diameter-2, diameter-2, fill=themes[current_theme]["sb"], outline="")
    label = canvas.create_text(diameter//2, diameter//2, text=text, fill=themes[current_theme]["fg"], font=("Roboto Mono", fontSize))

    if command:
        canvas.bind("<Button-1>", lambda e: command())
    
    if not alone:
        canvas.grid(row=spec[1], column=spec[2], padx=5, pady=5)
    return canvas

# Counter undo button
row_undo_button = create_circular_button(root, "-1", subtract_row, 30, True)
row_undo_button.place(x=42, relx=0.5, y=150, anchor="center")

for spec in button_specs:
    text, row, col = spec
    if text.startswith("+"):
        def make_cmd(x=int(text[1:])):
            return lambda: increment_by(x)
    else:
        def make_cmd(x=-int(text[1:])):
            return lambda: increment_by(x)
    btn = create_circular_button(button_frame, text, make_cmd(), 50, False, 20)
    circular_buttons.append(btn)

def increment_by(amount):
    global stitch_count
    stitch_count += amount
    s_label.config(text=f"{stitch_count}")

# Rows label
rows_label = tk.Label(counter_frame, text="Rows", font=("Roboto Mono", 20), bg=themes[current_theme]["bg"], fg=themes[current_theme]["fg"])
rows_label.pack()

# Row counter label
label = tk.Label(counter_frame, text="0", font=("Roboto Mono", 40), bg=themes[current_theme]["bg"], fg=themes[current_theme]["fg"])
label.pack()

# Stitches label
stitches_label = tk.Label(counter_frame, text="\nStitches", font=("Roboto Mono", 20), bg=themes[current_theme]["bg"], fg=themes[current_theme]["fg"])
stitches_label.pack()

# Stitch counter label
s_label = tk.Label(counter_frame, text="0", font=("Roboto Mono", 40), bg=themes[current_theme]["bg"], fg=themes[current_theme]["fg"])
s_label.pack()

# Sidebar frame
sidebar = tk.Frame(root, width=0, height=300)
sidebar.place(x=0,y=0,relheight=1)

# Sidebar buttons
def create_sidebar_button(text, command):
    btn = tk.Label(
        sidebar,
        text=text,
        bg=sidebar["bg"],       # true background
        fg=themes[current_theme]["fg"],
        anchor="w",              # left-align text
        padx=10,
        pady=2
    )
    btn.bind("<Button-1>", lambda e: command())

    # hover
    def on_enter(e):
        btn.config(bg=themes[current_theme]["hv_bg"], fg=themes[current_theme]["hv_fg"])
    def on_leave(e):
        btn.config(bg=themes[current_theme]["sb"], fg=themes[current_theme]["fg"])

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

theme_button = create_sidebar_button("theme", toggle_theme_options)
key_button = create_sidebar_button(f"key: {target_key.upper()}", change_keybind)
reset_button = create_sidebar_button("reset", reset)
undo_reset_button = create_sidebar_button("undo reset", undo_reset)

sidebar_buttons = [theme_button, key_button, reset_button, undo_reset_button]
for i, b in enumerate(sidebar_buttons):
    b.pack(pady=2,fill="x")

# Theme option buttons (start hidden)
def create_color_circle(parent, bg_color, fg_color, diameter=30, command=None):
    canvas = tk.Canvas(parent, width=diameter, height=diameter, highlightthickness=0, bg=parent["bg"])

    canvas.oval_id = canvas.create_oval(2, 2, diameter-2, diameter-2, fill=bg_color, outline=fg_color, width=2)

    if command:
        canvas.bind("<Button-1>", lambda e: command())

    def on_enter(e):
        scale_factor = 1.13
        canvas_width = int(canvas["width"])
        canvas_height = int(canvas["height"])

        new_size = int(diameter * scale_factor)
        offset = (new_size - diameter) // 2
        canvas.coords(canvas.oval_id, 2-offset, 2-offset, diameter-2+offset, diameter-2+offset)

    def on_leave(e):
        canvas.coords(canvas.oval_id, 2, 2, diameter-2, diameter-2)

    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)

    return canvas

theme_frame = tk.Frame(root, bg=themes[current_theme]["sb"], pady=10, padx=5)

theme_option_buttons = []
for name, t in themes.items():
    btn = create_color_circle(theme_frame, t["bg"], t["fg"], command=lambda n=name: set_theme(n))
    theme_option_buttons.append(btn)

set_theme(current_theme)

# Run the keyboard listener in a separate thread so Tkinter stays responsive
listener_thread = threading.Thread(target=start_listener, daemon=True)
listener_thread.start()

root.mainloop()