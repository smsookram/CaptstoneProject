import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from core.weather_api import get_weather
from core.storage import save_last_city, load_last_city, log_weather_data
from core.theme_selector import select_theme
from utils.style import get_theme_colors, get_background_image_path
from customtkinter import CTkImage

# Initialize CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Ask user for theme (Marvel, Anime, etc.)
user_theme = select_theme()
colors = get_theme_colors(user_theme)
bg_image_path = get_background_image_path(user_theme)

# Create main app window
app = ctk.CTk()
app.title("Weather Dashboard")
app.geometry("800x600")
app.resizable(True, True)

# Load and set background image with CTkImage
pil_bg_image = Image.open(bg_image_path).resize((800, 600))
bg_image = CTkImage(pil_bg_image)
bg_label = ctk.CTkLabel(app, image=bg_image, text="")
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.lower()  # send to back

# Create a transparent frame on top for your widgets
main_frame = ctk.CTkFrame(app, fg_color="transparent")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# City Entry
city_entry = ctk.CTkEntry(
    main_frame,
    placeholder_text="Enter City",
    width=200,
    fg_color="#ffffff80",  # White with some transparency, adjust as needed
    text_color=colors["fg"],
    placeholder_text_color="#888888",
    border_width=0
)
city_entry.pack(pady=10)

# Weather Labels with transparent backgrounds
weather_label = ctk.CTkLabel(main_frame, text="", text_color=colors["fg"], fg_color="transparent", font=("Helvetica", 20))
weather_label.pack(pady=5)

temp_label = ctk.CTkLabel(main_frame, text="", text_color=colors["fg"], fg_color="transparent", font=("Helvetica", 40, "bold"))
temp_label.pack(pady=5)

desc_label = ctk.CTkLabel(main_frame, text="", text_color=colors["accent"], fg_color="transparent", font=("Helvetica", 18))
desc_label.pack(pady=5)

# Unit toggle button (solid background, but keep it subtle)
unit_var = ctk.StringVar(value="C")
def toggle_unit():
    current = unit_var.get()
    unit_var.set("F" if current == "C" else "C")
    fetch_weather()

unit_toggle = ctk.CTkButton(main_frame, text="Switch °C / °F", command=toggle_unit, fg_color=colors["accent"])
unit_toggle.pack(pady=5)

# Fetch weather function
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

fetch_button = ctk.CTkButton(main_frame, text="Get Weather", command=fetch_weather, fg_color=colors["accent"])
fetch_button.pack(pady=10)

# Load last city and fetch weather on startup
last_city = load_last_city()
if last_city:
    city_entry.insert(0, last_city)
    fetch_weather()

app.mainloop()








