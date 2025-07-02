from datetime import datetime

def get_time_of_day():
    hour = datetime.now().hour
    return "day" if 6 <= hour < 18 else "night"

def get_color_theme(selected_theme):
    time_of_day = get_time_of_day()

    themes = {
        "anime": {
            "day":    ("#fef6e4", "#001858", "#ff8906"),
            "night":  ("#2b2d42", "#edf2f4", "#8d99ae")
        },
        "marvel": {
            "day":    ("#e6f0ff", "#003366", "#ff4d4d"),
            "night":  ("#1a1a2e", "#e94560", "#16213e")
        }
    }

    return themes.get(selected_theme, themes["anime"])[time_of_day]

FONT_LG = ("Helvetica", 40, "bold")
FONT_MD = ("Helvetica", 20)
FONT_SM = ("Helvetica", 16)

ENTRY_WIDTH = 200
TABVIEW_SIZE = (680, 460)


