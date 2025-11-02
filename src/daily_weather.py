"""
Optional Script — Daily Weather Automation
------------------------------------------
This script enables automated daily weather data collection from the OpenWeather API.
Currently not in use, as the project operates on synthetic data for analysis.
Retained for future scalability and demonstration purposes.
"""

from save_weather import fetch_weather, save_to_db
from datetime import datetime

def run_daily_weather():
    """Fetch and save today's weather data to the database."""
    print(f"🌤️ Starting weather fetch job at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    weather = fetch_weather()
    if weather:
        save_to_db(weather)
        print("✅ Daily weather data saved successfully.")
    else:
        print("❌ Failed to fetch weather data.")

if __name__ == "__main__":
    run_daily_weather()
