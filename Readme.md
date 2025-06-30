# Weather App

A Python desktop weather application built with Tkinter.  
Fetches current weather data via OpenWeatherMap API and offers features like theme switching, city comparison, and activity suggestions.

---

## Features

- Fetch and display current weather for any city.
- Save and preload the last searched city.
- Log weather history with date, city, temperature, and description.
- User preferences for theme (day/night) and units (metric/imperial).
- Modular design with separate folders for core functionality, features, assets, and config.
- Error handling for API and configuration issues.

---

## Folder Structure
weather_app/
├── main.py # Main GUI launcher
├── core/ # Core modules (API, storage, error handling)
├── features/ # Additional features (city comparison, theme switcher, activity suggester)
├── assets/ # Images and theme assets
├── config/ # Configuration files (settings.ini)
├── data/ # Stored data files (weather history, last city)
├── tests/ # Test scripts
└── utils/ # Helper utilities


---

## Setup Instructions

1. Clone the repository.

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

3. Install dependencies:
```bash
pip install -r requirements.txt

4. Create a .env file in the root directory with your OpenWeatherMap API key:
OPENWEATHER_API_KEY=your_api_key_here

5. Run the app:
```bash
python main.py

Usage
Enter a city name and click "Get Weather" to fetch current weather.

The app will save your last searched city and load it on startup.

Preferences for theme and units are saved in the config folder.

Testing:
Run tests using pytest:
```bash
pytest tests/test_weather.py
