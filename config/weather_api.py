import os
from dotenv import load_dotenv

# Load .env from the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
env_path = os.path.join(project_root, ".env")

load_dotenv(dotenv_path=env_path)

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Optional test print (remove later)
print("API Key:", OPENWEATHER_API_KEY)





