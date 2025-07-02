import customtkinter as ctk

def select_theme():
    """
    Popup for user to select between Marvel and Anime.
    Returns the selected theme as a lowercase string.
    """
    theme_choice = {"value": None}

    def choose(theme):
        theme_choice["value"] = theme
        popup.destroy()

    popup = ctk.CTk()
    popup.title("Choose Your Theme")
    popup.geometry("400x250")
    popup.resizable(False, False)

    label = ctk.CTkLabel(popup, text="Select Your Experience", font=("Helvetica", 18, "bold"))
    label.pack(pady=20)

    btn_frame = ctk.CTkFrame(popup, fg_color="transparent")
    btn_frame.pack(pady=10)

    anime_btn = ctk.CTkButton(btn_frame, text="Anime", command=lambda: choose("anime"), width=120)
    anime_btn.grid(row=0, column=0, padx=20)

    marvel_btn = ctk.CTkButton(btn_frame, text="Marvel", command=lambda: choose("marvel"), width=120)
    marvel_btn.grid(row=0, column=1, padx=20)

    popup.mainloop()
    return theme_choice["value"]

