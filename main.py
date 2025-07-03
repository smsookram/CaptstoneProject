customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from core.weather_api import get_weather
from core.storage import save_last_city, load_last_city, log_weather_data
from core.theme_selector import select_theme
from utils.style import get_theme_colors, get_background_image_path

# === Init CustomTkinter ===
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# === Ask for Theme Before Launch ===
user_theme = select_theme()
colors = get_theme_colors(user_theme)
bg_image_path = get_background_image_path(user_theme)

# === Create Main Window ===
app = ctk.CTk()
app.title("Weather Dashboard")
app.geometry("800x600")
app.resizable(True, True)

# === Set Background Image ===
bg_image = Image.open(bg_image_path).resize((800, 600))
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = ctk.CTkLabel(app, image=bg_photo, text="")
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# === Tabs ===
tabview = ctk.CTkTabview(app, width=760, height=540, segmented_button_selected_color=colors["accent"])
tabview.place(relx=0.5, rely=0.5, anchor="center")

weather_tab = tabview.add("Weather")
activity_tab = tabview.add("Activities")
settings_tab = tabview.add("Settings")

# === Weather Tab ===
city_entry = ctk.CTkEntry(weather_tab, placeholder_text="Enter City", width=200)
city_entry.pack(pady=10)

weather_label = ctk.CTkLabel(weather_tab, text="", text_color=colors["fg"], font=("Helvetica", 20))
weather_label.pack(pady=5)

temp_label = ctk.CTkLabel(weather_tab, text="", text_color=colors["fg"], font=("Helvetica", 40, "bold"))
temp_label.pack(pady=5)

desc_label = ctk.CTkLabel(weather_tab, text="", text_color=colors["accent"], font=("Helvetica", 18))
desc_label.pack(pady=5)

unit_var = ctk.StringVar(value="C")  # For toggle
def toggle_unit():
    current = unit_var.get()
    unit_var.set("F" if current == "C" else "C")
    fetch_weather()

unit_toggle = ctk.CTkButton(weather_tab, text="Switch °C / °F", command=toggle_unit)
unit_toggle.pack(pady=5)

def fetch_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showerror("Input Error", "Please enter a city.")
        return

    try:
        units = "imperial" if unit_var.get() == "F" else "metric"
        weather = get_weather(city, units=units)
        if weather:
            weather_label.configure(text=weather["city"])
            temp_label.configure(text=f"{weather['temp']}°{unit_var.get()}")
            desc_label.configure(text=weather["description"].title())
            save_last_city(city)
            log_weather_data(city, weather["temp"], weather["description"])
        else:
            messagebox.showerror("Error", "Could not retrieve weather.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

fetch_button = ctk.CTkButton(weather_tab, text="Get Weather", command=fetch_weather, fg_color=colors["accent"])
fetch_button.pack(pady=10)

# === Load Last City ===
last_city = load_last_city()
if last_city:
    city_entry.insert(0, last_city)
    fetch_weather()

app.mainloop()










