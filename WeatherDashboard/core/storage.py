# core/storage.py

import os
from datetime import datetime

DATA_DIR = "data"
LAST_CITY_FILE = os.path.join(DATA_DIR, "last_city.txt")
HISTORY_FILE = os.path.join(DATA_DIR, "weather_history.txt")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.txt")

def save_last_city(city):
    with open(LAST_CITY_FILE, "w") as f:
        f.write(city)

def load_last_city():
    if os.path.exists(LAST_CITY_FILE):
        with open(LAST_CITY_FILE, "r") as f:
            return f.read().strip()
    return None

def log_weather_data(city, temp, desc):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(HISTORY_FILE, "a") as f:
        f.write(f"{timestamp},{city},{temp},{desc}\n")

def get_user_settings():
    default_settings = {"theme": "day", "units": "metric"}
    if not os.path.exists(SETTINGS_FILE):
        return default_settings
    settings = {}
    with open(SETTINGS_FILE, "r") as f:
        for line in f:
            if "=" in line:
                key, val = line.strip().split("=", 1)
                settings[key] = val
    return {**default_settings, **settings}


