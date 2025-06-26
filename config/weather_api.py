import os
from dotenv import load_dotenv

# Get the real path to .env inside weather_app/
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "weather_app"))
env_path = os.path.join(project_root, ".env")

load_dotenv(dotenv_path=env_path)

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Temporary test
print("API Key:", OPENWEATHER_API_KEY)


