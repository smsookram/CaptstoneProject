import os
import tkinter as tk  
from PIL import Image, ImageTk

# Store currently active animation
_active_animation = {"label": None, "frames": []}

def apply_weather_effect(container, weather_desc, bg_color="#ffffff"):
    global _active_animation

    # Clear any existing animation
    if _active_animation["label"]:
        _active_animation["label"].destroy()
        _active_animation = {"label": None, "frames": []}

    weather_desc = weather_desc.lower()
    effect_file = None

    # Match description to animation file
    if "rain" in weather_desc:
        effect_file = "rain.jpg"
    elif "snow" in weather_desc:
        effect_file = "snow.jpg"
    elif "cloud" in weather_desc:
        effect_file = "clouds.jpg"
    elif "clear" in weather_desc:
        effect_file = "sun.jpg"

    if not effect_file:
        return

    path = os.path.join("assets", "effects", effect_file)

    try:
        img = Image.open(path)
        frames = []

        container.update_idletasks()
        width = container.winfo_width()
        height = container.winfo_height()

        try:
            while True:
                frame = img.copy().convert("RGBA").resize((800, 450))
                frames.append(ImageTk.PhotoImage(frame))
                img.seek(len(frames))  # Go to next frame
        except EOFError:
            pass

        if not frames:
            return

        label = tk.Label(container, image=frames[0], borderwidth=0, highlightthickness=0, bg=bg_color)
        label.place(relx=0.5, rely=0.5, anchor="center")
        label.lower()

        def animate(index=0):
            if not label.winfo_exists():
                return
            label.configure(image=frames[index])
            label.image = frames[index]
            label.after(100, animate, (index + 1) % len(frames))

        animate()
        _active_animation = {"label": label, "frames": frames}

    except Exception as e:
        print(f"[Animation Error] {e}")



