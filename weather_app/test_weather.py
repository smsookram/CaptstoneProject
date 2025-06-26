import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

from core.weather_api import get_weather

weather = get_weather("New York")
if weather:
    print(weather)

