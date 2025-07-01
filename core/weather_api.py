# core/weather_api.py

import os
import requests
from dotenv import load_dotenv
from core.error_handling import WeatherAPIError, ConfigError

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not API_KEY:
    raise ConfigError("Missing OpenWeather API key in .env file")

def get_weather(city, units="metric"):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": units
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code != 200:
            raise WeatherAPIError(data.get("message", "API request failed."))

        return {
            "city": data["name"],
            "temp": round(data["main"]["temp"]),
            "description": data["weather"][0]["description"]
        }

    except requests.RequestException as e:
        raise WeatherAPIError(str(e))
