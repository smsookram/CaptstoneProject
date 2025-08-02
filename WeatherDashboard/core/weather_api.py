import os
import requests
from dotenv import load_dotenv
from core.error_handling import WeatherAPIError, ConfigError
from geopy.geocoders import Nominatim

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
            "feels_like": round(data["main"]["feels_like"]),
            "humidity": data["main"]["humidity"],
            "temp_min": round(data["main"]["temp_min"]),
            "temp_max": round(data["main"]["temp_max"]),
            "description": data["weather"][0]["description"]
        }

    except requests.RequestException as e:
        raise WeatherAPIError(str(e))

def get_hourly_forecast(city_name, unit="C"):
    try:
        # Get coordinates from city name
        geolocator = Nominatim(user_agent="weather_app")
        location = geolocator.geocode(city_name)
        if not location:
            return None

        lat = location.latitude
        lon = location.longitude

        # Fetch hourly forecast data
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&"
            f"hourly=temperature_2m,relative_humidity_2m,precipitation_probability,"
            f"weathercode,windspeed_10m&timezone=auto"
        )
        
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to get weather data: {response.status_code}")
            return None
        
        data = response.json()

        hourly = data.get("hourly")
        if "hourly" not in data:
            return None
        
        # Parse and organize hourly data
        hours = hourly.get("time", [])
        temps = hourly.get("temperature_2m", [])
        humidities = hourly.get("relative_humidity_2m", [])
        precips = hourly.get("precipitation_probability", [])
        weathercodes = hourly.get("weathercode", [])
        winds = hourly.get("windspeed_10m", [])
        
        if unit == "F":
            temps = [(t * 9/5) + 32 for t in temps]

        forecast_data = []
        for i in range(len(hours)):
            forecast_data.append({
                "time": hours[i],
                "temp": temps[i],
                "humidity": humidities[i],
                "precip_prob": precips[i],
                "weathercode": weathercodes[i],
                "wind": winds[i]
            })

        return forecast_data

    except Exception as e:
        print(f"Error fetching forecast: {e}")
        return None