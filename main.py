import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from core.weather_api import get_weather
from core.storage import (
    save_last_city, load_last_city, log_weather_data, get_user_settings
)
from core.error_handling import WeatherAPIError
from utils.style import THEMES, apply_theme

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("600x400")
        self.root.resizable(True, True)

        # Load settings
        self.settings = get_user_settings()
        self.units = self.settings.get("units", "metric")

        # Detect time and assign day/night
        current_hour = datetime.now().hour
        if 6 <= current_hour < 18:
            self.time_theme = "day"
        else:
            self.time_theme = "night"

        self.visual_theme = self.settings.get("theme", "anime")  # default to anime
        self.current_theme = THEMES.get(self.visual_theme, THEMES["anime"])

        # Setup UI
        self.create_widgets()
        apply_theme(self.root, self.current_theme)

        # Preload last city
        last_city = load_last_city()
        if last_city:
            self.city_entry.insert(0, last_city)
            self.fetch_weather()

    def create_widgets(self):
        self.city_entry = tk.Entry(
            self.root,
            font=self.current_theme["font"],
            bg=self.current_theme["bg"],
            fg=self.current_theme["fg"]
        )
        self.city_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.root.grid_columnconfigure(0, weight=1)

        self.fetch_button = tk.Button(
            self.root,
            text="Get Weather",
            command=self.fetch_weather,
            bg=self.current_theme["fg"],
            fg=self.current_theme["bg"]
        )
        self.fetch_button.grid(row=0, column=1, padx=10, pady=10)

        self.theme_button = tk.Button(
            self.root,
            text="Toggle Theme",
            command=self.toggle_theme,
            bg=self.current_theme["fg"],
            fg=self.current_theme["bg"]
        )
        self.theme_button.grid(row=0, column=2, padx=10, pady=10)

        self.city_label = tk.Label(
            self.root,
            text="",
            font=self.current_theme["font"],
            bg=self.current_theme["bg"],
            fg=self.current_theme["fg"]
        )
        self.city_label.grid(row=1, column=0, columnspan=3, pady=10)

        self.temp_label = tk.Label(
            self.root,
            text="",
            font=self.current_theme["font"],
            bg=self.current_theme["bg"],
            fg=self.current_theme["fg"]
        )
        self.temp_label.grid(row=2, column=0, columnspan=3)

        self.desc_label = tk.Label(
            self.root,
            text="",
            font=self.current_theme["font"],
            bg=self.current_theme["bg"],
            fg=self.current_theme["fg"]
        )
        self.desc_label.grid(row=3, column=0, columnspan=3)

    def fetch_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showerror("Input Error", "Please enter a city name.")
            return

        try:
            weather = get_weather(city, units=self.units)
            if weather:
                self.city_label.config(text=weather["city"])
                self.temp_label.config(text=f"{weather['temp']}°")
                self.desc_label.config(text=weather["description"].title())

                save_last_city(city)
                log_weather_data(city=weather["city"], temp=weather["temp"], desc=weather["description"])
            else:
                messagebox.showerror("Weather Error", "Could not fetch weather data.")
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{e}")

    def toggle_theme(self):
        self.visual_theme = "marvel" if self.visual_theme == "anime" else "anime"
        self.current_theme = THEMES.get(self.visual_theme)
        apply_theme(self.root, self.current_theme)

        # Update widgets
        widgets = [
            self.city_entry, self.fetch_button, self.theme_button,
            self.city_label, self.temp_label, self.desc_label
        ]
        for widget in widgets:
            widget.config(
                bg=self.current_theme["bg"],
                fg=self.current_theme["fg"],
                font=self.current_theme["font"]
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()


