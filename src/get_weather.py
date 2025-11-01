import os
import requests
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = "Philadelphia"

if not API_KEY:
    raise ValueError("❌ API key not found. Make sure .env file exists and OPENWEATHER_API_KEY is set.")

url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

response = requests.get(url)
data = response.json()

if response.status_code == 200:
    print(f"✅ Weather data for {CITY}:")
    print(data)
else:
    print("❌ Error fetching data:", data)
