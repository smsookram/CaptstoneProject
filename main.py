import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from customtkinter import CTkImage
from core.weather_api import get_weather
from core.storage import save_last_city, load_last_city, log_weather_data
from utils.style import get_theme_colors, get_background_image_path, get_time_of_day

# === Init CustomTkinter ===
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# === Theme Selection Popup ===
def select_theme_popup():
    selected_theme = {}

    def on_select(theme_name):
        selected_theme['theme'] = theme_name
        popup.destroy()

    popup = ctk.CTkToplevel()
    popup.geometry("300x150")
    popup.title("Select Theme")

    label = ctk.CTkLabel(popup, text="Choose your theme:")
    label.pack(pady=10)

    btn_anime = ctk.CTkButton(popup, text="Anime", command=lambda: on_select("anime"))
    btn_anime.pack(pady=5, fill="x", padx=20)

    btn_marvel = ctk.CTkButton(popup, text="Marvel", command=lambda: on_select("marvel"))
    btn_marvel.pack(pady=5, fill="x", padx=20)

    popup.grab_set()
    popup.wait_window()

    return selected_theme.get('theme', 'anime')

# === Main App ===
def main():
    app = ctk.CTk()
    app.title("Weather Dashboard")
    app.geometry("800x600")
    app.resizable(True, True)

    user_theme = select_theme_popup()
    current_time_mode = get_time_of_day()

    colors = get_theme_colors(user_theme, current_time_mode)
    bg_image_path = get_background_image_path(user_theme, current_time_mode)

    # Background Image
    bg_image = Image.open(bg_image_path)
    bg_photo = CTkImage(light_image=bg_image, size=(800, 600))
    bg_label = ctk.CTkLabel(app, image=bg_photo, text="")
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.lower()

    # Tabs
    tabview = ctk.CTkTabview(
        app,
        width=600,
        height=450,
        segmented_button_selected_color=colors["accent"],
        fg_color="#f0f0f0",  # Soft background
        border_width=1,
        corner_radius=15
    )
    tabview.place(relx=0.5, rely=0.5, anchor="center")

    weather_tab = tabview.add("Weather")
    activity_tab = tabview.add("Activities")
    settings_tab = tabview.add("Settings")

    # Weather Tab Widgets
    city_entry = ctk.CTkEntry(weather_tab, placeholder_text="Enter City", width=200)
    city_entry.pack(pady=10)

    city_entry.bind("<Return>", lambda event: fetch_weather())


    weather_label = ctk.CTkLabel(weather_tab, text="", text_color=colors["fg"], font=("Helvetica", 20))
    weather_label.pack(pady=5)

    temp_label = ctk.CTkLabel(weather_tab, text="", text_color="black", font=("Helvetica", 40, "bold"))
    temp_label.pack(pady=5)

    desc_label = ctk.CTkLabel(weather_tab, text="", text_color=colors["accent"], font=("Helvetica", 18))
    desc_label.pack(pady=5)

    feels_like_label = ctk.CTkLabel(weather_tab, text="", text_color="gray", font=("Helvetica", 14))
    feels_like_label.pack(pady=2)

    humidity_label = ctk.CTkLabel(weather_tab, text="", text_color="gray", font=("Helvetica", 14))
    humidity_label.pack(pady=2)

    high_low_label = ctk.CTkLabel(weather_tab, text="", text_color="gray", font=("Helvetica", 14))
    high_low_label.pack(pady=2)

    unit_var = ctk.StringVar(value="C")

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
            print(weather)
            if weather:
                weather_label.configure(text=weather["city"])
                temp_label.configure(text=f"{weather['temp']}°{unit_var.get()}")
                desc_label.configure(text=weather["description"].title())
                feels_like_label.configure(text=f"Feels like: {weather['feels_like']}°{unit_var.get()}")
                humidity_label.configure(text=f"Humidity: {weather['humidity']}%")
                high_low_label.configure(
                text=f"High: {weather['temp_max']}° / Low: {weather['temp_min']}°"
)

                save_last_city(city)
                log_weather_data(city, weather["temp"], weather["description"])
            else:
                messagebox.showerror("Error", "Could not retrieve weather.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    fetch_button = ctk.CTkButton(weather_tab, text="Get Weather", command=fetch_weather, fg_color=colors["accent"])
    fetch_button.pack(pady=10)

    # Load last city
    last_city = load_last_city()
    if last_city:
        city_entry.insert(0, last_city)
        fetch_weather()

    # Settings Tab: Toggle Day/Night Mode
    def toggle_time_mode():
        nonlocal current_time_mode, colors, bg_image_path

        current_time_mode = "night" if current_time_mode == "day" else "day"
        colors = get_theme_colors(user_theme, current_time_mode)
        bg_image_path = get_background_image_path(user_theme, current_time_mode)

        # Reload background
        new_bg_image = Image.open(bg_image_path)
        new_bg_photo = CTkImage(light_image=new_bg_image, size=(800, 600))
        bg_label.configure(image=new_bg_photo)
        bg_label.image = new_bg_photo  # keep reference

        # Update widget colors
        weather_label.configure(text_color=colors["fg"])
        temp_label.configure(text_color="black")
        desc_label.configure(text_color=colors["accent"])
        fetch_button.configure(fg_color=colors["accent"])
        tabview.configure(segmented_button_selected_color=colors["accent"])

    toggle_btn = ctk.CTkButton(settings_tab, text="Toggle Light/Dark Mode", command=toggle_time_mode)
    toggle_btn.pack(pady=20)

    app.mainloop()

if __name__ == "__main__":
    main()












