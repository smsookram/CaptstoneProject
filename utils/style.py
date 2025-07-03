from datetime import datetime

def get_time_of_day():
    hour = datetime.now().hour
    return "day" if 6 <= hour < 18 else "night"

def get_theme_colors(theme):
    time = get_time_of_day()

    if theme == "anime":
        return {
            "day": {"bg": "#fef6e4", "fg": "#001858", "accent": "#ff8906"},
            "night": {"bg": "#2b2d42", "fg": "#edf2f4", "accent": "#8d99ae"}
        }[time]

    return {
        "day": {"bg": "#e6f0ff", "fg": "#003366", "accent": "#ff4d4d"},
        "night": {"bg": "#1a1a2e", "fg": "#e94560", "accent": "#16213e"}
    }[time]

def get_background_image_path(theme):
    time = get_time_of_day()
    return f"assets/{theme}/{time}.jpg"




