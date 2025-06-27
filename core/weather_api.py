import requests
from config import weather_api as config
from core.error_handling import WeatherAPIError, ConfigError

def get_weather(city):
    api_key = config.OPENWEATHER_API_KEY
    if not api_key:
        raise ConfigError("Missing OpenWeather API key.")

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        return {
            "city": data["name"],
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"]
        }

    except requests.exceptions.RequestException as e:
        raise WeatherAPIError(f"API request failed: {e}")

