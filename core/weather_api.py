import requests
from config import weather_api

def get_weather(city):
    api_key = weather_api.OPENWEATHER_API_KEY
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        weather_info = {
            "city": data["name"],
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"]
        }

        return weather_info

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None

