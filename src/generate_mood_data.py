from faker import Faker
import random
from datetime import date, timedelta
from db_connect import create_connection

fake = Faker()

def generate_fake_mood_data(num_days=365):
    """Generate a list of dictionaries with fake mood records for num_days."""
    today = date.today()
    data = []

    for i in range(num_days):
        day = today - timedelta(days=i)

        # Simulate seasonal/weather influence
        weather_condition = random.choice(["sunny", "rainy", "cloudy", "snowy", "humid", "windy"])
        base_mood = 7 if weather_condition == "sunny" else 5 if weather_condition == "cloudy" else 4

        mood_score = min(10, max(1, int(random.gauss(base_mood, 1.5))))
        energy_level = min(10, max(1, int(random.gauss(mood_score, 1.0))))
        sleep_hours = round(random.uniform(4, 9), 1)
        stress_level = min(10, max(1, int(random.gauss(6 - (mood_score - 5) * 0.8, 1.5))))
        productivity = min(10, max(1, int(random.gauss((mood_score + energy_level) / 2, 1.2))))
        notes = fake.sentence(nb_words=8)

        data.append({
            "date": day,
            "mood_score": mood_score,
            "energy_level": energy_level,
            "notes": notes,
            "sleep_hours": sleep_hours,
            "stress_level": stress_level,
            "productivity": productivity,
            "weather_condition": weather_condition
        })

    return data


def insert_fake_data_to_db(fake_data):
    """Insert the generated mood data into the MySQL table."""
    conn = create_connection()
    if not conn:
        print("❌ Could not connect to DB.")
        return

    cursor = conn.cursor()
    insert_query = """
        INSERT INTO mood_data 
        (date, mood_score, energy_level, notes, sleep_hours, stress_level, productivity, weather_condition)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
    """

    for record in fake_data:
        values = (
            record["date"], record["mood_score"], record["energy_level"], record["notes"],
            record["sleep_hours"], record["stress_level"], record["productivity"], record["weather_condition"]
        )
        cursor.execute(insert_query, values)

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Inserted {len(fake_data)} fake mood records successfully!")


if __name__ == "__main__":
    fake_records = generate_fake_mood_data(num_days=49980)  # 2 years of data
    insert_fake_data_to_db(fake_records)
