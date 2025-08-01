import requests
import time
import logging
from datetime import datetime
from typing import Dict, Optional
from config.weather_api import OPENWEATHER_API_KEY
from core.weather_api import get_weather, get_hourly_forecast
from geopy.geocoders import Nominatim

class WeatherDataCollector:
    def __init__(self, api_key: str = OPENWEATHER_API_KEY):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.session = requests.Session()
        self.last_request_time = 0
        self.min_request_interval = 1.0  # seconds
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _respect_rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()

    def _make_api_request(self, endpoint: str, params: Dict) -> Optional[Dict]:
        self._respect_rate_limit()
        params["appid"] = self.api_key
        url = f"{self.base_url}/{endpoint}"
        retries = [1, 2, 4]

        for attempt, delay in enumerate(retries):
            try:
                response = self.session.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    self.logger.error("❌ Invalid API Key.")
                    return None
                elif response.status_code == 429:
                    self.logger.warning("⏳ Rate limited, waiting...")
                    time.sleep(60)
                    continue
                else:
                    self.logger.warning(f"⚠️ API Error {response.status_code}")
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Request failed ({attempt + 1}): {e}")
            time.sleep(delay)

        self.logger.error("🚫 Max retries exceeded.")
        return None

    def get_current_weather(self, city: str, units: str = "metric") -> Optional[Dict]:
        params = {"q": city, "units": units}
        data = self._make_api_request("weather", params)
        if data:
            return self._clean_weather_data(data)
        return None

    def _clean_weather_data(self, raw: Dict) -> Optional[Dict]:
        try:
            weather = {
                "timestamp": datetime.now().isoformat(),
                "city": raw["name"],
                "country": raw["sys"]["country"],
                "temp": float(raw["main"]["temp"]),
                "feels_like": float(raw["main"]["feels_like"]),
                "humidity": int(raw["main"]["humidity"]),
                "description": raw["weather"][0]["description"],
                "wind_speed": float(raw.get("wind", {}).get("speed", 0)),
                "icon": raw["weather"][0]["icon"]
            }

            # Simple validation
            if not (-50 <= weather["temp"] <= 60):
                self.logger.warning("⚠️ Temperature out of range.")
                return None

            return weather
        except (KeyError, TypeError, ValueError) as e:
            self.logger.error(f"❌ Data formatting failed: {e}")
            return None
        
    def get_weather_with_forecast(self, city: str, units: str = "metric") -> Optional[Dict]:
        # Step 1: Get current weather
        current = self.get_current_weather(city, units)
        if not current:
            return None

        # Step 2: Use geopy to get coordinates for the city
        geolocator = Nominatim(user_agent="weather_dashboard")
        location = geolocator.geocode(city)
        if not location:
            self.logger.error("❌ Could not get coordinates for the city.")
            return None

        latitude = location.latitude
        longitude = location.longitude

        # Step 3: Get hourly forecast from Open-Meteo
        try:
            forecast = get_hourly_forecast(latitude, longitude)
        except Exception as e:
            self.logger.warning(f"⚠️ Failed to get forecast: {e}")
            forecast = []

        return {
            "current": current,
            "forecast": forecast  # A list of (time, temperature) tuples
        }
