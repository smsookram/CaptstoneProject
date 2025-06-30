import tkinter as tk
from tkinter import messagebox
from core.weather_api import get_weather
from core.storage import (save_last_city, load_last_city, log_weather_data, get_user_settings)
from core.error_handling import WeatherAPIError, ConfigError

# Basic day/night themes (expand later)
THEMES = {
    "day": {
        "bg": "#ffffff",
        "fg": "#000000",
        "font": ("Helvetica", 12)
    },
    "night": {
        "bg": "#1a1a1a",
        "fg": "#f5f5f5",
        "font": ("Helvetica", 12)
    }
}

# Load settings and theme
settings = get_user_settings()
current_theme = THEMES.get(settings["theme"], THEMES["day"])
units = settings["units"]

def fetch_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showerror("Input Error", "Please enter a city name.")
        return

    try:
        weather = get_weather(city, units=units)  # uses preferred unit (metric/imperial)
        if weather:
            # Update GUI
            city_label.config(text=f"{weather['city']}")
            temp_label.config(text=f"{weather['temp']}°")
            desc_label.config(text=weather["description"].title())

            # Save and log
            save_last_city(city)
            log_weather_data(
                city=weather["city"],
                temp=weather["temp"],
                desc=weather["description"]
            )
        else:
            messagebox.showerror("Weather Error", "Could not fetch weather data.")

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")


# GUI setup
root = tk.Tk()
root.title("Weather App")
root.geometry("400x400")

#apply theme colors
root.configure(bg=current_theme["bg"])

city_entry = tk.Entry(root, font=current_theme["font"], bg=current_theme["bg"], fg=current_theme["fg"])
city_entry.pack(pady=10)

fetch_button = tk.Button(root, text="Get Weather", command=fetch_weather, bg=current_theme["fg"], fg=current_theme["bg"])
fetch_button.pack(pady=5)


weather_label = tk.Label(root, text="", font=("Arial", 14))
weather_label.pack(pady=20)

city_label = tk.Label(root, text="", font=current_theme["font"], bg=current_theme["bg"], fg=current_theme["fg"])
city_label.pack(pady=5)

temp_label = tk.Label(root, text="", font=current_theme["font"], bg=current_theme["bg"], fg=current_theme["fg"])
temp_label.pack(pady=5)

desc_label = tk.Label(root, text="", font=current_theme["font"], bg=current_theme["bg"], fg=current_theme["fg"])
desc_label.pack(pady=5)
 

settings = get_user_settings()
current_theme = THEMES.get(settings["theme"], THEMES["day"])
units = settings["units"]

# Preload last city
last_city = load_last_city()
if last_city:
    city_entry.insert(0, last_city)
    fetch_weather()

root.mainloop()
