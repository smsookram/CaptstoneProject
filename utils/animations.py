# utils/animations.py
import customtkinter as ctk
from PIL import Image, ImageTk
import os

# Store currently active animation
_active_animation = {"label": None, "image": None}

def apply_weather_effect(container, weather_desc):
    global _active_animation

    # Clear any existing animation
    if _active_animation["label"]:
        _active_animation["label"].destroy()
        _active_animation = {"label": None, "image": None}

    weather_desc = weather_desc.lower()
    effect_file = None

    # Match description to an animation file
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
        # Load the GIF (works best if resized beforehand in a GIF editor)
        img = Image.open(path)
        frames = []

        try:
            while True:
                frames.append(img.copy())
                img.seek(len(frames))  # move to next frame
        except EOFError:
            pass

        gif_frames = [ImageTk.PhotoImage(f.resize((800, 450))) for f in frames]

        label = ctk.CTkLabel(container, text="", image=gif_frames[0])
        label.place(relx=0.5, rely=0.5, anchor="center")
        label.lower()  # send behind widgets

        def animate(index=0):
            if not label.winfo_exists():
                return
            label.configure(image=gif_frames[index])
            label.image = gif_frames[index]
            label.after(100, animate, (index + 1) % len(gif_frames))

        animate()
        _active_animation = {"label": label, "image": gif_frames[0]}

    except Exception as e:
        print(f"[Animation Error] {e}")

