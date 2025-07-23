import os
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image, ImageTk


# Store currently active animation
_active_animation = {"label": None, "frames": []}

def apply_weather_effect(container, weather_desc):
    global _active_animation

    # Clear any existing animation
    if _active_animation["label"]:
        _active_animation["label"].destroy()
        _active_animation = {"label": None, "frames": []}

    weather_desc = weather_desc.lower()
    effect_file = None

    # Match description to animation file
    if "rain" in weather_desc:
        effect_file = "rain.gif"
    elif "snow" in weather_desc:
        effect_file = "snow.gif"
    elif "cloud" in weather_desc:
        effect_file = "clouds.gif"
    elif "clear" in weather_desc:
        effect_file = "sun.gif"

    if not effect_file:
        return

    path = os.path.join("assets", "effects", effect_file)

    try:
        img = Image.open(path)
        frames = []

        try:
            while True:
                frame = img.copy().convert("RGBA").resize((800, 450))
                frames.append(CTkImage(light_image=frame, size=(800, 450)))
                img.seek(len(frames))  # Go to next frame
        except EOFError:
            pass

        if not frames:
            return

        label = ctk.CTkLabel(container, text="", image=frames[0])
        label.place(relx=0.5, rely=0.5, anchor="center")
        label.lift()

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
