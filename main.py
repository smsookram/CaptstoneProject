import tkinter as tk
from tkinter import messagebox
from core.weather_api import get_weather
from core.storage import save_last_city, load_last_city
from core.error_handling import WeatherAPIError, ConfigError

def search_weather():
    city = city_entry.get()
    try:
        weather = get_weather(city)
        if weather:
            save_last_city(city)
            weather_label.config(
                text=f"{weather['city']}:\n{weather['description']}, {weather['temp']}°C"
            )
    except (WeatherAPIError, ConfigError) as e:
        messagebox.showerror("Error", str(e))

# GUI setup
root = tk.Tk()
root.title("Weather App")

city_entry = tk.Entry(root, width=30)
city_entry.pack(pady=10)

search_btn = tk.Button(root, text="Search", command=search_weather)
search_btn.pack()

weather_label = tk.Label(root, text="", font=("Arial", 14))
weather_label.pack(pady=20)

# Preload last city
last_city = load_last_city()
if last_city:
    city_entry.insert(0, last_city)
    search_weather()

root.mainloop()
