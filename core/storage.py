import json
import os

FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "last_search.json")

def save_last_city(city_name):
    try:
        with open(FILE_PATH, "w") as f:
            json.dump({"last_city": city_name}, f)
    except Exception as e:
        print("Failed to save city:", e)

def load_last_city():
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r") as f:
                data = json.load(f)
                return data.get("last_city")
        except Exception:
            return None
    return None

