import pandas as pd
from db_connect import create_connection
import seaborn as sns
import matplotlib.pyplot as plt

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

def analyze_correlations(merged_df):
    """Compute and visualize correlations between mood, lifestyle, and weather features."""

    # Select numeric columns for correlation
    numeric_cols = [
        "mood_score", "energy_level", "sleep_hours",
        "stress_level", "productivity", "temperature",
        "feels_like", "humidity", "clouds", "wind_speed"
    ]
    df_corr = merged_df[numeric_cols].corr()

    # Display correlation matrix
    print("\n📊 Correlation matrix:\n", df_corr.round(2))

    # Plot heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(df_corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Matrix: Mood vs Weather")
    plt.tight_layout()
    plt.show()

    # Example scatterplot: mood vs temperature
    plt.figure(figsize=(7, 5))
    sns.scatterplot(x="temperature", y="mood_score", data=merged_df)
    plt.title("Mood vs Temperature")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Mood Score")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    weather, mood = load_data()
    merged = clean_and_merge(weather, mood)
    analyze_correlations(merged)