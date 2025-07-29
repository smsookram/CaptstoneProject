class WeatherAPIError(Exception):
    """Raised when weather API call fails."""
    pass

class ConfigError(Exception):
    """Raised when required config (like API key) is missing."""
    pass

