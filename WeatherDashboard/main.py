import os
import customtkinter as ctk
from gui import WeatherDashboardApp  # Our big GUI class (in gui.py)
from features.trivia import get_five_questions

os.chdir(os.path.dirname(os.path.abspath(__file__)))
print("Working Directory:", os.getcwd())

# === Init CustomTkinter Appearance and Theme ===
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
    user_theme = select_theme_popup()
    WeatherDashboardApp(app, user_theme)
    app.mainloop()


if __name__ == "__main__":
    main()
