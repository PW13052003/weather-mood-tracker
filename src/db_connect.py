import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            print("✅ Connected to MySQL database successfully.")
            return connection

    except Error as e:
        print("❌ Error while connecting to MySQL:", e)
        return None

if __name__ == "__main__":
    conn = create_connection()
    if conn:
        conn.close()
        print("🔒 Connection closed.")
