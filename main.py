import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from customtkinter import CTkImage
from core.weather_api import get_weather
from core.storage import save_last_city, load_last_city, log_weather_data
from utils.style import get_theme_colors, get_background_image_path, get_time_of_day
from utils.scrollable_frame import ScrollableFrame

# === Init CustomTkinter ===
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

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

def main():
    app = ctk.CTk()
    app.title("Weather Dashboard")
    app.geometry("800x600")
    app.minsize(600, 450)

    user_theme = select_theme_popup()
    current_time_mode = get_time_of_day()

    colors = get_theme_colors(user_theme, current_time_mode)
    bg_image_path = get_background_image_path(user_theme, current_time_mode)

    original_bg_image = Image.open(bg_image_path)

    # Initial background image
    initial_size = (800, 600)
    bg_photo = CTkImage(light_image=original_bg_image.resize(initial_size), size=initial_size)
    bg_label = ctk.CTkLabel(app, image=bg_photo, text="")
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.lower()

    def resize_bg(event):
        w, h = event.width, event.height
        orig_w, orig_h = original_bg_image.size
        ratio = min(w / orig_w, h / orig_h)
        new_size = (int(orig_w * ratio), int(orig_h * ratio))

        resized_img = original_bg_image.resize(new_size, Image.LANCZOS)
        new_photo = CTkImage(light_image=resized_img, size=new_size)

        bg_label.configure(image=new_photo)
        bg_label.image = new_photo  # keep reference

        # Center the image
        x = (w - new_size[0]) // 2
        y = (h - new_size[1]) // 2
        bg_label.place(x=x, y=y, width=new_size[0], height=new_size[1])

    app.bind("<Configure>", resize_bg)

    # Fixed size main tabview container, centered
    tabview = ctk.CTkTabview(
        app,
        width=600,
        height=400,
        segmented_button_selected_color=colors["accent"],
        fg_color="#f0f0f0",
        border_width=1,
        corner_radius=15
    )
    tabview.place(relx=0.5, rely=0.5, anchor="center")

    weather_tab = tabview.add("Weather")
    activity_tab = tabview.add("Activities")
    settings_tab = tabview.add("Settings")

    # Scrollable frame inside Weather tab
    scrollable = ScrollableFrame(weather_tab)
    scrollable.pack(fill="both", expand=True, padx=10, pady=10)

    city_entry = ctk.CTkEntry(scrollable.scrollable_frame, placeholder_text="Enter City", width=200)
    city_entry.pack(pady=10)

    weather_label = ctk.CTkLabel(scrollable.scrollable_frame, text="", text_color=colors["fg"], font=("Helvetica", 20))
    weather_label.pack(pady=5)

    # Explicit visible color for temp label
    temp_label = ctk.CTkLabel(scrollable.scrollable_frame, text="", text_color=colors["fg"] or "#000000", font=("Helvetica", 40, "bold"))
    temp_label.pack(pady=5)

    desc_label = ctk.CTkLabel(scrollable.scrollable_frame, text="", text_color=colors["accent"], font=("Helvetica", 18))
    desc_label.pack(pady=5)

    unit_var = ctk.StringVar(value="C")

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

    def toggle_unit():
        current = unit_var.get()
        unit_var.set("F" if current == "C" else "C")
        fetch_weather()

    fetch_button = ctk.CTkButton(scrollable.scrollable_frame, text="Get Weather", command=fetch_weather, fg_color=colors["accent"])
    fetch_button.pack(pady=10)

    unit_toggle = ctk.CTkButton(scrollable.scrollable_frame, text="Switch °C / °F", command=toggle_unit)
    unit_toggle.pack(pady=5)

    city_entry.bind("<Return>", lambda event: fetch_weather())

    # Load last city if any
    last_city = load_last_city()
    if last_city:
        city_entry.insert(0, last_city)
        fetch_weather()

    # Settings tab: toggle light/dark mode
    def toggle_time_mode():
        nonlocal current_time_mode, colors, bg_image_path, original_bg_image

        current_time_mode = "night" if current_time_mode == "day" else "day"
        colors = get_theme_colors(user_theme, current_time_mode)
        bg_image_path = get_background_image_path(user_theme, current_time_mode)

        original_bg_image = Image.open(bg_image_path)

        # Update background for current window size
        w, h = app.winfo_width(), app.winfo_height()
        orig_w, orig_h = original_bg_image.size
        ratio = min(w / orig_w, h / orig_h)
        new_size = (int(orig_w * ratio), int(orig_h * ratio))
        resized_img = original_bg_image.resize(new_size, Image.LANCZOS)
        new_photo = CTkImage(light_image=resized_img, size=new_size)
        bg_label.configure(image=new_photo)
        bg_label.image = new_photo
        x = (w - new_size[0]) // 2
        y = (h - new_size[1]) // 2
        bg_label.place(x=x, y=y, width=new_size[0], height=new_size[1])

        # Update colors on widgets
        weather_label.configure(text_color=colors["fg"])
        temp_label.configure(text_color=colors["fg"] or "#000000")
        desc_label.configure(text_color=colors["accent"])
        fetch_button.configure(fg_color=colors["accent"])
        unit_toggle.configure(fg_color=colors["accent"])
        tabview.configure(segmented_button_selected_color=colors["accent"])

    toggle_btn = ctk.CTkButton(settings_tab, text="Toggle Light/Dark Mode", command=toggle_time_mode)
    toggle_btn.pack(pady=20)

    app.mainloop()

if __name__ == "__main__":
    main()













