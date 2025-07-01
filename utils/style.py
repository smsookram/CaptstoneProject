# utils/style.py

THEMES = {
    "day": {
        "bg": "#ffffff",
        "fg": "#000000",
        "font": ("Comic Sans MS", 12)
    },
    "night": {
        "bg": "#1a1a1a",
        "fg": "#f5f5f5",
        "font": ("Courier New", 12)
    },
    "anime": {
        "bg": "#fce4ec",  # light pink
        "fg": "#880e4f",  # dark magenta
        "font": ("Helvetica", 12, "bold")
    },
    "marvel": {
        "bg": "#0d1b2a",  # navy
        "fg": "#e63946",  # crimson red
        "font": ("Impact", 12)
    }
}

def apply_theme(root, theme):
    root.configure(bg=theme["bg"])

