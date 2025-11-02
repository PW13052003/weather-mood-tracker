import pandas as pd
from db_connect import create_connection

def load_data():
    conn = create_connection()
    if not conn:
        print("❌ Could not connect to DB.")
        return None, None

    weather_df = pd.read_sql("SELECT * FROM weather_data;", conn)
    mood_df = pd.read_sql("SELECT * FROM mood_data;", conn)

    conn.close()
    print(f"✅ Loaded {len(weather_df)} weather records and {len(mood_df)} mood records.")
    return weather_df, mood_df

def clean_and_merge(weather_df, mood_df):
    # Ensure 'date' columns are actual datetime objects
    weather_df["date"] = pd.to_datetime(weather_df["date"])
    mood_df["date"] = pd.to_datetime(mood_df["date"])

    # Fill NaN values in mood data with reasonable defaults
    mood_df["sleep_hours"].fillna(mood_df["sleep_hours"].median(), inplace=True)
    mood_df["stress_level"].fillna(mood_df["stress_level"].median(), inplace=True)
    mood_df["productivity"].fillna(mood_df["productivity"].median(), inplace=True)
    mood_df["weather_condition"].fillna("unknown", inplace=True)

    # Merge the two DataFrames on date (left join so every mood entry keeps its date)
    merged_df = pd.merge(mood_df, weather_df, on="date", how="left")

    print(f"✅ Merged dataset has {len(merged_df)} rows and {merged_df.shape[1]} columns.")
    return merged_df

if __name__ == "__main__":
    weather, mood = load_data()
    merged = clean_and_merge(weather, mood)
    print(merged.head())