import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Access API key
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
