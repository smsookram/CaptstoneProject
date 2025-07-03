import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from core.weather_api import get_weather
from core.storage import save_last_city, load_last_city, log_weather_data
from core.theme_selector import select_theme
from utils.style import get_color_theme
from utils.style import FONT_LG, FONT_MD, FONT_SM, ENTRY_WIDTH, TABVIEW_SIZE




# ==== Initialize customtkinter ====
ctk.set_appearance_mode("System")  # Auto switch between light/dark
ctk.set_default_color_theme("blue")  # Can be "dark-blue", "green", "dark-blue", etc.


# ==== Ask user to choose theme ====
user_theme = select_theme()  # Assume this returns "marvel" or "anime"
bg_color, text_color, accent_color = get_color_theme(user_theme)

# ==== Create App Window ====
app = ctk.CTk()
app.title("Weather Dashboard")
app.geometry("700x500")
app.configure(fg_color=bg_color)

import customtkinter as ctk

app = ctk.CTk()
app.title("Weather Dashboard")
app.geometry("700x500")


# ==== Tabs using CTkTabview ====
tabview = ctk.CTkTabview(app, width=680, height=460, segmented_button_selected_color=accent_color)
tabview.pack(pady=10, padx=10)

weather_tab = tabview.add("Weather")
activity_tab = tabview.add("Activities")
settings_tab = tabview.add("Settings")

# ==== Weather Tab Widgets ====
city_entry = ctk.CTkEntry(weather_tab, placeholder_text="Enter City", width=200, height=35)
city_entry.pack(pady=10)

weather_label = ctk.CTkLabel(weather_tab, text="", text_color=text_color, font=("Helvetica", 20))
weather_label.pack(pady=5)

temp_label = ctk.CTkLabel(weather_tab, text="", text_color=text_color, font=("Helvetica", 40, "bold"))
temp_label.pack(pady=5)

desc_label = ctk.CTkLabel(weather_tab, text="", text_color=accent_color, font=("Helvetica", 18))
desc_label.pack(pady=5)

# ==== Fetch Weather ====
def fetch_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showerror("Input Error", "Please enter a city name.")
        return

    try:
        weather = get_weather(city)
        if weather:
            weather_label.configure(text=weather["city"])
            temp_label.configure(text=f"{weather['temp']}°C")
            desc_label.configure(text=weather["description"].title())
            save_last_city(city)
            log_weather_data(city, weather["temp"], weather["description"])
        else:
            messagebox.showerror("Error", "Weather data not found.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ==== Button ====
fetch_button = ctk.CTkButton(weather_tab, text="Get Weather", command=fetch_weather, fg_color=accent_color)
fetch_button.pack(pady=10)

# ==== Load Last City Automatically ====
last_city = load_last_city()
if last_city:
    city_entry.insert(0, last_city)
    fetch_weather()

# ==== Run App ====
app.mainloop()




