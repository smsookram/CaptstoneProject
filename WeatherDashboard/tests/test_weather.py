import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.weather_api import get_weather
from core.error_handling import WeatherAPIError

import pytest
from core.weather_api import get_weather
from core.error_handling import WeatherAPIError

def test_get_weather_valid_city():
    result = get_weather("New York")
    assert isinstance(result, dict)
    assert "city" in result
    assert "temp" in result

def test_get_weather_invalid_city():
    with pytest.raises(WeatherAPIError):
        get_weather("NoSuchCity_XYZ")


