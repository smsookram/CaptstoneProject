import os
from datetime import datetime
import configparser

# Set up path to /data folder (relative to this file)
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
LAST_CITY_PATH = os.path.join(DATA_DIR, "last_city.txt")
HISTORY_PATH = os.path.join(DATA_DIR, "weather_history.txt")
SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "settings.ini")

# --------- Save/Load Last City --------- #

def save_last_city(city, filename=LAST_CITY_PATH):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(city.strip())

def load_last_city(filename=LAST_CITY_PATH):
    try:
        with open(filename, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

# --------- Log Weather History --------- #

def log_weather_data(city, temp, desc, filename=HISTORY_PATH):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    date = datetime.now().strftime("%Y-%m-%d")
    with open(filename, "a") as f:
        f.write(f"{date},{city},{temp},{desc}\n")

# --------- Load/Save Settings (theme/units) --------- #

def get_user_settings():
    config = configparser.ConfigParser()
    if not os.path.exists(SETTINGS_PATH):
        return {"theme": "day", "units": "metric"}

    config.read(SETTINGS_PATH)
    return {
        "theme": config.get("Preferences", "theme", fallback="day"),
        "units": config.get("Preferences", "units", fallback="metric")
    }

def save_user_settings(theme="day", units="metric"):
    config = configparser.ConfigParser()
    config["Preferences"] = {
        "theme": theme,
        "units": units
    }
    with open(SETTINGS_PATH, "w") as f:
        config.write(f)

