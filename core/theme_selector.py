import tkinter as tk
from tkinter import simpledialog

def select_theme():
    root = tk.Tk()
    root.withdraw()

    theme = None
    while theme not in ["marvel", "anime"]:
        theme = simpledialog.askstring(
            "Choose Theme",
            "Type your theme: 'marvel' or 'anime'"
        )
        if theme:
            theme = theme.lower()

    root.destroy()
    return theme


