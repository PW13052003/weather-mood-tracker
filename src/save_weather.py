from db_connect import create_connection
from dotenv import load_dotenv
import os
import requests
from datetime import date

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = "Philadelphia"

def fetch_weather():
    """Fetch weather data from OpenWeather API."""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        return {
            "date": date.today(),
            "city": CITY,
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "weather_desc": data["weather"][0]["description"],
            "clouds": data["clouds"]["all"],
            "wind_speed": data["wind"]["speed"]
        }
    else:
        print("❌ Error fetching weather:", data)
        return None


def save_to_db(weather_data):
    """Insert weather data into MySQL table."""
    conn = create_connection()
    if not conn:
        return

    cursor = conn.cursor()
    insert_query = """
        INSERT INTO weather_data
        (date, city, temperature, feels_like, humidity, weather_desc, clouds, wind_speed)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    values = (
        weather_data["date"],
        weather_data["city"],
        weather_data["temperature"],
        weather_data["feels_like"],
        weather_data["humidity"],
        weather_data["weather_desc"],
        weather_data["clouds"],
        weather_data["wind_speed"]
    )

    cursor.execute(insert_query, values)
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Weather data saved to MySQL successfully.")


if __name__ == "__main__":
    weather = fetch_weather()
    if weather:
        save_to_db(weather)
